from mathlib.semicategory import Semicategory
from mathlib.object import Object
from mathlib.morphism import Morphism
from gfx.directed_graph import DirectedGraph
from gfx.graph_morphism import GraphMorphism
from gfx.node import Node
from gfx.arrow import Arrow

def initialize_builtins():
    global BigCat
    BigCat = Semicategory("𝐁𝐢𝐠𝐂𝐚𝐭", objects=DirectedGraph("𝓒", node_type=Node("A"), arrow_type=Arrow("a")), morphisms=GraphMorphism("F"))


BigCat = None