from gfx.base import Base
from gfx.node import Node
from copy import deepcopy
from PyQt6.QtCore import QPointF, QLineF, Qt, QRectF, QTimer, pyqtSignal
from PyQt6.QtGui import QPainterPath, QVector2D, QPainterPathStroker
from gfx.control_point import ControlPoint
from core.qt_pickle_utility import Pen
from PyQt6.QtWidgets import QMenu
from gfx.label import Label
from core.utility import min_bounding_rect
from bidict import bidict

class Arrow(Base):
    bezier_toggled = pyqtSignal(bool)
    source_was_set = pyqtSignal(Node)
    target_was_set = pyqtSignal(Node)
    
    default_relative_head_size = 5.0
    intersect_shape_width_multiple = 5.0
    control_point_visible_time = 5000
    
    SingleLine, DoubleLine, WavySingleLine, \
    WavyDoubleLine, TripleLine = range(5)    
    NoHead, SingleHead, DoubleHead, TripleHead = range(4)    
    NoTail, HookTail, VeeTail = range(3)    
    
    def __init__(self, label: str=None, source: Node = None, target: Node = None, pickled=False):
        super().__init__(label, pickled)
        self._source = source
        self._target = target        
        self._updatingPointPos = False
        self._lastLabelPosLine = None
        self._shape = QPainterPath()
        self._arrowShape = QPainterPath()
        self._pointVisTimer = None
        
        if self.label_item():                
            self.label_item().setFlags(self.label_item().flags() | self.GraphicsItemFlag.ItemIsMovable)
        self.setFlags(self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemIsFocusable)
        self.setAcceptHoverEvents(True)
        
        if not pickled:
            self._linePen = Pen(Qt.GlobalColor.black, 3.0)
            self._bezier = False
            self._relativeHeadSize = self.default_relative_head_size
            self._points = [ControlPoint() for i in range(0, 4)]
            self._tailStyle = self.NoTail
            self._headStyle = self.SingleHead
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
            point.setVisible(False)
            point.setParentItem(self)
        #self.update_shape()
        
    def __deepcopy__(self, memo):
        if id(self) not in memo:
            f = self.copy()
            f.set_source(deepcopy(self.source(), memo))
            f.set_target(deepcopy(self.target(), memo))
            memo[id(self)] = f
            return f
        return memo[id(self)]
    
    def copy(self):
        f = Arrow(label=None, source=self.source(), target=self.target())
        if self._label:
            f._label = self._label.copy()
        return f
    
    def source(self):
        return self._source
    
    def target(self):
        return self._target
    
    def set_source(self, source: Node):
        from gfx.directed_graph import DirectedGraph
        
        prev_node = self._source
        self._source = source
        space = self.parent_graph()
        
        if isinstance(space, DirectedGraph):
            space.arrow_source_was_set(self, prev_node)
        
        if source is not None:
            self.setZValue(source.zValue() - 1)
            
        self.source_was_set.emit(source)
        
                       
    def set_target(self, target: Node):
        from gfx.directed_graph import DirectedGraph
        
        prev_node = self._target
        self._target = target
        space = self.parent_graph()
        
        if isinstance(space, DirectedGraph):
            space.arrow_target_was_set(self, prev_node)
            
        if target is not None:
            self.setZValue(target.zValue() - 1)
            
        self.target_was_set.emit(target)
                    
    def boundingRect(self):
        h = self.head_size() / 2 + self._intersectShapeWidth() / 2
        rect_list = [self.label_item().boundingRect().translated(self.label_item().pos())]
        
        if self.is_bezier_curve():
            for point in self.control_points():
                rect_list.append(point.boundingRect().translated(point.pos()))
        else:
            rect_list.append(self.source_point().boundingRect().translated(self.source_point().pos()))
            rect_list.append(self.target_point().boundingRect().translated(self.target_point().pos()))
            
        return min_bounding_rect(rect_list).adjusted(-h, -h, h, h)
    
    def head_size(self):
        return self._relativeHeadSize * self.pen().widthF()
    
    def compute_head_path(self):
        line = self.line()
        if not self.is_bezier_curve():
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
            if self.is_bezier_curve():
                path.cubicTo(self._points[1].pos(), self._points[2].pos(), self._points[3].pos())
            else:
                path.lineTo(self.line().p2())        
        else:
            if not self.is_bezier_curve():
                path.moveTo(self.line().p1())
                path.lineTo(self.line().p2())
            else:
                path.moveTo(self.line().p1())
                path.cubicTo(self._points[1].pos(), self._points[2].pos(), self._points[3].pos())
        return path
    
    def tail_line(self):
        if self.is_bezier_curve():
            return QLineF(self._points[0].pos(), self._points[1].pos())
        return QLineF(self._points[0].pos(), self._points[-1].pos())
    
    def num_heads(self):
        return self._headStyle  # yes, this is right, check the enum
    
    def line(self) -> QLineF:
        return QLineF(self._points[0].pos(), self._points[-1].pos())
    
    def is_bezier_curve(self):
        return self._bezier
    
    def update_control_point_positions(self):
        if not self._updatingPointPos:
            self._updatingPointPos = True
            source = self.source_or_point()
            target = self.target_or_point()

            if not self.is_bezier_curve():
                a = source.closest_boundary_pos_to_item(target)
                b = target.closest_boundary_pos_to_item(source)
                if a is not None and b is not None:
                    a = self.mapFromItem(source, a)
                    b = self.mapFromItem(target, b)
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

            if not self.is_bezier_curve():
                self.set_line_points(a, b)
            else:
                if self._source is not None:
                    self.source_point().setPos(a)
                if self._target is not None:
                    self.target_point().setPos(b)                     

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
        if not self.is_bezier_curve():
            line = QLineF(self._points[0].pos(), self._points[-1].pos())    
        else:
            line = QLineF(self._points[1].pos(), self._points[-2].pos())
        return line            
            
    def pen(self):
        return self._linePen
    
    def set_pen(self, pen: Pen):
        self._linePen = pen
        self.update()
        
    def paint(self, painter, option, widget):
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        #painter.drawRect(self.boundingRect())
        painter.setPen(self.pen())
        painter.drawPath(self._arrowShape)        
        super().paint(painter, option, widget)

    def source_or_point(self):
        if self._source is None:
            return self.source_point()
        return self._source

    def target_or_point(self):
        if self._target is None:
            return self.target_point()
        return self._target    

    def target_point(self):
        return self._points[-1]

    def source_point(self):
        return self._points[0]
    
    def control_points(self) -> list:
        return self._points
    
    def _update(self, rect: QRectF, memo: set, arrows: bool = True):
        self.prepareGeometryChange()
        if arrows:
            self.update_control_point_positions()
        self.update_shape()
                         
    def delete(self):
        self.parent_graph().delete_arrow(self) 
        self.set_source(None)
        self.set_target(None)
        self.deleteLater()
        if self.scene():
            self.scene().update()
        
    def update_shape(self):
        path = self._arrowShape
        path.clear()
        self._linePath = self.compute_line_path()
        self._headPath = self.compute_head_path()
        stroker = QPainterPathStroker()
        stroker.setCapStyle(Qt.PenCapStyle.RoundCap)
        stroker.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        stroker.setWidth(self._intersectShapeWidth())
        path.addPath(self._linePath)
        path.addPath(self._headPath)
        self._shape = stroker.createStroke(path)
        
    def _intersectShapeWidth(self):
        return self.pen().widthF() * self.intersect_shape_width_multiple
                
    def shape(self):
        return self._shape    
    
    def _selectionShape(self):
        return self.shape()
    
    def hoverEnterEvent(self, event):
        if self.is_bezier_curve():
            for point in self._points[1:-1]:
                point.setVisible(True)  
        super().hoverEnterEvent(event)
        
    def hoverLeaveEvent(self, event):
        tmr = self._pointVisTimer = QTimer()
        tmr.setSingleShot(True)
        tmr.setInterval(self.control_point_visible_time)
        tmr.timeout.connect(self._hideControlPoints)
        tmr.start()
        super().hoverLeaveEvent(event)
        
    def _hideControlPoints(self):
        for point in self._points:
            point.setVisible(False)
        
    def _buildContextMenu(self, event):
        menu = QMenu()
        menu.addAction(f"Delete arrow {self.label()}").triggered.connect(self.delete)
        menu.addSeparator()
        action = menu.addAction("Bezier curve")
        action.setCheckable(True)
        action.setChecked(self.is_bezier_curve())
        action.toggled.connect(self.toggle_bezier)
        return menu
            
    def toggle_bezier(self, toggled:bool, emit: bool=True):        
        if toggled != self.is_bezier_curve():
            self._bezier = toggled
            self._points[1].setVisible(toggled)
            self._points[2].setVisible(toggled)
            if not toggled:
                self.set_line_points(self._points[0].pos(), self._points[-1].pos())
                self.update()
            if emit:
                self.bezier_toggled.emit(toggled)    
                
    def set_line_points(self, pos0, pos1):
        u = QVector2D(pos1 - pos0)
        a = u.length()
        a /= (len(self._points) - 1)
        u.normalize()
        self._points[0].setPos(pos0)
        self._points[-1].setPos(pos1)
        for k in range(1, len(self._points)-1):
            self._points[k].setPos(pos0 + k*a*u.toPointF())
            
    def center_label(self):
        self.label_item().setPos((self._points[0].pos() + self._points[-1].pos()) / 2)
        
    def show_control_points_longer(self):
        if self._pointVisTimer is not None:
            self._pointVisTimer.start()
