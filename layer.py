""" from __future__ import annotations
from functools import partial
import math

from PyQt6.QtWidgets import (
    QWidget,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QSizePolicy
)

from PyQt6.QtCore import (
    Qt,
    QSize,
    QMargins,
    QPoint,
    QObject,
    pyqtSlot
)

from PyQt6.QtGui import (
    QColor,
    QPen
)

from model import Model

class Layer:
    def __init__(self, model: Model, res: int = 1, name: str = None, location: int = None):
        self.model = model
        self.res = res
        self.name = name if name else f"Layer {len(self.model.layers)}"
        self.location = location
        
        self.rows = self.model.size.width()*self.res + 1
        self.columns = self.model.size.height()*self.res+1
        
        self.pointList = [None] * self.columns * self.rows
        for i in range(len(self.pointList)):
            x,y = self.xyAt(i)
            self.pointList[i] = Point(x, y)

        self.createLayer()

    def getPoint(self, idx: int) -> Point:
        return self.pointList[idx]
    
    def getPoint(self, x: int, y: int) -> Point:
        if x > self.rows or y > self.columns: 
            raise IndexError
        return self.pointList[self.idxAt(x,y)]
    
    def xyAt(self, idx) -> tuple:
        return (idx%self.rows, idx//self.rows)
    
    def idxAt(self, x, y) -> int:
        return y*self.rows + x
    
    def createListWidgetItem() -> QListWidgetItem:
        return
    
    def createLayer(self):
        listWidget = QListWidgetItem()
        
        listItem = QWidget()
        listLayout = QHBoxLayout()
        
        listText = QLabel(self.name)
        listLayout.addWidget(listText, alignment=Qt.AlignmentFlag.AlignLeft)

        mesher = QPushButton("Mesh")
        mesher.clicked.connect(partial(self.placeholderFunction))
        listLayout.addWidget(mesher, alignment=Qt.AlignmentFlag.AlignRight)

        listLayout.addStretch()
        listLayout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetFixedSize)
        listItem.setLayout(listLayout)
        listWidget.setSizeHint(listItem.sizeHint())

        self.model.view.list.addItem(listWidget)
        self.model.view.list.setItemWidget(listWidget, listItem)
        

class Point:
    def __init__(self, x: int, y: int, val: float = 0):
        self.x = x
        self.y = y
        self.val = val """