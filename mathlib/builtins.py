from mathlib.semicategory import Semicategory
from mathlib.object import Object
from mathlib.morphism import Morphism

def initialize_builtins():
    global Semicategories
    Semicategories = Semicategory("𝐒𝐞𝐦𝐢𝐜𝐚𝐭𝐞𝐠𝐨𝐫𝐢𝐞𝐬", objects=Semicategory("S", objects=Object("X"), morphisms=Morphism("f")))


Semicategories = None