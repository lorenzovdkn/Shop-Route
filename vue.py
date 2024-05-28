import sys,time, grid
import json, os
from PyQt6.QtWidgets import QApplication, QWidget, QDialog, QScrollArea, QDateEdit, QGridLayout, QFormLayout, QMainWindow, QHBoxLayout, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, QFileDialog, QComboBox, QLabel, QListWidget, QInputDialog, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QDate
from PyQt6.QtGui import QPixmap, QFont, QColor, QIcon

class Case(QWidget):
    
    signalChangedCategory : pyqtSignal = pyqtSignal(str)
    
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
        
        self.layout1.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # signaux
        self.category_combo.currentIndexChanged.connect(self.categoryChanged)
        
    # Set the display of the current case
    def setCase(self, position : tuple):
        self.case_number.setText(f"{position[0]}, {position[1]}")
    
    def updateProductCategory(self, list_article: list):
        self.category_combo.addItems(list_article)
    
    def getCategory(self):
        return self.category_combo.currentText()
    
    # Send the new category
    def categoryChanged(self):
        self.signalChangedCategory.emit(self.category_combo.currentText())


class Contenu(QWidget):
    
    signalAddProduct = pyqtSignal()
    signalProduct = pyqtSignal(dict)
    signalDeleteProduct = pyqtSignal(str)
    signalEditProduct = pyqtSignal(list) 
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
        
    def addProduct(self, product_list_import : list, current_category : str):
        if current_category == 'aucune':
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une catégorie de case pour ajouter un produit.")
            return 
        
        product_list = product_list_import
        product, ok = QInputDialog.getItem(self, 'Ajouter un produit', 'Sélectionnez un produit:',product_list,0,False)        
        if ok and product:
            quantity, ok = QInputDialog.getInt(self, 'Ajouter un produit', f'Sélectionnez la quantité pour {product}:', 1, 1)
            if ok:
                item_text = f"{product} - Quantité: {quantity}"
                self.signalProduct.emit({product: [quantity, False]})
            
    def updateArticle(self, articles : dict | None) :
        self.productList.clear()
        if articles != None :
            for key, value in articles.items():
                item_text = f"{key} - Quantité : {value[0]}"
                self.productList.addItem(item_text)
    
    def removeProductClicked(self):
        selected_items = self.productList.selectedItems()
        
        if selected_items:
            item = selected_items[0]
            nameSelection = item.text()
            parts = nameSelection.split(' - ')
            nameArticle = parts[0]
            self.signalDeleteProduct.emit(nameArticle)

    def productClicked(self, item):
        item_text = item.text()
        product, quantity = item_text.split(" - Quantité : ")
        quantity = int(quantity)
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
        data_projet = project_data.get('data_projet', {}) # Extrait le sous-dictionnaire data_projet de project_data.
        
        name = data_projet.get('nom_projet', 'Inconnu')
        authors = data_projet.get('auteurs', 'Inconnu')
        store_name = data_projet.get('nom_magasin', 'Inconnu')
        creation_date = data_projet.get('date', 'Inconnu')

        return (f"Nom: {name}\n"
                f"Auteurs: {authors}\n"
                f"Magasin: {store_name}\n"
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
                project_button.clicked.connect(self.create_project_selected_callback(file_name))
                self.project_grid.addWidget(project_button, row, col)
                col += 1
                if col > 4:
                    col = 0
                    row += 1

        create_button = QPushButton('+')
        create_button.setFixedSize(100, 100)
        create_button.clicked.connect(self.create_project)
        self.project_grid.addWidget(create_button, row, col)
        
    def create_project_selected_callback(self, file_name):
        def callback():
            self.project_selected(file_name)
        return callback
    
    def create_project(self):
        dialog = CreateProjectDialog(self)
        if dialog.exec() == QDialog.accepted:
            name, authors, store_name, store_address, creation_date = dialog.get_project_details()
            self.signalCreateProject.emit(name, authors, store_name, store_address, creation_date)
            self.load_projects()
    
    def project_selected(self, project_name):
        saves_folder = "saves"
        file_path = os.path.join(saves_folder, project_name)
        print("chemin du fichier : ", file_path) # temp

        with open(file_path, 'r', encoding='utf-8') as file:
            project_data = json.load(file)

        dialog = ProjectDetailsDialog(project_data, self)
        ret = dialog.exec()

        if ret == QDialog.DialogCode.Accepted:
            print("accepted")
            self.signalOpenProject.emit(project_name)
        elif ret == QDialog.DialogCode.Rejected:
            print("rejected")
            self.signalDeleteProject.emit(project_name)
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
    signalOpenProject = pyqtSignal(str)
    signalCreateProject = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        menu_bar = self.menuBar()
        menu_fichier = menu_bar.addMenu("Fichier")
        
        self.central_widget = QWidget()
        # self.setCentralWidget(self.central_widget)
        self.mainLayout = QHBoxLayout(self.central_widget)
        self.leftLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)
        
        self.case_widget = Case()
        self.contenu_widget = Contenu()

        self.leftLayout.addWidget(self.case_widget)
        self.leftLayout.addWidget(self.contenu_widget)
        
        self.gridWidget = grid.GridWidget()
        self.mainLayout.addWidget(self.gridWidget)
        
        self.gridWidget.grid.positionSignal.connect(self.case_widget.setCase)
        self.gridWidget.grid.positionSignal.connect(self.contenu_widget.setCase)

        # Ajouter la barre de menu
        action_ouvrir = menu_fichier.addAction("Ouvrir")
        action_ouvrir.triggered.connect(self.open_project)

        self.load_window = LoadProjectWindow()
        self.load_window.signalOpenProject.connect(self.open_existing_project)
        self.load_window.signalCreateProject.connect(self.create_new_project)

        self.setCentralWidget(self.load_window)

    def open_project(self):
        self.load_window.show()

    def open_existing_project(self, project_name):
        self.signalOpenProject.emit(project_name)
        

    def create_new_project(self, name, authors, store_name, store_address, creation_date):
        self.load_window.hide()
        # Code pour créer un nouveau projet dans MainWindow
        # Ici vous pouvez créer le nouveau projet
        
        # Exemple :
        # creer_nouveau_projet(name, authors, store_name, store_address, creation_date)
        # self.grid.setPicture(...)
        # self.grid.drawGrid(...)
        
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
