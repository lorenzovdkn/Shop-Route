from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, QSpinBox, QLabel, QPushButton
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QColor
import time,sys, os

class Grid(QGraphicsView):
    
    positionSignal : pyqtSignal = pyqtSignal(tuple)
    lockedSignal : pyqtSignal = pyqtSignal(bool)
    sizeSignal : pyqtSignal = pyqtSignal(int,int)
    stepSignal : pyqtSignal = pyqtSignal(int)
    offsetSignal : pyqtSignal = pyqtSignal(tuple)
    
    def __init__(self, parent=None):
        super(Grid, self).__init__(parent)
        
        self.scene : QGraphicsScene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.gridStep : int = 20
        self.width : int =  25
        self.height : int = 25
        self.offset : QPoint = QPoint(0,0)
        self.lastPos : QPoint = QPoint(0,0)
        self.dragging : bool = False
        self.locked : bool = False
        self.picture : str = "plan5.jpeg"
        self.grid : dict = {}
        
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self.drawGrid)
        
        self.drawGrid()
        self.sceneWidth = self.scene.width()
        self.sceneHeight = self.scene.height()

    def getGridSize(self):
        return (self.width,self.height)
    
    def getGridStep(self):
        return self.gridStep
        
    def isLocked(self):
        return self.locked

    def setPicture(self, picture : str):
        self.picture = picture
    
    def setGrid(self, grid: dict):
        self.grid = grid
        
    # Draw the grid
    def drawGrid(self, width: int = None, height: int = None, step : float = None, position_dict : dict = None):
        
        if(width is None):
            width = self.width
        else:
            self.width = width
        if(height is None):
            height = self.height
        else:
            self.height = height
        if(step is None):
            step = self.gridStep
        if(position_dict is None):
            position_dict = self.grid
            
        self.scene.clear()
        
        if(self.picture != None):
            pixmap = QPixmap(self.picture)
            self.image_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.image_item)   
        
        #position_dict = {(1,3): "red", (2,5): "blue", (6,9): "green"}
        
        for x in range(0, width):
            for y in range(0, height):
                rect : QGraphicsRectItem = QGraphicsRectItem((x-1)*step + self.offset.x(), (y-1)*step + self.offset.y(), step, step)
                if((x,y) in [position for position in position_dict.keys()]):
                    print(x,y)
                    print(position_dict.get((x,y)))
                    color = QColor(position_dict.get((x,y)))
                    color.setAlpha(100)
                    rect.setBrush(color)
                self.scene.addItem(rect)
                
     # Manage the click event
    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            if self.locked:
                # Get the case who the user clicked
                scenePos : QPoint = self.mapToScene(event.pos())
                posX : int = (int) ((scenePos.x() - self.offset.x()) // self.gridStep + 1)
                posY : int = (int) ((scenePos.y() - self.offset.y()) // self.gridStep + 1)
                if(posX >= 0 and posY >= 0 and posX <= self.width and posY <= self.height):
                    self.positionSignal.emit((posX, posY))
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
                self.gridStep = self.gridStep - 1
                self.drawGrid()
                self.update_timer.start(10)
        # Increase the size of the grid
        elif event.angleDelta().y() > 0 and not self.locked:
            if(self.gridStep < 50):
                event.ignore()
                self.gridStep = self.gridStep + 1
                self.drawGrid()
                self.update_timer.start(10)
    
    def lockGrid(self):
        if(not self.locked):
            self.locked = True
            self.sizeSignal.emit(self.width, self.height)
            self.stepSignal.emit(self.gridStep)
            self.offsetSignal.emit((self.offset.x(), self.offset.y()))

class GridWidget(QWidget):
    
    def __init__(self, parent=None):
        super(GridWidget, self).__init__(parent)
        
        self.grid = Grid()
        
        self.widthEdit : QSpinBox = QSpinBox()
        self.widthEdit.setFixedWidth(50)
        self.widthEdit.setMinimum(10)
        self.widthEdit.setMaximum(60)
        self.widthEdit.setValue(self.grid.width)
        self.widthEdit.textChanged.connect(self.modifiedSize)
        self.label : QLabel = QLabel("x")
        self.heightEdit : QSpinBox = QSpinBox()
        self.heightEdit.setFixedWidth(50)
        self.heightEdit.setMinimum(10)
        self.heightEdit.setMaximum(60)
        self.heightEdit.setValue(self.grid.height)
        self.heightEdit.textChanged.connect(self.modifiedSize)
        self.statusLabel : QLabel = QLabel("Veuillez positionner la grille - Statut : Non verrouillée")
        self.bouton : QPushButton = QPushButton("Verrouiller")
        self.bouton.clicked.connect(self.lockGrid) 
        
        self.topLayout = QHBoxLayout()  
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.widthEdit)
        self.topLayout.addWidget(self.label)
        self.topLayout.addWidget(self.heightEdit)
        self.topLayout.addWidget(self.statusLabel)
        self.topLayout.addWidget(self.bouton)
        self.topLayout.addSpacing(15)
        
        self.gridLayout = QVBoxLayout()
        self.gridLayout.addLayout(self.topLayout)
        self.gridLayout.addWidget(self.grid)
        self.setLayout(self.gridLayout)
    
            
    def modifiedSize(self):
        if(self.widthEdit.text() != self.grid.width and self.widthEdit.value() is not None):
            self.grid.drawGrid(int(self.widthEdit.value()))
        if(self.heightEdit.text() != self.grid.height and self.heightEdit.value() is not None):
            self.grid.drawGrid(None,int(self.heightEdit.value()))
        
    def lockGrid(self):
        self.bouton.setDisabled(True)
        self.widthEdit.setDisabled(True)
        self.heightEdit.setDisabled(True)
        self.grid.lockGrid()
        self.statusLabel.setText("Grille positionnée - Statut : Verrouillée")
        
    # use to copy the selected image of the user to put it in the app saves (return the copy image path)
    def copyFileToAppDir(self, source_file: str) -> str:
        # Vérifier si le dossier 'images' existe, sinon le créer
        dest_dir = 'images'
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Nom de l'image
        image_name = os.path.basename(source_file)

        # Destination du fichier
        dest_file = os.path.join(dest_dir, image_name)

        try:
            # Lire le fichier source
            with open(source_file, 'rb') as src:
                content = src.read()
            
            # Écrire dans le fichier de destination
            with open(dest_file, 'wb') as dst:
                dst.write(content)
            
            QMessageBox.information(self, "Succès", f"Le fichier a été copié dans {dest_file}")

            # Retourner le chemin relatif du fichier copié
            print(dest_file)
            file_path = "images/" + str(dest_file.split('/')[-1])
            return file_path
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la copie du fichier : {e}")
            return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gridWidget = GridWidget()
    #gridLayout.grid.setPicture('./plan11.jpg')
    gridWidget.show()
    sys.exit(app.exec())