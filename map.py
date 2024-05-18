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
    def __init__(self, model: model.Model):
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

    def renderMesh(self, layer: model.Layer):
        for idx in range(0, len(self.map), 4):
            x = idx/4 % self.size.width()
            y = idx/4 // self.size.width()
            for tri in layer.mesh:
                if self.inTri(x,y, tri):
                    self.pixSet(idx, QColor('white'))

        self.show()


    def inTri(self, x,y, tri): #https://www.geeksforgeeks.org/check-whether-a-given-point-lies-inside-a-triangle-or-not/
        A = (tri[0].x * self.model.dpi , tri[0].y * self.model.dpi)
        B = (tri[1].x * self.model.dpi , tri[1].y * self.model.dpi)
        C = (tri[2].x * self.model.dpi , tri[2].y * self.model.dpi)
        P = (x,y)

        denominator = ((B[1] - C[1]) * (A[0] - C[0]) +
                    (C[0] - B[0]) * (A[1] - C[1]))
        a = ((B[1] - C[1]) * (P[0] - C[0]) +
            (C[0] - B[0]) * (P[1] - C[1])) / denominator
        b = ((C[1] - A[1]) * (P[0] - C[0]) +
            (A[0] - C[0]) * (P[1] - C[1])) / denominator
        c = 1 - a - b
    
        if a >= 0 and b >= 0 and c >= 0:
            return True
        return False