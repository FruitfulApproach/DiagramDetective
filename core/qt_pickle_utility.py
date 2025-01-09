from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt


class SimpleBrush(QBrush):
    def __init__(self, color=None):
        super().__init__(color)
    
    def __setstate__(self, data):
        self.__init__(data['color'])
        self.setStyle(data['style'])    # BUGFIX: this includes Qt.NoBrush style (used on arrows)
        
    def __getstate__(self):
        return {
            'color' : self.color(),
            'style' : self.style()
        }
        
    def __deepcopy__(self, memo):
        brush = SimpleBrush(self.color())
        memo[id(self)] = brush
        return brush
    
class Pen(QPen):
    styleEnum = {
        int(Qt.NoPen) : Qt.NoPen,
        int(Qt.SolidLine) : Qt.SolidLine,
        int(Qt.DashLine) : Qt.DashLine,
        int(Qt.DotLine) : Qt.DotLine,
        int(Qt.DashDotLine) : Qt.DashDotLine,
        int(Qt.DashDotDotLine) : Qt.DashDotDotLine,
        int(Qt.CustomDashLine) : Qt.CustomDashLine,
    }

    capEnum = {
        int(Qt.FlatCap) : Qt.FlatCap,
        int(Qt.SquareCap) : Qt.SquareCap,
        int(Qt.RoundCap) : Qt.RoundCap,
    }

    joinEnum = {
        int(Qt.MiterJoin) : Qt.MiterJoin,
        int(Qt.BevelJoin) : Qt.BevelJoin,
        int(Qt.RoundJoin) : Qt.RoundJoin,
        int(Qt.SvgMiterJoin) : Qt.SvgMiterJoin,
    }

    def __init__(self, color=None, width=None, style=Qt.SolidLine, cap=Qt.RoundCap, join=Qt.RoundJoin):
        if color is None or color == Qt.NoPen:
            super().__init__(Qt.NoPen)
        else:
            super().__init__(color, width, style, cap, join)

    COLOR, WIDTH, STYLE, CAP, JOIN = range(5)
    def __getstate__(self):
        return (self.color(), self.widthF(), int(self.style()), int(self.capStyle()), int(self.joinStyle()))

    def __setstate__(self, data):
        color = data[self.COLOR]
        width = data[self.WIDTH]
        style = self.styleEnum[data[self.STYLE]]
        cap = self.capEnum[data[self.CAP]]
        join = self.joinEnum[data[self.JOIN]]
        self.__init__(color, width, style, cap, join)

    def __deepcopy__(self, memo):
        pen = Pen(self.color(), self.widthF(), self.style(), self.capStyle(), self.joinStyle())
        memo[id(self)] = pen
        return pen