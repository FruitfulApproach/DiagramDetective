from PyQt6.QtWidgets import QGraphicsScene
import mathlib.builtins as builtin
from PyQt6.QtCore import QPointF, Qt, pyqtSignal
from PyQt6.QtGui import QTransform, QFont, QPen
from gfx.label import Label
from gfx.node import Node
from gfx.arrow import Arrow
from core.qt_pickle_utility import SimpleBrush
from gfx.arrow import Arrow
from functools import cmp_to_key

class Scene(QGraphicsScene):
    scene_rect_pad = 10.0
    resize_scene_rect_time = 3500
    expand_to_scene_requested = pyqtSignal(QGraphicsScene)
    
    def __init__(self, pickled=False):
        super().__init__()
        
        # TODO
        self.setBackgroundBrush(SimpleBrush(Qt.GlobalColor.lightGray))
        self._mousePressed = False
        self._placingArrow = None
        self._movingItems = []
        self._moveItemsMemo = set()
        
        if not pickled:
            S = self._ambientSpace = builtin.BigCat
            S.setVisible(False)
            self.addItem(S)
            self.finish_setup()
            
    def finish_setup(self):
        self.setFont(QFont("Serif", 23))
        self.ambient_space().setFlag(self.ambient_space().GraphicsItemFlag.ItemIsSelectable, False)
           
    def ambient_space(self):
        return self._ambientSpace
    
    def drawBackground(self, painter, rect):
        space = self.ambient_space()
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.fillRect(rect, space.fill_brush())
        painter.setFont(space.label_item().font())
        painter.setPen(QPen(Qt.GlobalColor.black, 1.0))   # TODO: implement text_color in base; then here grab it from ambient_space
        painter.drawText(QPointF(), space.label())
        
    def mouseDoubleClickEvent(self, event):
        if self._placingArrow:
            a = self._placingArrow
            self._placingArrow = None            
            del a
            
        item = self.itemAt(event.scenePos(), QTransform())
        
        if item is None:
            S = self.ambient_space()
            pos = event.scenePos()
            X = S()
            X.setParentItem(None)
            self.addItem(X)
            X.set_center_pos(pos)
        else:
            if isinstance(item, Label):
                item = item.parentItem()
            
            pos = item.mapFromScene(event.scenePos())
            X = item()
            X.set_center_pos(pos)
            X.update()
            self.update()            
        #else:
            #if isinstance(item, Label):
                #item = item.parentItem()
                
            #expand_scene = item.expand_to_scene()
            
            #if expand_scene is not None:
                #self.expand_to_scene_requested.emit(expand_scene)
                
               
    def mousePressEvent(self, event):
        self._mousePressed = True
        item = self.itemAt(event.scenePos(), QTransform())
        
        if event.button() == Qt.MouseButton.LeftButton:                
            if item is None:
                for item in self.items():    
                    item.setSelected(False)             # BUGFIX: items were not automatically deselected already... o_o
                self.update()
            else:
                if isinstance(item, Node):
                    r = item.connect_button_rect()
                    p = item.mapFromScene(event.scenePos())
                    
                    if item is not self.ambient_space():                    
                        if len(self.selectedItems()) <= 1 and r.contains(p) and item.in_arrow_connect_mode:
                            X = item
                            #C = item.parentItem()
                            
                            #if C is None:
                                #C = self.ambient_space()
                            pos = event.scenePos()
                            a = Arrow(label="a", source=X, target=None)
                            
                            if X.parentItem() is None:
                                self.addItem(a)
                                
                            else:
                                a.setParent(X.parentItem())
                                pos = X.mapFromScene(pos)
                               
                            a.setPos(pos)
                            a.center_label()
                            self._placingArrow = a
                            event.accept()
                            self.update()
                            return
    
                if not item.isSelected():
                    if isinstance(item, Label):
                        item = item.parentItem()
                        if not item.isSelected():
                            for item1 in self.selectedItems():
                                item1.setSelected(False)
                            item.setSelected(True)
                    else:
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
                            if item.source() in self._movingItems and item.target in self._movingItems:
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
            a.target_point().setPos(pos)
            a.center_label()
            a.update_shape()                # BUG HACKFIX, don't call a.update() here, for some reason the length of the arrow doubles!
            self.update()
            event.accept()
        else:
            if self._movingItems:
                event.accept()
                delta = event.scenePos() - event.lastScenePos()
                memo = set(self._moveItemsMemo)
                
                for item in self._movingItems:
                    item.setPos(item.pos() + delta)
                    item.mouse_moved.emit(delta)
                    item.update(memo=memo, arrows=True)
                    
                self.update()

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
                if item not in (a, a.target_point(), a.source_point()):
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
                    a.set_target(item)
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
        #TODO:
        if arrow.parentItem() is None:
            return False
        # END TODO
        space = arrow.parent_graph()
        return space.arrow_cant_connect_target(arrow, node)
        
