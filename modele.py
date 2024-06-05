import json, os

class Case:
    def __init__(self, position, articles, categorie, couleur, statut):
        self.position : tuple = position
        self.articles : dict = articles
        self.categorie : str = categorie
        self.couleur :str = couleur
        self.statut : bool = statut # False = public ; True = private
        if(articles is not {}):
            statut = False
        
    def setColor(self,color :str):
        ''' 
        Définir la couleur de la case.
        Paramètre:
        color (str): couleur à définir pour la case
        '''
        self.couleur = color 
        
    def getColor(self) -> str:
        ''' 
        Récupérer la couleur de la case
        Return:
        nom de la couleur en str
        '''
        return self.couleur
    
    def getPosition(self):
        ''' 
        Récupérer la position de la case 
        Return:
        tuple sous la forme (x,y)
        '''
        return self.position
    
    def setCategory(self, category : str) -> None:
        ''' 
        Définir la catégorie de la case.
        Paramètre:
        category (str) : nom de la catégorie à définir pour la case
        '''
        self.categorie = category
    
    def getCategory(self):
        ''' 
        Récupérer la catégorie de la case
        Return:
        nom de la catégorie de la case en str
        '''
        return self.categorie
    
    ''' '''
    def getListe(self) -> list:
        return [self.position, self.articles, self.categorie, self.couleur, self.statut]
    
    def getStatut(self) -> bool:
        return self.statut
      
    # Méthode à revoir
    def ajouterArticle(self, article):
        ''' 
        Ajouter un article dans la liste des articles de la case.
        Paramètre:
        article () : article à ajouter à la case
        '''
        self.articles.update(article)
        
    def getArticles(self) -> dict:
        ''' 
        Récupérer tous les articles de la case
        Return:
        dictionnaire contenant tous les articles de la case
        '''
        return self.articles
    
    def setArticles(self, articles : dict) -> None:
        ''' 
        Définir la liste des articles sur une liste donnée.
        Paramètre:
        articles (dict): articles à mettre dans la case
        '''
        self.articles = articles

    def __str__(self):
        ''' 
        Affichage écrit de la case
        '''
        articles_str = ', '.join([f"{key}: {value}" for key, value in self.articles.items()])
        return f"Position: {self.position}\nArticles: {articles_str}\nCatégorie: {self.categorie}\nCouleur: {self.couleur}\nStatut: {self.statut}"

        
class Grille:
    def __init__(self, image : str, tailleGrille : tuple, pasFloat : float , decalage : tuple, verrouiller : bool):
        self.image : str = image
        self.tailleGrille : tuple = tailleGrille
        self.pas : float = pasFloat
        self.decalage : tuple = decalage
        self.verrouiller : bool = verrouiller
    
    def setImage(self, image : str) -> None:
        ''' 
        Définir l'image qui va servir de plan.
        Paramètre:
        image (str) : Chemin vers l'image à définir
        '''
        self.image = image
    
    def getImage(self) -> str:
        ''' 
        Récupérer l'image qui sert de plan
        Return:
        chemin de l'image en str
        '''
        return self.image
    
    def setTailleGrille(self, taille : tuple) -> None:
        ''' 
        Définir la taille de la grille. 
        Paramètre:
        taille (tuple) : taille de la grille sous la forme (longueur,hauteur)
        '''
        self.tailleGrille = taille
        
    def getTailleGrille(self) -> tuple:
        ''' 
        Récupérer la taille de la grille
        Return:
        tuple sous la forme (longueur,hauteur)
        '''
        return self.tailleGrille
    
    def setVerrouiller(self, state : bool) -> None:
        ''' 
        Définir le statut de la grille. 
        Paramètre:
        state(bool) : pour verrouiller/déverouiller la grille
        '''
        self.verrouiller = state
    
    def setOffset(self, offset : tuple) -> None:
        print("setOffset function : ", offset)
        self.decalage = offset
        
    def setStep(self, step : int) -> None:
        self.pas = step
    
    def getDecalage(self) -> tuple:
        return self.decalage
    
    def getPas(self) -> float:
        return self.pas
        
    def setPas(self, pas : float) -> None:
        self.pas = pas
        
    def getVerrouiller(self) -> bool:
        ''' 
        Récupérer le statut de la grille. 
        Returns:
        - True = Verrouiller
        - False = Déverrouiller
        '''
        return self.verrouiller

