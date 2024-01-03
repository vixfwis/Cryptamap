from __future__ import annotations
import math
from enum import Enum

import model

from PyQt6.QtGui import (
    QImage,
    QColor,
    qRgb
)

from PyQt6.QtCore import (
    QPoint,
    QByteArray
)

class COLOURS(Enum):
    alpha: 0
    red: 1
    green: 2
    blue: 3

class Map():
    def __init__(self, model: model.Model, *args):
        #super().__init__(*args)
        self.model = model
        self.dpi = self.model.dpi
        self.pixSize = self.model.size * self.dpi
        self.map = bytearray(self.pixSize.width() * self.pixSize.height() * 4)

        self.initMap()

    def show(self):
        return QImage(
            self.map,
            self.pixSize.width(),
            self.pixSize.height(),
            QImage.Format.Format_ARGB32
        ).scaledToWidth(math.floor(self.pixSize.width()*self.model.scale))

    def initMap(self):
        self.fill(self.model.background)

        #self.drawGridLines()
        self.fillWhite()

    def drawGridLines(self):
        print("Draw lines")
        bits = bytearray(self.bits().asstring(self.width() * self.height() * 4))

    def fill(self, color: QColor):
        for idx in range(0, len(self.map), 4):
            self.map[idx+0] = color.alpha()
            self.map[idx+1] = color.red()
            self.map[idx+2] = color.green()
            self.map[idx+3] = color.blue()

    def fillWhite(self):
        self.fill(QColor('white'))

def intFromCol(col: QColor) -> int:
    return qRgb(col.red(), col.green(), col.blue())