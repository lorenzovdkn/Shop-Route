from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, QSpinBox, QLabel, QPushButton, QGraphicsLineItem
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QPixmap, QColor
import time,sys, os

class Grid(QGraphicsView):
    
    # Signaux émits
    positionSignal : pyqtSignal = pyqtSignal(tuple)
    lockedSignal : pyqtSignal = pyqtSignal(bool)
    sizeSignal : pyqtSignal = pyqtSignal(int,int)
    stepSignal : pyqtSignal = pyqtSignal(float)
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
        
        ########### QTimer de la grille ###########
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self.drawGrid)

    
    ############## Setter/Getter de la grille ##############

    def getGridSize(self) -> tuple:
        '''
        Permet de récupérer la taille de la grille
        Return
        tuple : (longueur, hauteur) de la grille
        '''
        return (self.width,self.height)
    
    def getStep(self) -> float:
        '''
        Permet de récupérer la taille d'une case
        Return:
        float: Taille longueur/hauteur d'une case
        '''
        return self.step
    

    def isLocked(self) -> bool:
        '''
        Permet de récupérer l'état de la grille.
        Return:
        boolean : True, la grille est verrouillé / False , la grille n'est pas verrouillé
        '''
        return self.locked

    
    def setPicture(self, picture : str):
        '''
        Permet de définir l'image en fond de la grille
        Paramètre:
        picture (str): chemin vers l'image
        '''
        self.picture = picture
        self.drawGrid()
    
    def setGridContent(self, gridContent: dict):
        '''
        Permet de définir le contenu de la grille
        @param gridContent (dict) : dictionnaire des cases à afficher
        '''
        self.gridContent = gridContent
    
    
    ############## Dessin de la grille ##############
    
    def setGrid(self, width : int, height : int, step : float, offset : tuple, locked : bool, position_dict : dict):
        
        '''
        Permet de redéfinir toutes les caratéristiques de la grille 
        si elle ne valent pas None et redessine la grille
        @param width (int) : longueur de la grille
        @param height (int) : hauteur de la grille
        @param step (float) : taille des cases
        @param offset (tuples) : décalage de la grille (x,y)
        @param locked (bool) : grille verrouillé ou non
        @param position_dict (dict) : dictionnaire des cases à afficher
        '''
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
    
    def drawGrid(self, position_dict : dict = None):
        '''
        Permet de dessinner la grille, utilise des lignes lorsque la grille est en mouvement 
        et des rectangles lorsqu'elle est verrouillée. Supprime tout pour réafficher l'image 
        et la grille.
        @param position_dict (dict) : dictionnaire des cases à afficher (non obligatoire), redéfinit automatiquement
            la valeur de l'attribut gridContent si le paramètre est utilisé
        '''
        if(position_dict is not None):
            self.gridContent = position_dict

        self.scene.clear()
        
        if(self.picture != None):
            pixmap = QPixmap(self.picture)
            pixmap = pixmap.scaledToWidth(1000, Qt.TransformationMode.SmoothTransformation)
            self.image_item = QGraphicsPixmapItem(pixmap)
            self.image_item.setPos(0,0)
            self.scene.addItem(self.image_item)
        
        if(self.locked):
            # Grille dessinnée en rectangle
            for x in range(0, self.width):
                for y in range(0, self.height):
                    rect : QGraphicsRectItem = QGraphicsRectItem((x-1)*self.step + self.offset.x(), (y-1)*self.step + self.offset.y(), self.step, self.step)
                    if((x,y) in [position for position in self.gridContent.keys()]):
                        color = QColor(self.gridContent.get((x,y)))
                        color.setAlpha(150)
                        rect.setBrush(color)
                    self.scene.addItem(rect)
        else:
            # Grille dessinée en lignes (optimisation : reduction du nombre de calcul par rapport aux rectangles)
            # n'affiche pas les couleurs
            long = (self.width-1) * self.step + self.offset.x()
            haut = (self.height-1) * self.step + self.offset.y()
            for x in range(0,self.width+1):
                for y in range(0,self.height+1):
                                        
                    lineX = QGraphicsLineItem((x-1)*self.step + self.offset.x(), (y-1)*self.step + self.offset.y(), long ,(y-1)*self.step + self.offset.y())
                    lineY = QGraphicsLineItem((x-1)*self.step + self.offset.x(), (y-1)*self.step + self.offset.y(), (x-1)*self.step + self.offset.x() , haut)
                    self.scene.addItem(lineX)
                    self.scene.addItem(lineY)
                    
    
    ############## Redefinition de méthode ##############
    
    def mousePressEvent(self, event):
        '''
        Redéfinition de la méthode de clique event. Remplace l'action de base par la possibilité de mouvoir
        la grille lorsqu'on clique gauche dessus ou récupère la case cliqué si la grille est verrouillée
        '''
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

    def mouseMoveEvent(self, event):
        '''
        Redéfinition de la méthode de mouvement de la souris. Si un mouvement est détecté et que l'utilisateur
        est en train de maintenir son clique. Une limite de mouvement est définit sur la taille de la scène
        '''
        if self.dragging and not self.locked:
            delta = event.pos() - self.lastPos
            self.offset += delta
            if self.offset.x() <= -self.size().width()//5:
                self.offset.setX(-self.size().width()//5 +1)
            if self.offset.x() + (self.width * self.step) > self.size().width() + 500:
                self.offset.setX((int) (self.size().width() + 499 - (self.width * self.step)))
            if self.offset.y() <= -self.size().height()//5:
                self.offset.setY(-self.size().height()//5+1)
            if self.offset.y() + (self.height * self.step) > self.size().height() + self.size().height()//5:
                self.offset.setY((int) (self.size().height() + self.size().height()//5 -1 - (self.height * self.step)))
            
            self.lastPos = event.pos()
            self.drawGrid()

    def mouseReleaseEvent(self, event):
        '''
        Redéfinition de la méthode du relachement de la souris. Désactive la possibilité de mouvoir la grille
        '''
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
    
    def wheelEvent(self, event):
        '''
        Redéfinition de la méthode de la molette. Zoom ou dézoom la grille en fonction du sens de rotation.
        '''
        # Increase the size of the grid
        if event.angleDelta().y() > 0 and not self.locked:
            if(self.step > 10):
                event.ignore()
                self.step = self.step - 1
                self.drawGrid()
                self.update_timer.start(10)
        # Reduce the size of the grid
        elif event.angleDelta().y() < 0 and not self.locked:
            if(self.step < 50):
                event.ignore()
                self.step = self.step + 1
                self.drawGrid()
                self.update_timer.start(10)
    
    
    ############# Verrouillage de la grille #############
    
    def lockGrid(self):
        self.sizeSignal.emit(self.width, self.height)
        self.stepSignal.emit(self.step)
        self.offsetSignal.emit((self.offset.x(), self.offset.y()))
            

class GridWidget(QWidget):
    
    def __init__(self, parent=None):
        super(GridWidget, self).__init__(parent)
        
        self.grid = Grid()
        
        # Création des widgets à inclure en bas
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
        
        # Layout en bas (options de la grille)
        self.bottomLayout = QHBoxLayout()  
        self.bottomLayout.addStretch()
        self.bottomLayout.addWidget(self.widthEdit)
        self.bottomLayout.addWidget(self.label)
        self.bottomLayout.addWidget(self.heightEdit)
        self.bottomLayout.addWidget(self.statusLabel)
        self.bottomLayout.addWidget(self.bouton)
        self.bottomLayout.addSpacing(15)
        
        self.gridLayout = QVBoxLayout()
        self.gridLayout.addWidget(self.grid)
        self.gridLayout.addLayout(self.bottomLayout)
        self.setLayout(self.gridLayout)
    
    # use to update the Qspinboxs
    def updateSpinbox(self, width, height):
        '''
        Met à jour les spinbox de taille de la grille
        @param width (int) : nombre de case en longueur
        @param height (int) : nombre de case en hauteur
        '''
        self.heightEdit.setValue(height)
        self.widthEdit.setValue(width)
            
    def modifiedSize(self):
        '''
        Permet de modifier le nombre de case de la grille en longueur et hauteur.
        Redessinne la grille a chaque modification
        '''
        if(self.widthEdit.text() != self.grid.width and self.widthEdit.value() is not None):
            self.grid.width = int(self.widthEdit.value())
            self.grid.width = int(self.widthEdit.value())
        if(self.heightEdit.text() != self.grid.height and self.heightEdit.value() is not None):
            self.grid.height = int(self.heightEdit.value())

        self.grid.drawGrid()
    
    
    ############# Grid locking methods #############
    
    def lockGrid(self):
        '''
        Inverse le verrouillage de la grille et met à jour la vue en conséquence
        '''
        self.grid.locked = not self.grid.locked
        self.grid.lockedSignal.emit(self.grid.locked)
        self.lockStateUpdate()
        self.grid.drawGrid()
    
    def lockStateUpdate(self):
        '''
        Permet de mettre à jour l'affichage en fonction du verrouillage de la grille.
        '''
        if(self.grid.isLocked()):
            # Grille en mode verrouiller
            self.bouton.setText("Déplacer")
            self.widthEdit.setDisabled(True)
            self.heightEdit.setDisabled(True)
            self.statusLabel.setText("Grille positionnée - Statut : Verrouillée")
        else:
            # Grille en mode déplacer
            self.bouton.setText("Verrouiller")
            self.statusLabel.setText("Veuillez positionner la grille - Statut : Non verrouillée")
    
    ############# Manage picture path #############
    
    def copyFileToAppDir(self, source_file: str) -> str:
        '''
        Permet de copier l'image utilisée dans un répertoire propre à l'application pour éviter les
        problèmes de chemin sortant du répertoire d'execution de l'application.
        @param source_file (str) : chemin source de l'image
        '''
        # Vérifier si le dossier 'images' existe, sinon le créer
        dest_dir = 'images'
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Nom de l'image
        print("source_file copyfiletoapp : ", source_file)
        image_name = os.path.basename(source_file)
        

        # Destination du fichier
        dest_file = os.path.join(dest_dir, image_name)

        # Lire le fichier source
        with open(source_file, 'rb') as src:
            content = src.read()
        
        # Écrire dans le fichier de destination
        with open(dest_file, 'wb') as dst:
            dst.write(content)
        
        # Retourner le chemin relatif du fichier copié
        file_path = os.path.relpath(dest_file)
        return file_path
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gridWidget = GridWidget()
    gridWidget.grid.setPicture('./images/plan11.jpg')
    gridWidget.show()
    sys.exit(app.exec())
