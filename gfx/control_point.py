from PyQt5.QtCore import Qt, QPointF
#from core.qt_tools import Pen, SimpleBrush
from PyQt5.QtGui import QPainterPath, QColor, QVector2D
from PyQt5.QtWidgets import QGraphicsEllipseItem
from core.qt_pickle_utility import SimpleBrush, Pen
from core.utility import closest_point_on_path

class ControlPoint(QGraphicsEllipseItem):
    default_fill_brush = SimpleBrush(Qt.cyan)
    default_border_pen = Pen(QColor(Qt.blue), 1.0)
    default_radius = 7.5
    
    def __init__(self, new=None):
        if new is None: new = True
        super().__init__()
        super().__init__()
        self.setFlag(self.ItemIsMovable, True)  # BUGFIX: don't wipe out other flags
        self.setFlag(self.ItemIsFocusable, True)
        self.setFlag(self.ItemSendsScenePositionChanges, True)
        self.setFlag(self.ItemSendsGeometryChanges, True)        
        
        if new:
            #d = core.app.inst.control_point_diameter
            self.radius = self.default_radius
            self.setBrush(self.default_fill_brush)
            self.setPen(self.default_border_pen)
            #self.setZValue(100)
            self.finish_setup()
        
    def __setstate__(self, data):
        self.__init__(pickled=True)
        self.radius = data['radius']
        self.setPen(data['pen'])
        self.setBrush(data['brush'])
        self.finish_setup()
        
    def __getstate__(self):
        return {
            'radius' : self.radius,
            'pen' : self.pen(),
            'brush' : self.brush(),
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
    
    @property
    def radius(self):
        return self._radius    

    @radius.setter
    def radius(self, radius):
        self._radius = radius
        r = radius
        self.setRect(-r, -r, 2*r, 2*r)
        self.update()
                
    def closest_boundary_pos_to_item(self, item):
        shape = item.shape()
        A = closest_point_on_path(self.pos(), self.mapFromItem(item, shape))
        v = QVector2D(A - self.pos())
        v.normalize()
        return self.pos() + self.radius * v.toPointF()
        
    def paint(self, painter, option, widget):
        painter.setRenderHint(painter.Antialiasing)
        super().paint(painter, option, widget)
        
    def mouseMoveEvent(self, event):
        self.parentItem().show_control_points_longer()
        self.parentItem().update()
        super().mouseMoveEvent(event)