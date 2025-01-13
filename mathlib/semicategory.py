from mathlib.object import Object
from mathlib.morphism import Morphism
from gfx.directed_graph import DirectedGraph
from gfx.arrow import Arrow
from gfx.node import Node
from core.unicode_utility import ascii_letters_to_script, next_ascii_prime_variable, can_display_char

class Semicategory(DirectedGraph):
    node_label_start = 'C'
    arrow_label_start = 'F'
    
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
        X = Semicategory(label=self.label(), objects=self.object_type(), morphisms=self.morphism_type())
        return X
    
    def morphism_type(self):
        return self.arrow_type()

    def object_type(self):
        return self.node_type()
    
    def _arrowCantConnect(self, arrow: Arrow, node: Node, other_end: Node):
        if not isinstance(arrow, self.arrow_type().__class__):
            return True
        if not isinstance(node, self.node_type().__class__):
            return True
        if not isinstance(other_end, self.node_type().__class__):
            return True
        if other_end.category() is not node.category():
            return True
        return super()._arrowCantConnect(arrow, node, other_end)               
        
    def unused_node_variable_label(self):
        return self._unusedVariableLabel(self.node_label_start, self._nodesByLabel, bold=True, scr=True)
        
    def unused_arrow_variable_label(self):
        return self._unusedVariableLabel(self.arrow_label_start, self._arrowsByLabel, bold=False)
    
    def _unusedVariableLabel(self, var_start, by_label, bold, scr=False):
        var = var_start
        if scr:
            scr_var = ascii_letters_to_script(var, bold) + var[1:]
        else:
            scr_var = var
        while scr_var + var_start[1:] in by_label or not can_display_char(scr_var):
            var = next_ascii_prime_variable(var)
            if scr:
                scr_var = ascii_letters_to_script(var[0], bold)
            else:
                scr_var = var
        scr_var += var_start[1:]  # restore the 's (primes)
        return scr_var
        