from model import Model

from PyQt6.QtWidgets import(
    QWidget,
    QApplication,
    QScrollArea
)
from PyQt6.QtGui import(
    QPainter,
    QColor,
    QFont,
    QPalette
)
from PyQt6.QtCore import (
    Qt,
    QSize,
    QRect,
    QPoint
)

class Canvas(QWidget):
    def __init__(self, model: Model):
        super().__init__()
        self.model = model

        self.size = self.model.size
        self.dpi = self.model.dpi

        self.initUI()

    def initUI(self):
        self.text = "YOYOYOY"
        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), QColor('red'))
        self.setPalette(p)

        screenSize = QApplication.primaryScreen().size()
        self.pixSize = QSize(self.size.width()*self.dpi, self.size.height()*self.dpi)

        self.setGeometry(QRect(QPoint(200, 200), self.pixSize))
        self.setWindowTitle("Drawer")
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QColor(0,0,0))
        qp.setFont(QFont("Decorative", 10, 10))
        qp.drawText(event.rect(), Qt.AlignmentFlag.AlignCenter, self.text)

    def wheelEvent(self, event):
        self.model.changeScale(event.angleDelta().y()/120 * 0.1)
        self.setGeometry(QRect(QPoint(200, 200), self.pixSize*self.model.scale))
        print(self.model.scale)