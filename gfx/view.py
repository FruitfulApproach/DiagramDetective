from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt

class View(QGraphicsView):
    def __init__(self, pickled=False):
        super().__init__()
        self._scale = (1.0, 1.0)                    
        #self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)        
        if not pickled:
            self._wheelZoom = True
            self._zoomFactor = (1.1, 1.1)
            self._zoomLimit = 25
            self.finish_setup()
            
    def finish_setup(self):
        pass
    
    def scale(self, sx, sy):
        s = self._scale
        super().scale(sx, sy)
        self._scale = (s[0]*sx, s[1]*sy)        

    def zoom_100(self):
        import core.geom_tools
        transform = self.transform()
        sx, sy = core.geom_tools.extract_transform_scale(transform)
        self.setTransform(transform.scale(1.0/sx, 1.0/sy).scale(self._scale[0], self._scale[1]))    
        #IDK why this works...
        self.scale(1.0/self._scale[0], 1.0/self._scale[1])

    def zoom_in(self, times=None):
        if times is None:
            times = 1
        s = self._scale
        if s[0] < self._zoomLimit:
            z = self._zoomFactor
            s = (z[0]**times, z[1]**times)
        else:
            return 
        self.scale(*s)
        self.scene().update()   

    def zoom_out(self, times=None):
        if times is None:
            times = 1
        s = self._scale
        if s[0] > 1/self._zoomLimit:
            z = self._zoomFactor
            s = (1.0/z[0]**times, 1.0/z[1]**times)
        else:
            return   
        self.scale(*s)
        self.scene().update()           

    def wheelEvent(self, event):
        if self._wheelZoom:
            self.setTransformationAnchor(self.AnchorUnderMouse)
            #Scale the view / do the zoom
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else: 
                self.zoom_out()
        super().wheelEvent(event)    
    
    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_Equal:
                self.zoom_in()
                
            elif event.key() == Qt.Key_Minus:
                self.zoom_out()
        super().keyPressEvent(event)
                