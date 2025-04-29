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
3. Unicode subscript support when the user types in x_10 => x + (subscripted 10), x_1 0 => x_1 * 0
4. Instead of nested nodes, the user double-clicks to jump to a tab who's ambient space is the parent node
5. Pointier arrows (make this a setting per directed_graph)
6. Axioms editable by user:

class AbelianMagma(Set):
    def closure_axiom(self):
        A = self
        for (x,y) in A^2    # Should work with __iter__
            x + y in A      # Python __contains__ gets converted to boolean, so will have to __enter__ / __exit__ a mode

