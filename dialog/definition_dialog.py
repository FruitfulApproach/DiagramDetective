from ui.definition_dialog import Ui_DefinitionDialog
from PyQt6.QtWidgets import QDialog
from core.definition import Definition

class DefinitionDialog(QDialog, Ui_DefinitionDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().__init__()
        self.setupUi(self)
        
    def gather_definition(self) -> Definition:
        return Definition()
        