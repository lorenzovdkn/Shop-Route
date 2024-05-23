import sys,time
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, QFileDialog, QComboBox, QLabel, QListWidget, QInputDialog, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont, QColor, QIcon

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
        self.width : int =  50
        self.height : int = 50
        self.offset : QPoint = QPoint(0,0)
        self.lastPos : QPoint = QPoint(0,0)
        self.dragging : bool = False
        self.locked : bool = False
        self.picture : str = "./plan11.jpg"
        self.grid : dict = {}
        
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
        
        position_dict = {(1,3): "red", (2,5): "blue", (6,9): "green"}
        
        for x in range(-1, width):
            for y in range(-1, height):
                rect : QGraphicsRectItem = QGraphicsRectItem(x*step + self.offset.x(), y*step + self.offset.y(), step, step)
                if((x,y) in [position for position in position_dict.keys()]):
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
                print(posX, posY)
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
                time.sleep(0.01)
        # Increase the size of the grid
        elif event.angleDelta().y() > 0 and not self.locked:
            if(self.gridStep < 50):
                event.ignore()
                self.gridStep = self.gridStep + 1
                self.drawGrid()
                time.sleep(0.01)
    
    def lockGrid(self):
        if(not self.locked):
            self.locked = True
            self.sizeSignal.emit(self.width, self.height)
            self.stepSignal.emit(self.gridStep)
            self.offsetSignal.emit((self.offset.x(), self.offset.y()))
        
class Case(QWidget):
    
    signalChangedCategory : pyqtSignal = pyqtSignal()
    
    def __init__(self):
        
        super().__init__()
        self.layout1 = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()
        self.layout4 = QHBoxLayout()

        self.setLayout(self.layout1)
        self.resize(800, 600) 
        
        self.titre = QLabel("Mode Edition de plan")
        self.titre_font = QFont()
        self.titre_font.setPointSize(30)
        self.titre.setFont(self.titre_font)

        self.case = QLabel("Case")
        self.case_font = QFont()
        self.case_font.setPointSize(20)
        self.case.setFont(self.case_font)

        self.type_case_label = QLabel("Type de case:")
        self.type_case_combo = QComboBox()
        self.type_case_combo.addItems(["publique", "privé"])
        
        self.category_label = QLabel("Catégorie de la case:")
        self.category_combo = QComboBox()
        
        position = (0, 0)
        self.case_number_label = QLabel("Numéro de la case:")
        self.case_number = QLineEdit(f"{position[0]}, {position[1]}")
        self.case_number.setReadOnly(True)
        
        # layouts
        self.layout1.addWidget(self.titre)
        self.layout1.addWidget(self.case)
        self.layout1.addLayout(self.layout2)
        self.layout1.addLayout(self.layout3)
        self.layout1.addLayout(self.layout4)
        self.layout2.addWidget(self.type_case_label)
        self.layout2.addWidget(self.type_case_combo)
        self.layout3.addWidget(self.category_label)
        self.layout3.addWidget(self.category_combo)
        self.layout4.addWidget(self.case_number_label)
        self.layout4.addSpacing(61)
        self.layout4.addWidget(self.case_number)
        
        # Alignement des layouts
        self.layout1.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # signaux
        self.category_combo.currentIndexChanged.connect(self.signalChangedCategory.emit)
        
    # Set the display of the current case
    def setCase(self, position : tuple):
        self.case_number.setText(f"{position[0]}, {position[1]}")
    
    def updateProductCategory(self, list_article: list):
        self.category_combo.addItems(list_article)
    
    def currentCategory(self):
        return self.category_combo.currentText()
    
    def currentCase(self):
        pass


