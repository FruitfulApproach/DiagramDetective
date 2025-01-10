from gfx.arrow import Arrow
from gfx.node import Node
from mathlib.object import Object
from copy import copy

class DirectedGraph(Object):
    def __init__(self, label: str = None, node_type: Node = None, arrow_type: Arrow = None, pickled=False):
        super().__init__(label, pickled)
        self._nodes = {}    # Keyed by id()
        self._arrows = {}
        self._nodesByLabel = {}
        self._arrowsByLabel = {}
        self._nodeType = node_type
        self._arrowType = arrow_type
        self._arrowsFromNode = {}
        self._arrowsToNode = {}  # Keyed by target node id()
        
    @property
    def vertices(self):
        return self._vertex.values()
    
    @property
    def arrows(self):
        return self._arrows.values()
    
    def arrows_to(self, n: Node):
        return self._arrowsToNode.get(id(n), [])
    
    def arrows_from(self, n: Node):
        return self._arrowsFromNode.get(id(n), [])
    
    def arrow_target_was_set(self, arrow, prev_node):
        self._setupArrowsToFromNode(arrow.target, prev_node, arrow, self._arrowsToNode)
        
    def arrow_source_was_set(self, arrow, prev_node):
        self._setupArrowsToFromNode(arrow.source, prev_node, arrow, self._arrowsFromNode)
        
    def _setupArrowsToFromNode(self, node, prev_node, arrow, to_from_node):
        if prev_node is not None:
            i = id(prev_node)
            if i in to_from_node:
                if arrow in to_from_node[i]:
                    to_from_node[i].remove(arrow)
        if node is not None:
            i = id(node)
            if i in to_from_node:
                to_from_node[i].append(arrow)
            else:
                to_from_node[i] = [arrow]        
        
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
            a = copy(self._arrowType)
            self._addArrow(a)
            a.label = label
            a.source = source
            a.target = target            
            return a
    
    def _addNode(self, n: Node):
        self._nodes[id(n)] = n
        self._addItem(n, self._nodesByLabel)
                
    def _addArrow(self, a: Arrow):
        self._arrows[id(a)] = a
        self._addItem(a, self._arrowsByLabel)
                
    def _addItem(self, i, by_label):
        if i.label not in by_label:
            by_label[i.label] = [i]
        else:
            by_label[i.label].append(i)        
        
        if self is self.scene().ambient_space:
            self.scene().addItem(i)
        else:
            i.setParentItem(self)
            
    def update_connecting_arrows(self, n: Node, memo: set):
        for a in self.arrows_from(n):
            a.update(None, memo)            
        for a in self.arrows_to(n):
            a.update(None, memo)
            
    def delete_arrow(self, a: Arrow):
        a.setParentItem(None)        
        l = a.label
        by_label = self._arrowsByLabel
        if l in by_label:
            if a in by_label[l]:
                by_label[l].remove(a)
        i = id(a)
        if i in self._arrows:
            del self._arrows[i]
        i = id(a.source)
        from_node = self._arrowsFromNode
        if i in from_node:
            if a in from_node[i]:
                from_node[i].remove(a)
        to_node = self._arrowsToNode
        i = id(a.target)
        if i in to_node:
            if a in to_node[i]:
                to_node[i].remove(a)
                
    def arrow_cant_connect_target(self, arrow: Arrow, target: Node) -> bool:
        return self._arrowCantConnect(arrow, target, arrow.source)
    
    def arrow_cant_connect_source(self, arrow: Arrow, source: Node) -> bool:
        return self._arrowCantConnect(arrow, source, arrow.target)
    
    def _arrowCantConnect(self, arrow, node, other_end):            
        if other_end is None:
            return False
        parent = other_end.parent_graph        
        while parent is not None:
            if parent.isAncestorOf(node):
                return True
            parent = parent.parentItem()
        return False

            
        
        