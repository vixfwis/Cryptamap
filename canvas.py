from __future__ import annotations
import math

import model
import view
import map
import overlay


from PyQt6.QtWidgets import(
    QWidget,
    QApplication,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QLayout
)
from PyQt6.QtGui import(
    QColor,
    QFont,
    QPalette,
    QImage,
    QPixmap,
    QWheelEvent
)
from PyQt6.QtCore import (
    Qt,
    QSize,
    QRect,
    QPoint,
    QPointF,
    QMargins
)

class Canvas(QWidget):
    def __init__(self, model: model.Model, view: view.View):
        super().__init__()
        self.model = model
        self.view = view
        self.map = map.Map(self.model)
        self.overlay = overlay.Overlay(self.model)

        self.initUI()

    def initUI(self):
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(self.model.margin)

        self.imageWr = QLabel("")
        self.imageWr.setPixmap(QPixmap.fromImage(self.map.show()))
        self._layout.addWidget(self.imageWr)
        self.imageWr._layout = QVBoxLayout(self.imageWr)
        self.imageWr._layout.setContentsMargins(QMargins())
        self.imageWr._layout.addWidget(self.overlay)

        screenSize = QApplication.primaryScreen().size()

        self.setGeometry(QRect(QPoint(0, 0), self.map.size))
        self.setWindowTitle("Drawer")

    def wheelEvent(self, event: QWheelEvent):
        self.model.changeScale(event.angleDelta().y()/120 * 0.1)

        hsbi = self.view._scroll.horizontalScrollBar().value() # horizontal scroll bar initial
        vsbi = self.view._scroll.verticalScrollBar().value() # vertical scroll bar inital

        mPos = event.position() + QPointF(hsbi, vsbi) # mouse position on global space

        si = self.size() # inital size
        self.updateGeo()
        sf = self.size() # final size

        kx = si.width()/sf.width() 
        ky = si.height()/sf.height()

        hsbf = round(mPos.x()-kx*(mPos.x()-hsbi))
        vsbf = round(mPos.y()-ky*(mPos.y()-vsbi))

        self.view._scroll.horizontalScrollBar().setValue(hsbf)
        self.view._scroll.verticalScrollBar().setValue(vsbf)   

        self.model.overlay.repaint()

    def updateGeo(self):

        geo = QRect(QPoint(0,0), self.map.size*self.model.scale)
        canvasGeo = QRect(QPoint(0,0), (self.map.size*self.model.scale) + QSize(self.model.netMargin))
        self.overlay.setGeometry(geo)
        self.imageWr.setPixmap(QPixmap.fromImage(self.map.show()))
        self.imageWr.setGeometry(geo)
        self.setGeometry(canvasGeo)