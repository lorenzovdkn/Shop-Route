import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
import vue
import modele

class Controller:
    def __init__(self):
        self.model = modele.ModelMagasin()
        self.view = vue.MainWindow()

        self.addCategory()
        
        # Signaux contenu
        self.view.contenu_widget.signalAddProduct.connect(self.add_article_selection)
        self.view.contenu_widget.signalProduct.connect(self.add_article_modele)
        self.view.contenu_widget.signalDeleteProduct.connect(self.delete_article)
        self.view.contenu_widget.signalEditProduct.connect(self.edit_product)
        
        # signals linked to the selecting projet
        self.view.load_window.signalOpenProject.connect(self.open_project)
        self.view.load_window.signalCreateProject.connect(self.open_new_project)
        self.view.load_window.signalCreateProject.connect(self.create_new_project)
        
        # Signals linked to the grid (view)
        #self.view.grid.lockedSignal.connect()
        self.view.gridWidget.grid.sizeSignal.connect(self.setGridSize)
        #self.view.grid.stepSignal.connect(self.setStep)
        #self.view.grid.offsetSignal.connect(self.setOffset)
        self.view.gridWidget.grid.positionSignal.connect(self.setClickedCase)
        
        # Signaux Case
        self.view.case_widget.signalChangedCategory.connect(self.changedCategory)
    
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
        self.view.gridWidget.grid.setPicture(picture)
    
    # Define the selected case    
    def setClickedCase(self, position : tuple):
        self.model.setCurrentCase(position)
        self.view.case_widget.setCategory(self.model.getCurrentCaseCategory())
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase())
        
    '''Define the grid methods'''
    # Load in the model the creating project and update the view
    def create_new_project(self, name, authors, store_name, store_address, creation_date, file_name) :  # name, authors, store_name, store_address, creation_date, file_name
        self.image_path = self.view.gridWidget.copyFileToAppDir(file_name)
        
        self.model.grille.setImage(self.image_path)
        self.model.setDataProject(name, authors, store_name, store_address, creation_date)
        self.model.save(str(name) + str(creation_date))
        
        self.view.load_window.hide()
        self.view.setCentralWidget(self.view.central_widget)
        
        imagePath = self.view.gridWidget.copyFileToAppDir(file_name)
        self.view.gridWidget.grid.setPicture(imagePath)
        
    
    '''Define the selecting project functions'''
    # Open the project and load the main window
    def open_project(self, filename):
        self.model.load(filename)
        self.view.load_window.hide()
        self.view.setCentralWidget(self.view.central_widget)
        
        width = self.model.grille.getTailleGrille()[0]
        print(width)
        height = self.model.grille.getTailleGrille()[1]
        step = self.model.grille.getPas()
        offset = self.model.grille.getDecalage()
        lock = self.model.grille.getVerouiller()
        positions : dict = self.model.getUsedCase()        
        
        self.view.gridWidget.grid.setPicture(self.model.grille.getImage()) # temporaire (il manque la mise à jour de la vue)
        self.view.updateAllView(self.model.getArticlesCase(), self.model.currentCase, self.model.getCategoryJson, self.model.getCase(self.model.currentCase).getStatut(), self.model.getCase(self.model.currentCase).getCategory(),
                                width, height, step, offset, lock, positions)
        
    def open_new_project(self, project):
        self.view.load_window.hide()
        self.view.setCentralWidget(self.view.central_widget)
        
        # manque la mise à jour de la vue
    
    def addCategory(self):
        list_category = ['Aucune'] + list(self.model.getCategoryJson())
        self.view.case_widget.updateProductCategory(list_category)
        
    def add_article_selection(self) -> None :
        category : str = self.view.case_widget.getCategory()
        if category != 'Aucune' :
            list_article = self.model.getArticlesJson(category)
        else:
            list_article = [] 
        self.view.contenu_widget.addProduct(list_article, category)
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase())

        
    def add_article_modele(self, article : dict) -> None :
        self.model.ajouterArticle(article)
        self.view.contenu_widget.updateArticle(article)
        self.view.gridWidget.grid.drawGrid(None,None,None,None,None,self.model.getUsedCase())
        
    def delete_article(self, articleName : str) -> None :
        self.model.supprimerArticle(articleName) # manque la case
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase())
    
    def edit_product(self, productInfo : list) -> None :
        self.model.changerQuant(productInfo[0], productInfo[1])
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase())

    def changedCategory(self, category : str) -> None :
        self.model.clearArticle()
        self.model.setCategory(category)
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase())
        usedCase = self.model.getUsedCase()
        self.view.gridWidget.grid.setGrid(None,None,None,None,None,self.model.getUsedCase())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.view.show()
    sys.exit(app.exec())
    
