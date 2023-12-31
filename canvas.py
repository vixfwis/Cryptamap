from __future__ import annotations

import model
import view
import map


from PyQt6.QtWidgets import(
    QWidget,
    QApplication,
    QLabel,
    QScrollArea,
    QVBoxLayout
)
from PyQt6.QtGui import(
    QPainter,
    QColor,
    QFont,
    QPalette,
    QImage,
    QPixmap
    
)
from PyQt6.QtCore import (
    Qt,
    QSize,
    QRect,
    QPoint
)

class Canvas(QWidget):
    def __init__(self, model: model.Model, view: view.View):
        super().__init__()
        self.model = model
        self.view = view
        self.map = map.Map(self.model, self.model.size*self.model.dpi, QImage.Format.Format_ARGB32)

        self.initUI()

    def initUI(self):
        self.text = "YOYOYOY"
        self.layout = QVBoxLayout(self)

        self.imageWr = QLabel("")
        self.imageWr.setPixmap(QPixmap.fromImage(self.map))
        self.layout.addWidget(self.imageWr)

        screenSize = QApplication.primaryScreen().size()

        self.setGeometry(QRect(QPoint(200, 200), self.map.pixSize))
        self.setWindowTitle("Drawer")

        self.show()

    def wheelEvent(self, event):
        self.model.changeScale(event.angleDelta().y()/120 * 0.1)
        self.imageWr.setGeometry(QRect(QPoint(0,0), self.map.pixSize*self.model.scale))
        print(self.model.scale)