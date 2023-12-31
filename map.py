from __future__ import annotations
import math

import model

from PyQt6.QtGui import (
    QImage,
    QColor,
    qRgb
)

from PyQt6.QtCore import (
    QPoint
)

class Map(QImage):
    def __init__(self, model: model.Model, *args):
        super().__init__(*args)
        self.model = model

        self.dpi = self.model.dpi
        self.pixSize = self.model.size * self.dpi

        self.initMap()

    def initMap(self):
        self.fill(self.model.background)

        self.drawGridLines()

    def drawGridLines(self):
        for y in range(self.size().height()):
            for x in range(self.size().width()):
                point = QPoint(math.floor(x*self.model.scale), math.floor(y*self.model.scale))

                if point.x() % self.model.dpi == 0 or point.y() % self.model.dpi == 0:
                    col = self.model.line
                else:
                    col = self.model.background
                self.setPixelColor(QPoint(x, y), col)


def intFromCol(col: QColor) -> int:
    return qRgb(col.red(), col.green(), col.blue())