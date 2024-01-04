from __future__ import annotations
import math

from PyQt6.QtCore import (
    Qt,
    QSize
)

from PyQt6.QtGui import (
    QColor,
    QPen
)

class Model:
    def __init__(self, size: QSize, dpi: int, background: QColor, line: QPen = QPen(QColor('white'), 1)):
        self.background = background
        self.line = line
        self.size = size
        self.dpi = dpi
        self.scale = 1
    
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