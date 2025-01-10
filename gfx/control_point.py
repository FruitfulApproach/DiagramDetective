from PyQt5.QtCore import Qt, QPointF
#from core.qt_tools import Pen, SimpleBrush
from PyQt5.QtGui import QPainterPath, QColor, QVector2D
from PyQt5.QtWidgets import QGraphicsEllipseItem
from core.qt_pickle_utility import SimpleBrush, Pen
from core.utility import closest_point_on_path

class ControlPoint(QGraphicsEllipseItem):
    default_fill_brush = SimpleBrush(Qt.yellow)
    default_border_pen = Pen(QColor(Qt.white), 1.0)
    default_radius = 5.0
    
    def __init__(self, new=None):
        if new is None: new = True
        super().__init__()
        super().__init__()
        #self.setFlag(self.ItemIsMovable, True)  # BUGFIX: don't wipe out other flags
        #self.setFlag(self.ItemIsSelectable, True)
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
        shape = self.shape()
        item_shape = item.shape()
        if shape and item_shape:
            r0 = shape.boundingRect()
            r1 = self.mapFromItem(item, item_shape.boundingRect()).boundingRect()

            horiz = (max(r0.left(), r1.left()), min(r0.right(), r1.right()))
            vert = (max(r0.top(), r1.top()), min(r0.bottom(), r1.bottom()))

            dx = horiz[1] - horiz[0]
            dy = vert[1] - vert[0]

            c0 = r0.center()
            c1 = r1.center()

            if dx > 0 or dy > 0:
                if dx > dy:     # Shared horizontal interval is more prominent
                    if r1.left() > r0.left():
                        x = r1.left() + dx/2.0
                    else:
                        x = r0.left() + dx/2.0
                    if c0.y() < c1.y():
                        y = r0.bottom()
                    else:
                        y = r0.top()
                else:       # Shared vertical interval is more prominent
                    if r1.top() > r0.top():
                        y = r1.top() + dy/2.0
                    else:
                        y = r0.top() + dy/2.0
                    if c0.x() < c1.x():
                        x = r0.right()
                    else:
                        x = r0.left()
                return QPointF(x, y)

            return closest_point_on_path(self.mapFromItem(item, item.boundingRect().center()), shape)
        

      
