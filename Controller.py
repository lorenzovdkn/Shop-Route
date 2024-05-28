import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import pyqtSlot

import vue
import modele

class Controller:
    def __init__(self):
        self.model = modele.ModelMagasin()
        self.view = vue.MainWindow()

        # Exemple 3 : Case de produits d'hygiène
        position_hygiene = (0, 0)
        hygiene_articles = {'savon': [10, True], 'dentifrice': [8, True]}
        hygiene_category = 'Produits d\'hygiène'
        hygiene_color = 'bleu'
        hygiene_status = False
        
        self.model.ajouterCase([position_hygiene, hygiene_articles, hygiene_category, hygiene_color, hygiene_status])
        # self.view.case_widget.type_case_combo.currentTextChanged.connect(self.on_type_case_changed)
        # self.view.contenu_widget.addButton.clicked.connect(self.on_add_product)
        # self.view.contenu_widget.removeButton.clicked.connect(self.on_remove_product)
        # self.view.contenu_widget.editButton.clicked.connect(self.on_edit_product)
        # self.view.contenu_widget.productClickedSignal.connect(self.on_product_clicked)
        
        self.addCategory()
        
        # Signaux contenu
        self.view.contenu_widget.signalAddProduct.connect(self.add_article_selection)
        self.view.contenu_widget.signalProduct.connect(self.add_article_modele)
        self.view.contenu_widget.signalDeleteProduct.connect(self.delete_article)
        self.view.contenu_widget.signalEditProduct.connect(self.edit_product)
        
        # signals linked to the selecting projet
        self.view.load_window.signalOpenProject.connect(self.open_project)
        
        # Signals linked to the grid (view)
        #self.view.grid.lockedSignal.connect()
        self.view.grid.sizeSignal.connect(self.setGridSize)
        #self.view.grid.stepSignal.connect(self.setStep)
        #self.view.grid.offsetSignal.connect(self.setOffset)
        
        # Signaux Case
        #self.view.case_widget.signalChangedCategory.connect(self.changedCategory)
    
    # Define the size of the grid    
    def setGridSize(self, size : tuple):
        self.model.grille.setTailleGrille(size)
    
    # Define the size of each case
    def setStep(self, step : float):
        self.model.grille.setStep(step)
    
    # Define the offset of the grid
    def setOffset(self, offset : tuple):
        self.model.grille.setOffset(offset)
    
    # Define the picture
    def setPicture(self, picture : str):
        self.model.grille.setPicture(picture)
        self.view.grid.setPicture(picture)
    
    '''Define the selecting project functions'''
    # Open the project and load the main window
    def open_project(self):
        print("hey got there [controller]")
        self.view.load_window.hide()
        self.view.setCentralWidget(self.view.central_widget)
    
    def addCategory(self):
        list_category = ['aucune'] + list(self.model.getCategoryJson())
        self.view.case_widget.updateProductCategory(list_category)
        
    def add_article_selection(self) -> None :
        category : str = self.view.case_widget.currentCategory()
        if category != 'aucune' :
            list_article = self.model.getArticlesJson(category)
        else:
            list_article = [] 
        self.view.contenu_widget.addProduct(list_article, category)
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase(self.view.contenu_widget.getCase())) # besoin de mettre la case

        
    def add_article_modele(self, article : dict) -> None :
        # case = self.view.case_widget.
        self.model.ajouterArticle(self.view.contenu_widget.getCase(), article) # besoin d'ajouter la case
        self.view.contenu_widget.updateArticle(article)
        
    def delete_article(self, articleName : str) -> None :
        self.model.supprimerArticle(self.view.contenu_widget.getCase(), articleName) # manque la case
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase(self.view.contenu_widget.getCase())) # besoin de mettre la case
    
    def edit_product(self, productInfo : list) -> None :
        self.model.changerQuant(self.view.contenu_widget.getCase(), productInfo[0], productInfo[1]) # besoin de mettre la case
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase(self.view.contenu_widget.getCase())) #  besoin de mettre la case

    def changedCategory(self):
        self.model.clearArticle(self.view.contenu_widget.getCase()) # besoin de mettre la case
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase(self.view.contenu_widget.getCase())) # besoin de mettre la case
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.view.show()
    sys.exit(app.exec())
    
