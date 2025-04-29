# DiagramDetective 🕵🏾‍♀️

## ToDo's (Outdated)
1. GraphMorphism class together with taking images / reflecting name changes using signals/slots.
2. DiagramRules/Properties (what should we call them; where do they reside etc).  These are each of the type ForAll ... There Exists (dashed lines drawn).
3. It's true that even surjection can be written as a single ForAll...Exists (dashed lines)diagram, and so can most definitions / theorems.
4. Cancel R-Mod as functor - it is not a match to how we typically think about R-Modules as structured sets.  
5. If a category doesn't "have binary products", then introducing a product is under a supposition that it exists and thus a hypothesis to a theorem builder.
6. Consider going through Weibel and classifying the types of statements made "... then this row is exact", "... there exists a well-defined hom from X to Y.", etc.
7. Rounded-corner rect, colored tags as properties on objects, diagrams, arrows: "injective", "chain complex", "reverse chain complex", 
"-- exact --" at different angles of sequence arrows.  These can be enabled from the context menu, or disabled by right-clicking and going
to the tag's context menu, and then "Remove property".
8. Directory library of .dd Scene pickles which represent above-mentioned DiagramRules.  E.g. category-theory > morphism > epimorphism > definition.dd

## TODO's (New)
1. Don't allow node nesting (too cludgy)
2. Modular expression parsing, e.g. RingElement has its own parser, AbelianCategory has its own parser, etc.
3. Unicode subscript support when the user types in x10 => x + (subscripted 10), x1 0 => x_1 * 0
4. Instead of nested nodes, the user double-clicks to jump to a tab who's ambient space is the parent node
5. Pointier arrows (make this a setting per directed_graph)
6. Axioms editable by user:

class AbelianMagma(Axioms):
    def closure_axiom(self):
        A = self.subject() 
        for x in A:
            for y in A:
                x + y in A
            
            # Python __contains__ gets converted to boolean, so will have to __enter__ / __exit__ a mode
    
    def commutativity_axiom(self):
        A = self.subject()        
        for x in A:                 # Use python ast to decode if we need to
            for y in A:
                if x + y in A:
                    x + y == y + x
                    
                    
class Object:
    def add_property(self, p)
        p.set_subject(self)
        
If you add property "commutes" to an object, it's refering to its nested diagram / expanded scene

class DiagramCommutes(Axiom):
    def applicable_to(self, subject):
        return isinstance(subject, Node)        
        
    def axiom(self):
        D = self.subject()        
        for X in Ob(D):
            for Y in Ob(D):
                for p in D.paths(X, Y):
                    for q in D.paths(X, Y):
                        p == q
                    
class CategoryHasProducts(self, subject):
    def applicable_to(self):
        return isinstance(subject, Node)
        
7. Properties / axioms can be added via context-menu on a node or arrow.  To apply to a diagram, therefore,
all diagram items must sit inside of a node (nested) (?)  Or should we allow arbitrary selections?  

8. The property then appears as a tag which the user can then delete to remove the property.

9. Taking elements is built-in, as well as gluing along a common subdiagram.  (or should we model it using a pullback of graphs?)


class CDsGlueAlongMaximalCommonSubdiagram(Axiom):
    @staticmethod
    def is_applicable_to(subject):
        if isinstance(subject, tuple) and len(subject) == 2:
            return all(isinstance(D, Node) and D.has_property(DiagramCommutes) for D in subject)
        return False
        
    def axiom(self):
        C = self.subject()[0]
        D = self.subject()[1]
        G = None
        
        for E in C.subdiagrams():
            for F in D.subdiagrams():
                if E.equals(F):     # Equality / isomorphism check
                    if G is None:
                        G = E
                    else:
                        if E.size() > G.size():
                            G = E
                            
        DiagramCommutes(G)   # If C,D are in the same scene, then G goes there, else, G goes into its own new scene / tab.
        
    
10.  If for some reason we need to select two arrows or something for a property.  We put a diagramming node around the connected component, and give it a 
property tag about g & f (?)
        

