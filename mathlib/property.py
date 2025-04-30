from gfx.label import Label
from stringcase import sentencecase
from copy import deepcopy

class Property(Label):
    def __init__(self, subject: tuple, text: callable = None, pickled=False):
        super().__init__()
        
        if text is None:
            text = lambda subj: sentencecase(self.__class__.__name__)
            
        super().setPlainText(text(subject))
        self._textFn = text
        self._subject = subject
        
        #self.setFlags(self.ItemIsFocusable)
        
        if not pickled:
            self.finish_setup()
    
    def __setstate__(self, data):
        self.__init__(pickled=True)
        super()._setstate(data)
        self._textFn = data['text fn']
        self._subject = data['subject']
        self.finish_setup()
    
    def __getstate__(self):
        data = super().__getstate__()
        data['subject'] = self._subject
        data['text fn'] = self._textFn
        return data
    
    def finish_setup(self):
        super().finish_setup()
    
    def __deepcopy__(self, memo):
        if id(self) not in memo:
            p = self.copy()
            memo[id(self)] = p
            subject = [None] * len(self._subject)
            for i,s in enumerate(self._subject):
                subject[i] = deepcopy(s, memo)
            p._subject = subject
            return p
        return memo[id(self)]
    
    def copy(self):
        p = Property(subject=None, text=self.text_function())
        return p
    
    def text_function(self):
        return self._textFn
        
    def text(self):
        return self.text_function()(self._subject)
    
    def subject(self) -> tuple:
        return self._subject