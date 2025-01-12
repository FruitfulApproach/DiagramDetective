from PyQt5.QtWidgets import QGraphicsScene
import mathlib.builtins as builtin
from PyQt5.QtCore import QPointF, Qt, QRectF, QTimer
from PyQt5.QtGui import QTransform, QFont, QBrush, QColor, QPen
from gfx.directed_graph import DirectedGraph
from gfx.label import Label
from gfx.node import Node
from core.qt_pickle_utility import SimpleBrush
from gfx.arrow import Arrow
from functools import cmp_to_key

class Scene(QGraphicsScene):
    scene_rect_pad = 10.0
    resize_scene_rect_time = 3500
    
    def __init__(self, pickled=False):
        super().__init__()
        
        # TODO
        self.setBackgroundBrush(SimpleBrush(Qt.lightGray))
        self._mousePressed = False
        self._placingArrow = None
        self._movingItems = []
        self._moveItemsMemo = set()
        
        if not pickled:
            S = self._ambientSpace = builtin.BigCat
            self.addItem(S)
            A = S()
            A.setPos(QPointF(-100, -100))
            B = S()
            B.setPos(QPointF(100, 100))
            self.finish_setup()
            
    def finish_setup(self):
        self.setFont(QFont("Serif", 23))
        self.ambient_space.setFlag(self.ambient_space.ItemIsSelectable, False)
           
    @property
    def ambient_space(self):
        return self._ambientSpace
    
    #def drawBackground(self, painter, rect):
        #space = self.ambient_space
        #r = space.corner_radius
        #painter.setRenderHint(painter.Antialiasing)
        #painter.setBrush(space.fill_brush)
        #painter.setPen(space.border_pen)
        #painter.drawRoundedRect(self.sceneRect(), r, r)
        #painter.setRenderHint(painter.Antialiasing)
        #painter.setFont(self.font())
        #painter.setPen(QPen(Qt.black, 1.0))   # TODO: implement text_color in base; then here grab it from ambient_space
        #painter.drawText(QPointF(), self.ambient_space.label)
        
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
                    X.update()
                else:
                    super().mouseDoubleClickEvent(event)
    
    def mousePressEvent(self, event):
        self._mousePressed = True
        item = self.itemAt(event.scenePos(), QTransform())
        
        if event.button() == Qt.LeftButton:                
            if item is None:
                for item in self.items():    
                    item.setSelected(False)             # BUGFIX: items were not automatically deselected already... o_o
                self.update()
            else:
                if isinstance(item, Node):
                    r = item.connect_button_rect()
                    p = item.mapFromScene(event.scenePos())
                    
                    if item is not self.ambient_space:                    
                        if len(self.selectedItems()) <= 1 and r.contains(p) and item.in_arrow_connect_mode:
                            X = item
                            C = item.parentItem()
                            
                            if C is None:
                                C = self.ambient_space
                            
                            a = C(None, X, None)
                            pos = event.scenePos()
                            if a.parentItem() is not None:
                                pos = a.parentItem().mapFromScene(pos)
                            a.setPos(pos)
                            a.center_label()
                            self._placingArrow = a
                            event.accept()
                            self.update()
                            return
    
                if not item.isSelected():
                    if isinstance(item, Label):
                        item = item.parentItem()
                    for item1 in self.selectedItems():
                        item1.setSelected(False)
                    item.setSelected(True)
                
                self._movingItems = self.selectedItems()
                                              
                if self._movingItems:
                    for item in list(self._movingItems):
                        if isinstance(item, Label):
                            parent = item.parentItem()
                            if isinstance(parent, Node):
                                if parent not in self._movingItems:
                                    self._movingItems.append(parent)
                            self._movingItems.remove(item)                    
                                        
                        if isinstance(item, Arrow):
                            if item.source in self._movingItems and item.target in self._movingItems:
                                self._moveItemsMemo.add(id(item))
                            else:
                                self._movingItems.remove(item)
                                item.setSelected(False)
                                
                    self._movingItems = list(filter(lambda i: not any(j.isAncestorOf(i) for j in self._movingItems), self._movingItems))
                                
                    event.accept()             
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        if self._placingArrow:
            a = self._placingArrow
            pos = a.mapFromScene(event.scenePos())
            a.target_point.setPos(pos)
            #a.set_line_points()
            a.center_label()
            a.update()
            self.update()
            event.accept()
        else:
            if self._movingItems:
                event.accept()
                delta = event.scenePos() - event.lastScenePos()
                memo = set(self._moveItemsMemo)
                
                for item in self._movingItems:
                    item.setPos(item.pos() + delta)
                    item.update(memo=memo, arrows=True)
                    
                self.update()
                    
                    #if isinstance(item, Node):
                        #space: DirectedGraph = item.parent_graph
                        
                        #for arrow in space.arrows_from(item):
                            #arrow.update(memo=memo)
                            
                        #for arrow in space.arrows_to(item):
                            #arrow.update(memo=memo)
                        
                        #parent = item
                        #while (parent := parent.parentItem()) is not None:
                            #parent.update(memo=memo)
                        
                        #self.ambient_space.update(memo=memo)
                                 
        super().mouseMoveEvent(event)
        
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
            item = None
            
            for item in items:                
                if item not in (a, a.target_point, a.source_point):
                    while (not isinstance(item, Node)) or self.arrow_cant_connect_target(a, item):
                        item = item.parentItem()
                        
                        if item is None:
                            break
                    else:
                        break
        
            if item is None:
                self.update()
                a.delete()
            else:
                if isinstance(item, Node) and not self.arrow_cant_connect_target(a, item):
                    a.target = item
                    a.center_label()
                    a.update(force=True)
                else:
                    a.delete()
                    
            self.update()
        
        elif self._movingItems:
            self._movingItems.clear()
            self._moveItemsMemo.clear()
        super().mouseReleaseEvent(event)
        
    def arrow_cant_connect_target(self, arrow: Arrow, node: Node) -> bool:
        space = arrow.parent_graph
        return space.arrow_cant_connect_target(arrow, node)
        
