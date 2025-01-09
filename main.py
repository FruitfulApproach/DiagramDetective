from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from mathlib.object import Object
from gfx.view import View
from gfx.scene import Scene
from mathlib.builtins import initialize_builtins

if __name__ == '__main__':
    app = QApplication([])
    
    initialize_builtins()
    
    window = QMainWindow()
    view = View()
    window.setCentralWidget(view)
    scene = Scene()
    view.setScene(scene)
    window.show()
    sys.exit(app.exec_())