from gfx.arrow import Arrow
from mathlib.object import Object

class Morphism(Arrow):
    def __init__(self, label: str, dom: Object = None, cod: Object = None, pickled=False):
        super().__init__(label, dom, cod, pickled)
        
    @property
    def category(self):
        return self.parent_graph
    
    def copy(self):
        f = Morphism(label=self.label, dom=self.dom, cod=self.cod)
        return f
    
    @property
    def dom(self):
        return self.source
    
    @property
    def cod(self):
        return self.target