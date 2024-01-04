from __future__ import annotations

import model
import view
import map
import overlay


from PyQt6.QtWidgets import(
    QWidget,
    QApplication,
    QLabel,
    QScrollArea,
    QVBoxLayout
)
from PyQt6.QtGui import(
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
        self.overlay = overlay.Overlay(self.model)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.imageWr = QLabel("")
        self.imageWr.setPixmap(QPixmap.fromImage(self.map.show()))
        self.layout.addWidget(self.imageWr)

        self.overlay.setParent(self.imageWr)

        screenSize = QApplication.primaryScreen().size()

        self.setGeometry(QRect(QPoint(0, 0), self.map.size))
        self.setWindowTitle("Drawer")

        self.show()

    def wheelEvent(self, event):
        self.model.changeScale(event.angleDelta().y()/120 * 0.1)

        geo = QRect(QPoint(0,0), self.map.size*self.model.scale)
        self.overlay.setGeometry(geo)
        self.imageWr.setPixmap(QPixmap.fromImage(self.map.show()))
        self.imageWr.setGeometry(geo)
        self.setGeometry(geo)
        print(self.model.scale)