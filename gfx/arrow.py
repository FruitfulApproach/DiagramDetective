from gfx.base import Base
from gfx.node import Node
from copy import copy, deepcopy
from PyQt5.QtCore import QPointF, QLineF
from PyQt5.QtGui import QPainterPath, QVector2D
from gfx.control_point import ControlPoint
from core.qt_pickle_utility import Pen
from PyQt5.QtCore import Qt, QRectF
from gfx.label import Label

class Arrow(Base):
    default_relative_head_size = 5.0
    
    def __init__(self, label: str=None, source: Node = None, target: Node = None, pickled=False):
        super().__init__(label, pickled)
        self._source = source
        self._target = target        
        self._updatingPointPos = False
        self._lastLabelPosLine = None
        
        if not pickled:
            self._linePen = Pen(Qt.black, 3.0)
            self._bezier = False
            self._relativeHeadSize = self.default_relative_head_size
            self._points = [ControlPoint() for i in range(0, 4)]
            self._bezier = None
            self._points[1].setVisible(False)
            self._points[2].setVisible(False)            
            Arrow.finish_setup(self)
            
    def __setstate__(self, data):
        self.__init__(pickled=True)
        super()._setstate(data)
        Arrow.finish_setup(self)
        
    def __getstate__(self):
        return self._getstate({})
    
    def _getstate(self, data: dict):
        super()._getstate(data)
        return data
            
    def finish_setup(self):
        for point in self._points:
            point.setParentItem(self)
        
    def __deepcopy__(self, memo):
        if id(self) not in memo:
            f = copy(self)
            f.source = deepcopy(self.source, memo)
            f.target = deepcopy(self.target, memo)
            memo[id(self)] = f
            return f
        return memo[id(self)]
    
    def __copy__(self):
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
        from gfx.directed_graph import DirectedGraph
        
        prev_node = self._source
        self._source = source
        space = self.parent_graph
        
        if isinstance(space, DirectedGraph):
            space.arrow_source_was_set(self, prev_node)
        
        self.update()
        
    @target.setter
    def target(self, target):
        from gfx.directed_graph import DirectedGraph
        
        prev_node = self._target
        self._target = target
        space = self.parent_graph
        
        if isinstance(space, DirectedGraph):
            space.arrow_target_was_set(self, prev_node)
            
        self.update()
        
    def boundingRect(self):
        h = self.head_size() / 2.0
        return self.childrenBoundingRect().adjusted(-h, -h, h, h)
    
    def head_size(self):
        return self._relativeHeadSize * self.pen.widthF()
    
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
    
    def update_control_point_positions(self):
        if not self._updatingPointPos:
            self._updatingPointPos = True
            self.prepareGeometryChange()
            source = self.source_or_point
            target = self.target_or_point

            if not self.is_bezier:
                a = source.closest_boundary_pos_to_item(target)
                b = target.closest_boundary_pos_to_item(source)
                if a is not None and b is not None:
                    a = self.mapFromItem(self.source, a)
                    b = self.mapFromItem(self.target, b)
                else:
                    return
            else:
                a = source.closest_boundary_pos_to_item(self._points[1])
                b = target.closest_boundary_pos_to_item(self._points[-2])
                if a is not None and b is not None:
                    a = self.mapFromItem(source, a)
                    b = self.mapFromItem(target, b)
                else:
                    return

            if self._target is not None:
                self.target_point.setPos(b) 
            if self._source is not None:
                self.source_point.setPos(a) 

            if not self.is_bezier:
                v = b - a
                mag_v = QVector2D(v).length()
                if abs(mag_v) > 0.0:
                    v /= mag_v
                seg_len = mag_v / (len(self._points) - 1)
                v *= seg_len
                c = v + a
                d = c + v
                self._points[1].setPos(c)
                self._points[-2].setPos(d)

            self.update_text_position()
            self._updatingPointPos = False
            
    def update_text_position(self):
        line = self.label_pos_line()
        last_line = self._lastLabelPosLine
        if last_line is None:
            self._lastLabelPosLine = line
            return        
        du = line.p1() - last_line.p1()
        dv = line.p2() - last_line.p2()
        delta = (du + dv) / 2
        for c in self.childItems():
            if isinstance(c, Label):
                c.setPos(c.pos() + delta)
        self._lastLabelPosLine = line    
            
    def label_pos_line(self):
        if not self.is_bezier:
            line = QLineF(self._points[0].pos(), self._points[-1].pos())    
        else:
            line = QLineF(self._points[1].pos(), self._points[-2].pos())
        return line            
            
    @property
    def pen(self):
        return self._linePen
    
    @pen.setter
    def pen(self, pen: Pen):
        self._linePen = pen
        self.update()
        
    def paint(self, painter, option, widget):
        painter.setRenderHint(painter.Antialiasing)
        line = self.line()
        painter.setPen(self.pen)
        painter.drawLine(line)
        print("PAINTING")

    @property
    def source_or_point(self):
        if self._source is None:
            return self.source_point
        return self._source

    @property
    def target_or_point(self):
        if self._target is None:
            return self.target_point
        return self._target    

    @property
    def target_point(self):
        return self._points[-1]

    @property
    def source_point(self):
        return self._points[0]
    
    def _update(self, rect: QRectF, memo: set):
        self.prepareGeometryChange()
        self.update_control_point_positions()
        ancestor = self.parentItem()
        while ancestor is not None:
            ancestor.update(rect, memo)
            ancestor = ancestor.parentItem()
            
                
    def delete(self):
        self.space.delete_arrow(self) 
        self.source = None
        self.target = None
        self.deleteLater()
        