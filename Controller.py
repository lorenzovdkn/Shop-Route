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
        
        # Signaux Case
        self.view.case_widget.signalChangedCategory.connect(self.changedCategory)
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
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase((0, 0))) # besoin de mettre la case

        
    def add_article_modele(self, article : dict) -> None :
        # case = self.view.case_widget.
        self.model.ajouterArticle((0, 0), article) # besoin d'ajouter la case
        self.view.contenu_widget.updateArticle(article)
        
    def delete_article(self, articleName : str) -> None :
        self.model.supprimerArticle((0, 0), articleName) # manque la case
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase((0, 0))) # besoin de mettre la case
    
    def edit_product(self, productInfo : list) -> None :
        self.model.changerQuant((0, 0), productInfo[0], productInfo[1]) # besoin de mettre la case
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase((0, 0))) #  besoin de mettre la case

    def changedCategory(self):
        self.model.clearArticle((0, 0)) # besoin de mettre la case
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase((0, 0))) # besoin de mettre la case
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.view.show()
    sys.exit(app.exec())
    
