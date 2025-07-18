from PyQt6.QtWidgets import QApplication
import sys
from mathlib.object import Object
from gfx.view import View
from gfx.scene import Scene
from mathlib.builtins import initialize_builtins
from dialog.main_window import MainWindow
from core.utility import set_appid_on_windows_os

#def my_exception_hook(exctype, value, traceback):
    #sys.__excepthook__(exctype, value, traceback)  # Print the usual traceback

#sys.excepthook = my_exception_hook

if __name__ == '__main__':
    app = QApplication([])
    set_appid_on_windows_os(u'DiagramDetecive')    
    initialize_builtins()        
    window = MainWindow()
    view = View()
    window.tabs.addTab(view, "Test")
    scene = Scene()
    view.setScene(scene)    
    window.showMaximized()
        
    sys.exit(app.exec())
