import sys,time, grid
import json, os
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow,QStackedLayout, QStackedWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QComboBox, QLabel, QListWidget, QInputDialog, QPushButton, QLineEdit, QMessageBox, QStatusBar
from PyQt6.QtCore import Qt, pyqtSignal, QDir
from PyQt6.QtGui import QFont, QAction, QIcon
from selectProject import LoadProjectWindow

class Case(QWidget):
    
    signalChangedCategory : pyqtSignal = pyqtSignal(str)
    signalChangedType : pyqtSignal = pyqtSignal(str)
    
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

        #self.case = QLabel("Case")
        #self.case_font = QFont()
        #self.case_font.setPointSize(20)
        #self.case.setFont(self.case_font)

        self.type_case_label = QLabel("Type de case:")
        self.type_case_combo = QComboBox()
        self.type_case_combo.addItems(["Publique", "Privé"])
        
        self.category_label = QLabel("Catégorie de la case:")
        self.category_combo = QComboBox()
        
        position = (0, 0)
        self.case_number_label = QLabel("Numéro de la case:")
        self.case_number = QLineEdit(f"{position[0]}, {position[1]}")
        self.case_number.setReadOnly(True)
        
        self.layout1.addWidget(self.titre)
        #self.layout1.addWidget(self.case)
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
        
        self.controllerChangeCategory = False
        
        # signaux
        self.category_combo.currentIndexChanged.connect(self.categoryChanged)
        self.type_case_combo.currentIndexChanged.connect(self.typeChanged)
        
    # Set the display of the current case
    def setCase(self, position : tuple):
        self.case_number.setText(f"{position[0]}, {position[1]}")
    
    def updateProductCategory(self, list_article: list):
        self.category_combo.clear()
        self.category_combo.addItems(list_article)
    
    def getCategory(self):
        return self.category_combo.currentText()
    
    def setCategory(self, category : str):
        if category != None:
            self.controllerChangeCategory = True
            self.category_combo.setCurrentText(category)
            self.controllerChangeCategory = False
    
    # Send the new category
    def categoryChanged(self):
        if not self.controllerChangeCategory:
            self.signalChangedCategory.emit(self.category_combo.currentText())
        
    def setType(self, type : str):
        if(type == "Privé" or type == "Publique"):
            self.type_case_combo.setCurrentText(type)
    
    def locked(self,lock: bool):
        if(lock):
            self.category_combo.setEnabled(True)
            self.type_case_combo.setEnabled(True)
        else:
            self.category_combo.setEnabled(False)
            self.type_case_combo.setEnabled(False)
    def typeChanged(self):
        self.signalChangedType.emit(self.type_case_combo.currentText())
        if(self.type_case_combo.currentText() == "Privé"):
            self.category_combo.setEnabled(False)
        else:
            self.category_combo.setEnabled(True)
            
    def updateCase(self, position: tuple, type_case: str, categories: list, current_category: str):
        """
        Actualise tous les widgets de cette classe avec les paramètres fournis.
        
        :param position: Position actuelle de la case sous forme de tuple (x, y).
        :param type_case: Type de la case sélectionné dans le combo box ("publique" ou "privé").
        :param categories: Liste des catégories disponibles.
        :param current_category: Catégorie actuelle sélectionnée.
        """
        # Mise à jour de la position de la case
        self.setCase(position)
        
        # Mise à jour du type de case
        index = type_case
        if index == False:
            self.type_case_combo.setCurrentIndex(0)
        elif index == True:
            self.type_case_combo.setCurrentIndex(1)
        
        # Mise à jour des catégories disponibles
        self.updateProductCategory(categories)
        
        # Mise à jour de la catégorie actuelle
        index = self.category_combo.findText(current_category)
        if index != -1:
            self.category_combo.setCurrentIndex(index)


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
        
    def addProduct(self, product_list_import : list, current_category : str, current_state :str):
        if  current_state == 'Privé':
            erreurState : QMessageBox = QMessageBox()
            erreurState.warning(self, "Erreur", "Cette case a été mise en privé, il est impossible d'y placer des articles")
            erreurState.setIcon(QMessageBox.Icon.Warning)
            
            return 
        elif current_category == 'Aucune':
            erreurCategory : QMessageBox = QMessageBox()
            erreurCategory.warning(self, "Erreur", "Veuillez sélectionner une catégorie de case pour ajouter un produit.")
            erreurCategory.setIcon(QMessageBox.Icon.Warning)
            return 
        elif current_category == 'Caisse' or current_category == 'Entrée':
            erreurCategory : QMessageBox = QMessageBox()
            erreurCategory.warning(self, "Erreur", "Une case qui a pour catégorie %s ne peut pas avoir d'article assigné" % current_category)  
            erreurCategory.setIcon(QMessageBox.Icon.Warning)
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

