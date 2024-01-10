from __future__ import annotations
import math

from PyQt6.QtWidgets import (
    QWidget
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

class Model(QObject):
    def __init__(self, 
                 size: QSize, 
                 dpi: int, 
                 background: QColor, 
                 line: QPen = QPen(QColor('white'), 1),
                 pointOff: QPen = QPen(QColor('blue'), 8), 
                 pointOn: QPen = QPen(QColor('red'), 8), 
                 margin: QMargins = QMargins(4,4,4,4)
                 ):
        self.background = background
        self.margin = margin
        self.line = line
        self.size = size
        self.dpi = dpi
        self.pixSize = self.size * self.dpi
        self.scale = 1
        self.pointOff = pointOff
        self.pointOn = pointOn

        self.netMargin = QSize(self.margin.top()+self.margin.bottom(), self.margin.left()+self.margin.right())

        self.layers = []
        self.activeLayer = None
    
    def setMap(self, map):
        self.map = map

    def setOverlay(self, overlay):
        self.overlay = overlay
    
    def setView(self, view):
        self.view = view

    def placeholderFunction(self):
        print(f"PLACEHOLDER of {self}")

    def changeScale(self, scaleFac):
        if self.scale >= 0.15 or scaleFac > 0:
            self.scale += scaleFac

    def addLayer(self, location: int | None = None, res: int = 1):
        print(f"Add layer {self}")
        layer = Layer(model = self)

        if not location:
            self.setActiveLayer(len(self.layers))
            self.layers.append(layer)
            return 

        self.layers.insert(location, layer)
        self.setActiveLayer(location)

    def setActiveLayer(self, idx: int):
        self.activeLayer = idx

class Layer:
    def __init__(self, model: Model, res: int = 1):
        self.model = model
        self.res = res
        
        self.rows = self.model.size.width()*self.res + 1
        self.columns = self.model.size.height()*self.res+1
        
        self.pointList = [None] * self.columns * self.rows
        for i in range(len(self.pointList)):
            x,y = self.xyAt(i)
            self.pointList[i] = Point(x, y)

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
        

class Point:
    def __init__(self, x: int, y: int, val: float = 0):
        self.x = x
        self.y = y
        self.val = val