import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QDockWidget, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, QTreeWidgetItem, QTreeWidget
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPixmap, QColor,QKeySequence,QShortcut
from PyQt6.QtCore import QTimer


class Grid(QGraphicsView):
    positionSignal = pyqtSignal(QPoint)
    lockedSignal = pyqtSignal(bool)
    sizeSignal = pyqtSignal(int, int)
    stepSignal = pyqtSignal(int)
    offsetSignal = pyqtSignal(tuple)
    indexReset = pyqtSignal()
    

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
        self.parcours = []
        self.produit = []
        self.position = ()
        self.caseprive = []
        self.couleur = "brown"
        self.index = 0
        self.caisses = []
        self.entree = []

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
        self.drawGrid()
    
    def setGrid(self, grid):
        self.grid = grid

    def setParcours(self, parcours):
        self.parcours = parcours
        self.drawGrid()

    def setProduit(self, produit):
        self.produit = produit
        self.drawGrid()
    
    def setPosition(self,position):
        self.position = position
        self.drawGrid()

    def setCasePrive(self,prive):
        self.caseprive = prive
        self.drawGrid()

    def setIndex(self,index):
        self.index = index
        self.drawGrid()

    def setCaisses(self,caisses):
        self.caisses = caisses
        self.drawGrid()

    def setEntree(self,entree):
        self.entree = entree
        self.drawGrid()

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
        
        if self.parcours:
            self.drawNextParcours()

        if self.produit:
            for pos,couleur in self.produit:
                x, y = pos
                if 0 <= x < width and 0 <= y < height:
                    rect = QGraphicsRectItem(x * step + self.offset.x() - step, y * step - step+ self.offset.y(), step, step)
                    color = QColor(couleur)
                    color.setAlpha(100)
                    rect.setBrush(color)
                    self.scene.addItem(rect)
        
        if self.position:
            for pos in self.position:
                x, y = pos
                if 0 <= x < width and 0 <= y < height:
                    rect = QGraphicsRectItem(x * step + self.offset.x() - step, y * step + self.offset.y() - step, step, step)
                    color = QColor("orange")
                    color.setAlpha(100)
                    rect.setBrush(color)
                    self.scene.addItem(rect)
        
        if self.caseprive:
            for pos in self.caseprive:
                x, y = pos
                if 0 <= x < width and 0 <= y < height:
                    rect = QGraphicsRectItem(x * step + self.offset.x() - step, y * step + self.offset.y() - step, step, step)
                    color = QColor("red")
                    color.setAlpha(100)
                    rect.setBrush(color)
                    self.scene.addItem(rect)

        if self.caisses :
            for pos in self.caisses:
                x, y = pos
                if 0 <= x < width and 0 <= y < height:
                    rect = QGraphicsRectItem(x * step + self.offset.x() - step, y * step + self.offset.y() - step, step, step)
                    color = QColor("grey")
                    color.setAlpha(120)
                    rect.setBrush(color)
                    self.scene.addItem(rect)

        if self.entree:
            for pos in self.entree:
                x, y = pos
                if 0 <= x < width and 0 <= y < height:
                    rect = QGraphicsRectItem(x * step + self.offset.x() - step, y * step + self.offset.y() - step, step, step)
                    color = QColor("green")
                    color.setAlpha(120)
                    rect.setBrush(color)
                    self.scene.addItem(rect)
        
        for x in range(-1, width):
            for y in range(-1, height):
                rect = QGraphicsRectItem(x * step + self.offset.x(), y * step + self.offset.y(), step, step)
                if (x, y) in position_dict:
                    color = QColor(position_dict.get((x, y)))
                    color.setAlpha(100)
                    rect.setBrush(color)
                self.scene.addItem(rect)

    def drawNextParcours(self):
        # Vérifier si l'index de parcours est inférieur à la longueur de parcours
        if self.index + 2 > len(self.parcours):
            print("DDDD")
            self.indexReset.emit()
        for pos in self.parcours[self.index]:
            x, y = pos
            if 0 <= x < self.width and 0 <= y < self.height:
                rect = QGraphicsRectItem(x * self.gridStep - self.gridStep + self.offset.x(), y * self.gridStep + self.offset.y() - self.gridStep, self.gridStep, self.gridStep)
                color = QColor("#000000")
                color.setAlpha(200)
                rect.setBrush(color)
                self.scene.addItem(rect)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            if self.locked:
                scenePos = self.mapToScene(event.pos())
                posX = int((scenePos.x() - self.offset.x()) // self.gridStep+ 1)
                posY = int((scenePos.y() - self.offset.y()) // self.gridStep + 1)
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
    ajoutClicked = pyqtSignal(str) # Envoi le produit a ajouter à la liste de course
    supprimerClicked = pyqtSignal(str) # Envoi le produit a delete
    analyseClicked = pyqtSignal() # Lance l'affichage du parcours
    fnameOpen = pyqtSignal(str)
    dicoAleatoireClicked = pyqtSignal()
    indexClicked = pyqtSignal()
    fnameOpen_bis = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        self.dico_courses = []
        self.parcours = []

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
        self.dico_create = QPushButton('Génerer une liste de courses aléatoire')
        self.setpos = QPushButton('Continuer')

        self.setpos.setVisible(False)

        # Grid Widget
        self.grid = Grid()
        
        # Right Layout
        self.rightLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.rightLayout.addLayout(self.topLayout)
        self.topLayout.addWidget(self.analyse)
        self.topLayout.addWidget(self.dico_create)
        self.rightLayout.addWidget(self.grid)
        self.bottomRight_layout.addWidget(self.setpos)
        self.rightLayout.addLayout(self.bottomRight_layout)
        
        
        # Add right layout to main layout
        self.layout_principal.addLayout(self.dock_container)
        self.layout_principal.addLayout(self.rightLayout)
        
        # Menu bar
        menu_bar = self.menuBar()
        menu_fichier = menu_bar.addMenu("Fichier")
        menu_fichier.addAction('Ouvrir', self.ouvrir)
        menu_fichier.addAction('Ouvrir plan',self.ouvrir_plan)
        menu_action = menu_bar.addMenu("Action")
        menu_action.addAction('Analyser le parcours',self.analyseParcours)
        menu_action.addAction('Créer une liste de course aléatoire',self.course_aleatoire)
        menu_action.addAction('Suivant',self.definirPosition)

        
        # Docks
        self.dock = QDockWidget('Liste des articles')
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
        self.articles_listWidget = QTreeWidget()
        self.articles_listWidget.setHeaderLabel("Ajouter à la liste de courses")
        self.dock.setWidget(self.articles_listWidget)
        self.dock.setMaximumWidth(500)
        
        self.dock2 = QDockWidget('Liste de course')
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock2)
        self.liste_course = QTreeWidget()
        self.liste_course.setHeaderLabel("Votre liste de course")
        self.dock2.setWidget(self.liste_course)
        self.dock2.setMaximumWidth(500)
        
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
        self.ajout.clicked.connect(self.ajouter_article)
        self.supprimer.clicked.connect(self.supprimer_article)
        self.analyse.clicked.connect(self.analyseParcours)  # Corrected signal connection
        self.dico_create.clicked.connect(self.course_aleatoire)
        self.setpos.clicked.connect(self.definirPosition)

        # Define shortcuts
        self.shortcut_analyser = QShortcut(QKeySequence('a'), self)
        self.shortcut_analyser.activated.connect(self.analyseParcours)

        self.shortcut_continue = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        self.shortcut_continue.activated.connect(self.definirPosition)

        self.shortcut_create_random = QShortcut(QKeySequence('r'), self)
        self.shortcut_create_random.activated.connect(self.course_aleatoire)

        self.shortcut_add_product = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        self.shortcut_add_product.activated.connect(self.ajouter_article)

        self.shortcut_add_product = QShortcut(QKeySequence(Qt.Key.Key_Backspace), self)
        self.shortcut_add_product.activated.connect(self.supprimer_article)

    def ouvrir(self) -> str:
        """
        Opens a file dialog and emits the selected file path if a file is chosen.

        Returns:
            str: The selected file path if a file is chosen, otherwise None.
        """
        boite = QFileDialog.getOpenFileName(self, "Sélectionner un fichier", "", "Fichiers JSON (*.json)")
        if boite[0] != '':
            self.fnameOpen.emit(boite[0])

    def ouvrir_plan(self) -> str :
        boite = QFileDialog.getOpenFileName(self, "Sélectionner une image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)")
        if boite[0] != '':
            self.fnameOpen_bis.emit(boite[0])


    def afficherArticles(self, data):        
        """
        Display the articles in a QTreeWidget.

        Parameters:
            data (dict): A dictionary containing categories as keys and a list of products as values.

        Returns:
            None
        """
        for category, products in data.items():
            category_item = QTreeWidgetItem([category])
            self.articles_listWidget.addTopLevelItem(category_item)
            for product in products:
                product_item = QTreeWidgetItem([product])
                category_item.addChild(product_item)
                

    def ajouter_article(self):
        """
        Add the currently selected article to the list of courses.

        This function retrieves the currently selected item from the `articles_listWidget` and checks if it is not `None`.
        If an item is selected, it retrieves the text of the first column of the item and appends it to the `dico_courses` list. 
        Then, it creates a new `QTreeWidgetItem` with the product name and adds it to the `liste_course`.

        Parameters:
            self (object): The instance of the class.
        
        Returns:
            None
        """
        item = self.articles_listWidget.currentItem()
        if item and item.parent() is not None:
            product_name = item.text(0)
            self.ajoutClicked.emit(product_name)
        
    def supprimer_article(self):
        """
        Remove the currently selected article from the list of courses.

        This function retrieves the currently selected item from the `liste_course` QTreeWidget and checks if it is not `None`.
        If an item is selected, it retrieves the text of the first column of the item and removes it from the `dico_courses` list.
        Then, it searches for the item in the `liste_course` and removes it if found.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        item = self.liste_course.currentItem()
        if item:
            product_name = item.text(0)
            self.supprimerClicked.emit(product_name)
            
                
    def afficher_liste_course(self,liste):
        self.liste_course.clear()
        for product in liste:
            course_item = QTreeWidgetItem([product])
            self.liste_course.addTopLevelItem(course_item)

    def cocheCourse(self, liste, produits):
        self.liste_course.clear()
        for product in liste:
            found = False
            for i in range(self.grid.index + 1):
                print(product)
                print(produits)
                if product in produits[i]:
                    course_item = QTreeWidgetItem([product + " ✓"])
                    self.liste_course.addTopLevelItem(course_item)
                    found = True
                    break
            if not found:
                course_item = QTreeWidgetItem([product])
                self.liste_course.addTopLevelItem(course_item)


    def definirPosition(self):
        if self.grid.parcours and self.setpos.isVisible():
            self.indexClicked.emit()

    def analyseParcours(self):
        self.analyseClicked.emit()
    
    def set_parcours(self, liste_cases):
        self.parcours = liste_cases
        
    def set_produit(self, liste_cases):
        self.produit = liste_cases

    def get_parcours(self):
        return self.parcours
            
    def set_dico_articles(self, dico_articles):
        self.dico_articles = dico_articles

    def course_aleatoire(self):
        self.dicoAleatoireClicked.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dico_articles = {'Légumes': ['carotte', 'tomate', 'savon'], 'Produits laitiers': ['lait', 'fromage']}  
    parcours = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9),
                (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
                (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9),
                (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
                (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
                (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),]
    fenetre = VueProjet()
    fenetre.afficherArticles(dico_articles)
    fenetre.set_parcours(parcours)
    fenetre.grid.setParcours(parcours)
    fenetre.show()
    sys.exit(app.exec())