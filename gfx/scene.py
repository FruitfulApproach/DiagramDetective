from PyQt5.QtWidgets import QGraphicsScene
import mathlib.builtins as builtin
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QTransform, QFont, QBrush
from gfx.directed_graph import DirectedGraph
from gfx.label import Label

class Scene(QGraphicsScene):
    def __init__(self, pickled=False):
        super().__init__()
        
        # TODO
        self.setBackgroundBrush(QBrush(Qt.lightGray))
        
        if not pickled:
            self._ambientSpace = builtin.Semicategories
            self.finish_setup()
            
    def finish_setup(self):
        self.setFont(QFont("Serif", 23))
        self._ambientSpace.setVisible(False)
        self.addItem(self._ambientSpace)        
    
    @property
    def ambient_space(self):
        return self._ambientSpace
    
    def drawBackground(self, painter, rect):
        #painter.setBackground(self.backgroundBrush())
        #painter.setBackgroundMode(Qt.OpaqueMode)
        painter.setBrush(self.backgroundBrush())
        painter.drawRect(rect)
        painter.setRenderHint(painter.Antialiasing)
        painter.setFont(self.font())
        painter.drawText(QPointF(), self.ambient_space.label)
        
    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.scenePos(), QTransform())
        
        if item is None:
            S = self.ambient_space
            dbg_label = "S"
            pos = event.scenePos()
        else:
            if isinstance(item, Label):
                item = item.parentItem()
            
            if isinstance(item, DirectedGraph):
                S = item
                dbg_label = "s"
                pos = item.mapFromScene(event.scenePos())
            else:
                super().mouseDoubleClickEvent(event)
                return
            
        X = S(dbg_label)
        X.set_center_pos(pos)
