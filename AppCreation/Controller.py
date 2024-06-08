import sys
from PyQt6.QtWidgets import QApplication
import vue
import modele

class Controller:
    def __init__(self):
        self.model = modele.ModelMagasin()
        self.view = vue.MainWindow()
        
        ############# SIGNAUX #############
        
        # Signaux contenu
        self.view.contenu_widget.signalAddProduct.connect(self.add_article_selection)
        self.view.contenu_widget.signalProduct.connect(self.add_article_modele)
        self.view.contenu_widget.signalDeleteProduct.connect(self.delete_article)
        self.view.contenu_widget.signalEditProduct.connect(self.edit_product)
        
        # signals linked to the selecting projet
        self.view.load_window.signalOpenProject.connect(self.open_project)
        self.view.load_window.signalCreateProject.connect(self.open_new_project)
        self.view.load_window.signalCreateProject.connect(self.create_new_project)
        self.view.signalCreateProject.connect(self.create_new_project)
        self.view.load_window.signalDeleteProject.connect(self.delete_project)
        
        # Signals linked to the grid (view)
        self.view.gridWidget.grid.sizeSignal.connect(self.setGridSize)
        self.view.gridWidget.grid.stepSignal.connect(self.setStep)
        self.view.gridWidget.grid.offsetSignal.connect(self.setOffset)
        self.view.gridWidget.grid.positionSignal.connect(self.setClickedCase)
        
        # Signaux Case
        self.view.case_widget.signalChangedCategory.connect(self.changedCategory)
        self.view.case_widget.signalChangedType.connect(self.changedType)
        
        # Signaux menu
        self.view.signalOpen.connect(self.openMenu)
        self.view.signalSave.connect(self.saveMenu)
        self.view.signalChangedPicture.connect(self.setPicture)
    
    
    ############# SET METHODS #############
    
    def setGridSize(self, width : int , height : int):
        '''
        Définir la taille de la grille
        @param width (int) : longueur de la grille
        @param height (int) : hauteur de la grille
        '''
        size = (width, height)
        self.model.grille.setTailleGrille(size)
    
    def setStep(self, step : float):
        '''
        Définir la taille des cases
        @param step (float) : taille d'une case
        '''
        self.model.grille.setPas(step)
    
    def setOffset(self, offset : tuple):
        '''
        Définir le décalage de la grille
        @param offset (tuple(int,int)) : position x et y du coin en haut à gauche de la grille 
        '''
        self.model.grille.setOffset(offset)
        self.model.grille.setVerrouiller(True)
    
    def setPicture(self, picture : str):
        '''
        Définir le plan en fond 
        @param picture (str) : chemin vers l'image
        '''
        self.model.grille.setImage(picture)
        self.view.gridWidget.grid.setPicture(picture)
    
    def setClickedCase(self, position : tuple):
        '''
        Mettre à jour la vue lorsqu'on clique sur une case
        @param position (tuple(int,int)) : position de la case sélectionnée
        '''
        self.model.setCurrentCase(position)
        self.view.case_widget.setType(self.model.getCurrentCaseStatut())
        self.view.case_widget.setCategory(self.model.getCurrentCaseCategory())
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase())

    def updateAllView(self):
        '''
        Permet de mettre à jour la vue avec les informations du modèle
        '''
        width = self.model.grille.getTailleGrille()[0]
        height = self.model.grille.getTailleGrille()[1]
        step = self.model.grille.getPas()
        offset = self.model.grille.getDecalage()
        lock = self.model.grille.getVerrouiller()
        positions : dict = self.model.getUsedCase()        
        
        self.view.gridWidget.grid.setPicture(self.model.grille.getImage())
        self.view.updateAllView(self.model.getArticlesCase(), self.model.currentCase, self.model.getCategoryJson(), None, None,
                               width, height, step, offset, lock, positions)
    
    
    ############# MANAGING PROJECT METHODS #############
        
    def create_new_project(self, name, authors, store_name, store_address, creation_date, file_name) :
        '''
        Charge le nouveau projet dans la vue et la met à jour
        @param name (str) : le nom du projet
        @param authors (str) : le nom de l'auteur
        @param store_name (str) : le nom du magasin
        @param store_address (str) : l'adresse du magasin
        @param creation_date (str) : la date de création du magasin
        @param file_name (str) : le chemin vers le plan
        '''
        self.image_path = self.view.gridWidget.copyFileToAppDir(file_name)
        
        self.setPicture(self.image_path)
        self.model.setDataProject(name, authors, store_name, store_address, creation_date)
        self.model.save("./saves/" + str(name) + str(creation_date))
        
        self.view.switchWidget("project_open")
        imagePath = self.view.gridWidget.copyFileToAppDir(file_name)
        self.view.gridWidget.grid.setPicture(imagePath)
        self.updateAllView()
        
    def open_project(self, filename):
        '''
        Ouvre le projet et le charge dans la fenetre 
        @param filename (str) : chemin vers le fichier à ouvrir
        '''
        self.model.load(filename)
        self.view.switchWidget("project_open")
        self.view.showMaximized()
        
        width = self.model.grille.getTailleGrille()[0]
        height = self.model.grille.getTailleGrille()[1]
        step = self.model.grille.getPas()
        offset = self.model.grille.getDecalage()
        lock = self.model.grille.getVerrouiller()
        positions : dict = self.model.getUsedCase()        
        
        self.view.gridWidget.grid.setPicture(self.model.grille.getImage()) # temporaire (il manque la mise à jour de la vue)
        self.view.updateAllView(self.model.getArticlesCase(), self.model.currentCase, self.model.getCategoryJson(), None, None,
                               width, height, step, offset, lock, positions)
 
    def open_new_project(self):
        '''
        Permet d'ouvrir un nouveau projet
        '''
        self.view.switchWidget("project_open")
        self.updateAllView()

    def delete_project(self, project):
        '''
        Permet de supprimer un projet
        @param project (str) : chemin vers le projet
        '''
        self.model.RemoveSave(str(project))
    
    ############# MENUBAR METHODS #############
        
    def openMenu(self):
        '''
        Permet d'afficher la fênetre d'ouverture des projets
        '''
        self.view.showNormal()
        self.view.switchWidget("load_window")
        
    def saveMenu(self, file_path):
        '''
        Permet de sauvegarder des projets.
        @param file_path (str) : chemin vers la sauvegarde du projet. 
            La valeur peut être nulle, dans ce cas la valeur prise est celle stockée dans le modèle
        '''
        if(file_path == '' or file_path == None):
            file_path = self.model.getFilePath()
            self.model.save(file_path)
        self.model.save(file_path)
    
    
    ############# EDITING CASE METHODS #############

    def addCategory(self):
        '''
        Récupère toutes les catégories de case existantes pour les mettres dans la ComboBox de catégorie de case
        '''
        list_category = ['Aucune','Caisse','Entrée'] + list(self.model.getCategoryJson())
        self.view.case_widget.updateProductCategory(list_category)
        
    def add_article_selection(self) -> None :
        
        '''
        Permet à l'utilisateur d'ajouter une article de la catégorie de la case
        '''
        
        category : str = self.view.case_widget.getCategory()
        if category != 'Aucune' and category != 'Caisse' and category != 'Entrée':
            list_article = self.model.getArticlesJson(category)
        else:
            list_article = [] 
        self.view.contenu_widget.addProduct(list_article, category, self.model.getCurrentCaseStatut())
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase())

        
    def add_article_modele(self, article : dict) -> None :
        '''
        Permet d'ajouter des articles au modele dans la case sélectionné 
        @param article (dict) : articles à ajouter ("nom_article": quantité)
        '''
        self.model.ajouterArticle(article)
        self.view.contenu_widget.updateArticle(article)
        self.view.gridWidget.grid.drawGrid(self.model.getUsedCase())
        
    def delete_article(self, articleName : str) -> None :
        '''
        Permet de supprimer un article de la case sélectionnée
        @param articleName (str) : nom de l'article à supprimer
        '''
        self.model.supprimerArticle(articleName)
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase())
    
    def edit_product(self, productInfo : list) -> None :
        '''
        Permet de changer la quantité d'un article dans une case
        @param productInfo (tuple): liste contenant le nom de l'article et la nouvelle quantité
        '''
        self.model.changerQuant(productInfo[0], productInfo[1])
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase())

    def changedCategory(self, category : str) -> None :
        '''
        Met à jour la case lorsqu'on change sa catégorie
        @param category (str) : nom de la nouvelle categorie
        '''
        self.model.clearArticle()
        self.model.setCategory(category)
        self.view.contenu_widget.updateArticle(self.model.getArticlesCase())
        self.view.gridWidget.grid.drawGrid(self.model.getUsedCase())
    
    def changedType(self, statut : bool) -> None :
        '''
        Permet de définir le statut d'une case
        @param statut (boolean) : nouveau statut de la case sélectionné, true : privée, false : publique
        '''
        self.model.lockCase(statut)
        self.view.case_widget.setCategory(self.model.getCurrentCaseCategory())
        self.view.gridWidget.grid.drawGrid(self.model.getUsedCase())
        
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.view.show()
    sys.exit(app.exec())
    