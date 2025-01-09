from gfx.base import Base
from gfx.node import Node
from copy import copy, deepcopy
from PyQt5.QtCore import QPointF, QLineF
from PyQt5.QtGui import QPainterPath, QVector2D
from gfx.control_point import ControlPoint

class Arrow(Base):
    default_relative_head_size = 5.0
    
    def __init__(self, label=None, source: Node = None, target: Node = None, pickled=False):
        super().__init__(label, pickled)
        self._source = source
        self._target = target
        
        if not pickled:
            self._bezier = False
            self._relativeHeadSize = self.default_relative_head_size
            self._points = [ControlPoint() for i in range(0, 4)]
            self._bezier = None
            self._points[1].setVisible(False)
            self._points[2].setVisible(False)            
            self.finish_setup()
            
    def __setstate__(self, data):
        self.__init__(pickled=True)
        super()._setstate(data)
        self.finish_setup()
        
    def __getstate__(self):
        return self._getstate({})
    
    def _getstate(self, data: dict):
        super()._getstate(data)
        return data
            
    def finish_setup(self):
        super().finish_setup()
        
    def __deepcopy__(self, memo):
        if id(self) not in memo:
            f = copy(self)
            f.source = deepcopy(self.source, memo)
            f.target = deepcopy(self.target, memo)
            memo[id(self)] = f
            return f
        return memo[id(self)]
    
    def __copy__(self, memo):
        f = Arrow(label=self.label, source=self.source, target=self.target)
        return f
    
    @property
    def source(self):
        return self._source
    
    @property
    def target(self):
        return self._target
    
    @source.setter
    def source(self, source):
        self._source = source
        
    @target.setter
    def target(self, target):
        self._target = target
        
    def boundingRect(self):
        h = self.head_size() / 2.0
        return self.childrenBoundingRect().adjusted(-h, -h, h, h)
    
    def head_size(self):
        return self._relativeHeadSize * self.pen().widthF()
    
    def compute_head_path(self):
        line = self.line()
        if not self.is_bezier:
            u = line.p2() - line.p1()
        else:
            u = self._points[-1].pos() - self._points[-2].pos()   
        mag_u = QVector2D(u).length()
        if abs(mag_u) == 0.0:
            return QPainterPath()
        u /= mag_u
        v = QPointF(-u.y(), u.x())      # perp vector
        path = QPainterPath()
        size = self.head_size()
        for k in range(0, self.num_heads()):
            tip = line.p2() - u * size * k
            p = tip - (u + v) * size
            q = tip + (v - u) * size
            r = tip - u * size
            path.moveTo(p)
            path.quadTo((p + tip + r)/3, tip)
            path.quadTo((q + tip + r)/3, q)
        return path
    
    def compute_line_path(self):
        path = QPainterPath()
        line = self.tail_line()
        u = line.p2() - line.p1()
        mag = QVector2D(u).length()
        if abs(mag) > 0.0:        
            u /= mag
        if self._tailStyle == self.HookTail:
            u *= self.head_size()
            v = QPointF(u.y(), -u.x())            
            line_end = line.p1() + u 
            perp_end = 1.5 * v
            path.moveTo(line_end + perp_end)
            path.cubicTo(line.p1() + perp_end, line.p1(), line_end)
            if self.is_bezier:
                path.cubicTo(self._points[1].pos(), self._points[2].pos(), self._points[3].pos())
            else:
                path.lineTo(self.line().p2())        
        else:
            if not self.is_bezier:
                path.moveTo(self.line().p1())
                path.lineTo(self.line().p2())
            else:
                path.moveTo(self.line().p1())
                path.cubicTo(self._points[1].pos(), self._points[2].pos(), self._points[3].pos())
        return path
    
    def tail_line(self):
        if self.is_bezier:
            return QLineF(self._points[0].pos(), self._points[1].pos())
        return QLineF(self._points[0].pos(), self._points[-1].pos())
    
    def num_heads(self):
        return self._headStyle  # yes, this is right, check the enum
    
    def line(self):
        return QLineF(self._points[0].pos(), self._points[-1].pos())
    
    @property
    def is_bezier(self):
        return self._bezier    