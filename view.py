import yaml

from canvas import Canvas
# from map import Map
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
    QIcon
)
from PyQt6.QtCore import (
    Qt,
    QSize
)

class View(QMainWindow):
    def __init__(self, model: Model):
        super().__init__(parent=None)
        self.model = model

        self.layout = QVBoxLayout(self)
        # self.setLayout(self.layout)

        self.scroll = QScrollArea()
        self.widget = Canvas(model, self)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidget(self.widget)

        self.setWindowTitle("Cryptamap")
        self.setCentralWidget(self.scroll)
        self.createToolBar(Qt.ToolBarArea.LeftToolBarArea, "Tools", self)

        self.show()

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
    