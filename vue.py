import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, QFileDialog, QComboBox, QLabel, QListWidget, QInputDialog, QPushButton
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont

class Grid(QGraphicsView):
    
    positionSignal : pyqtSignal = pyqtSignal(QPoint)
    lockedSignal : pyqtSignal = pyqtSignal(bool)
    sizeSignal : pyqtSignal = pyqtSignal(int,int)
    stepSignal : pyqtSignal = pyqtSignal(int)
    
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
        self.picture : str = None
        
        self.setPicture("./plan11.jpg")
        self.drawGrid()
        self.sceneWidth = self.scene.width()
        self.sceneHeight = self.scene.height()

    def getGridSize(self):
        self.sizeSignal.emit(self.width,self.height)
    
    def getGridStep(self):
        self.stepSignal.emit(self.gridStep)
        
    def isLocked(self):
        self.lockedSignal.emit(self.locked)

    def setPicture(self, picture : str):
        self.picture = picture
    # Draw the grid
    def drawGrid(self, width: int = None, height: int = None):
        
        if(width is None):
            width = self.width
        else:
            self.width = width
        if(height is None):
            height = self.height
        else:
            self.height = height
            
        self.scene.clear()
        if(self.picture != None):
            pixmap = QPixmap(self.picture)
            self.image_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.image_item)
        
        for x in range(-1, width):
            for y in range(-1, height):
                rect : QGraphicsRectItem = QGraphicsRectItem(x*self.gridStep + self.offset.x(), y*self.gridStep + self.offset.y(), self.gridStep, self.gridStep)
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
                self.positionSignal.emit(QPoint(posX, posY))
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
                self.gridStep = self.gridStep - 0.25
                self.drawGrid()
        # Increase the size of the grid
        elif event.angleDelta().y() > 0 and not self.locked:
            if(self.gridStep < 50):
                event.ignore()
                self.gridStep = self.gridStep + 0.25
                self.drawGrid()
        
class Case(QWidget):
    def __init__(self):
        super().__init__()
        self.layout1 = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()
        self.layout4 = QHBoxLayout()

        self.setLayout(self.layout1)
        self.resize(800, 600) 
        titre = QLabel("Mode Edition de plan")

        self.layout1.addWidget(titre)
        titre_font = QFont()
        titre_font.setPointSize(30)
        titre.setFont(titre_font)

        case = QLabel("Case")
        case_font = QFont()
        case_font.setPointSize(20)
        case.setFont(case_font)
        self.layout1.addWidget(case)
        self.layout1.addLayout(self.layout2)
        self.layout1.addLayout(self.layout3)
        type_case_label = QLabel("Type de case:")
        self.layout2.addWidget(type_case_label)
        self.type_case_combo = QComboBox()
        self.type_case_combo.addItems(["publique", "privé"])
        self.layout2.addWidget(self.type_case_combo)
        category_label = QLabel("Catégorie de la case:")
        self.layout3.addWidget(category_label)
        self.category_combo = QComboBox()
        self.layout3.addWidget(self.category_combo)
        # Alignement des layouts
        self.layout1.setAlignment(Qt.AlignmentFlag.AlignTop)

    def updateProductCategory(self, dico_article: dict):
        self.category_combo.addItems(dico_article.keys())
    
    def currentCategory(self):
        return self.category_combo.currentText()


class Contenu(QWidget):
    productSignal = pyqtSignal(dict)
    categorySignal = pyqtSignal(str)
    addProduct = pyqtSignal()
    supprimerProduct = pyqtSignal()
    productClickedSignal = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.layout1 = QVBoxLayout()
        self.setLayout(self.layout1)
        self.resize(800, 600) 
        contenu = QLabel("Contenu :")
        self.layout1.addWidget(contenu)
        self.productList = QListWidget()
        self.layout1.addWidget(self.productList)
        self.productList.itemClicked.connect(self.productClicked)
        self.addButton = QPushButton('Ajouter un produit')
        self.layout1.addWidget(self.addButton)
        self.addButton.clicked.connect(self.addProduct)
        self.removeButton = QPushButton('Supprimer un produit')
        self.layout1.addWidget(self.removeButton)
        self.removeButton.clicked.connect(self.removeProductClicked)
        self.editButton = QPushButton('Modifier un produit')
        self.layout1.addWidget(self.editButton)
        self.editButton.clicked.connect(self.editProductClicked)

    def addProduct(self):
        product_list = ["Produit A", "Produit B", "Produit C","Chaussure"]
        product, ok = QInputDialog.getItem(self, 'Ajouter un produit', 'Sélectionnez un produit:',product_list,0,False)        
        if ok and product:
            quantity, ok = QInputDialog.getInt(self, 'Ajouter un produit', 'Quantité:', 1, 1)
            if ok:
                item_text = f"{product} - Quantité: {quantity}"
                self.productList.addItem(item_text)
                self.productSignal.emit({product: [quantity, False]})
                

    def removeProduct(self,liste_product):
        for index in range(self.productList.count()):
            item = self.productList.item(index)
            liste = item.text().split((" - Quantité: "))
            liste[1] = int(liste[1])
            print(liste)
            if liste == liste_product  :
                self.productList.takeItem(index)
                break
    
    def removeProductClicked(self):
        self.supprimerProduct.emit()

    def productClicked(self, item):
        item_text = item.text()
        product, quantity = item_text.split(" - Quantité: ")
        quantity = int(quantity)
        print({product : [quantity, False]})
        self.productClickedSignal.emit({product : [quantity, False]})

    def editProductClicked(self):
        liste_product = {"Produit A": [1, False]}
        produit = list(liste_product.keys())[0]
        print(type(produit))  # This will print <class 'str'> since produit is a string

        new_quantity, ok = QInputDialog.getInt(self, 'Modifier un produit', f'Nouvelle quantité pour {produit}:', liste_product[produit][0], 1)

        if ok:
            for index in range(self.productList.count()):
                item = self.productList.item(index)
                print(item.text())
                if item.text().startswith(produit) and item.text().endswith(str(liste_product[produit][0])):                    
                    # Correctly emit the signal with the updated product details
                    print({produit: [new_quantity, False]})
                    self.productSignal.emit({produit: [new_quantity, False]})

                    item.setText(f"{produit} - Quantité: {new_quantity}")

                    break


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        menu_bar = self.menuBar()
        menu_fichier = menu_bar.addMenu("Fichier")
        menu_editer = menu_bar.addMenu("Editer")
        menu_consulter = menu_bar.addMenu("Consulter")
        menu_theme = menu_bar.addMenu("Themes")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.mainLayout = QHBoxLayout(self.central_widget)
        self.leftLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)
        
        self.case_widget = Case()
        self.contenu_widget = Contenu()
        self.grid = Grid()

        self.leftLayout.addWidget(self.case_widget)
        self.leftLayout.addWidget(self.contenu_widget)
        
        self.mainLayout.addWidget(self.grid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
