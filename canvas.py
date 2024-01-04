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
    QPixmap,
    QWheelEvent
)
from PyQt6.QtCore import (
    Qt,
    QSize,
    QRect,
    QPoint,
    QMargins
)

class Canvas(QWidget):
    def __init__(self, model: model.Model, view: view.View):
        super().__init__()
        self.model = model
        self.view = view
        self.map = map.Map(self.model)
        self.overlay = overlay.Overlay(self.model)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(self.model.margin)

        self.imageWr = QLabel("")
        self.imageWr.setPixmap(QPixmap.fromImage(self.map.show()))
        self.layout.addWidget(self.imageWr)

        self.imageWr.layout = QVBoxLayout(self.imageWr)
        self.imageWr.layout.setContentsMargins(QMargins())
        self.imageWr.layout.addWidget(self.overlay)

        screenSize = QApplication.primaryScreen().size()

        self.setGeometry(QRect(QPoint(0, 0), self.map.size))
        self.setWindowTitle("Drawer")

    def wheelEvent(self, event: QWheelEvent):
        self.model.changeScale(event.angleDelta().y()/120 * 0.1)
        self.updateGeo()

    def updateGeo(self):
        geo = QRect(QPoint(0,0), self.map.size*self.model.scale)
        canvasGeo = QRect(QPoint(0,0), (self.map.size*self.model.scale) + QSize(self.model.netMargin))
        self.overlay.setGeometry(geo)
        self.imageWr.setPixmap(QPixmap.fromImage(self.map.show()))
        self.imageWr.setGeometry(geo)
        self.setGeometry(canvasGeo)