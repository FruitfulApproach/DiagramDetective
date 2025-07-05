from PyQt6.QtCore import QObject, pyqtSignal
from core.math_object import MathObject

class Definition(MathObject):
    def __init__(self):
        self._context = None
        self._vocab:str = None
        self._var:str = None
        self._structure:tuple = None
        self._property:list = [
            
        ]
        
        