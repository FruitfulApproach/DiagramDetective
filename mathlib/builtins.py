from mathlib.semicategory import Semicategory
from mathlib.object import Object
from mathlib.morphism import Morphism

def initialize_builtins():
    global BigCat
    BigCat = Semicategory("𝐁𝐢𝐠𝐂𝐚𝐭", objects=Semicategory("𝓒", objects=Object("A"), morphisms=Morphism("a")), morphisms=Morphism("f"))


BigCat = None