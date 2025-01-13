from gfx.arrow import Arrow
from gfx.directed_graph import DirectedGraph
from PyQt5.QtWidgets import QMenu
from bidict import bidict

class GraphMorphism(Arrow):
    def __init__(self, label: str=None, domain: DirectedGraph = None, codomain: DirectedGraph = None, pickled=False):
        super().__init__(label, domain, codomain, pickled)
        
        self._imageMap = bidict()
        self._domainNodes = {}
        self._domainArrows = {}
        self._codomainNodes = {}
        self._codomainArrows = {}
        
        if not pickled:
            GraphMorphism.finish_setup(self)
    
    def take_image(self):
        if self.dom() is None or self.cod() is None:
            raise Exception("Both domain and codomain must be set before calling GraphMorphism.take_image().")
        
        for X in self.dom().nodes():            
            if id(X) not in self._domainNodes:
                self._domainNodes[id(X)] = X
                FX = X.copy()
                self.cod().add_node(FX)
                FX.setPos(X.pos())
                self._codomainNodes[id(FX)] = FX
                self._imageMap[id(X)] = id(FX)
        
        for A in self.dom().arrows():
            if id(A) not in self._domainArrows:
                FA = A.copy()
                self.cod().add_arrow(FA)
                FA.setPos(A.pos())
                FA.set_label(A.label())
                FA.set_source(self._codomainNodes[self._imageMap[id(A.source())]])
                FA.set_target(self._codomainNodes[self._imageMap[id(A.target())]])
                FA.update()
                self._domainArrows[id(FA)] = FA
                self._imageMap[id(A)] = id(FA)
               
    def copy(self):
        f = GraphMorphism(label=self.label(), domain=self.dom(), codomain=self.cod())
        return f
    
    def dom(self):
        return self.source()
    
    def cod(self):
        return self.target()

    def _buildContextMenu(self, event):
        menu = QMenu()
        menu.addAction("Take image").triggered.connect(self.take_image)
        return menu