from gfx.arrow import Arrow
from gfx.directed_graph import DirectedGraph
from PyQt5.QtWidgets import QMenu

class GraphMorphism(Arrow):
    def __init__(self, label: str=None, domain: DirectedGraph = None, codomain: DirectedGraph = None, pickled=False):
        super().__init__(label, domain, codomain, pickled)
        
        if not pickled:
            GraphMorphism.finish_setup(self)
    
    def take_image(self):
        assert self.dom and self.cod
        print("TAKE IMAGE MOFO")
               
    def copy(self):
        f = GraphMorphism(label=self.label, domain=self.dom, codomain=self.cod)
        return f
    
    @property
    def dom(self):
        return self.source
    
    @property
    def cod(self):
        return self.target

    def _buildContextMenu(self, event):
        menu = QMenu()
        menu.addAction("Take image").triggered.connect(self.take_image)
        return menu