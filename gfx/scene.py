from PyQt5.QtWidgets import QGraphicsScene
import mathlib.builtins as builtin
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QTransform, QFont, QBrush, QColor, QPen
from gfx.directed_graph import DirectedGraph
from gfx.label import Label
from gfx.node import Node
from core.qt_pickle_utility import SimpleBrush

class Scene(QGraphicsScene):
    def __init__(self, pickled=False):
        super().__init__()
        
        # TODO
        self.setBackgroundBrush(SimpleBrush(QColor(255, 250, 115)))
        self._mousePressed = False
        
        if not pickled:
            C = self._ambientSpace = builtin.BigCat
            C.setVisible(False)
            self.addItem(C)
            A = C("A")
            A.setPos(QPointF(-100, -100))
            B = C("B")
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
        item = self.itemAt(event.scenePos(), QTransform())
        
        if item is None:
            S = self.ambient_space
            dbg_label = "S"
            pos = event.scenePos()
            X = S(dbg_label)
            X.set_center_pos(pos)
        else:
            if isinstance(item, Label):
                item = item.parentItem()

            if isinstance(item, Node):
                r = item.connect_button_rect()
                p = item.mapFromScene(event.scenePos())
                
                if r.contains(p) and item.in_arrow_connect_mode():
                    print("CONNECT")
            
                if isinstance(item, DirectedGraph):
                    S = item
                    dbg_label = "s"
                    pos = item.mapFromScene(event.scenePos())
                    X = S(dbg_label)
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
        super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event):
        self._mousePressed = False
        self.update()                           # BUGFIX: selection rubber band artifacts
        super().mouseReleaseEvent(event)
        
    def mouseMoveEvent(self, event):
        if self._mousePressed:
            self.update()                       # BUGFIX: selection rubber band artifacts
        super().mouseMoveEvent(event)       
        
        