class Contenu(QWidget):
    
    signalAddProduct = pyqtSignal()
    signalProduct = pyqtSignal(dict)
    signalDeleteProduct = pyqtSignal(str)
    signalEditProduct = pyqtSignal(list) # [nomDuProduit, Quantité]
    signalProductClick = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.layout1 = QVBoxLayout()
        self.setLayout(self.layout1)
        self.resize(800, 600) 
        self.case = None
        
        contenu = QLabel("Contenu :")
        self.productList = QListWidget()
        self.addButton = QPushButton('Ajouter un produit')
        self.removeButton = QPushButton('Supprimer un produit')
        
        self.layout1.addWidget(contenu)
        self.layout1.addWidget(self.productList)
        self.layout1.addWidget(self.addButton)
        self.layout1.addWidget(self.removeButton)
        
        self.productList.itemClicked.connect(self.productClicked)
        self.productList.itemDoubleClicked.connect(self.editProductDoubleClicked)
        self.addButton.clicked.connect(self.signalAddProduct.emit)
        self.removeButton.clicked.connect(self.removeProductClicked)
      
    def setCase(self, case : tuple):
        self.case = case
    
    def getCase(self):
        return self.case
        
    # Permet d'ajouter un produit dans la liste si une catégorie est choisie
    def addProduct(self, product_list_import : list, current_category : str):
        if current_category == 'aucune':
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une catégorie de case pour ajouter un produit.")
            return 
        
        product_list = product_list_import
        product, ok = QInputDialog.getItem(self, 'Ajouter un produit', 'Sélectionnez un produit:',product_list,0,False)        
        if ok and product:
            quantity, ok = QInputDialog.getInt(self, 'Ajouter un produit', 'Quantité:', 1, 1)
            if ok:
                item_text = f"{product} - Quantité: {quantity}"
                self.signalProduct.emit({product: [quantity, False]})
                
    # Permet de mettre à jour l'affichage de la liste des produits       
    def updateArticle(self, articles : dict | None) :
        self.productList.clear()
        if articles != None :
            for key, value in articles.items():
                item_text = f"{key} - Quantité : {value[0]}"
                self.productList.addItem(item_text)
    
    # Permet de supprimer un élement de la liste
    def removeProductClicked(self):
        selected_items = self.productList.selectedItems()
        
        if selected_items:
            item = selected_items[0]
            nameSelection = item.text()
            parts = nameSelection.split(' - ')
            nameArticle = parts[0]
            print(nameArticle)
            self.signalDeleteProduct.emit(nameArticle)

    def productClicked(self, item):
        item_text = item.text()
        product, quantity = item_text.split(" - Quantité : ")
        quantity = int(quantity)
        print({product : [quantity, False]})
        self.signalProductClick.emit({product : [quantity, False]})

        
    def editProductDoubleClicked(self, item):
        item_text = item.text()
        product, quantity = item_text.split(" - Quantité : ")
        
        new_quantity, ok = QInputDialog.getInt(self, 'Modifier un produit', f'Nouvelle quantité pour {product}:', int(quantity), 1)

        if ok:
            self.signalEditProduct.emit([product, new_quantity])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        menu_bar = self.menuBar()
        menu_fichier = menu_bar.addMenu("Fichier")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.mainLayout = QHBoxLayout(self.central_widget)
        self.leftLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)
        
         # Widget creation
        self.case_widget = Case()
        self.contenu_widget = Contenu()
        self.grid = Grid()
        
        self.bouton = QPushButton("Verrouiller", self)
        self.bouton.clicked.connect(self.grid.lockGrid)
        
        self.statusLabel = QLabel("Veuillez positionner la grille - Status : Non verrouillée")
       
        
        self.rightBottomLayout = QHBoxLayout()  
        self.rightBottomLayout.addWidget(self.statusLabel)
        self.rightBottomLayout.addStretch()
        self.rightBottomLayout.addWidget(self.bouton)
        self.rightBottomLayout.addSpacing(15)
        
        self.rightLayout = QVBoxLayout()
        self.rightLayout.addLayout(self.rightBottomLayout)
        self.rightLayout.addWidget(self.grid)
        self.mainLayout.addLayout(self.rightLayout)

        self.leftLayout.addWidget(self.case_widget)
        self.leftLayout.addWidget(self.contenu_widget)
        
        #self.mainLayout.addWidget(self.grid)
        
        # Signals definition
        self.grid.positionSignal.connect(self.case_widget.setCase)
        self.grid.positionSignal.connect(self.contenu_widget.setCase)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
