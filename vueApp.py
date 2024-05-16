import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtCore import Qt, QPoint

class Grid(QGraphicsView):
    def __init__(self, parent=None):
        super(Grid, self).__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.gridSize = 100
        self.gridStep = 20

        self.offset = QPoint(int(-self.gridStep * (self.gridSize/2)) , (int)(-self.gridStep * (self.gridSize/2)))
        self.lastPos = QPoint(0,0)
        self.dragging = False
        
        self.drawGrid()


    # Draw the grid
    def drawGrid(self):
        self.scene.clear()
        for x in range(0, self.gridSize):
            for y in range(0, self.gridSize):
                self.scene.addItem(QGraphicsRectItem(x*self.gridStep + self.offset.x(), y*self.gridStep + self.offset.y(), self.gridStep, self.gridStep))
     
     # Enable the click move event   
    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.lastPos = event.pos()
            self.dragging = True

    # Move the grid if a click is detected
    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.pos() - self.lastPos
            self.offset += delta
            self.lastPos = event.pos()
            print(self.offset.x(),self.offset.y())
            self.drawGrid()

    # Disable the move click event
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
        

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Grille déplaçable avec PyQt6")

        self.grid = Grid()
        self.setCentralWidget(self.grid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
