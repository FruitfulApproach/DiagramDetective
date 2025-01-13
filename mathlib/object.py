import gfx.node as node

class Object(node.Node):
    def __init__(self, label: str, pickled=False):
        super().__init__(label, pickled)
        
        if not pickled:
            self.finish_setup()
            
    def finish_setup(self):
        pass        
    
    def category(self):
        return self.parent_graph()
    
    def copy(self):
        X = Object(label=self.label())
        return X
    
    def __repr__(self):
        return f'{self.label()}:Object(@{id(self)})'    