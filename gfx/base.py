from PyQt6.QtWidgets import QGraphicsObject, QGraphicsItem
from gfx.label import Label
from PyQt6.QtCore import QRectF, Qt, pyqtSignal, QPointF
from core.utility import simple_max_contrasting_color
from PyQt6.QtGui import QPen
from datetime import datetime, timedelta

class Base(QGraphicsObject):
    position_changing = pyqtSignal(QPointF)   # Sends delta
    position_changed = pyqtSignal(QPointF)    # "
    mouse_moved = pyqtSignal(QPointF)  # Sends delta
    adding_child = pyqtSignal(QGraphicsItem)
    removing_child = pyqtSignal(QGraphicsItem)
    
    minimum_update_interval = timedelta(milliseconds=25)
    
    def __init__(self, label: str = None, pickled=False):
        super().__init__()
        
        self._posChangingMemo = set()
        self._previousUpdateTime = None
        self._expandToScene = None
        
        if not pickled:
            if label is not None:
                self._label = Label(label)
            else:
                self._label = None
            Base.finish_setup(self)
            
    def __setstate__(self, data):
        self.__init__(pickled=True)
        self._setstate(data)
        self.finish_setup()
        
    def _setstate(self, data):
        # Called by subclass __setstate__'s
        self._label = data['label']
        
    def __getstate__(self):
        return self._getstate({})
        
    def _getstate(self, data: dict):
        data['label'] = self._label
        return data
        
    def finish_setup(self):
        if self._label:
            self._label.setParentItem(self)
        
    def __deepcopy__(self, memo: dict):
        if id(self) not in memo:
            n = copy(self)
            memo[id(self)] = n
        return memo[id(self)]
    
    def copy(self):
        n = Base(label=self.label())
        return n
    
    def label(self):
        return self._label.text()
    
    def set_label(self, label: str):
        self._label.set_text(label)
    
    def label_item(self):
        return self._label
              
    def __repr__(self):
        return f'{self.text()}:Base(@{id(self)}'
    
    def parent_graph(self):
        parent = self.parentItem()        
        if parent is None:
            return self.scene().ambient_space()     
        return parent
    
    def update(self, rect: QRectF = None, memo: set = None, force=False, arrows=True):
        if memo is None:
            memo = set()
        if force or id(self) not in memo:
            memo.add(id(self))
            
            if force or self._previousUpdateTime is None or \
               (datetime.now()- self._previousUpdateTime) > self.minimum_update_interval:
                self._update(rect, memo, arrows)
                
                ancestor = self.parentItem()
                while ancestor is not None:
                    ancestor.update(rect, memo, force, arrows)
                    ancestor = ancestor.parentItem()
                    
                if rect is None:
                    QGraphicsObject.update(self)
                else:
                    QGraphicsObject.update(self, rect)
                
                self._previousUpdateTime = datetime.now()
            
    def paint(self, painter, option, widget):        
        if self.isSelected() and self.scene():
            shape = self._selectionShape()
            bgcolor = self.scene().backgroundBrush().color()
            col = simple_max_contrasting_color(bgcolor)
            painter.strokePath(shape, QPen(col, 1.0, Qt.PenStyle.DotLine))
            
    def _selectionShape(self):
        raise NotImplementedError
    
    def contextMenuEvent(self, event):
        menu = self._buildContextMenu(event)
        menu.exec(event.screenPos())
        
    def _buildContextMenu(self, event):
        raise NotImplementedError
    
    def setPos(self, pos: QPointF):
        if pos != self.pos():        
            super().setPos(pos)
            
    def delete(self):
        raise NotImplementedError
        
    def expand_to_scene(self):
        if self._expandToScene is None:
            self._setupExpandToScene()
        return self._expandToScene
    
    def _setupExpandToScene(self):
        pass