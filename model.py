from __future__ import annotations
import math

from PyQt6.QtCore import (
    Qt,
    QSize,
    QMargins
)

from PyQt6.QtGui import (
    QColor,
    QPen
)

class Model:
    def __init__(self, size: QSize, dpi: int, background: QColor, line: QPen = QPen(QColor('white'), 1), margin: QMargins = QMargins(4,4,4,4)):
        self.background = background
        self.margin = margin
        self.line = line
        self.size = size
        self.dpi = dpi
        self.scale = 1

        self.netMargin = QSize(self.margin.top()+self.margin.bottom(), self.margin.left()+self.margin.right())
    
    def setMap(self, map):
        self.map = map

    def setOverlay(self, overlay):
        self.overlay = overlay

    def placeholderFunction():
        print("PLACEHOLDER")

    def changeScale(self, scaleFac):
        print(scaleFac)
        if self.scale >= 0.15 or scaleFac > 0:
            self.scale += scaleFac