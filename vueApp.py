from PyQt6.QtWidgets import QWidget, QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem,QStackedLayout, QLabel
from PyQt6.QtGui import QPixmap, QColor
import sys

class Graphic (QGraphicsView):
    def __init__ (self):
        super().__init__()
        self.scene : QGraphicsScene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.setAutoFillBackground(False)
        self.setContentsMargins(0, 0, 0, 0)
        self.scene.setBackgroundBrush(QColor(0,0,0,0))
        
        self.graphicSize : int = 20
        self.caseSize : int = 50
        
        for i in range(0, self.graphicSize):
            for j in range(0, self.graphicSize):
                rect : QGraphicsRectItem = QGraphicsRectItem(i*self.caseSize,j*self.caseSize,self.caseSize,self.caseSize)
                rect.setBrush(QColor(0,0,0,0))
                self.scene.addItem(rect)
                
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        
class vueGraphic(QWidget):
    def __init__ (self):
        super().__init__()
        
        self.scene = Graphic()
        
        self.mainLayout = QStackedLayout()
        self.label = QLabel("test")
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.label.setAutoFillBackground(False)
        self.label.setContentsMargins(0, 0, 0, 0)
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.picture = QPixmap("./plan11.jpg")
        
        self.pictureLabel = QLabel()
        self.pictureLabel.setPixmap(self.picture)
        self.pictureLabel.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        
        
        self.mainLayout.addWidget(self.scene)
        self.mainLayout.addWidget(self.pictureLabel)
        self.mainLayout.addWidget(self.label)
        self.setLayout(self.mainLayout)
        
        self.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    vue = vueGraphic()
    sys.exit(app.exec())
    