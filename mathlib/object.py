from gfx.node import Node

class Object(Node):
    @property
    def category(self):
        return self.parent_graph