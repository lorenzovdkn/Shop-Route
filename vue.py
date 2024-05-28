import sys,time, grid
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, QFileDialog, QComboBox, QLabel, QListWidget, QInputDialog, QPushButton, QLineEdit, QMessageBox, QSpinBox
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
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

        self.leftLayout.addWidget(self.case_widget)
        self.leftLayout.addWidget(self.contenu_widget)
        
        self.gridWidget = grid.GridWidget()
        self.mainLayout.addWidget(self.gridWidget)
        
        # Signals definition
        self.gridWidget.grid.positionSignal.connect(self.case_widget.setCase)
        self.gridWidget.grid.positionSignal.connect(self.contenu_widget.setCase)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
