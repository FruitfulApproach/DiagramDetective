from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt
from gfx.arrow import Arrow
from gfx.node import Node
from mathlib.object import Object
from core.unicode_utility import next_ascii_prime_variable
from core.qt_pickle_utility import SimpleBrush
from gfx.base import Base

class DirectedGraph(Object):
    node_label_start = 'A'
    arrow_label_start = 'a'
        
    def __init__(self, label: str = None, node_type: Node = None, arrow_type: Arrow = None, pickled=False):
        self._addingChildMemo = set()
        self._removingChildMemo = set()        
        super().__init__(label, pickled)       
        self._nodes = {}    # Keyed by id()
        self._arrows = {}
        self._nodesByLabel = {}
        self._arrowsByLabel = {}
        self._nodeType = node_type
        self._arrowType = arrow_type
        self._arrowsFromNode = {}
        self._arrowsToNode = {}  # Keyed by target node id()
        
    def nodes(self):
        return self._nodes.values()

    def arrows(self):
        return self._arrows.values()
    
    def arrows_to(self, n: Node):
        return self._arrowsToNode.get(id(n), [])
    
    def arrows_from(self, n: Node):
        return self._arrowsFromNode.get(id(n), [])
    
    def arrow_target_was_set(self, arrow, prev_node):
        self._setupArrowsToFromNode(arrow.target(), prev_node, arrow, self._arrowsToNode)
        
    def arrow_source_was_set(self, arrow, prev_node):
        self._setupArrowsToFromNode(arrow.source(), prev_node, arrow, self._arrowsFromNode)
        
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
        
    def node_type(self) -> Node:
        return self._nodeType
    
    def arrow_type(self) -> Arrow:
        return self._arrowType
        
    def is_empty(self):
        return self.node_type() is None
    
    def __call__(self, label: str = None, source: Node=None, target: Node=None):
        if target is None and source is None:
            if label is None:
                label = self.unused_node_variable_label()            
            n = self._nodeType.copy()
            n.set_label(label)
            self.add_node(n)
            return n
        else:
            if label is None:
                label = self.unused_arrow_variable_label()
            a = self._arrowType.copy()
            a.set_label(label)                       
            self.add_arrow(a)
            if source is not None:
                a.set_source(source)
            if target is not None:
                a.set_target(target)            
            return a
    
    def add_node(self, n: Node):
        self._nodes[id(n)] = n
        self._addItem(n, self._nodesByLabel)
                
    def add_arrow(self, a: Arrow):
        self._arrows[id(a)] = a
        self._addItem(a, self._arrowsByLabel)
                
    def _addItem(self, i, by_label):
        if i.label() not in by_label:
            by_label[i.label()] = [i]
        else:
            by_label[i.label()].append(i)          
        i.setParentItem(self)
            
    def update_connecting_arrows(self, n: Node, memo: set):
        for a in self.arrows_from(n):
            a.update(None, memo)            
        for a in self.arrows_to(n):
            a.update(None, memo)
            
    def delete_arrow(self, a: Arrow):
        a.setParentItem(None)        
        l = a.label()
        by_label = self._arrowsByLabel
        if l in by_label:
            if a in by_label[l]:
                by_label[l].remove(a)
            if len(by_label[l]) == 0:
                del by_label[l]
        i = id(a)
        if i in self._arrows:
            del self._arrows[i]
        i = id(a.source())
        from_node = self._arrowsFromNode
        if i in from_node:
            if a in from_node[i]:
                from_node[i].remove(a)
            if len(from_node[i]) == 0:
                del from_node[i]
        to_node = self._arrowsToNode
        i = id(a.target())
        if i in to_node:
            if a in to_node[i]:
                to_node[i].remove(a)
            if len(to_node[i]) == 0:
                del to_node[i]
                
    def delete_node(self, n: Node):
        for arrow in self.arrows_from(n):
            arrow.delete()
        for arrow in self.arrows_to(n):
            arrow.delete()        
        n.setParentItem(None)
        l = n.label()
        by_label = self._nodesByLabel
        if l in by_label:
            if n in by_label[l]:
                by_label[l].remove(n)
        i = id(n)
        if i in self._nodes:
            del self._nodes[i]      
                        
    def arrow_cant_connect_target(self, arrow: Arrow, target: Node) -> bool:
        return self._arrowCantConnect(arrow, target, arrow.source())
    
    def arrow_cant_connect_source(self, arrow: Arrow, source: Node) -> bool:
        return self._arrowCantConnect(arrow, source, arrow.target())
    
    def _arrowCantConnect(self, arrow, node, other_end):            
        if other_end is None:
            return False
        if node.isAncestorOf(arrow):
            return True
        return False
    
    def unused_node_variable_label(self):
        var = self.node_label_start        
        while var in self._nodesByLabel:
            var = next_ascii_prime_variable(var)
        return var
    
    def unused_arrow_variable_label(self):
        var = self.arrow_label_start
        while var in self._arrowsByLabel:
            var = next_ascii_prime_variable(var)
        return var
            
    def copy(self):
        X = DirectedGraph(label=self.label(), node_type=self.node_type(), arrow_type=self.arrow_type())
        return X            
        
    def itemChange(self, change, value):
        if change == self.ItemChildAddedChange:
            self.adding_child.emit(value)
        elif change == self.ItemChildRemovedChange:
            self.removing_child.emit(value)
        return super().itemChange(change, value)
        
    #def connected_component(self, item: Base, component: dict = None):
        #assert isinstance(item, (Node, Arrow))
        
        #if component is None:
            #component = {}
            
        #if id(item) not in component:
            #component[id(item)] = item
            
            #if isinstance(item, Node):
                #for arrow in self.arrows_from(item):
                    #self.connected_component(arrow, component)
                #for arrow in self.arrows_to(item):
                    #self.connected_component(arrow, component)
            #else:
                #self.connected_component(item.target(), component)
                #self.connected_component(item.source(), component)
            
        #return component
        