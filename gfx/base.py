from PyQt5.QtWidgets import QGraphicsObject
from gfx.label import Label
from PyQt5.QtCore import QRectF, Qt
from core.utility import simple_max_contrasting_color
from PyQt5.QtGui import QPen
from datetime import datetime, timedelta

class Base(QGraphicsObject):
    minimum_update_interval = timedelta(milliseconds=25)
    
    def __init__(self, label: str = None, pickled=False):
        super().__init__()
        
        self._previousUpdateTime = None
        
        if not pickled:
            self._label = Label(label)
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
        self._label.setParentItem(self)
        
    def __deepcopy__(self, memo: dict):
        if id(self) not in memo:
            n = copy(self)
            memo[id(self)] = n
        return memo[id(self)]
    
    def copy(self):
        n = Base(label=self.label)
        return n
    
    @property
    def label(self):
        return self._label.text
    
    @label.setter
    def label(self, label: str):
        self._label.text = label
    
    @property
    def label_item(self):
        return self._label
        
    @property
    def space(self):
        parent = self.parentItem()
        if parent is None:
            return self.scene().ambient_space
        return parent
        
    def __repr__(self):
        return f'{self.text}:Base(@{id(self)}'
    
    @property
    def parent_graph(self):
        parent = self.parentItem()        
        if parent is None:
            return self.scene().ambient_space        
        return parent
    
    def update(self, rect: QRectF = None, memo: set = None, force=False):
        if memo is None:
            memo = set()
        if id(self) not in memo:
            memo.add(id(self))
            
            if force or self._previousUpdateTime is None or \
               (datetime.now()- self._previousUpdateTime) > self.minimum_update_interval:
                self._update(rect, memo)
                
                ancestor = self.parentItem()
                while ancestor is not None:
                    ancestor.update(rect, memo)
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
            painter.strokePath(shape, QPen(col, 1.0, Qt.DotLine))
            
    def _selectionShape(self):
        raise NotImplementedError