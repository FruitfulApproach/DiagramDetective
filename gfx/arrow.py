from gfx.base import Base
from gfx.node import Node
from copy import copy, deepcopy

class Arrow(Base):
    def __init__(self, label=None, source: Node = None, target: Node = None, pickled=False):
        super().__init__(label, pickled)
        self._source = source
        self._target = target
        
        if not pickled:
            self.finish_setup()
            
    def __setstate__(self, data):
        self.__init__(pickled=True)
        super()._setstate(data)
        self.finish_setup()
        
    def __getstate__(self):
        return self._getstate({})
    
    def _getstate(self, data: dict):
        super()._getstate(data)
        return data
            
    def finish_setup(self):
        super().finish_setup()
        
    def __deepcopy__(self, memo):
        if id(self) not in memo:
            f = copy(self)
            f.source = deepcopy(self.source, memo)
            f.target = deepcopy(self.target, memo)
            memo[id(self)] = f
            return f
        return memo[id(self)]
    
    def __copy__(self, memo):
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
        self._source = source
        
    @target.setter
    def target(self, target):
        self._target = target