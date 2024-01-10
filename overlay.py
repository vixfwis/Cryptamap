import model

import math
from enum import Enum

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
    QLineF,
    QPoint
)

class Overlay(QWidget):
    def __init__(self, model: model.Model):
        super().__init__()
        self.model = model
        self.model.setOverlay(self)

    def paintEvent(self, event: QPaintEvent):
        qp = QPainter(self)

        self.drawGrid(qp)
        self.drawPoints(qp)


    def drawGrid(self, qp: QPainter):
        pen = self.model.line
        qp.setPen(pen)

        mapWidth = self.model.pixSize.width() * self.model.scale
        mapHeight = self.model.pixSize.height() * self.model.scale

        for x in range(1, self.model.size.width()):
            pX = x*mapWidth/(self.model.size.width())
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

    def drawPoints(self, qp: QPainter):
        pen = QPen(self.model.line)
        pen.setWidth(pen.width()+4)
        qp.setPen(pen)

        # draw corners 
        for y in range(self.model.size.height() + 1):
            for x in range(self.model.size.width() + 1):
                qp.drawPoint(QPoint(x,y)*self.model.dpi*self.model.scale)