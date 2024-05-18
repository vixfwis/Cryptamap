import model
from model import Layer

import math
from enum import Enum

from PyQt6.QtWidgets import(
    QWidget
)

from PyQt6.QtGui import(
    QMouseEvent,
    QPaintEvent,
    QPainter,
    QPen,
    QBrush,
    QColor,
    QResizeEvent,
    qRgba
)

from PyQt6.QtCore import (
    Qt,
    QLineF,
    QPoint,
    QPointF
)

drawCursor = {
    model.Mode.MESHEDIT: True
}

class Overlay(QWidget):
    def __init__(self, model: model.Model):
        super().__init__()
        self.model = model
        self.model.setOverlay(self)
        self.mousePos = QPointF(0,0)
        self.setMouseTracking(True)

    def paintEvent(self, event: QPaintEvent):
        qp = QPainter(self)

        self.drawGrid(qp)
        self.drawPoints(qp)
        if drawCursor.get(self.model.mode, False):
            self.drawCursor(qp)

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
        curr = self.model.layers[self.model.activeLayer]

        pen = QPen(self.model.line)
        pen.setWidth(pen.width()+4)
        qp.setPen(pen)

        # draw corners 
        for y in range(curr.columns):
            for x in range(curr.rows):
                value = curr.getPoint(x,y).val
                r = round(255*min(value, 1))
                b = 255-r
                p = QPen(QColor(r, 0, b, 255))
                p.setWidth(5)
                qp.setPen(p)
                qp.drawPoint(QPoint(x,y)*self.model.dpi*self.model.scale)

    def drawCursor(self, qp: QPainter):
        pen = self.model.cursor
        qp.setPen(pen)

        qp.drawEllipse(self.mousePos, 20, 20)

    #Events
    def mouseMoveEvent(self, event: QMouseEvent):
        self.mousePos = event.position()

        if event.buttons() == Qt.MouseButton.LeftButton:
            match self.model.mode:
                case model.Mode.VIEW:
                    self.model.viewTranslate(self.model.mousePos - event.globalPosition())
                case model.Mode.MESHEDIT:
                    self.model.pointIncAt(self.mousePos)
        
        self.model.mousePos = event.globalPosition()

        self.repaint()
        return super().mouseMoveEvent(event)
    
    