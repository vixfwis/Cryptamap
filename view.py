import yaml

from canvas import Canvas
from model import Model

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QToolBar,
    QScrollArea,
    QVBoxLayout
)
from PyQt6.QtGui import (
    QPainter,
    QColor,
    QFont,
    QAction,
    QIcon,
    QResizeEvent,
    QWheelEvent
)
from PyQt6.QtCore import (
    Qt,
    QSize,
    QRect,
    QPoint
)

class View(QMainWindow):
    def __init__(self, model: Model):
        super().__init__(parent=None)
        self.model = model
        self.model.setView(self)

        self.layout = QVBoxLayout(self)
        # self.setLayout(self.layout)

        self._scroll = ScrollAreaZoom(self.model, self)
        self.widget = Canvas(model, self)
        self._scroll.setWidget(self.widget)

        self.setWindowTitle("Cryptamap")
        self.setCentralWidget(self._scroll)
        self.createToolBar(Qt.ToolBarArea.LeftToolBarArea, "Tools", self)

        self.show()
        self.widget.updateGeo()

    def createToolBar(self, location, *args):
        self.toolBar = QToolBar(*args)
        self.addToolBar(location, self.toolBar)

        buttons = self.createButtonsFromYAML(".\\icons\\icons.yaml")
        
        for button in buttons.values():
            self.toolBar.addAction(button)

    def createButtonsFromYAML(self, path: str):
        buttons = {}
        with open(path, "r") as stream:
            try:
                buttonDef = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
            
            for button, props in buttonDef.items():
                action = QAction(
                    QIcon(props["iconPath"]),
                    button,
                    self
                )
                action.triggered.connect(getattr(Model, props["func"]))
                action.setStatusTip(props["desc"])
                if "shortcut" in props:
                    action.setShortcut(props["shortcut"])

                buttons.update({button: action})

        return buttons
    
    
class ScrollAreaZoom(QScrollArea):
    def __init__(self, model: Model, view: View, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view = view
        self.model = model

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def wheelEvent(self, event):
        QApplication.sendEvent(self.widget(), event)