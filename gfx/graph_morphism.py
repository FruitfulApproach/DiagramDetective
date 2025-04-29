from gfx.arrow import Arrow
from gfx.directed_graph import DirectedGraph
from PyQt5.QtWidgets import QMenu
from bidict import bidict
from gfx.node import Node
from PyQt5.QtCore import QPointF
from gfx.control_point import ControlPoint
from gfx.base import Base

class GraphMorphism(Arrow):
    def __init__(self, label: str=None, domain: DirectedGraph = None, codomain: DirectedGraph = None, pickled=False):
        super().__init__(label, domain, codomain, pickled)
        
        self._imageMap = bidict()
        self._domainNodes = {}
        self._domainArrows = {}
        self._codomainNodes = {}
        self._codomainArrows = {}
        self._domainControlPoints = {}
        self._codomainControlPoints = {}
        self._reflectPosChanges = True    # TODO: pickle these
        self._reflectDeletions = True
        self._imageTaken = False
        
        if not pickled:
            GraphMorphism.finish_setup(self)
    
    def take_image(self):
        D = self.dom()
        C = self.cod()
        
        if D is None or C is None:
            raise Exception("Both domain and codomain must be set before taking image.")
        
        for X in list(D.nodes()):
            self._setupNode(X)        
        for A in list(D.arrows()):
            self._setupArrow(A)            
            
        D.adding_child.connect(lambda child: self._onChildAddedToDomain(child))
        D.removing_child.connect(lambda child: self._onChildRemoved(child))
        #C.adding_child.connect(lambda child: self._onChildAddedToCodomain(child))
        C.removing_child.connect(lambda child: self._onChildRemoved(child))            
            
        self._imageTaken = True
        
    def _setupNode(self, X: Node):
        C = self.cod()        
        if id(X) not in self._domainNodes:
            self._domainNodes[id(X)] = X
            FX = X.copy()
            FX.set_label(self.image_label(X.label()))
            C.add_node(FX)
            FX.setPos(X.pos())
            self._codomainNodes[id(FX)] = FX
            self._imageMap[id(X)] = id(FX)
            X.mouse_moved.connect(lambda delta, item=X: self._onItemPositionChanged(item, delta))
            FX.mouse_moved.connect(lambda delta, item=FX: self._onItemPositionChanged(item, delta))
            
    def _setupArrow(self, A: Arrow):
        C = self.cod()
        if id(A) not in self._domainArrows:
            self._domainArrows[id(A)] = A
            FA = A.copy()
            C.add_arrow(FA)
            FA.setPos(A.pos())
            FA.label_item().setPos(A.label_item().pos())
            FA.set_label(A.label())
            #FA.set_source(self._codomainNodes[self._imageMap[id(A.source())]])
            #FA.set_target(self._codomainNodes[self._imageMap[id(A.target())]])
            # BUGFIX: ^^ above causes exception; do it this way:
            A.source_was_set.connect(lambda source: self._reflectArrowSource(source, FA))
            A.target_was_set.connect(lambda target: self._reflectArrowTarget(target, FA))
            self._codomainArrows[id(FA)] = FA
            self._imageMap[id(A)] = id(FA)
            A.mouse_moved.connect(lambda delta, item=A: self._onItemPositionChanged(item, delta))
            A.bezier_toggled.connect(lambda b, arrow=A: self._onBezierToggled(arrow, b))
            for k, point in enumerate(A.control_points()):
                FA.setPos(point.pos())
                FA.mouse_moved.connect(lambda delta, item=FA: self._onItemPositionChanged(item, delta))
                FA.bezier_toggled.connect(lambda b, arrow=A: self._onBezierToggled(arrow, b))
                if k in {1, 2}:
                    point1 = FA.control_points()[k]
                    self._domainControlPoints[id(point)] = point
                    self._codomainControlPoints[id(point1)] = point1
                    self._imageMap[id(point)] = id(point1) 
                    point.mouse_moved.connect(
                                lambda delta, point=point: self._onItemPositionChanged(point, delta))
                    point1.mouse_moved.connect(
                                lambda delta, point1=point1: self._onItemPositionChanged(point1, delta))                  
            FA.update()
            
    def _reflectArrowSource(self, source: Node, A: Arrow):
        if source:
            A.set_source(self._codomainNodes[self._imageMap[id(source)]])
        else:
            A.set_source(None)
        A.update()
    
    def _reflectArrowTarget(self, target: Node, A: Arrow):
        if target:
            A.set_target(self._codomainNodes[self._imageMap[id(target)]])
        else:
            A.set_target(None)
        A.update()
               
    def copy(self):
        f = GraphMorphism(label=self.label(), domain=self.dom(), codomain=self.cod())
        return f
    
    def dom(self):
        return self.source()
    
    def cod(self):
        return self.target()

    def _buildContextMenu(self, event):
        menu = QMenu()
        if not self._imageTaken:
            menu.addAction("Take image").triggered.connect(self.take_image)
        action = menu.addAction("Reflect position changes")
        action.setCheckable(True)
        action.setChecked(self.reflect_pos_changes())
        action.toggled.connect(self.set_reflect_pos_changes)
        return menu
    
    def reflect_pos_changes(self):
        return self._reflectPosChanges
        
    def set_reflect_pos_changes(self, reflect: bool):
        self._reflectPosChanges = reflect
        
    def reflect_deletions(self):
        return self._reflectDeletions
    
    def set_reflect_deletions(self, reflect: bool):
        self._reflectDeletions = reflect
        
    def _onBezierToggled(self, arrow: Arrow, toggled: bool, memo:set = None):
        if memo is None:
            memo = set()            
        if id(arrow) not in memo:
            memo.add(id(arrow))
            arrow_parent = arrow.parent_graph()
            parent = self.parent_graph()
            for F in parent.arrows_from(arrow_parent):
                if isinstance(F, GraphMorphism):
                    if F.reflect_pos_changes():
                        reflect = None
                        if id(arrow) in F._imageMap:
                            reflect = F._codomainArrows[F._imageMap[id(arrow)]]
                        elif id(arrow) in F._imageMap.inv:
                            reflect = F._domainArrows[F._imageMap.inv[id(arrow)]]                        
                        if reflect and id(reflect) not in memo:
                            reflect.toggle_bezier(toggled, emit=False)
                            self._onBezierToggled(reflect, toggled, memo)
        
    def _onItemPositionChanged(self, item, delta:QPointF, memo: set = None):
        if memo is None:
            memo = set()        
        if id(item) not in memo:
            memo.add(id(item))
            item_parent = item.parent_graph()
            parent = self.parent_graph()
            for F in parent.arrows_from(item_parent):
                if isinstance(F, GraphMorphism):
                    if F.reflect_pos_changes():                            
                        reflect = self._getReflection(item, F)
                        if reflect and id(reflect) not in memo:
                            reflect.setPos(reflect.pos() + delta)
                            reflect.update()
                            self._onItemPositionChanged(reflect, delta, memo)
    
    def image_label(self, label: str) -> str:
        F = self.label()
        if "." in F:
            return F.replace(".", label)
        return F + label
                        
    def _onChildAddedToDomain(self, child: Base, memo: set = None):
        if memo is None:
            memo = set()
        if id(child) not in memo:
            memo.add(id(child))            
        if isinstance(child, Node):
            self._setupNode(child)
        elif isinstance(child, Arrow):
            self._setupArrow(child)
            
    def _onChildRemoved(self, child: Base, memo: set = None):
        if memo is None:
            memo = set()
        if id(child) not in memo:
            memo.add(id(child))
            item_parent = child.parent_graph()
            parent = self.parent_graph()            
            for F in parent.arrows_from(item_parent):
                if isinstance(F, GraphMorphism):
                    if F.reflect_deletions():
                        reflect = self._getReflection(child, F)
                        if reflect and id(reflect) not in memo:
                            reflect.delete()
                            self._onChildRemoved(reflect, memo)
                            
    def _getReflection(self, item: Base, F) -> Base:
        reflect = None
        try:                
            if id(item) in F._imageMap:
                item_id = F._imageMap[id(item)]
                if isinstance(item, Node):
                    reflect = F._codomainNodes[item_id]
                elif isinstance(item, Arrow):
                    reflect = F._codomainArrows[item_id]
                elif isinstance(item, ControlPoint):
                    reflect = F._codomainControlPoints[item_id]            
            elif id(item) in F._imageMap.inv:
                item_id = F._imageMap.inv[id(item)]
                if isinstance(item, Node):
                    reflect = F._domainNodes[item_id]
                elif isinstance(item, Arrow):
                    reflect = F._codomainArrows[item_id]
                elif isinstance(item, ControlPoint):
                    reflect = F._domainControlPoints[item_id] 
        except:
            pass
        return reflect        
                        
