from PyQt5.QtWidgets import QGraphicsObject
from gfx.label import Label
from copy import copy
from PyQt5.QtCore import QRectF

class Base(QGraphicsObject):
    def __init__(self, label: str = None, pickled=False):
        super().__init__()
        
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
    
    def __copy__(self):
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
    
    def update(self, rect: QRectF = None, memo: set = None):
        if memo is None:
            memo = set()
        if id(self) not in memo:
            memo.add(id(self))
            self._update(rect, memo)    
        if rect is None:
            QGraphicsObject.update(self)
        else:
            QGraphicsObject.update(self, rect)            
    