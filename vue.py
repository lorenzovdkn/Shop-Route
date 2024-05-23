import sys
import json,os 
from PyQt6.QtWidgets import QApplication, QWidget, QDialog, QScrollArea, QDateEdit, QGridLayout, QFormLayout, QMainWindow, QHBoxLayout, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, QFileDialog, QComboBox, QLabel, QListWidget, QInputDialog, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QDate
from PyQt6.QtGui import QPixmap, QFont

class Grid(QGraphicsView):
    
    positionSignal : pyqtSignal = pyqtSignal(QPoint)
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
        self.picture : str = None
        
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
        
        self.offsetSignal.emit((self.offset.x(), self.offset.y()))
        
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
        #self.category_combo.currentIndexChanged.connect(self.signalChangedCategory.emit)
        
    # Set the display of the current case
    def setCase(self, position : QPoint):
        self.case_number.setText(f"{position.x()}, {position.y()}")
    
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
      
    def setCase(self, case : QPoint):
        self.case = (case.x(), case.y())
    
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
            
class ProjectDetailsDialog(QDialog):
    def __init__(self, project_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Projet")

        self.layout = QVBoxLayout(self)

        self.details_label = QLabel(self.format_project_details(project_data), self)
        self.layout.addWidget(self.details_label)

        self.buttons_layout = QHBoxLayout()

        self.open_button = QPushButton("Ouvrir", self)
        self.open_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.open_button)

        self.delete_button = QPushButton("Supprimer", self)
        self.delete_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.delete_button)

        self.cancel_button = QPushButton("Annuler", self)
        self.cancel_button.clicked.connect(self.close)
        self.buttons_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.buttons_layout)

    def format_project_details(self, project_data):
        name = project_data.get('Nom', 'Inconnu')
        authors = project_data.get('Auteurs', 'Inconnu')
        store_name = project_data.get('Magasin', 'Inconnu')
        store_address = project_data.get('Adresse', 'Inconnu')
        creation_date = project_data.get('Date', 'Inconnu')

        return (f"Nom: {name}\n"
                f"Auteurs: {authors}\n"
                f"Magasin: {store_name}\n"
                f"Adresse: {store_address}\n"
                f"Date: {creation_date}")
        
            
class LoadProjectWindow(QWidget):
    signalOpenProject = pyqtSignal(str)
    signalCreateProject = pyqtSignal(str, str, str, str, str)
    signalDeleteProject = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Charger ou Créer un Projet')
        self.layout = QVBoxLayout(self)

        self.title = QLabel("Sélectionner un projet ou en créer un nouveau")
        self.layout.addWidget(self.title)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.scroll_widget = QWidget()
        self.project_grid = QGridLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        
        self.load_projects()
        
    def load_projects(self):
        # Clear the grid layout
        for i in reversed(range(self.project_grid.count())): 
            widget_to_remove = self.project_grid.itemAt(i).widget()
            self.project_grid.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        saves_folder = "saves"
        if not os.path.exists(saves_folder):
            os.makedirs(saves_folder)
        
        row, col = 0, 0
        for file_name in os.listdir(saves_folder):
            if file_name.endswith(".json"):
                project_button = QPushButton(file_name)
                project_button.setFixedSize(100, 100)
                project_button.clicked.connect(lambda _, f=file_name: self.project_selected(f))
                self.project_grid.addWidget(project_button, row, col)
                col += 1
                if col > 4:
                    col = 0
                    row += 1

        # Add the create project button
        create_button = QPushButton('+')
        create_button.setFixedSize(100, 100)
        create_button.clicked.connect(self.create_project)
        self.project_grid.addWidget(create_button, row, col)
    
    def create_project(self):
        dialog = CreateProjectDialog(self)
        if dialog.exec() == QDialog.accepted:
            name, authors, store_name, store_address, creation_date = dialog.get_project_details()
            self.signalCreateProject.emit(name, authors, store_name, store_address, creation_date)
            self.load_projects()
    
    def project_selected(self, project_name):
        saves_folder = "saves"
        file_path = os.path.join(saves_folder, project_name)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            project_data = json.load(file)
        
        dialog = ProjectDetailsDialog(project_data, self)
        ret = dialog.exec()

        if ret == QDialog.accepted:
            self.signalOpenProject.emit(project_name)
        elif ret == QDialog.rejected:
            self.signalDeleteProject(project_name)
            self.load_projects()

class CreateProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Créer un Projet')
        self.layout = QVBoxLayout(self)
        
        self.form_layout = QFormLayout()
        
        self.name_input = QLineEdit(self)
        self.authors_input = QLineEdit(self)
        self.store_name_input = QLineEdit(self)
        self.store_address_input = QLineEdit(self)
        self.creation_date_input = QDateEdit(self)
        self.creation_date_input.setCalendarPopup(True)
        self.creation_date_input.setDate(QDate.currentDate())
        
        self.form_layout.addRow("Nom du projet:", self.name_input)
        self.form_layout.addRow("Auteurs:", self.authors_input)
        self.form_layout.addRow("Nom du magasin:", self.store_name_input)
        self.form_layout.addRow("Adresse du magasin:", self.store_address_input)
        self.form_layout.addRow("Date de création:", self.creation_date_input)
        
        self.layout.addLayout(self.form_layout)
        
        self.buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.clicked.connect(self.reject)
        
        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_layout.addWidget(self.cancel_button)
        
        self.layout.addLayout(self.buttons_layout)
    
    def get_project_details(self):
        name = self.name_input.text()
        authors = self.authors_input.text()
        store_name = self.store_name_input.text()
        store_address = self.store_address_input.text()
        creation_date = self.creation_date_input.date().toString('yyyy-MM-dd')
        return name, authors, store_name, store_address, creation_date
    
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

        self.leftLayout.addWidget(self.case_widget)
        self.leftLayout.addWidget(self.contenu_widget)
        
        self.mainLayout.addWidget(self.grid)
        
        # Signals definition
        self.grid.positionSignal.connect(self.case_widget.setCase)
        self.grid.positionSignal.connect(self.contenu_widget.setCase)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window2 = LoadProjectWindow()
    window2.show()
    window.show()
    sys.exit(app.exec())
