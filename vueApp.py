import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPixmap

class Grid(QGraphicsView):
    
    positionSignal : pyqtSignal = pyqtSignal(QPoint)
    lockedSignal : pyqtSignal = pyqtSignal(bool)
    sizeSignal : pyqtSignal = pyqtSignal(int)
    stepSignal : pyqtSignal = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super(Grid, self).__init__(parent)
        
        self.scene : QGraphicsScene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.gridSize : int = 20
        self.gridStep : int = 20
        self.offset : QPoint = QPoint(0,0)
        self.lastPos : QPoint = QPoint(0,0)
        self.dragging : bool = False
        self.locked : bool = True
        
        self.drawGrid()


    # Draw the grid
    def drawGrid(self):
        self.scene.clear()
        pixmap = QPixmap('./plan11.jpg')
        self.image_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.image_item)
        for x in range(0, self.gridSize):
            for y in range(0, self.gridSize):
                self.scene.addItem(QGraphicsRectItem(x*self.gridStep + self.offset.x(), y*self.gridStep + self.offset.y(), self.gridStep, self.gridStep))
     
     # Manage the click event
    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            if self.locked:
                # Get the case who the user clicked
                scenePos : QPoint = self.mapToScene(event.pos())
                posX : int = (int) (scenePos.x() - self.offset.x()) // self.gridStep + 1
                posY : int = (int) (scenePos.y() - self.offset.y()) // self.gridStep + 1
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
            self.lastPos = event.pos()
            self.drawGrid()

    # Disable the move click event
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
        

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Grille")

        self.grid = Grid()
        self.setCentralWidget(self.grid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
