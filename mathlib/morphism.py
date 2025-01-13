from gfx.arrow import Arrow
from mathlib.object import Object

class Morphism(Arrow):
    def __init__(self, label: str, dom: Object = None, cod: Object = None, pickled=False):
        super().__init__(label, dom, cod, pickled)
        self._supposedlyEpic = False
        
    def category(self):
        return self.parent_graph()
    
    def copy(self):
        f = Morphism(label=self.label(), dom=self.dom(), cod=self.cod())
        return f
    
    def dom(self):
        return self.source()
    
    def cod(self):
        return self.target
    
    def _buildContextMenu(self, event):
        menu = super()._buildContextMenu(event)
        menu.addSeparator()
        action = menu.addAction("Epimorphism")
        action.setCheckable(True)
        action.setChecked(self.is_supposedly_epic)
        action.triggered.connect(self.suppose_epimorphism)        
        return menu
    
    def suppose_epimorphism(self, true: bool):
        if true:
            self._supposedlyEpic = True
            self._headStyle = self.DoubleHead
        else:
            self._supposedlyEpic = False
            self._headStyle = self.SingleHead
        self.update()
        
    def is_supposedly_epic(self):
        return self._supposedlyEpic