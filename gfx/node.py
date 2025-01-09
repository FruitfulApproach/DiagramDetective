from gfx.base import Base
from PyQt5.QtCore import pyqtSignal, QPointF, QRectF, Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QPainterPath
from gfx.utility import filter_out_gfx_descendents
from gfx.connect_button import ConnectButton
from copy import copy
from core.utility import simple_max_contrasting_color
from core.qt_pickle_utility import SimpleBrush, Pen

class Node(Base):
    bounding_rect_pad = 10  # BUGFIX: needs to be -1 or else boundingRect always gets rendered for some reason (Qt bug)
    children_rect_pad = 8  # So there's some area to click inside of
    boundary_proximity_distance = 6
    selection_shape_pad = 3    
    position_changed = pyqtSignal(QPointF)   # Sends delta
    
    default_border_pen = Pen(QColor(51, 180, 255), 3.0)
    default_fill_brush = QBrush(SimpleBrush(QColor(180, 255, 51)))
    default_corner_radius = 11.0
        
    def __init__(self, label: str=None, pickled=False):
        super().__init__(label)
        
        self._lastPos = self.pos()
        self._collisionMemo = set()
        self._connectButton = ConnectButton()
        self._connectButton.visible = False
        
        self.setFlags(
            self.ItemSendsScenePositionChanges|self.ItemSendsGeometryChanges|
            self.ItemIsMovable|self.ItemIsFocusable|self.ItemIsSelectable
        )
        
        self.setAcceptHoverEvents(True)                
        
        if not pickled:
            self._pen = self.default_border_pen
            self._brush = self.default_fill_brush
            self._cornerRadius = self.default_corner_radius
            self.finish_setup()
            
    def __setstate__(self, data):
        self.__init__(pickled=False)
        self._setstate(data)
        self.finish_setup()
        
    def _setstate(self, data):
        super()._setstate(data)
        self._pen = data['pen']
        self._brush = data['brush']
        
    @property
    def corner_radius(self):
        return self._cornerRadius
    
    @corner_radius.setter
    def corner_radius(self, radius: float):
        self._cornerRadius = radius
        self.update()
    
    @property
    def border_pen(self):
        return self._pen
    
    @border_pen.setter
    def border_pen(self, pen: QPen):
        self._pen = pen
        self.update()
        
    @property
    def fill_brush(self):
        return self._brush
    
    @fill_brush.setter
    def fill_brush(self, brush: QBrush):
        self._brush = brush
        self.update()   
        
    def __getstate__(self):
        data = {}
        super()._getstate(data)
        return data
    
    def finish_setup(self):
        super().finish_setup()
        
    def __deepcopy__(self, memo):
        if id(self) not in memo:
            X = copy(self)
            memo[id(self)] = X
        return memo[id(self)]
    
    def __copy__(self):
        X = Node(label=self.label)
        return X
        
    def boundingRect(self) -> QRectF:
        p = self.bounding_rect_pad
        return self.childrenBoundingRect().adjusted(-p, -p, p, p)
    
    def _selectionShape(self):
        p = self.selection_shape_pad
        r = self.childrenBoundingRect().adjusted(-p, -p, p, p)
        shape = QPainterPath()
        shape.addRect(r)
        return shape
    
    def paint(self, painter, option, widget):
        painter.setRenderHint(painter.Antialiasing)
        painter.setBrush(self.fill_brush)
        painter.setPen(self.border_pen)
        r = self.corner_radius
        painter.drawRoundedRect(self.childrenBoundingRect(), r, r)
        
        if self.isSelected() and self.scene():
            shape = self._selectionShape()
            bgcolor = self.scene().backgroundBrush().color()
            col = simple_max_contrasting_color(bgcolor)
            painter.strokePath(shape, QPen(col, 1.0, Qt.DotLine))
            
        if self._connectButton.visible:
            self._connectButton.paint(painter)
        
    def __repr__(self):
        return f'{self.label}:Node(@{id(self)}'
    
    def mouseMoveEvent(self, event):
        self.handle_collisions(event.pos() - event.lastPos())
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        self._clearCollisionMemos()
        super().mouseReleaseEvent(event)
    
    def handle_collisions(self, delta_pos: QPointF):
        items_colliding = self.collidingItems()
        items_colliding = list(filter(lambda i: not (i.isAncestorOf(self) or self.isAncestorOf(i)), items_colliding))
        items_colliding = filter_out_gfx_descendents(items_colliding)        
        
        if len(items_colliding) > 0:
            self._collisionMemo.add(id(self))
            
            for item in items_colliding:
                if isinstance(item, Node):
                    if id(item) not in self._collisionMemo:
                        if QPointF.dotProduct(item.pos() - self.pos(), delta_pos) > 0:
                            self._collisionMemo.add(id(item))
                            item.setPos(item.pos() + delta_pos)
                            
        parent = self.parentItem()        
        if parent is not None and isinstance(parent, Node):
            parent.handle_collisions(delta_pos)
                            
    def _clearCollisionMemos(self):
        self._collisionMemo.clear()
        parent = self.parentItem()
        if parent is not None and isinstance(parent, Node):
            parent._clearCollisionMemos()
    
    def itemChange(self, change, value):
        if change == self.ItemPositionChange:
            self._lastPos = self.pos()
            
            if self.scene():
                self.handle_collisions(delta_pos=value - self.pos())
            
        if change == self.ItemPositionHasChanged:
            self._clearCollisionMemos()
            self.scene().update()
            
        return super().itemChange(change, value)
            
    def set_center_pos(self, pos: QPointF):
        rect = self.boundingRect()
        pos -= rect.center()
        self.setPos(pos)
        
    def childrenBoundingRect(self) -> QRectF:
        r = super().childrenBoundingRect()
        p = self.children_rect_pad
        return r.adjusted(-p, -p, p, p)
    
    def hoverMoveEvent(self, event):
        p = self.boundary_proximity_distance
        r = self.childrenBoundingRect()
        r_outer = r.adjusted(-p, -p, p, p)
        r_inner = r.adjusted(p, p, -p, -p)
        
        if r_outer.contains(event.pos()):
            if not r_inner.contains(event.pos()):
                self._connectButton.pos = event.pos()
                if not self._connectButton.visible:
                    self._connectButton.visible = True
            else:
                self._connectButton.visible = False
        else:
            self._connectButton.visible = False
        
        if self._connectButton.visible:
            self.setCursor(Qt.UpArrowCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
            
        self.update()                         
        super().hoverMoveEvent(event)
        
    def hoverLeaveEvent(self, event):
        self._connectButton.visible = False
        self.setCursor(Qt.ArrowCursor)
        self.update()
        super().hoverLeaveEvent(event)
        
    def mousePressEvent(self, event):
        self._connectButton.visible = False
        super().mousePressEvent(event)
        
    def focusOutEvent(self, event):
        self.setSelected(False)
        super().focusOutEvent(event)
        
    def connect_button_rect(self):
        return self._connectButton.rect
    
    def in_arrow_connect_mode(self):
        return self._connectButton.visible
    
    def mouseMoveEvent(self, event):
        self.scene().update()
        super().mouseMoveEvent(event)
