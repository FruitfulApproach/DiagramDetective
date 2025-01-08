from PyQt5.QtWidgets import QGraphicsTextItem
from copy import copy

class Label(QGraphicsTextItem):
    def __init__(self, text: str = None, pickled=False):
        super().__init__()
        if text is not None:
            self.setPlainText(text)
        if not pickled:
            self.finish_setup()
    
    def __setstate__(self, data):
        self.__init__(pickled=True)
        self.setPlainText(data['text'])
        self.finish_setup()
    
    def __getstate__(self):
        return {
            'text' : self.text,
        }
    
    def finish_setup(self):
        pass
    
    def __deepcopy__(self, memo):
        if id(self) not in memo:
            l = copy(self)
            memo[id(self)] = l
            return l
        return memo[id(self)]
    
    def __copy__(self):
        l = Label(text=self.text)
        return l
    
    @property
    def text(self):
        return self.toPlainText()
    
    @text.setter
    def text(self, text: str):
        self.setPlainText(text)
        
    def __repr__(self):
        return f'{self.text}:Label(@{id(self)}'