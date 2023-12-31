import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget
)
from PyQt6.QtGui import (
    QPainter,
    QColor,
    QRgba64,
    QFont
)

from PyQt6.QtCore import(
    Qt,
    QSize
)

from view import View
from model import Model

def main():
    app = QApplication([])
    model = Model(
        size = QSize(30,20),
        dpi = 72,
        background = QColor('black')
    )
    view = View(model)
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()