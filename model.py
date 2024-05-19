from __future__ import annotations
from functools import partial
import math
from enum import IntEnum

from PyQt6.QtWidgets import (
    QWidget,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QComboBox,
    QSizePolicy
)

from PyQt6.QtCore import (
    Qt,
    QSize,
    QMargins,
    QPoint,
    QObject,
    pyqtSlot,
    QPointF,
    QStringConverter
)

from PyQt6.QtGui import (
    QColor,
    QPen
)

class Mode(IntEnum):
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
                 strength: float = 1,
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
        self.incDir = 1

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

    def setIncDir(self, sign: int):
        self.incDir = sign

    def setIncDir_Plus(self):
        self.setIncDir(1)
    
    def setIncDir_Minus(self):
        self.setIncDir(-1)

    def addLayer(self, location: int | None = None, res: int = 1):
        print(len(self.layers))
        loc = location if location else len(self.layers)

        layer = Layer(model = self, location = loc)

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
                    point.val += self.strength*self.incDir
                    point.val = min(max(point.val, 0), 1)
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

class MesherType(IntEnum):
    SIMPLE_MESH = 0
    MARCHING_SQUARES = 1

class Layer:
    def __init__(self, model: Model, res: int = 1, name: str = None, location: int = None):
        self.model = model
        self.res = res
        self.name = name if name else f"Layer {len(self.model.layers)}"
        self.location = location
        self.mesherType = MesherType.SIMPLE_MESH

        self.mesh = []
        
        self.rows = self.model.size.width()*self.res + 1
        self.columns = self.model.size.height()*self.res+1
        
        self.pointList = [None] * self.columns * self.rows
        for i in range(len(self.pointList)):
            x,y = self.xyAt(i)
            self.pointList[i] = Point(x, y)

        self.createLayerBox()

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

    def createLayerBox(self):
        listWidget = QListWidgetItem()
        
        listItem = QWidget()
        listLayout = QHBoxLayout()
        
        listText = QLabel(self.name)
        listLayout.addWidget(listText, alignment=Qt.AlignmentFlag.AlignLeft)

        mesher = QPushButton("Mesh")
        mesher.clicked.connect(self.createMesh)
        listLayout.addWidget(mesher, alignment=Qt.AlignmentFlag.AlignRight)

        meshType = QComboBox()
        meshType.addItems([
            "Simple Mesh",
            "Marching Squares"
        ])
        meshType.currentIndexChanged.connect(self.changeMesher)
        listLayout.addWidget(meshType)

        listLayout.addStretch()
        listLayout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetFixedSize)
        listItem.setLayout(listLayout)
        listWidget.setSizeHint(listItem.sizeHint())

        self.model.view.list.addItem(listWidget)
        self.model.view.list.setItemWidget(listWidget, listItem)

    def changeMesher(self, idx):
        self.mesherType = idx

    def createMesh(self):
        if self.mesherType == MesherType.SIMPLE_MESH:
            self.createSimpleMesh()
        elif self.mesherType == MesherType.MARCHING_SQUARES: 
            self.createMSMesh()

        else:
            raise NotImplementedError

    def createSimpleMesh(self):
        self.mesh = []
        for x in range(self.rows - 1):
            for y in range(self.columns - 1):
                points = [
                    self.getPoint(x+0,y+0),
                    self.getPoint(x+0,y+1),
                    self.getPoint(x+1,y+0),
                    self.getPoint(x+1,y+1)
                ]
                points = list(filter(lambda x: x.val > 0, points))
                if len(points) == 4:
                    self.mesh.append((points[0], points[1], points[2]))
                    self.mesh.append((points[1], points[2], points[3]))

                elif len(points) == 3:
                    self.mesh.append((points[0], points[1], points[2]))

                else:
                    pass

        self.model.map.renderMesh(self)

    def createMSMesh(self):
        triangulationTable = {
            0: [''],
            1: ['1ab'],
            2: ['2ac'],
            3: ['12b', '2bc'],
            4: ['4bd'],
            5: ['1a4', '4ad'],
            6: ['2ac', '4bd'],
            7: ['12c', '1cd', '1d4'],
            8: ['8cd'],
            9: ['1ab', '8cd'],
            10: ['2ad', '82d'],
            11: ['21b', '2bd', '2d8'],
            12: ['4bc', '84c'],
            13: ['41a', '4ac', '4c8'],
            14: ['82a', '8ab', '8b4'],
            15: ['124', '248']
        }
        surfaceLevel = 0.5

        self.mesh = []
        for x in range(self.rows - 1):
            for y in range(self.columns - 1):
                triangulationIndex = 0

                p1 = self.getPoint(x+0,y+0)
                p2 = self.getPoint(x+0,y+1)
                p4 = self.getPoint(x+1,y+0)
                p8 = self.getPoint(x+1,y+1)

                if p1.val >= surfaceLevel: 
                    triangulationIndex += 1
                if p2.val >= surfaceLevel:
                    triangulationIndex += 2
                if p4.val >= surfaceLevel:
                    triangulationIndex += 4
                if p8.val >= surfaceLevel:
                    triangulationIndex += 8

                if p1.val != p2.val:
                    pa = Point(p1.x + (surfaceLevel - p1.val)/(p1.val-p2.val), p1.y, surfaceLevel)
                if p1.val != p4.val:
                    pb = Point(p1.x, p1.y + (surfaceLevel - p1.val)/(p1.val-p4.val), surfaceLevel)
                if p2.val != p8.val:
                    pc = Point(p2.x, p2.y + (surfaceLevel - p2.val)/(p2.val-p8.val), surfaceLevel)
                if p4.val != p8.val:
                    pd = Point(p4.x + (surfaceLevel - p4.val)/(p4.val-p8.val), p4.y, surfaceLevel)

                tris = []
                for tri in triangulationTable[triangulationIndex]:
                    tp = []
                    if '1' in tri:
                        tp.append(p1)
                    if '2' in tri:
                        tp.append(p2)
                    if '4' in tri:
                        tp.append(p4)
                    if '8' in tri:
                        tp.append(p8)
                    if 'a' in tri:
                        tp.append(pa)
                    if 'b' in tri:
                        tp.append(pb)
                    if 'c' in tri:
                        tp.append(pc)
                    if 'd' in tri:
                        tp.append(pd)
                    
                    if tp: tris.append(tuple(tp))
                
                for tri in tris:
                    self.mesh.append(tri)

        self.model.map.renderMesh(self)
            
class Point:
    def __init__(self, x: int, y: int, val: float = 0):
        self.x = x
        self.y = y
        self.val = val
        self.found = False

    def __repr__(self):
        return f"x: {self.x}\ty: {self.y}\tval: {self.val}"