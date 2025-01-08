from gfx.arrow import Arrow
from gfx.node import Node
from mathlib.object import Object
from copy import copy


class DirectedGraph(Object):
    def __init__(self, label: str = None, node_type: Node = None, arrow_type: Arrow = None, pickled=False):
        super().__init__(label, pickled)
        self._nodes = {} # Keyed by id()
        self._arrows = {}
        self._nodesByLabel = {}
        self._arrowsByLabel = {}
        self._nodeType = node_type
        self._arrowType = arrow_type
        
    @property
    def vertices(self):
        return self._vertex.values()
    
    @property
    def arrows(self):
        return self._arrows.values()
    
    @property
    def node_type(self) -> Node:
        return self._nodeType
    
    @property
    def arrow_type(self) -> Arrow:
        return self._arrowType
        
    @property
    def is_empty(self):
        return self.node_type is None
    
    def __call__(self, label: str, source: Node=None, target: Node=None):
        if target is None and source is None:
            n = copy(self._nodeType)
            n.label = label
            self._addNode(n)
            return n
        else:
            if target is None:
                target = source
            a = copy(self._arrowType)
            a.label = label
            a.source = source
            a.target = target
            self._addArrow(a)
            return a
    
    def _addNode(self, n: Node):
        self._nodes[id(n)] = n
        self._addItem(n, self._nodesByLabel)
        self.update()
        
    def _addArrow(self, a: Arrow):
        self._arrows[id(a)] = a
        self._addItem(a, self._arrowsByLabel)
        self.update()
        
    def _addItem(self, i, by_label):
        if i.label not in by_label:
            by_label[i.label] = [i]
        else:
            by_label[i.label].append(i)        
        
        if self is self.scene().ambient_space:
            self.scene().addItem(i)
        else:
            i.setParentItem(self)        