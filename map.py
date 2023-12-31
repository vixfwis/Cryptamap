from model import Model

from PyQt6.QtGui import (
    QImage,
    QColor,
    qRgb
)

class Map(QImage):
    def __init__(self, model: Model, *args):
        super().__init__(*args)
        self.model = model

        self.dpi = self.model.dpi
        self.pixSize = self.model.size * self.dpi

        self.fill(qRgb(255,0,0))