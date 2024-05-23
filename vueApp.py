import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QDockWidget, QFileDialog, QListWidget, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, QListWidgetItem
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPixmap, QColor

class Grid(QGraphicsView):
    positionSignal = pyqtSignal(QPoint)
    lockedSignal = pyqtSignal(bool)
    sizeSignal = pyqtSignal(int, int)
    stepSignal = pyqtSignal(int)
    offsetSignal = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super(Grid, self).__init__(parent)
        
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.gridStep = 20
        self.width = 50
        self.height = 50
        self.offset = QPoint(0, 0)
        self.lastPos = QPoint(0, 0)
        self.dragging = False
        self.locked = True
        self.picture = "./plan11.jpg"
        self.grid = {}
        
        self.drawGrid()
        self.sceneWidth = self.scene.width()
        self.sceneHeight = self.scene.height()

    def getGridSize(self):
        return (self.width, self.height)
    
    def getGridStep(self):
        return self.gridStep
        
    def isLocked(self):
        return self.locked

    def setPicture(self, picture):
        self.picture = picture
    
    def setGrid(self, grid):
        self.grid = grid
        
    def drawGrid(self, width=None, height=None, step=None, position_dict=None):
        if width is None:
            width = self.width
        else:
            self.width = width
        if height is None:
            height = self.height
        else:
            self.height = height
        if step is None:
            step = self.gridStep
        if position_dict is None:
            position_dict = self.grid
            
        self.scene.clear()
        
        if self.picture is not None:
            pixmap = QPixmap(self.picture)
            self.image_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.image_item)
        
        position_dict = {(1, 3): "red", (2, 5): "blue"}
        
        for x in range(-1, width):
            for y in range(-1, height):
                rect = QGraphicsRectItem(x * step + self.offset.x(), y * step + self.offset.y(), step, step)
                if (x, y) in [position for position in position_dict.keys()]:
                    color = QColor(position_dict.get((x, y)))
                    color.setAlpha(100)
                    rect.setBrush(color)
                self.scene.addItem(rect)
                
    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            if self.locked:
                scenePos = self.mapToScene(event.pos())
                posX = int((scenePos.x() - self.offset.x()) // self.gridStep + 1)
                posY = int((scenePos.y() - self.offset.y()) // self.gridStep + 1)
                print(posX, posY)
                self.positionSignal.emit(QPoint(posX, posY))
            else:
                self.lastPos = event.pos()
                self.dragging = True

    def mouseMoveEvent(self, event):
        if self.dragging and not self.locked:
            delta = event.pos() - self.lastPos
            self.offset += delta
            if self.offset.x() <= -self.sceneWidth // 10:
                self.offset.setX(0)
                self.dragging = False
            if self.offset.x() + (self.width * self.gridStep) > self.sceneWidth + self.sceneWidth // 10:
                self.offset.setX(int(self.sceneWidth - (self.width * self.gridStep)))
                self.dragging = False
            if self.offset.y() <= -self.sceneHeight // 10:
                self.offset.setY(0)
                self.dragging = False
            if self.offset.y() + (self.height * self.gridStep) > self.sceneHeight + self.sceneHeight // 10:
                self.offset.setY(int(self.sceneHeight - (self.height * self.gridStep)))
                self.dragging = False
            
            self.lastPos = event.pos()
            self.drawGrid()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
    
    def wheelEvent(self, event):
        if event.angleDelta().y() < 0 and not self.locked:
            if self.gridStep > 10:
                event.ignore()
                self.gridStep -= 1
                self.drawGrid()
                time.sleep(0.01)
        elif event.angleDelta().y() > 0 and not self.locked:
            if self.gridStep < 50:
                event.ignore()
                self.gridStep += 1
                self.drawGrid()
                time.sleep(0.01)
    
    def lockGrid(self):
        if not self.locked:
            self.locked = True
            self.sizeSignal.emit(self.width, self.height)
            self.stepSignal.emit(self.gridStep)
            self.offsetSignal.emit((self.offset.x(), self.offset.y()))
            


class VueProjet(QMainWindow):
    ajoutClicked = pyqtSignal()
    supprimerClicked = pyqtSignal()
    analyseClicked = pyqtSignal()
    fnameOpen = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Parcours de courses')
        self.setGeometry(100, 100, 800, 600)
        
        # Layouts
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QHBoxLayout(self.central_widget)       
        self.dock_container = QVBoxLayout()
        self.button_layout = QVBoxLayout()      
        self.dock_layout = QVBoxLayout()
        self.bottomRight_layout = QHBoxLayout()
        
        # Widgets
        self.analyse = QPushButton('Analyser')
        self.analyse.setMaximumWidth(400)
        self.ajout = QPushButton('Ajouter à la liste de courses')
        self.supprimer = QPushButton('Supprimer de la liste de courses')
        
        # Grid Widget
        self.grid = Grid()
        
        # Right Layout
        self.rightLayout = QVBoxLayout()
        self.rightLayout.addWidget(self.grid)
        self.bottomRight_layout.addWidget(self.analyse)
        self.rightLayout.addLayout(self.bottomRight_layout)

        
        # Add right layout to main layout
        self.layout_principal.addLayout(self.dock_container)
        self.layout_principal.addLayout(self.rightLayout)
        
        # Menu bar
        menu_bar = self.menuBar()
        menu_fichier = menu_bar.addMenu("Fichier")
        menu_fichier.addAction('Ouvrir', self.ouvrir)
        
        # Docks
        self.dock = QDockWidget('Liste des articles')
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
        self.articles_listWidget = QListWidget()
        self.dock.setWidget(self.articles_listWidget)
        self.dock.setMaximumWidth(300)
        
        self.dock2 = QDockWidget('Liste de course')
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock2)
        self.liste_course = QListWidget()
        self.dock2.setWidget(self.liste_course)
        self.dock2.setMaximumWidth(300)
        
        # Add docks to dock layout
        self.dock_layout.addWidget(self.dock)
        self.dock_layout.addWidget(self.dock2)
        
        # Add buttons to button layout
        self.button_layout.addWidget(self.ajout)
        self.button_layout.addWidget(self.supprimer)
        
        # Add dock and button layouts to dock container
        self.dock_container.addLayout(self.dock_layout)
        self.dock_container.addLayout(self.button_layout)
        
        # Connect signals
        self.ajout.clicked.connect(self.ajoutClicked.emit)
        self.supprimer.clicked.connect(self.supprimerClicked.emit)
        self.analyse.clicked.connect(self.analyseClicked.emit)

    def ouvrir(self) -> str:
        boite = QFileDialog()
        chemin, validation = boite.getOpenFileName(directory=sys.path[0])
        if validation:
            self.fnameOpen.emit(chemin)
            
    
    dico_articles = {'Légumes': 'carotte', "Légumes": 'tomate', "Hygiène": 'savon', "Hygiène": 'serviette'}
    
    def afficherArticles(self):
        for categorie, produit in self.liste_articles:
            # Ajouter la catégorie comme élément de haut niveau si elle n'existe pas déjà
            if not any(categorie == self.articles_listWidget.item(i).text() for i in range(self.articles_listWidget.count())):
                categorie_item = QListWidgetItem(categorie)
                self.articles_listWidget.addItem(categorie_item)
            # Ajouter le produit comme sous-élément
            produit_item = QListWidgetItem(produit)
            for i in range(self.articles_listWidget.count()):
                if self.articles_listWidget.item(i).text() == categorie:
                    self.articles_listWidget.item(i).addChild(produit_item)

            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = VueProjet()
    fenetre.show()
    sys.exit(app.exec())
