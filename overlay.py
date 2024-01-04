import model

import math

from PyQt6.QtWidgets import(
    QWidget
)

from PyQt6.QtGui import(
    QPaintEvent,
    QPainter,
    QPen,
    QColor,
    QResizeEvent,
    qRgba
)

from PyQt6.QtCore import (
    Qt,
    QLineF
)

class Overlay(QWidget):
    def __init__(self, model: model.Model):
        super().__init__()
        self.model = model
        self.model.setOverlay(self)


    def paintEvent(self, event: QPaintEvent):
        qp = QPainter(self)

        self.drawGrid(qp)


    def drawGrid(self, qp: QPainter):
        pen = self.model.line
        qp.setPen(pen)

        mapWidth = self.model.size.width() * self.model.dpi * self.model.scale
        mapHeight = self.model.size.height() * self.model.dpi * self.model.scale

        for x in range(1, self.model.size.width()):
            #print(f"{self.width()=}\t{qp.device().width()=}\t{mapWidth=}")
            pX = x*self.model.dpi*self.model.scale
            qp.drawLine(QLineF(
                pX, 0,
                pX, mapHeight
            ))

        for y in range(1, self.model.size.height()):
            pY = y*self.model.dpi*self.model.scale
            qp.drawLine(QLineF(
                0, pY,
                mapWidth, pY
            ))