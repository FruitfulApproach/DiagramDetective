from PyQt5.QtCore import Qt, QPointF, pyqtSignal, QRectF
from PyQt5.QtGui import QColor, QVector2D, QPen, QBrush
from gfx.base import Base
from core.qt_pickle_utility import SimpleBrush, Pen
from core.utility import closest_point_on_path
from PyQt5.QtWidgets import QGraphicsObject

class ControlPoint(Base):
    mouse_moved = pyqtSignal(QPointF)
    
    default_fill_brush = SimpleBrush(Qt.cyan)
    default_border_pen = Pen(QColor(Qt.blue), 1.0)
    default_radius = 7.5
    
    def __init__(self, pickled=False):
        super().__init__(None, pickled)
        self.setFlag(self.ItemIsMovable, True)  # BUGFIX: don't wipe out other flags
        self.setFlag(self.ItemIsFocusable, True)
        self.setFlag(self.ItemSendsScenePositionChanges, True)
        self.setFlag(self.ItemSendsGeometryChanges, True)        
        
        if not pickled:
            self._rect = QRectF()
            self._radius = self.default_radius
            self._updateRect()
            self._brush = self.default_fill_brush
            self._pen = self.default_border_pen
            #self.setZValue(100)
            self.finish_setup()
        
    def __setstate__(self, data):
        self.__init__(pickled=True)
        self._radius = data['radius']
        self._pen = data['pen']
        self._brush = data['brush']
        self._rect = data['rect']
        self.finish_setup()
        
    def __getstate__(self):
        return {
            'radius' : self.radius,
            'pen' : self.pen(),
            'brush' : self.brush(),
            'rect' : self.rect(),
        }
    
    def finish_setup(self):
        pass
                   
    def closest_boundary_point(self, pos):
        radius = self.radius()
        v = pos - self._innerRect.center()
        mag = QVector2D(v).length()
        if abs(mag) == 0:
            return self._innerRect.center()
        return v / mag * radius
    
    def radius(self):
        return self._radius    

    def set_radius(self, radius):
        self._radius = radius
        self._updateRect()
        
    def _updateRect(self):
        r = self.radius()
        self.set_rect(QRectF(-r, -r, 2*r, 2*r))        
                
    def closest_boundary_pos_to_item(self, item):
        shape = item.shape()
        A = closest_point_on_path(self.pos(), self.mapFromItem(item, shape))
        v = QVector2D(A - self.pos())
        v.normalize()
        return self.pos() + self.radius() * v.toPointF()
        
    def paint(self, painter, option, widget):
        painter.setRenderHint(painter.Antialiasing)
        painter.setPen(self.border_pen())
        painter.setBrush(self.fill_brush())
        painter.drawEllipse(self.rect())
        
    def mouseMoveEvent(self, event):
        self.parentItem().show_control_points_longer()
        self.parentItem().update()
        super().mouseMoveEvent(event)
        self.mouse_moved.emit(event.pos() - event.lastPos())
        
    def fill_brush(self) -> QBrush:
        return self._brush
    
    def set_fill_brush(self, brush: QBrush):
        self._brush = brush
        self.update()
    
    def border_pen(self) -> QPen:
        return self._pen
    
    def set_border_pen(self, pen: QPen):
        self._pen = pen
        self.update()
        
    def rect(self):
        return self._rect
    
    def set_rect(self, rect: QRectF):
        self._rect = rect
        self.update()
        
    def boundingRect(self):
        return self._rect    
    
    def update(self, rect: QRectF = None, memo: set = None, force=False, arrows=True):
        if rect is not None:
            QGraphicsObject.update(self, rect)
        else:
            QGraphicsObject.update(self)
        parent = self.parentItem()
        if parent:
            parent.update()
            
    def parent_graph(self):
        return self.parentItem().parent_graph()
            
         