class ModelMagasin:
    def __init__(self, jsonFile: (str | None) = None) -> None:
        # Attributs de la grille et des cases
        self.grille = Grille(None, (10, 20), 1.0, (2, 5), False)
        self.__listCase = [self.grille, []]
        self.currentCase : tuple = (0,0)
        self.category : str = None
        self.filepath : str = None
        self.categoryColors: dict = {
        'Légumes': '#228B22',           
        'Poissons': '#1E90FF',          
        'Viandes': '#FF4500',           
        'Épicerie': '#FFD700',          
        'Épicerie sucrée': '#FF69B4',   
        'Petit déjeuner': '#D2691E',   
        'Fruits': '#FF8C00',        
        'Rayon frais': '#ADD8E6',    
        'Crèmerie': '#FFFACD',        
        'Conserves': '#8B4513',       
        'Apéritifs': '#DB7093',      
        'Boissons': '#87CEFA',         
        'Articles Maison': '#B0E0E6',  
        'Hygiène': '#FFB6C1',          
        'Bureau': '#4682B4',           
        'Animaux': '#8A2BE2'            
    }
        # Informations sur le projet
        self.data_projet = {
            "nom_projet": "",
            "auteurs": "",
            "nom_magasin": "",
            "adresse_du_magasin": "",
            "date": ""  
            
        }
    
    
    def setCategory(self, category : str):
        ''' 
        Permet de définir la catégorie d'une case, change la couleur de la case en fonction de la 
        catégorie (mise en violet si la catégorie n'est pas reconnue).
        Si une case vient d'être mise sur "Aucune", la case est supprimée de la liste des cases.
        Créer une case si la case à la position donnée n'existe pas dans la liste des cases enregistrées.
        Paramètre:
        - category (str) : Nom de la catégorie à définir sur la case courante
        '''
        self.category = category
        positionList = self.getAllPosition()

        # Si la case n'existe pas
        if(self.currentCase not in positionList):
            color : str = ""
            if self.category in self.categoryColors:
                color = self.categoryColors[self.category]
            elif self.category != "Aucune":
                color = "purple"
            self.ajouterCase([self.currentCase, {}, self.category ,color , False])
        
        # Si la case existe
        else:
            for case in self.__listCase[1]:
                if case.getPosition() == self.currentCase:
                    if self.category == "Aucune":
                        self.supprimerCase()
                    else:
                        case.setCategory(category)
                        case.setColor(self.categoryColors[category])
                    break
    
    def setCurrentCase(self, position : tuple) -> None:
        ''' 
        Définit la case sélectionée par l'utilisateur. 
        Paramètre:
        position (tuple) : Position de la case courante sous la forme (x,y)
        '''
        self.currentCase = position
    
    def getCurrentCaseCategory(self) -> str:
        ''' 
        Récupérer la catégorie de la case sélectionnée.
        Paramètre:
        - categorie (str) de la case actuelle
        - "Aucune" si la case n'existe pas
        '''
        for case in self.__listCase[1]:
            if case.getPosition() == self.currentCase:
                return case.getCategory()
        return "Aucune"
    
    def setDataProject(self, projectName : str, authors : str, marketName : str, addressMarket :str, dateCreation : str) -> None:
        print("setdataproject :", projectName, authors, marketName, addressMarket, dateCreation)
        self.data_projet["nom_projet"] = projectName
        self.data_projet["auteurs"] = authors
        self.data_projet["nom_magasin"] = marketName
        self.data_projet["adresse_du_magasin"] = addressMarket
        self.data_projet["date"] = dateCreation
        
    def ajouterCase(self, case : list):
        self.__current: int = 0

    # Méthode à revoir
    def ajouterCase(self, case: list):
        ''' 
        Permet de créer une case. 
        '''
        caseAJoutee = Case(case[0], case[1], case[2], case[3], case[4])
        self.__listCase[1].append(caseAJoutee)

    def getAllPosition(self) -> list:
        '''
        Récupére toutes les positions des classes existantes.
        Returns:
        - liste de tuple sous la forme (x,y)
        '''
        positionList = []
        for case in self.__listCase[1]:
            positionList.append(case.getPosition())
        return positionList
    
     
    def ajouterArticle(self, articles: dict): 
        ''' 
        Permet d'ajouter un article dans une case. Vérifie si la case sélectionnée existe, ne fait rien si ce n'est pas le cas
        Paramètre:
        - articles (dict) : liste des articles sous la forme {"Article": Quantité}
        '''        
        for case in self.__listCase[1]:
            if case.getPosition() == self.currentCase:
                case.ajouterArticle(articles)
                break
    
    def supprimerCase(self):
        ''' 
        Permet de supprimer une case, ne fait rien si la case n'existe pas
        '''    
        for case in self.__listCase[1]:
            if case.getPosition() == self.currentCase:
                self.__listCase[1].remove(case)
                break
    
         
    def supprimerArticle(self, nom_article: str):
        ''' 
        Permet de retirer un article d'une case. Vérifie si la case sélectionnée existe et si l'article est présent dans la case,
        ne fait rien si ce n'est pas le cas
        Parametre:
        - nom_article (str) : Nom de l'article à retirer
        '''    
        for case in self.__listCase[1]:
            if case.getPosition() == self.currentCase:
                if nom_article in case.articles:
                    del case.articles[nom_article]
                    break
    
    def getProductsJson(self) -> dict:
        ''' 
        Permet de récupérer le dictionnaire des produits existants dans le fichier liste_produits.json
        '''
        with open('liste_produits.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        return self.data
    
    def getArticlesJson(self, nomCategory : str) -> list:
        ''' 
        Permet de récupérer la liste des produits d'une catégorie.
        Paramètre:
        - nomCategory (str): Nom de la catégorie voulue
        '''
        dict_product = self.getProductsJson()
        
        return dict_product[nomCategory]
    
    def getCategoryJson(self) -> list:
        ''' 
        Permet de récupérer la liste des catégories existantes.
        '''
        dict_product = self.getProductsJson()
        
        return dict_product.keys()
    
    def getArticlesCase(self) -> dict:
        ''' 
        Permet de récupérer la liste des articles de la case courante.
        Returns:
        - dictionnaire d'articles de la case sélectionnée (dict)
        - None si la case n'existe pas
        '''
        for case in self.__listCase[1]:
            if case.getPosition() == self.currentCase:
                return case.getArticles()
        return None
       
    def getUsedCase(self) -> dict:
        ''' 
        Renvoi un dictionnaire des cases existantes avec leur catégorie. 
        Returns:
        {(x,y): "catégorie"}
        '''
        caseList : dict = {} 
        for case in self.__listCase[1]:
            if(case.getCategory() != "Aucune"):
                caseList[case.getPosition()] = self.categoryColors[case.getCategory()]
        return caseList
    
    def getCase(self, position : tuple) -> Case :
        for case in self.__listCase[1]:
            if case.getPosition() == position:
                return case
            
    def getData(self) -> dict:
        return self.data_projet
           
    def getFilePath(self) -> str:
        return self.filepath
    
    def changerQuant(self, nomArticle : str, quantite: int) -> str | None:
        ''' 
        Permet de changer la quantité d'un article dans la case courante. Vérifie si la case existe, 
        si la quantité peut être modifiée ou que la quantité donnée ne soit pas négative.
        Paramètres:
        nomArticle (str): Nom de l'article à modifier dans la case
        quantite (int):  Quantité à définir
        Returns:
        Peut retourner un str avec un message
        '''            
        for case in self.__listCase[1]:
            if case.getPosition() == self.currentCase:
                if (case.getArticles()[nomArticle][1] == True ):
                    return ("Quantité verrouillée")
                elif (quantite > 0):
                    case.getArticles()[nomArticle][0] = quantite
                else :
                    return ("Quantité invalide")
        #return ("Case non définie")

    def clearArticle(self):
        ''' 
            Permet de vider la liste des articles de la case courante.
        '''
        for case in self.__listCase[1]:
            if case.getPosition() == self.currentCase:
                case.setArticles({})
                
    def load(self, filename: str):
        ''' 
            Permet de charger un fichier de sauvegarde.
            Paramètre: 
            filename (str): Chemin du fichier de sauvegarde
        '''
        self.filepath = filename
        print("load", filename)
        
        # Lire le fichier JSON
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Charger la grille
        grille_data = data["grille"]
        self.grille = Grille(
            grille_data["image"],
            tuple(grille_data["tailleGrille"]),
            grille_data["pas"],
            tuple(grille_data["decalage"]),
            grille_data["verrouiller"]
        )
        print("load function : ", tuple(grille_data["decalage"]))

        # Charger les cases
        self.__listCase[1] = []
        for case_data in data["cases"]:
            case = Case(
                tuple(case_data["position"]),
                case_data["articles"],
                case_data["categorie"],
                case_data["couleur"],
                case_data["statut"]
            )
            self.__listCase[1].append(case)

        # Charger les données du projet
        self.data_projet = data["data_projet"]


    def save(self, filename: str):
        ''' 
        Permet de sauvegarder le projet courant. 
        Paramètre: 
        filename (str): Chemin du fichier de sauvegarde
        '''
        # Vérifier si le dossier 'saves' existe, sinon le créer
        save_dir = 'saves'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Construire le chemin complet du fichier
        full_path = os.path.join(filename)
        self.filepath = full_path
        print("save : ", full_path)
        # Convertir la grille en dictionnaire
        grille_dict = {
            "image": self.grille.getImage(),
            "tailleGrille": self.grille.getTailleGrille(),
            "pas": self.grille.pas,
            "decalage": self.grille.decalage,
            "verrouiller": self.grille.getVerrouiller()
        }
        
        print("saving... offset :", self.grille.decalage)

        # Convertir les cases en liste de dictionnaires
        cases_dict = []
        for case in self.__listCase[1]:
            case_dict = {
                "position": case.getPosition(),
                "articles": case.getArticles(),
                "categorie": case.categorie,
                "couleur": case.getColor(),
                "statut": case.statut
            }
            cases_dict.append(case_dict)

        # Construire le dictionnaire final
        data = {
            "grille": grille_dict,
            "cases": cases_dict,
            "data_projet": self.data_projet
        }

        # Sauvegarder dans un fichier JSON
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


                
    def RemoveSave(self, filepath: str):
        """
        Removes the specified file if it exists.

        Parameters:
        filepath (str): The path to the file to be removed.

        Returns:
        str: A message indicating whether the file was successfully removed or if it didn't exist.
        """
        if os.path.exists(filepath):
            os.remove(filepath)
            return f"File '{filepath}' has been removed."
        else:
            return f"File '{filepath}' does not exist."
        
    def __str__(self):
        if not self.__listCase[1]:
            return "Aucune case dans le magasin."
        
        magasin_str = ""
        index = 1 
        for case in self.__listCase[1]:
            magasin_str += f"Case {index}:\n{case}\n\n"
            index += 1  
        
        return magasin_str.strip()
