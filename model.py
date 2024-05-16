from __future__ import annotations
from functools import partial
import math
from enum import Enum

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
    pyqtSlot,
    QPointF
)

from PyQt6.QtGui import (
    QColor,
    QPen
)

class Mode(Enum):
    VIEW = 0
    MESHEDIT = 1

class Model(QObject):
    def __init__(self, 
                 size: QSize, 
                 dpi: int, 
                 background: QColor, 
                 line: QPen = QPen(QColor('white'), 1),
                 pointOff: QPen = QPen(QColor('blue'), 8), 
                 pointOn: QPen = QPen(QColor('red'), 8), 
                 cursor: QPen = QPen(QColor('gray'), 2, Qt.PenStyle.DashLine),
                 cursorSize: int = 20,
                 strength: float = 0.1,
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
        self.cursor = cursor
        self.cursorSize = cursorSize
        self.strength = strength

        self.mousePos = QPointF(0,0)

        self.netMargin = QSize(self.margin.top()+self.margin.bottom(), self.margin.left()+self.margin.right())

        self.layers = []
        self.activeLayer = None

        self.mode = Mode.VIEW
    
    def setMap(self, map):
        self.map = map

    def setOverlay(self, overlay):
        self.overlay = overlay
    
    def setView(self, view):
        self.view = view

    def placeholderFunction(self):
        print(f"PLACEHOLDER")

    def changeScale(self, scaleFac):
        if self.scale >= 0.15 or scaleFac > 0:
            self.scale += scaleFac

    def addLayer(self, location: int | None = None, res: int = 1):
        print(len(self.layers))
        loc = location if location else len(self.layers)

        layer = Layer(model = self, location = loc)

        listWidget = QListWidgetItem()
        
        listItem = QWidget()
        listLayout = QHBoxLayout()
        
        listText = QLabel(layer.name)
        listLayout.addWidget(listText, alignment=Qt.AlignmentFlag.AlignLeft)

        listButton = QPushButton("TEST TEST TEST")
        listButton.clicked.connect(partial(self.placeholderFunction))
        listLayout.addWidget(listButton, alignment=Qt.AlignmentFlag.AlignRight)

        listLayout.addStretch()
        listLayout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetFixedSize)
        listItem.setLayout(listLayout)
        listWidget.setSizeHint(listItem.sizeHint())

        self.view.list.addItem(listWidget)
        self.view.list.setItemWidget(listWidget, listItem)

        self.layers.insert(loc, layer)
        self.setActiveLayer(loc)
        
    def setActiveLayer(self, idx: int):
        print(f"{idx=}")
        if idx < 0:
            self.activeLayer = None
            return
        self.activeLayer = idx
        
        self.overlay.repaint()

    def deleteLayer(self, location: int | None = None):
        if location == None or location == False:
            location = self.activeLayer
            
        self.layers.pop(location)
        self.setActiveLayer(location-1)
        self.view.list.takeItem(location)

    def pointIncAt(self, location: QPointF):
        for point in self.layers[self.activeLayer].pointList:
            if (location.x() - point.x*self.dpi)**2 + (location.y() - point.y*self.dpi)**2 <= self.cursorSize**2:
                if point.found == False:
                    point.val += self.strength
                    point.found = True
                    #print("Found")
            else:
                point.found = False

    def viewTranslate(self, scroll: QPointF):
        hsbi = self.view._scroll.horizontalScrollBar().value() # horizontal scroll bar initial
        vsbi = self.view._scroll.verticalScrollBar().value() # vertical scroll bar inital

        hsbf = math.floor(hsbi + scroll.x())
        vsbf = math.floor(vsbi + scroll.y())

        self.view._scroll.horizontalScrollBar().setValue(hsbf)
        self.view._scroll.verticalScrollBar().setValue(vsbf)   

    def setMode(self, mode: Mode):
        self.mode = mode

    def setMode_MeshEdit(self):
        self.setMode(Mode.MESHEDIT)
    
    def setMode_View(self):
        self.setMode(Mode.VIEW)

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
        

class Point:
    def __init__(self, x: int, y: int, val: float = 0):
        self.x = x
        self.y = y
        self.val = val
        self.found = False

    def __repr__(self):
        return f"x: {self.x}\ty: {self.y}\tval: {self.val}"