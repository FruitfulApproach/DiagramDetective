from gfx.base import Base
from PyQt5.QtCore import pyqtSignal, QPointF, QRectF, Qt
from PyQt5.QtGui import QPen, QBrush, QColor
from gfx.utility import filter_out_gfx_descendents

from copy import copy

class Node(Base):
    bounding_rect_pad = 1  # BUGFIX: needed to remove drag artifacts when zoomed in
    
    position_changed = pyqtSignal(QPointF)   # Sends delta
        
    def __init__(self, label: str=None, pickled=False):
        super().__init__(label)
        
        self._lastPos = self.pos()
        self._collisionMemo = set()
        
        self.setFlags(
            self.ItemSendsScenePositionChanges|self.ItemSendsGeometryChanges|
            self.ItemIsMovable|self.ItemIsFocusable|self.ItemIsSelectable
        )
        
        if not pickled:
            self._pen = QPen(Qt.blue, 2.0)
            self._brush = QBrush(Qt.yellow)
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
    
    def paint(self, painter, option, widget):
        painter.setRenderHint(painter.Antialiasing)
        painter.setBrush(self.fill_brush)
        painter.setPen(self.border_pen)
        painter.drawRect(self.childrenBoundingRect())
        
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