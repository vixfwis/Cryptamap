import model

from PyQt6.QtWidgets import(
    QWidget
)

from PyQt6.QtGui import(
    QPaintEvent,
    QPainter,
    QPen,
    QColor,
    qRgba
)

from PyQt6.QtCore import (
    Qt
)

class Overlay(QWidget):
    def __init__(self, model: model.Model):
        super().__init__()
        self.model = model


    def paintEvent(self, event: QPaintEvent):
        qp = QPainter(self)
        qp.begin(self)

        self.drawGrid(qp)

        qp.end()

    def drawGrid(self, qp: QPainter):
        pen = self.model.line
        qp.setPen(pen)

        qp.drawLine(10,10, 100,100)