class MainWindow(QMainWindow):
    signalOpenProject = pyqtSignal(str)
    signalCreateProject = pyqtSignal()
    
    '''signals for the menu'''
    signalNew = pyqtSignal()
    signalSave = pyqtSignal(str)
    signalExport = pyqtSignal()
    signalOpen = pyqtSignal()
    signalChangedPicture = pyqtSignal(str)
    
    
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        
        self.setStyleSheet(open("styles/qssSelect.qss").read())
        
        self.central_widget = QWidget()
        self.temp_widget = QWidget()
        self.mainLayout = QHBoxLayout(self.central_widget)
        self.leftLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)
        
        
        # Widget creation
        self.gridWidget = grid.GridWidget()
        self.case_widget = Case()
        self.contenu_widget = Contenu()
        self.load_window = LoadProjectWindow()

        self.leftLayout.addWidget(self.case_widget)
        self.leftLayout.addWidget(self.contenu_widget)
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.gridWidget,2)
        
        self.centrallayout = QStackedLayout()
        self.centrallayout.addWidget(self.load_window)
        self.centrallayout.addWidget(self.mainWidget)
        self.central = QWidget()
        self.central.setLayout(self.centrallayout)
        
        self.gridWidget.grid.positionSignal.connect(self.case_widget.setCase)
        self.gridWidget.grid.positionSignal.connect(self.contenu_widget.setCase)
        self.gridWidget.grid.lockedSignal.connect(self.case_widget.locked)

        # Ajouter la barre de menu

        self.load_window.signalOpenProject.connect(self.open_existing_project)

        self.setCentralWidget(self.central)
        
        menu_bar = self.menuBar()
        
        # Menu fichier
        menu_fichier = menu_bar.addMenu("Fichier")
        nouveau = QAction('Nouveau',self)
        nouveau.setShortcut('Ctrl+N')
        nouveau.setIcon(self.style().standardIcon(QApplication.style().StandardPixmap.SP_FileIcon))
        nouveau.triggered.connect(self.new)
        menu_fichier.addAction(nouveau)
        ouvrir = QAction('Ouvrir',self)
        ouvrir.setShortcut('Ctrl+O')
        ouvrir.setIcon(self.style().standardIcon(QApplication.style().StandardPixmap.SP_DirIcon))
        ouvrir.triggered.connect(self.signalOpen)
        menu_fichier.addAction(ouvrir)
        menu_fichier.addSeparator()
        save = QAction('Enregistrer',self)
        save.setShortcut('Ctrl+S')
        save.setIcon(self.style().standardIcon(QApplication.style().StandardPixmap.SP_DialogSaveButton))
        save.triggered.connect(self.save)
        menu_fichier.addAction(save)
        save_as = QAction('Enregistrer sous',self)
        save_as.setShortcut('Ctrl+Shift+S')
        save_as.setIcon(self.style().standardIcon(QApplication.style().StandardPixmap.SP_DialogSaveButton))
        save_as.triggered.connect(self.saveas)
        menu_fichier.addAction(save_as)
        menu_fichier.addSeparator()
        leave = QAction('Quitter',self)
        leave.setIcon(self.style().standardIcon(QApplication.style().StandardPixmap.SP_DialogCloseButton))
        leave.triggered.connect(self.leave)
        menu_fichier.addAction(leave)
        
        # Menu édition
        menu_edition = menu_bar.addMenu("Edition")
        changePicture : QAction = QAction("Changer d'image",self)
        changePicture.setShortcut("Ctrl+Q")
        changePicture.setIcon(QIcon("./images/picture.png"))
        changePicture.triggered.connect(self.changePicture)
        menu_edition.addAction(changePicture)
        lock : QAction = QAction("Verrouiller la grille",self)
        lock.setShortcut("Ctrl+Shift+L")
        lock.setIcon(QIcon("./images/lock.png"))
        lock.triggered.connect(self.lock)
        menu_edition.addAction(lock)
        unlock : QAction = QAction("Déplacer la grille",self)
        unlock.setShortcut("Ctrl+Shift+U")
        unlock.setIcon(QIcon("./images/unlock.png"))
        unlock.triggered.connect(self.unlock)
        menu_edition.addAction(unlock)
    
    def switchWidget(self, widget : str):
        if widget == "load_window":
            self.central.layout().setCurrentIndex(0)
        elif widget == "project_open":
            print("project_open")
            self.central.layout().setCurrentIndex(1)
                
    def open_project(self) -> LoadProjectWindow:
        self.load_window.show()

    def open_existing_project(self, project_name):
        self.signalOpenProject.emit(project_name)
        
    '''methods for the menu'''
        
    def new(self):
        self.load_window.create_project()
        self.load_window.signalCreateProject.connect(self.open_existing_project)

        
    def save(self):
        self.signalSave.emit(None)
        
    def saveas(self):
        selected_directory : list = QFileDialog.getSaveFileName(self, "Enregistrer sous", "", "JSON Files (*.json)")
        if(selected_directory[0] != ''):
            self.signalSave.emit(selected_directory[0])
    
    def leave(self):
        if(self.load_window.isHidden()):
            warning_leave = QMessageBox()
            warning_leave.setWindowTitle("Enregistrer le document ?")
            warning_leave.setIcon(QMessageBox.Icon.Warning)
            warning_leave.setText("Enregistrer le projet avant la fermeture de l'application.")
            warning_leave.setStandardButtons(QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
            result = warning_leave.exec()
            
            if result == QMessageBox.StandardButton.Save:
                self.save()
                QApplication.exit()
            elif result == QMessageBox.StandardButton.Discard:
                QApplication.exit()
        QApplication.quit()
        
    def changePicture(self):
        if(self.central.layout().currentIndex() == 1):
            file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner une image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)")
            if file_name:
                file_name : str = QDir().relativeFilePath(file_name)
                self.gridWidget.grid.setPicture(file_name)
                self.signalChangedPicture.emit(file_name)
        else:
            self.statusBar().showMessage("Impossible de modifier une image dans ce menu")
    
    def lock(self):
        if(self.central.layout().currentIndex() == 1):
            if(not self.gridWidget.grid.isLocked()):
                self.gridWidget.lockGrid()
        else:
            self.statusBar().showMessage("Impossible de verrouiller la grille dans ce menu")
    
    def unlock(self):
        if(self.central.layout().currentIndex() == 1):
            if(self.gridWidget.grid.isLocked()):
                self.gridWidget.lockGrid()
        else:
            self.statusBar().showMessage("Impossible de déplacer la grille dans ce menu")
    
    def closeEvent(self, event):
        if(self.central.layout().currentIndex() == 1):
            event.ignore()
            self.leave() 

    def updateAllView(self, articles : dict, position : tuple, categories : list, status : bool, current_category : str, width : int , height : int, step : float, offset : tuple, lock : bool, position_dict : dict):
        self.gridWidget.widthEdit.setEnabled(True)
        self.gridWidget.heightEdit.setEnabled(True)
        self.gridWidget.grid.setGrid(width, height, step , offset , lock , position_dict)
        self.contenu_widget.updateArticle(articles)
        self.case_widget.updateCase(position, status, categories, current_category)
        self.gridWidget.updateSpinbox(width, height)
        self.case_widget.locked(lock)
        self.gridWidget.lockStateUpdate()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())