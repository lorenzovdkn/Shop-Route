from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor

class Grid(QWidget):
    def __init__(self):
        super().__init__()
        self.gridSize = 20
        self.offset = QPoint(0,0)
        print(self.offset)
        self.dragging = False
        self.lastPos = QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor("black"))
        for x in range(0, (int)((self.width()//self.gridSize)*self.gridSize), self.gridSize):
            for y in range(0, (int)((self.height()//self.gridSize)*self.gridSize), self.gridSize):
                painter.drawRect(x + self.offset.x(), y + self.offset.y(), self.gridSize, self.gridSize)
        #-(self.width()*2//self.gridSize)//4*self.gridSize,-(self.height()*2//self.gridSize)//4*self.gridSize)

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
            self.update()
            #elif self.offset.x() <= self.width()+self.gridSize:
            #    if(event.pos().x() < self.width()+ self.gridSize):
            #        x_move = event.pos().x() - self.lastPos.x()
            #        self.offset.setX(x_move)
            #        self.lastPos = event.pos()
            #        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            
if __name__ == "__main__":
    app = QApplication([])
    gridWidget = Grid()
    gridWidget.setMinimumSize(600,300)
    gridWidget.show()
    app.exec()
