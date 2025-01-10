from PyQt5.QtCore import QRectF, Qt, QPointF
from PyQt5.QtGui import QColor, QBrush, QPen

class ConnectButton:
    default_radius = 11
    default_fill_brush = QBrush(Qt.green)
    default_border_pen = QPen(Qt.darkGreen, 1)
    
    def __init__(self, radius=None, pickled=False):
        if radius is None:
            radius = self.default_radius
        r = radius
        self._radius = r
        self._rect = QRectF(-r, r, 2*r, 2*r)
        self._visible = False
    
    @property
    def rect(self) -> QRectF:
        return self._rect
    
    @property
    def bounding_rect(self) -> QRectF:
        w = self._rect.width()
        w /= 2
        return self._rect.adjusted(-w, -w, w, w)
    
    @property
    def visible(self) -> bool:
        return self._visible
    
    @visible.setter
    def visible(self, visible: bool):
        self._visible = visible
        
    def paint(self, painter):
        painter.setPen(self.default_border_pen)
        painter.setBrush(self.default_fill_brush)
        painter.drawEllipse(self._rect)
        
    @property
    def pos(self) -> QPointF:
        return self._pos
    
    @pos.setter
    def pos(self, pos: QPointF):
        self._pos = pos
        self._updateRect()
        
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, radius: float):
        self._radius = radius
        self._updateRect()
            
    def _updateRect(self):
        r = self._radius
        pos = self.pos
        self._rect = QRectF(pos.x() - r, pos.y() - r, 2*r, 2*r)        
