from PyQt5.QtWidgets import QGraphicsTextItem, QMenu
from PyQt5.QtCore import Qt, QPoint, QRectF
import gfx.node as node

class Label(QGraphicsTextItem):
    def __init__(self, text: str = None, pickled=False):
        super().__init__()
        if text is not None:
            self.setPlainText(text)
        
        #self.setFlags(self.ItemIsFocusable)
        
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
            l = self.copy()
            memo[id(self)] = l
            return l
        return memo[id(self)]
    
    def copy(self):
        l = Label(text=self.text)
        return l
    
    @property
    def text(self):
        return self.toPlainText()
    
    @text.setter
    def text(self, text: str):
        self.setPlainText(text)
        
    def __repr__(self):
        return f'{self.text}:Label(@{id(self)})'
    
    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.addAction("Edit text").triggered.connect(lambda b: self.start_editing_text(event.pos()))
        menu.exec_(event.screenPos())
        
    def start_editing_text(self, mouse_pos: QPoint):
        if self.textInteractionFlags() != Qt.TextEditorInteraction:
            self.setTextInteractionFlags(Qt.TextEditorInteraction)
            self.setFocus()
            # the following lines are used to correctly place the text 
            # cursor at the mouse cursor position
            cursorPos = self.document().documentLayout().hitTest(
                        mouse_pos, Qt.FuzzyHit)
            textCursor = self.textCursor()
            textCursor.setPosition(cursorPos)
            self.setTextCursor(textCursor)
            
    def focusOutEvent(self, event):
        # this is required in order to allow movement using the mouse
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        
    def update(self, rect: QRectF = None, memo: set = None, force: bool = False, arrows: bool = True):
        if memo is None:
            memo = set()
            
        if force or id(self) not in memo:
            memo.add(id(self))
            parent = self.parentItem()
            
            if rect is None:
                super().update()
            else:
                super().update(rect)
            
            if isinstance(parent, node.Node):
                parent.update(None, memo, force, arrows)
                