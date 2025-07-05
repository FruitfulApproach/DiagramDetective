from PyQt6.QtWidgets import QMainWindow
from ui.main_window import Ui_MainWindow
from widget.tab_widget import TabWidget
from dialog.definition_dialog import DefinitionDialog

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().__init__()
        self.setupUi(self)

        self._tabs = TabWidget(self)
        self.setCentralWidget(self._tabs)
        
        self.definition_dialog = DefinitionDialog(parent=self)
        
        self.actionDefine.triggered.connect(lambda b: self.create_definition())
        
    def create_definition(self):
        result = self.definition_dialog.exec()
        
        if result == self.definition_dialog.DialogCode.Accepted:
            definition = self.definition_dialog.gather_definition()
            print(definition)
        
        
    @property
    def tabs(self):
        return self._tabs