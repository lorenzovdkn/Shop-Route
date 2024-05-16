import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsLineItem
from PyQt6.QtCore import Qt, QPoint

class Grid(QGraphicsView):
    def __init__(self, parent=None):
        super(Grid, self).__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.offset = QPoint(0,0)
        self.lastPos = QPoint(0,0)
        self.dragging = False
        
        self.gridSize = 8
        self.gridStep = 20
        self.drawGrid()

    def drawGrid(self):
        self.scene.clear()
        for i in range(-self.gridSize, self.gridSize+1):
            self.scene.addItem(QGraphicsLineItem(i*self.gridStep + self.offset.x(), -self.gridSize*self.gridStep  + self.offset.y(), i*self.gridStep  + self.offset.x(), self.gridSize*self.gridStep  + self.offset.y()))
            self.scene.addItem(QGraphicsLineItem(-self.gridSize*self.gridStep  + self.offset.x(), i*self.gridStep  + self.offset.y(), self.gridSize*self.gridStep  + self.offset.x(), i*self.gridStep  + self.offset.y()))

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.lastPos = event.pos()
            self.dragging = True

    def mouseMoveEvent(self, event):
        if self.dragging:
            if self.offset.x() < self.width() and self.offset.x()+ 2*self.width() > self.width():
                pass
            #if self.offset.x() < self.width() and self.offset.y() < self.height():
            delta = event.pos() - self.lastPos
            self.offset += delta
            self.lastPos = event.pos()
            print(self.offset.x(),self.offset.y())
            self.drawGrid()
            #elif self.offset.x() <= self.width()+self.gridSize:
            #    if(event.pos().x() < self.width()+ self.gridSize):
            #        x_move = event.pos().x() - self.lastPos.x()
            #        self.offset.setX(x_move)
            #        self.lastPos = event.pos()
            #        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
        

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Grille déplaçable avec PyQt6")

        self.grid = Grid()
        self.setCentralWidget(self.grid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
