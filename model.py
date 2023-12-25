from PyQt6.QtCore import (
    Qt,
    QSize
)

class Model:
    def __init__(self, size: QSize, dpi: int):
        self.size = size
        self.dpi = dpi
        self.scale = 1

    def placeholderFunction():
        print("PLACEHOLDER")

    def changeScale(self, scaleFac):
        if self.scale >= 0.1:
            self.scale += scaleFac