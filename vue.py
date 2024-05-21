import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QMainWindow
from PyQt6.QtWidgets import QPushButton, QFileDialog, QComboBox, QLabel, QListWidget, QInputDialog, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

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
    addSignal = pyqtSignal()
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
                self.productSignal.emit({product: [quantity, False]})
                

    def removeProduct(self,liste_product):
        for index in range(self.productList.count()):
            item = self.productList.item(index)
            liste = item.text().split((" - Quantité: "))
            liste[1] = int(liste[1])
            if liste == liste_product :
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
        new_quantity, ok = QInputDialog.getInt(self, 'Modifier un produit', f'Nouvelle quantité pour {produit}:', liste_product[produit][0], 1)

        if ok:
            for index in range(self.productList.count()):
                item = self.productList.item(index)
                print(item.text())
                if item.text().startswith(produit) and item.text().endswith(str(liste_product[produit][0])):                    
                    print({produit: [new_quantity, False]})
                    self.productSignal.emit({produit: [new_quantity, False]})

                    item.setText(f"{produit} - Quantité: {new_quantity}")

                    break


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout1 = QVBoxLayout(self.central_widget)

        self.case_widget = Case()
        self.contenu_widget = Contenu()

        self.layout1.addWidget(self.case_widget)
        self.layout1.addWidget(self.contenu_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
