import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout,QMainWindow
from PyQt6.QtWidgets import QPushButton,QFileDialog,QComboBox,QLabel,QListWidget,QInputDialog,QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
import json


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

    def updateProductCategory(self,dico_article : dict):
        self.category_combo.addItems(self.data.keys())
    
    def currentCategory(self):
        return self.category_combo.currentText()
    

class Contenu(QWidget):
    productSignal = pyqtSignal(dict)
    categorySignal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.layout1 = QVBoxLayout()
        self.setLayout(self.layout1)
        self.resize(800, 600) 
        contenu = QLabel("Contenu :")
        self.layout1.addWidget(contenu)
        self.productList = QListWidget()
        self.layout1.addWidget(self.productList)
        self.addButton = QPushButton('Ajouter un produit')
        self.layout1.addWidget(self.addButton)
        self.addButton.clicked.connect(self.sendCategory)
        self.removeButton = QPushButton('Supprimer un produit')
        self.layout1.addWidget(self.removeButton)
        self.removeButton.clicked.connect(self.removeProduct)
        self.editButton = QPushButton('Modifier un produit')
        self.layout1.addWidget(self.editButton)


    def sendCategory(self):
        category = Case.currentCategory
        self.categorySignal.emit(category)

    def addProduct(self,liste_produit : list):
        product, ok = QInputDialog.getItem(self, 'Ajouter un produit', 'Sélectionnez un produit:',liste_produit,0,False)        
        if ok and product:
            quantity, ok = QInputDialog.getInt(self, 'Ajouter un produit', 'Quantité:', 1, 1)
            if ok:
                self.productSignal.emit({product : [quantity,False]})
                

    def removeProduct(self):
        selectedItems = self.productList.selectedItems()
        if not selectedItems:
            QMessageBox.information(self, 'Erreur', 'Veuillez sélectionner un produit à supprimer.')
            return

        for item in selectedItems:
            self.productList.takeItem(self.productList.row(item))


        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    vue = Case() 
    vue.show()
    vue1 = Contenu()
    vue1.show()
    
    sys.exit(app.exec())
