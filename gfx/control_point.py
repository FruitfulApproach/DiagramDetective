from PyQt5.QtCore import Qt
#from core.qt_tools import Pen, SimpleBrush
from PyQt5.QtGui import QPainterPath, QColor, QVector2D
from PyQt5.QtWidgets import QGraphicsEllipseItem
from core.qt_pickle_utility import SimpleBrush, Pen

class ControlPoint(QGraphicsEllipseItem):
    default_fill_brush = SimpleBrush(Qt.yellow)
    default_border_pen = Pen(QColor(Qt.white), 1.0)
    default_radius = 5.0
    
    def __init__(self, new=None):
        if new is None: new = True
        super().__init__()
        self.setFlag(self.ItemIsMovable, True)  # BUGFIX: don't wipe out other flags
        self.setFlag(self.ItemIsSelectable, True)
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
                

        

      
