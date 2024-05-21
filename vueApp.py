import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPixmap

class Grid(QGraphicsView):
    
    positionSignal : pyqtSignal = pyqtSignal(QPoint)
    lockedSignal : pyqtSignal = pyqtSignal(bool)
    sizeSignal : pyqtSignal = pyqtSignal(int,int)
    stepSignal : pyqtSignal = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super(Grid, self).__init__(parent)
        
        self.scene : QGraphicsScene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.gridStep : int = 20
        self.width : int =  50
        self.height : int = 50
        self.offset : QPoint = QPoint(0,0)
        self.lastPos : QPoint = QPoint(0,0)
        self.dragging : bool = False
        self.locked : bool = False
        self.picture : str = None
        
        self.setPicture("./plan11.jpg")
        self.drawGrid()
        self.sceneWidth = self.scene.width()
        self.sceneHeight = self.scene.height()

    def getGridSize(self):
        self.sizeSignal.emit(self.width,self.height)
    
    def getGridStep(self):
        self.stepSignal.emit(self.gridStep)
        
    def isLocked(self):
        self.lockedSignal.emit(self.locked)

    def setPicture(self, picture : str):
        self.picture = picture
    # Draw the grid
    def drawGrid(self, width: int = None, height: int = None):
        
        if(width is None):
            width = self.width
        else:
            self.width = width
        if(height is None):
            height = self.height
        else:
            self.height = height
            
        self.scene.clear()
        if(self.picture != None):
            pixmap = QPixmap(self.picture)
            self.image_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.image_item)
        
        for x in range(-1, width):
            for y in range(-1, height):
                rect : QGraphicsRectItem = QGraphicsRectItem(x*self.gridStep + self.offset.x(), y*self.gridStep + self.offset.y(), self.gridStep, self.gridStep)
                self.scene.addItem(rect)
                
     # Manage the click event
    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            if self.locked:
                # Get the case who the user clicked
                scenePos : QPoint = self.mapToScene(event.pos())
                posX : int = (int) ((scenePos.x() - self.offset.x()) // self.gridStep + 1)
                posY : int = (int) ((scenePos.y() - self.offset.y()) // self.gridStep + 1)
                print(posX, posY)
                self.positionSignal.emit(QPoint(posX, posY))
            else:
                # Enable grid movement
                self.lastPos = event.pos()
                self.dragging = True

    # Move the grid if a click is detected
    def mouseMoveEvent(self, event):
        if self.dragging and not self.locked:
            delta = event.pos() - self.lastPos
            self.offset += delta
            if self.offset.x() <= -self.sceneWidth//10:
                self.offset.setX(0)
                self.dragging = False
            if self.offset.x() + (self.width * self.gridStep) > self.sceneWidth + self.sceneWidth//10:
                self.offset.setX((int) (self.sceneWidth - (self.width * self.gridStep)))
                self.dragging = False
            if self.offset.y() <= -self.sceneHeight//10:
                self.offset.setY(0)
                self.dragging = False
            if self.offset.y() + (self.height * self.gridStep) > self.sceneHeight + self.sceneHeight//10:
                self.offset.setY((int) (self.sceneHeight - (self.height * self.gridStep)))
                self.dragging = False
            
            self.lastPos = event.pos()
            self.drawGrid()

    # Disable the move click event
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
    
    # Scroll event
    def wheelEvent(self, event):
        # Reduce the size of the grid
        if event.angleDelta().y() < 0 and not self.locked:
            if(self.gridStep > 10):
                event.ignore()
                self.gridStep = self.gridStep - 0.25
                self.drawGrid()
        # Increase the size of the grid
        elif event.angleDelta().y() > 0 and not self.locked:
            if(self.gridStep < 50):
                event.ignore()
                self.gridStep = self.gridStep + 0.25
                self.drawGrid()
        

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("Grille")

        self.grid = Grid()
        self.setCentralWidget(self.grid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
