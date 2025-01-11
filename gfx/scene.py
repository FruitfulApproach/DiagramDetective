from PyQt5.QtWidgets import QGraphicsScene
import mathlib.builtins as builtin
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QTransform, QFont, QBrush, QColor, QPen
from gfx.directed_graph import DirectedGraph
from gfx.label import Label
from gfx.node import Node
from core.qt_pickle_utility import SimpleBrush
from gfx.arrow import Arrow
from functools import cmp_to_key

class Scene(QGraphicsScene):
    def __init__(self, pickled=False):
        super().__init__()
        
        # TODO
        self.setBackgroundBrush(SimpleBrush(QColor(255, 250, 115)))
        self._mousePressed = False
        self._placingArrow = None
        
        if not pickled:
            S = self._ambientSpace = builtin.BigCat
            S.setVisible(False)
            self.addItem(S)
            A = S()
            A.setPos(QPointF(-100, -100))
            B = S()
            B.setPos(QPointF(100, 100))
            self.finish_setup()
            
    def finish_setup(self):
        self.setFont(QFont("Serif", 23))
           
    @property
    def ambient_space(self):
        return self._ambientSpace
    
    def drawBackground(self, painter, rect):
        space = self.ambient_space
        r = space.corner_radius
        painter.setRenderHint(painter.Antialiasing)
        painter.setBrush(space.fill_brush)
        painter.setPen(space.border_pen)
        painter.drawRoundedRect(self.sceneRect(), r, r)
        painter.setRenderHint(painter.Antialiasing)
        painter.setFont(self.font())
        painter.setPen(QPen(Qt.black, 1.0))   # TODO: implement text_color in base; then here grab it from ambient_space
        painter.drawText(QPointF(), self.ambient_space.label)
        
    def mouseDoubleClickEvent(self, event):
        if self._placingArrow:
            a = self._placingArrow
            self._placingArrow = None            
            del a
            
        item = self.itemAt(event.scenePos(), QTransform())
        
        if item is None:
            S = self.ambient_space
            pos = event.scenePos()
            X = S()
            X.set_center_pos(pos)
        else:
            if isinstance(item, Label):
                item = item.parentItem()

            if isinstance(item, Node):
                r = item.connect_button_rect()
                p = item.mapFromScene(event.scenePos())
            
                if isinstance(item, DirectedGraph):
                    S = item
                    pos = item.mapFromScene(event.scenePos())
                    X = S()
                    X.set_center_pos(pos)
                else:
                    super().mouseDoubleClickEvent(event)
    
    def mousePressEvent(self, event):
        self._mousePressed = True
        item = self.itemAt(event.scenePos(), QTransform())
        if item is None:
            for item in self.items():    
                item.setSelected(False)             # BUGFIX: items were not automatically deselected already... o_o
            self.update()
        else:
            if isinstance(item, Node):
                r = item.connect_button_rect()
                p = item.mapFromScene(event.scenePos())
                
                if r.contains(p) and item.in_arrow_connect_mode:
                    X = item
                    C = item.parentItem()
                    
                    if C is None:
                        C = self.ambient_space
                    
                    a = C(None, X, None)
                    pos = a.mapFromScene(event.scenePos())
                    a.source_point.setPos(pos)
                    a.target_point.setPos(pos)
                    self._placingArrow = a
                    event.accept()
                    
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        if self._placingArrow:
            a = self._placingArrow
            pos = a.mapFromScene(event.scenePos())
            a.target_point.setPos(pos)
            a.center_label()
            a.update()
        else:
            if self._mousePressed:
                self.update()                        
            
            super().mouseMoveEvent(event)
        self.setSceneRect(self.itemsBoundingRect())
        
    def mouseReleaseEvent(self, event):
        self._mousePressed = False
        
        if self._placingArrow:
            a = self._placingArrow                
            self._placingArrow = None
            
            items = self.items(event.scenePos())
            
            def compare(a, b):
                if a.isAncestorOf(b):
                    return 1
                elif b.isAncestorOf(a):
                    return -1
                return 0
            
            items.sort(key=cmp_to_key(compare))
            
            for item in items:                
                if item not in (a, a.target_point, a.source_point):
                    while (not isinstance(item, Node)) or self.arrow_cant_connect_target(a, item):
                        item = item.parentItem()
                        
                        if item is None:
                            break
                    else:
                        break
        
            if item is None:
                a.delete()
            else:
                if isinstance(item, Node) and not self.arrow_cant_connect_target(a, item):
                    a.target = item
                    a.center_label()
                else:
                    a.delete()
                
        self.update()                           # BUGFIX: selection rubber band artifacts
        super().mouseReleaseEvent(event)
        self.setSceneRect(self.itemsBoundingRect())
        
    def arrow_cant_connect_target(self, arrow: Arrow, node: Node) -> bool:
        space = arrow.parent_graph
        return space.arrow_cant_connect_target(arrow, node)
        
        