from gfx.arrow import Arrow
from gfx.directed_graph import DirectedGraph

class GraphMorphism(Arrow):
    def __init__(self, label: str=None, domain: DirectedGraph = None, codomain: DirectedGraph = None, pickled=False):
        super().__init__(label, domain, codomain, pickled)
        
        if not pickled:
            GraphMorphism.finish_setup(self)

    def set_source(self, source: DirectedGraph):
        super().set_source(source)
        
    def set_target(self, target: DirectedGraph):
        super().set_target(target)
        
    def copy(self):
        f = GraphMorphism(label=self.label, domain=self.source, codomain=self.target)
        return f
    
    @property
    def dom(self):
        return self.source
    
    @property
    def cod(self):
        return self.target