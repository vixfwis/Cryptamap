from __future__ import annotations
import math
from enum import Enum

import model

from PyQt6.QtGui import (
    QImage,
    QColor
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
        self.size = self.model.size * self.model.dpi
        self.map = bytearray(self.size.width() * self.size.height() * 4)
        self.model.setMap(self)

        self.initMap()

    def show(self):
        return QImage(
            self.map,
            self.size.width(),
            self.size.height(),
            QImage.Format.Format_ARGB32
        ).scaledToWidth(math.floor(self.size.width()*self.model.scale))
    
    def pixSet(self, idx: int, color: QColor):
        self.map[idx+0] = color.blue()
        self.map[idx+1] = color.green()
        self.map[idx+2] = color.red()
        self.map[idx+3] = color.alpha()

    def initMap(self):
        self.fill(self.model.background)

    def fill(self, color: QColor):
        for idx in range(0, len(self.map), 4):
            self.pixSet(idx, color)