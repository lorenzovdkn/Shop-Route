from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QInputDialog, QMessageBox
from PyQt6.QtCore import pyqtSignal, QPoint, Qt

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

    def setCase(self, case: QPoint):
        self.case = (case.x(), case.y())

    def getCase(self):
        return self.case

    def addProduct(self, product_list_import: list, current_category: str):
        if current_category == 'aucune':
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une catégorie de case pour ajouter un produit.")
            return

        product_list = product_list_import
        product, ok = QInputDialog.getItem(self, 'Ajouter un produit', 'Sélectionner un produit', product_list, 0, False)
        if ok and product:
            self.signalProduct.emit({'case': self.case, 'nom': product})

    def addProductToList(self, name: str):
        self.productList.addItem(name)

    def productClicked(self, item):
        self.signalProductClick.emit({'case': self.case, 'nom': item.text()})

    def editProductDoubleClicked(self, item):
        product = item.text()
        edit_product, ok = QInputDialog.getText(self, 'Modifier un produit', 'Modifier le produit:', text=product)
        if ok and edit_product:
            self.signalEditProduct.emit([self.case, product, edit_product])

    def removeProductClicked(self):
        selected = self.productList.currentRow()
        if selected >= 0:
            product = self.productList.takeItem(selected).text()
            self.signalDeleteProduct.emit(product)

    def removeProduct(self, name: str):
        items = self.productList.findItems(name, Qt.MatchFlag.MatchExactly)
        for item in items:
            row = self.productList.row(item)
            self.productList.takeItem(row)
