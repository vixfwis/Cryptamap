from __future__ import annotations

import map

from PyQt6.QtCore import (
    Qt,
    QSize
)

from PyQt6.QtGui import (
    QColor
)

class Model:
    def __init__(self, size: QSize, dpi: int, background: QColor, line: QColor = QColor('white')):
        self.background = background
        self.line = line
        self.size = size
        self.dpi = dpi
        self.scale = 1
    
    def setMap(self, map: map.Map):
        self.map = map

    def placeholderFunction():
        print("PLACEHOLDER")

    def changeScale(self, scaleFac):
        print(scaleFac)
        if self.scale >= 0.15 or scaleFac > 0:
            self.scale += scaleFac