import sys, time, grid
import json, os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QStackedLayout, QHBoxLayout,
    QVBoxLayout, QFileDialog, QComboBox, QLabel, QListWidget,
    QInputDialog, QPushButton, QLineEdit, QMessageBox, QToolBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QDir
from PyQt6.QtGui import QFont, QAction, QIcon
from selectProject import LoadProjectWindow

class Case(QWidget):
    # Définir des signaux personnalisés pour les changements de catégorie et de type
    signalChangedCategory: pyqtSignal = pyqtSignal(str)
    signalChangedType: pyqtSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        # Initialiser les layouts
        self.layout1 = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()
        self.layout4 = QHBoxLayout()

        self.setLayout(self.layout1)
        self.resize(800, 600) 
        
        # Définir le label du titre
        self.titre = QLabel("Mode Edition de plan")
        self.titre_font = QFont()
        self.titre_font.setPointSize(30)
        self.titre.setFont(self.titre_font)

        # Définir le label et la combo box pour le type de case
        self.type_case_label = QLabel("Type de case:")
        self.type_case_combo = QComboBox()
        self.type_case_combo.addItems(["Publique", "Privé"])
        
        # Définir le label et la combo box pour la catégorie de la case
        self.category_label = QLabel("Catégorie de la case:")
        self.category_combo = QComboBox()
        
        # Position par défaut de la case
        position = (0, 0)
        self.case_number_label = QLabel("Numéro de la case:")
        self.case_number = QLineEdit(f"{position[0]}, {position[1]}")
        self.case_number.setReadOnly(True)
        
        # Ajouter les widgets aux layouts
        self.layout1.addWidget(self.titre)
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
        
        # Initialiser le contrôleur de changement de catégorie
        self.controllerChangeCategory = False
        
        # Connecter les signaux aux méthodes correspondantes
        self.category_combo.currentIndexChanged.connect(self.categoryChanged)
        self.type_case_combo.currentIndexChanged.connect(self.typeChanged)
    
    def setCase(self, position: tuple):
        """
        Met à jour l'affichage de la case actuelle.
        
        :param position: La position de la case sous forme de tuple (x, y).
        """
        self.case_number.setText(f"{position[0]}, {position[1]}")
    
    def updateProductCategory(self, list_article: list):
        """
        Met à jour la liste des catégories de produits.
        
        :param list_article: Liste des articles à afficher dans la combo box.
        """
        self.category_combo.clear()
        self.category_combo.addItems(list_article)
    
    def getCategory(self):
        """
        Retourne la catégorie actuellement sélectionnée.
        """
        return self.category_combo.currentText()
    
    def setCategory(self, category: str):
        """
        Définit la catégorie sélectionnée.
        
        :param category: La catégorie à sélectionner.
        """
        if category is not None:
            self.controllerChangeCategory = True
            self.category_combo.setCurrentText(category)
            self.controllerChangeCategory = False
    
    def categoryChanged(self):
        """
        Méthode appelée lorsque la catégorie est changée.
        Émet un signal si le changement n'est pas contrôlé.
        """
        if not self.controllerChangeCategory:
            self.signalChangedCategory.emit(self.category_combo.currentText())
        
    def setType(self, type: str):
        """
        Définit le type de case sélectionné.
        
        :param type: Le type de case ("Privé" ou "Publique").
        """
        if type in ["Privé", "Publique"]:
            self.type_case_combo.setCurrentText(type)
    
    def locked(self, lock: bool):
        """
        Verrouille ou déverrouille les widgets de la case.
        
        :param lock: Booléen indiquant si la case est verrouillée.
        """
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
    # Définir des signaux personnalisés pour les interactions avec les produits
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
      
    def setCase(self, case: tuple):
        """
        Définir la case actuelle.
        
        :param case: Position de la case sous forme de tuple (x, y).
        """
        self.case = case
    
    def getCase(self):
        """
        Retourner la case actuelle.
        """
        return self.case
        
    def addProduct(self, product_list_import: list, current_category: str, current_state: str):
        """
        Ajouter un produit à la case actuelle.
        
        :param product_list_import: Liste des produits disponibles.
        :param current_category: Catégorie actuelle de la case.
        :param current_state: État actuel de la case ("Privé" ou "Publique").
        """
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
                self.signalProduct.emit({product: [quantity]})
            
    def updateArticle(self, articles: dict | None):
        """
        Mettre à jour la liste des articles affichés.
        
        :param articles: Dictionnaire des articles à afficher.
        """
        self.productList.clear()
        if articles != None :
            for key, value in articles.items():
                item_text = f"{key} - Quantité : {value[0]}"
                self.productList.addItem(item_text)
    
    def productClicked(self, item):
        """
        Méthode appelée lors du clic sur un produit.
        
        :param item: L'élément cliqué dans la liste des produits.
        """
        item_text = item.text()
        product, quantity = item_text.split(" - Quantité : ")
        quantity = int(quantity)
        self.signalProductClick.emit({product : [quantity, False]})
    
    def removeProductClicked(self):
        """
        Méthode appelée pour supprimer un produit sélectionné.
        """
        item = self.productList.currentItem()
        if item:
            product = item.text().split(' - ')[0]
            self.signalDeleteProduct.emit(product)
    
    def editProductDoubleClicked(self, item):
        """
        Méthode appelée lors du double-clic sur un produit pour le modifier.
        
        :param item: L'élément double-cliqué dans la liste des produits.
        """
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
        self.setWindowTitle("ShopRoute")
        
        # Appliquer le style à l'application
        self.setStyleSheet(open("AppCreation/styles/qssSelect.qss").read())
        
        self.central_widget = QWidget()
        self.temp_widget = QWidget()
        self.mainLayout = QHBoxLayout(self.central_widget)
        self.leftLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)
        
        # Création des widgets
        self.gridWidget = grid.GridWidget()
        self.case_widget = Case()
        self.contenu_widget = Contenu()
        self.load_window = LoadProjectWindow()

        # Ajouter les widgets à la mise en page
        self.leftLayout.addWidget(self.case_widget)
        self.leftLayout.addWidget(self.contenu_widget)
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.gridWidget, 2)
        
        self.centrallayout = QStackedLayout()
        self.centrallayout.addWidget(self.load_window)
        self.centrallayout.addWidget(self.mainWidget)
        self.central = QWidget()
        self.central.setLayout(self.centrallayout)
        
        # Connexion des signaux et des slots
        self.gridWidget.grid.positionSignal.connect(self.case_widget.setCase)
        self.gridWidget.grid.positionSignal.connect(self.contenu_widget.setCase)
        self.gridWidget.grid.lockedSignal.connect(self.case_widget.locked)

        # Ajouter la barre de menu
        self.load_window.signalOpenProject.connect(self.open_existing_project)
        self.setCentralWidget(self.central)
        
        """Initialise le menu de la fenêtre principale."""
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
        
        toolbar : QToolBar = QToolBar()
        toolbar.addAction(nouveau)
        toolbar.addAction(ouvrir)
        toolbar.addAction(save)
        toolbar.addSeparator()
        toolbar.addAction(changePicture)
        toolbar.addAction(lock)
        toolbar.addAction(unlock)
        
        self.addToolBar(toolbar)
    
    def switchWidget(self, widget: str):
        """Permet de changer de widget affiché.
        
        param: widget (str): Le nom du widget à afficher ('load_window' ou 'project_open').
        """
        if widget == "load_window":
            self.central.layout().setCurrentIndex(0)
        elif widget == "project_open":
            print("project_open")
            self.central.layout().setCurrentIndex(1)
                
    def open_project(self) -> LoadProjectWindow:
        """Affiche la fenêtre de sélection de projet."""
        self.load_window.show()

    def open_existing_project(self, project_name: str):
        """Ouvre un projet existant.
        
        param: project_name (str): Le nom du projet à ouvrir.
        """
        self.signalOpenProject.emit(project_name)
        
    def new(self):
        """Crée un nouveau projet."""
        self.load_window.create_project()
        self.load_window.signalCreateProject.connect(self.open_existing_project)
        
    def save(self):
        """Sauvegarde le projet actuel."""
        if self.central.layout().currentIndex() == 1:
            self.signalSave.emit(None)
        
    def saveas(self):
        """Sauvegarde le projet actuel sous un nouveau nom."""
        if self.central.layout().currentIndex() == 1:
            selected_directory = QFileDialog.getSaveFileName(self, "Enregistrer sous", "", "JSON Files (*.json)")
            if selected_directory[0] != '':
                self.signalSave.emit(selected_directory[0])
    
    def leave(self):
        """Quitte l'application après avoir demandé à l'utilisateur de sauvegarder."""
        if self.central.layout().currentIndex() == 1:
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
            else:
                return
        QApplication.quit()
        
    def changePicture(self):
        """Change l'image de fond de la grille."""
        if self.central.layout().currentIndex() == 1:
            file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner une image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)")
            if file_name:
                file_name = QDir().relativeFilePath(file_name)
                self.gridWidget.grid.setPicture(file_name)
                self.signalChangedPicture.emit(file_name)
        else:
            self.statusBar().showMessage("Impossible de modifier une image dans ce menu", 5000)
    
    def lock(self):
        """Verrouille la grille pour empêcher les modifications."""
        if(self.central.layout().currentIndex() == 1):
            if(not self.gridWidget.grid.isLocked()):
                self.gridWidget.lockGrid()
        else:
            self.statusBar().showMessage("Impossible de verrouiller la grille dans ce menu",5000)
    
    def unlock(self):
        """Déverrouille la grille pour permettre les modifications."""
        if(self.central.layout().currentIndex() == 1):
            if(self.gridWidget.grid.isLocked()):
                self.gridWidget.lockGrid()
        else:
            self.statusBar().showMessage("Impossible de déplacer la grille dans ce menu",5000)
    def closeEvent(self, event):
        """Gère l'événement de fermeture de la fenêtre."""
        if self.central.layout().currentIndex() == 1:
            event.ignore()
            self.leave() 

    def updateAllView(self, articles: dict, position: tuple, categories: list, status: bool, current_category: str, width: int, height: int, step: float, offset: tuple, lock: bool, position_dict: dict):
        """Met à jour toutes les vues avec les nouvelles données.
        
        param:
            articles (dict): Dictionnaire contenant les informations sur les articles.
            position (tuple): Tuple contenant la position actuelle.
            categories (list): Liste des catégories disponibles.
            status (bool): Statut actuel.
            current_category (str): Catégorie actuellement sélectionnée.
            width (int): Largeur de la grille.
            height (int): Hauteur de la grille.
            step (float): Taille des cases de la grille.
            offset (tuple): Décalage de la grille.
            lock (bool): Statut de verrouillage de la grille.
            position_dict (dict): Dictionnaire contenant les positions.
        """
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
