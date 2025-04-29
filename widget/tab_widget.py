from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtCore import Qt, QPoint, QMimeData
from PyQt6.QtGui import QPixmap, QRegion, QDrag, QCursor

class TabWidget(QTabWidget):
    def __init__(self, parent=None, new=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.tabBar().setMouseTracking(True)
        self.setMovable(True)
        if new:
            TabWidget.setup(self)

    def __setstate__(self, data):
        self.__init__(new=False)
        #self.setParent(data['parent'])
        for widget, tabname in data['tabs']:
            self.addTab(widget, tabname)
        TabWidget.setup(self)

    def __getstate__(self):
        data = {
          'parent' : self.parent(),
         'tabs' : [],
      }
        tab_list = data['tabs']
        for k in range(self.count()):
            tab_name = self.tabText(k)
            widget = self.widget(k)
            tab_list.append((widget, tab_name))
        return data

    def setup(self):
        pass

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.RightButton:
            return

        globalPos = self.mapToGlobal(e.pos())
        tabBar = self.tabBar()
        posInTab = tabBar.mapFromGlobal(globalPos)
        index = tabBar.tabAt(posInTab)
        tabBar.dragged_content = self.widget(index)
        tabBar.dragged_tabname = self.tabText(index)
        tabRect = tabBar.tabRect(index)

        pixmap = QPixmap(tabRect.size())
        tabBar.render(pixmap,QPoint(),QRegion(tabRect))
        mimeData = QMimeData()

        drag = QDrag(tabBar)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)

        cursor = QCursor(Qt.OpenHandCursor)

        drag.setHotSpot(posInTab)
        drag.setDragCursor(cursor.pixmap(),Qt.MoveAction)
        drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, e):
        e.accept()
        #self.parent().dragged_index = self.indexOf(self.widget(self.dragged_index))

    def dragLeaveEvent(self,e):
        e.accept()

    def dropEvent(self, e):
        if e.source().parentWidget() == self:
            return

        e.setDropAction(Qt.MoveAction)
        e.accept()
        tabBar = e.source()
        if tabBar and hasattr(tabBar, 'dragged_content'):
            self.addTab(tabBar.dragged_content, tabBar.dragged_tabname)


if __name__ == '__main__':
    from PyQt6.QtWidgets import QWidget, QApplication, QHBoxLayout
    import sys

    class Window(QWidget):
        def __init__(self):

            super().__init__()

            self.dragged_index = None
            tabWidgetOne = TabWidget(self)
            tabWidgetTwo = TabWidget(self)
            tabWidgetOne.addTab(QWidget(), "tab1")
            tabWidgetTwo.addTab(QWidget(), "tab2")

            layout = QHBoxLayout()

            self.moveWidget = None

            layout.addWidget(tabWidgetOne)
            layout.addWidget(tabWidgetTwo)

            self.setLayout(layout)

    app = QApplication(sys.argv)
    window = Window()
    window1 = Window()
    window.show()
    window1.show()
    sys.exit(app.exec_())