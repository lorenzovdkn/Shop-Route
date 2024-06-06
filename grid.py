from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, QSpinBox, QLabel, QPushButton, QGraphicsLineItem
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QPixmap, QColor
import time,sys, os

class Grid(QGraphicsView):
    
    # Signaux émits
    positionSignal : pyqtSignal = pyqtSignal(tuple)
    lockedSignal : pyqtSignal = pyqtSignal(bool)
    sizeSignal : pyqtSignal = pyqtSignal(int,int)
    stepSignal : pyqtSignal = pyqtSignal(int)
    offsetSignal : pyqtSignal = pyqtSignal(tuple)
    
    def __init__(self, parent=None):
        super(Grid, self).__init__(parent)
        
        self.scene : QGraphicsScene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.step : int = 20
        self.width : int =  25
        self.height : int = 25
        self.offset : QPoint = QPoint(0,0)
        self.lastPos : QPoint = QPoint(0,0)
        self.dragging : bool = False
        self.locked : bool = False
        self.picture : str = ""
        self.gridContent : dict = {}
        self.sceneWidth = self.size().width()
        self.sceneHeight = self.size().height()
        self.drawGrid({})
        
        
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self.drawGrid)

    '''
    Permet de récupérer la taille de la grille
    Return
    tuple : (longueur, hauteur) de la grille
    '''
    def getGridSize(self) -> tuple:
        return (self.width,self.height)
    
    '''
    Permet de récupérer la taille d'une case
    Return:
    float: Taille longueur/hauteur d'une case
    '''
    def getStep(self) -> float:
        return self.step
    
    '''
    Permet de récupérer l'état de la grille.
    Return:
    boolean : True, la grille est verrouillé / False , la grille n'est pas verrouillé
    '''
    def isLocked(self) -> bool:
        return self.locked

    '''
    Permet de définir l'image en fond de la grille
    Paramètre:
    picture (str): chemin vers l'image
    '''
    def setPicture(self, picture : str):
        self.picture = picture
        self.drawGrid()
    
    def setGridContent(self, gridContent: dict):
        self.gridContent = gridContent
        
    # Draw the grid
    def drawGrid(self, position_dict : dict = None):
        if(position_dict is not None):
            self.gridContent = position_dict

        self.scene.clear()
        
        if(self.picture != None):
            pixmap = QPixmap(self.picture)
            pixmap = pixmap.scaledToWidth(self.size().width(), Qt.TransformationMode.SmoothTransformation)
            self.image_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.image_item)
        
        if(self.locked):
            for x in range(0, self.width):
                for y in range(0, self.height):
                    rect : QGraphicsRectItem = QGraphicsRectItem((x-1)*self.step + self.offset.x(), (y-1)*self.step + self.offset.y(), self.step, self.step)
                    if((x,y) in [position for position in self.gridContent.keys()]):
                        color = QColor(self.gridContent.get((x,y)))
                        color.setAlpha(150)
                        rect.setBrush(color)
                    self.scene.addItem(rect)
        else:
            long = (self.width-1) * self.step + self.offset.x()
            haut = (self.height-1) * self.step + self.offset.y()
            for x in range(0,self.width+1):
                for y in range(0,self.height+1):
                                        
                    lineX = QGraphicsLineItem((x-1)*self.step + self.offset.x(), (y-1)*self.step + self.offset.y(), long ,(y-1)*self.step + self.offset.y())
                    lineY = QGraphicsLineItem((x-1)*self.step + self.offset.x(), (y-1)*self.step + self.offset.y(), (x-1)*self.step + self.offset.x() , haut)
                    self.scene.addItem(lineX)
                    self.scene.addItem(lineY)
                
     # Manage the click event
    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            if self.locked:
                # Get the case who the user clicked
                scenePos : QPoint = self.mapToScene(event.pos())
                posX : int = (int) ((scenePos.x() - self.offset.x()) // self.step + 1)
                posY : int = (int) ((scenePos.y() - self.offset.y()) // self.step + 1)
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
            if self.offset.x() <= -self.size().width()//10:
                self.offset.setX(0)
                #self.dragging = False
            if self.offset.x() + (self.width * self.step) > self.size().width() + self.size().width()//10:
                self.offset.setX((int) (self.size().width() - (self.width * self.step)))
                #self.dragging = False
            if self.offset.y() <= -self.size().height()//10:
                self.offset.setY(0)
                #self.dragging = False
            if self.offset.y() + (self.height * self.step) > self.size().height() + self.size().height()//10:
                self.offset.setY((int) (self.size().height() - (self.height * self.step)))
                #self.dragging = False
            
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
            if(self.step > 10):
                event.ignore()
                self.step = self.step - 1
                self.drawGrid()
                self.update_timer.start(10)
                self.update_timer.start(10)
        # Increase the size of the grid
        elif event.angleDelta().y() > 0 and not self.locked:
            if(self.step < 50):
                event.ignore()
                self.step = self.step + 1
                self.drawGrid()
                self.update_timer.start(10)
    
    def lockGrid(self):
        self.sizeSignal.emit(self.width, self.height)
        self.stepSignal.emit(self.step)
        self.offsetSignal.emit((self.offset.x(), self.offset.y()))
            
    # Define the caracteristic of the grid and update the grid in the app
    def setGrid(self, width : int, height : int, step : float, offset : tuple, locked : bool, position_dict : dict):
        if(width is not None):
            self.width = width
        if(height is not None):
            self.height = height
        if(step is not None):
            self.step = step
        if(offset is not None):
            self.offset = QPoint(offset[0],offset[1])
        if(locked is not None):
            self.locked = locked
        self.drawGrid(position_dict)

class GridWidget(QWidget):
    
    def __init__(self, parent=None):
        super(GridWidget, self).__init__(parent)
        
        self.grid = Grid()
        
        self.widthEdit : QSpinBox = QSpinBox()
        self.widthEdit.setFixedWidth(50)
        self.widthEdit.setMinimum(10)
        self.widthEdit.setMaximum(100)
        self.widthEdit.setValue(self.grid.width)
        self.widthEdit.textChanged.connect(self.modifiedSize)
        self.label : QLabel = QLabel("x")
        self.heightEdit : QSpinBox = QSpinBox()
        self.heightEdit.setFixedWidth(50)
        self.heightEdit.setMinimum(10)
        self.heightEdit.setMaximum(100)
        self.heightEdit.setValue(self.grid.height)
        self.heightEdit.textChanged.connect(self.modifiedSize)
        self.statusLabel : QLabel = QLabel("Veuillez positionner la grille - Statut : Non verrouillée")
        self.bouton : QPushButton = QPushButton("Verrouiller")
        self.bouton.setToolTip("Lorsqu'elle est verrouillé une fois, il \nn'est plus possible de redimensionner la grille")
        self.bouton.clicked.connect(self.lockGrid)
        self.bouton.clicked.connect(self.grid.lockGrid)
        
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
            self.grid.width = int(self.widthEdit.value())
            self.grid.width = int(self.widthEdit.value())
        if(self.heightEdit.text() != self.grid.height and self.heightEdit.value() is not None):
            self.grid.height = int(self.heightEdit.value())

        self.grid.drawGrid()
        
    def lockGrid(self):
        self.grid.locked = not self.grid.locked
        self.lockStateUpdate()
    
    def lockStateUpdate(self):
        if(self.grid.isLocked()):
            self.bouton.setText("Déplacer")
            self.widthEdit.setDisabled(True)
            self.heightEdit.setDisabled(True)
            self.statusLabel.setText("Grille positionnée - Statut : Verrouillée")
        else:
            self.bouton.setText("Verrouiller")
            self.statusLabel.setText("Veuillez positionner la grille - Statut : Non verrouillée")
        
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
        
    # use to update the Qspinboxs
    def updateSpinbox(self, width, height):
        self.heightEdit.setValue(height)
        self.widthEdit.setValue(width)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gridWidget = GridWidget()
    #gridLayout.grid.setPicture('./plan11.jpg')
    gridWidget.show()
    sys.exit(app.exec())