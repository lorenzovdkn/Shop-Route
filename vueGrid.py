from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPixmap

class Grid(QGraphicsView):
    positionSignal: pyqtSignal = pyqtSignal(QPoint)
    lockedSignal: pyqtSignal = pyqtSignal(bool)
    sizeSignal: pyqtSignal = pyqtSignal(int, int)
    stepSignal: pyqtSignal = pyqtSignal(int)
    offsetSignal: pyqtSignal = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super(Grid, self).__init__(parent)
        self.scene: QGraphicsScene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.gridStep: int = 20
        self.width: int = 50
        self.height: int = 50
        self.offset: QPoint = QPoint(0, 0)
        self.lastPos: QPoint = QPoint(0, 0)
        self.dragging: bool = False
        self.locked: bool = False
        self.picture: str = None

        self.drawGrid()
        self.sceneWidth = self.scene.width()
        self.sceneHeight = self.scene.height()

    def getGridSize(self):
        return (self.width, self.height)

    def getGridStep(self):
        return self.gridStep

    def isLocked(self):
        return self.locked

    def setPicture(self, picture: str):
        self.picture = picture

    def drawGrid(self, width: int = None, height: int = None):
        if width is None:
            width = self.width
        else:
            self.width = width
        if height is None:
            height = self.height
        else:
            self.height = height

        self.scene.clear()

        if self.picture is not None:
            pixmap = QPixmap(self.picture)
            self.image_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.image_item)

        self.offsetSignal.emit((self.offset.x(), self.offset.y()))

        for x in range(-1, width):
            for y in range(-1, height):
                rect: QGraphicsRectItem = QGraphicsRectItem(x * self.gridStep + self.offset.x(), y * self.gridStep + self.offset.y(), self.gridStep, self.gridStep)
                self.scene.addItem(rect)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            if self.locked:
                scenePos: QPoint = self.mapToScene(event.pos())
                posX: int = int((scenePos.x() - self.offset.x()) // self.gridStep + 1)
                posY: int = int((scenePos.y() - self.offset.y()) // self.gridStep + 1)
                self.positionSignal.emit(QPoint(posX, posY))
            else:
                self.lastPos = event.pos()
                self.dragging = True

    def mouseMoveEvent(self, event):
        if self.dragging and not self.locked:
            delta = event.pos() - self.lastPos
            self.offset += delta
            if self.offset.x() <= -self.sceneWidth // 10:
                self.offset.setX(0)
                self.dragging = False
            if self.offset.x() + (self.width * self.gridStep) > self.sceneWidth + self.sceneWidth // 10:
                self.offset.setX(int(self.sceneWidth - (self.width * self.gridStep)))
                self.dragging = False
            if self.offset.y() <= -self.sceneHeight // 10:
                self.offset.setY(0)
                self.dragging = False
            if self.offset.y() + (self.height * self.gridStep) > self.sceneHeight + self.sceneHeight // 10:
                self.offset.setY(int(self.sceneHeight - (self.height * self.gridStep)))
                self.dragging = False

            self.lastPos = event.pos()
            self.drawGrid()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def wheelEvent(self, event):
        if event.angleDelta().y() < 0 and not self.locked:
            if self.gridStep > 10:
                event.ignore()
                self.gridStep -= 0.25
                self.drawGrid()
        elif event.angleDelta().y() > 0 and not self.locked:
            if self.gridStep < 50:
                event.ignore()
                self.gridStep += 0.25
                self.drawGrid()
