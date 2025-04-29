from PyQt6.QtGui import QBrush, QPen
from PyQt6.QtCore import Qt


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
        int(Qt.PenStyle.NoPen.value) : Qt.PenStyle.NoPen, 
        int(Qt.PenStyle.SolidLine.value) : Qt.PenStyle.SolidLine,
        int(Qt.PenStyle.DashLine.value) : Qt.PenStyle.DashLine,
        int(Qt.PenStyle.DotLine.value) : Qt.PenStyle.DotLine,
        int(Qt.PenStyle.DashDotLine.value) : Qt.PenStyle.DashDotLine,
        int(Qt.PenStyle.DashDotDotLine.value) : Qt.PenStyle.DashDotDotLine,
        int(Qt.PenStyle.CustomDashLine.value) : Qt.PenStyle.CustomDashLine,
    }

    capEnum = {
        int(Qt.PenCapStyle.FlatCap.value) : Qt.PenCapStyle.FlatCap,
        int(Qt.PenCapStyle.SquareCap.value) : Qt.PenCapStyle.SquareCap,
        int(Qt.PenCapStyle.RoundCap.value) : Qt.PenCapStyle.RoundCap,
    }

    joinEnum = {
        int(Qt.PenJoinStyle.MiterJoin.value) : Qt.PenJoinStyle.MiterJoin,
        int(Qt.PenJoinStyle.BevelJoin.value) : Qt.PenJoinStyle.BevelJoin,
        int(Qt.PenJoinStyle.RoundJoin.value) : Qt.PenJoinStyle.RoundJoin,
        int(Qt.PenJoinStyle.SvgMiterJoin.value) : Qt.PenJoinStyle.SvgMiterJoin,
    }

    def __init__(self, color=None, width=None, style=Qt.PenStyle.SolidLine, cap=Qt.PenCapStyle.RoundCap, join=Qt.PenJoinStyle.RoundJoin):
        if color is None or color == Qt.PenStyle.NoPen:
            super().__init__(Qt.PenStyle.NoPen)
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