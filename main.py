import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget
)
from PyQt6.QtGui import (
    QPainter,
    QColor,
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
    model = Model(QSize(30,20), 72)
    view = View(model)
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()