from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from mathlib.object import Object
from gfx.view import View
from gfx.scene import Scene
from mathlib.builtins import initialize_builtins

def my_exception_hook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)  # Print the usual traceback

sys.excepthook = my_exception_hook

if __name__ == '__main__':
    try:            
        app = QApplication([])
        
        initialize_builtins()
        
        window = QMainWindow()
        view = View()
        window.setCentralWidget(view)
        scene = Scene()
        view.setScene(scene)    
        window.showMaximized()    
        sys.exit(app.exec_())
    except Exception as e:
        print(e)