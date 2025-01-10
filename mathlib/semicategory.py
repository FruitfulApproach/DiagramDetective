from mathlib.object import Object
from mathlib.morphism import Morphism
from gfx.directed_graph import DirectedGraph
from gfx.arrow import Arrow
from gfx.node import Node

class Semicategory(DirectedGraph):
    def __init__(self, label=None, objects: Object = None, morphisms: Morphism = None, pickled=False):
        super().__init__(label, objects, morphisms)
        
        if not pickled:
            self.finish_setup()
            
    def __setstate__(self, data):
        self.__init__(pickled=False)
        self._setstate(data)
        self.finish_setup()
        
    def _setstate(self, data):
        super()._setstate(data)
        
    def __getstate__(self):
        data = {}
        super()._getstate(data)
        return data
    
    def finish_setup(self):
        super().finish_setup()
        
    def __deepcopy__(self, memo):
        if id(self) not in memo:
            X = self.copy()
            memo[id(self)] = X
        return memo[id(self)]
    
    def copy(self):
        X = Semicategory(label=self.label, objects=self.object_type, morphisms=self.morphism_type)
        return X
    
    @property
    def morphism_type(self):
        return self.arrow_type
    
    @property
    def object_type(self):
        return self.node_type
    
    def _arrowCantConnect(self, arrow: Arrow, node: Node, other_end: Node):
        if not isinstance(arrow, self.arrow_type.__class__):
            return True
        if not isinstance(node, self.node_type.__class__):
            return True
        if not isinstance(other_end, self.node_type.__class__):
            return True
        if other_end.category is not node.category:
            return True
        return super()._arrowCantConnect(arrow, node, other_end)       
        