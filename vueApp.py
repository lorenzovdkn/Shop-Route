#from PyQt6.QtWidgets import QWidget, QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem,QStackedLayout, QLabel
#from PyQt6.QtGui import QPixmap, QColor
#import sys
#
#class Graphic (QGraphicsView):
#    def __init__ (self):
#        super().__init__()
#        self.scene : QGraphicsScene = QGraphicsScene(self)
#        self.setScene(self.scene)
#        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
#        self.setAutoFillBackground(False)
#        self.setContentsMargins(0, 0, 0, 0)
#        self.scene.setBackgroundBrush(QColor(0,0,0,0))
#        
#        self.graphicSize : int = 20
#        self.caseSize : int = 50
#        
#        for i in range(0, self.graphicSize):
#            for j in range(0, self.graphicSize):
#                rect : QGraphicsRectItem = QGraphicsRectItem(i*self.caseSize,j*self.caseSize,self.caseSize,self.caseSize)
#                rect.setBrush(QColor(0,0,0,0))
#                self.scene.addItem(rect)
#                
#        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
#        
#class vueGraphic(QWidget):
#    def __init__ (self):
#        super().__init__()
#        
#        self.scene = Graphic()
#        
#        self.mainLayout = QStackedLayout()
#        self.label = QLabel("test")
#        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
#        self.label.setAutoFillBackground(False)
#        self.label.setContentsMargins(0, 0, 0, 0)
#        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
#        #self.picture = QPixmap("./plan11.jpg")
#        
#        #self.pictureLabel = QLabel()
#        #self.pictureLabel.setPixmap(self.picture)
#        #self.pictureLabel.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
#        #
#        
#        self.mainLayout.addWidget(self.scene)
#        #self.mainLayout.addWidget(self.pictureLabel)
#        self.mainLayout.addWidget(self.label)
#        self.setLayout(self.mainLayout)
#        
#        self.show()
#        
#if __name__ == "__main__":
#    app = QApplication(sys.argv)
#    vue = vueGraphic()
#    sys.exit(app.exec())
#    #

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor

class Grid(QWidget):
    def __init__(self):
        super().__init__()
        self.gridSize = 20
        self.offset = QPoint(int(self.width()/2), int(self.height()/2))
        self.dragging = False
        self.lastPos = QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor("black"))
        for x in range(-self.width(), self.width(), self.gridSize):
            for y in range(-self.height(), self.height(), self.gridSize):
                painter.drawRect(x + self.offset.x(), y + self.offset.y(), self.gridSize, self.gridSize)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.lastPos = event.pos()
            self.dragging = True

    def mouseMoveEvent(self, event):
        
        if self.dragging:
            if self.offset.x() < self.width() and self.offset.y() < self.height():
                delta = event.pos() - self.lastPos
                self.offset += delta
                self.lastPos = event.pos()
                print(self.offset.x(),self.offset.y())
                self.update()
            elif self.offset.x() <= self.width()+self.gridSize:
                if(event.pos().x() < self.width()+ self.gridSize):
                    x_move = event.pos().x() - self.lastPos.x()
                    self.offset.setX(x_move)
                    self.lastPos = event.pos()
                    print("t")
                    self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            
if __name__ == "__main__":
    app = QApplication([])
    gridWidget = Grid()
    gridWidget.show()
    app.exec()
