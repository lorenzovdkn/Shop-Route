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
        
    def getColor(self) -> str:
        return self.couleur
    
    def getPosition(self):
        return self.position
    
    def getListe(self) -> list:
        return [self.position, self.articles, self.categorie, self.couleur, self.statut]
    
    def getArticles(self) -> dict:
        return self.articles
    
    def ajouterArticle(self, article):
        self.articles.update(article)
        
    def setArticles(self, articles : dict) -> None:
        self.articles = articles
    
    def setCategory(self, category : str) -> None:
        self.categorie = category

    
    def __str__(self):
        articles_str = ', '.join([f"{key}: {value}" for key, value in self.articles.items()])
        return f"Position: {self.position}\nArticles: {articles_str}\nCatégorie: {self.categorie}\nCouleur: {self.couleur}\nStatut: {self.statut}"

        
class Grille:
    def __init__(self, image : str, tailleGrille : tuple, pasFloat : float, decalage : tuple, verrouiller : bool):
        self.image : str = image
        self.tailleGrille : tuple = tailleGrille
        self.pas : float = pasFloat
        self.decalage : tuple = decalage
        self.verouiller : bool = verrouiller
        
    def getImage(self) -> str:
        return self.image
    
    def getTailleGrille(self) -> tuple:
        return self.tailleGrille
    
    def getVerouiller(self) -> bool:
        return self.verouiller
    
    def setImage(self, image : str) -> None:
        self.image = image
        
    def setTailleGrille(self, taille : tuple) -> None:
        self.tailleGrille = taille
        
    def setVerouiller(self, state : bool) -> None:
        self.verouiller = state

class ModelMagasin:
    def __init__(self, jsonFile: (str | None) = None) -> None:
        # Attributs de la grille et des cases
        self.grille = Grille('/media/lorenzo/Disque secondaire/BUT-IUT/BUT1/SAE/SAE_C12/sae_C12/plan11.jpg', (10, 20), 1.0, (2, 5), False)
        self.__listCase = [self.grille, []]
        self.currentCase : tuple = (0,0)
        self.category : str = None
        self.categoryColors: dict = {
            'Légumes': 'green',
            'Poissons': 'blue',
            'Viandes': 'red',
            'Épicerie': 'yellow',
            'Épicerie sucrée': 'pink',
            'Petit déjeuner': 'brown',
            'Fruits': 'orange',
            'Rayon frais': 'white',
            'Crèmerie': 'white',
            'Conserves': 'black'
        }
        # Informations sur le projet
        self.data_projet = {
            "nom_projet": "Nom du projet",
            "auteurs": "",
            "nom_magasin": "Nom du magasin",
            "date": "2024-05-23"  # Exemple de date
        }
        
        # si un fichier est fourni : on charge 
        # if jsonFile: self.open(jsonFile)
    
    def setCategory(self, category : str) -> None:
        self.category = category
        for case in self.__listCase[1]:
            if case.getPosition() == self.currentCase:
                case.setCategory(category)
                break
    
    def setCurrentCase(self, position : tuple) -> None:
        self.currentCase = position
    
    def getCurrentCase(self) -> tuple:
        return self.currentCase
    
    def ajouterCase(self, case : list):
        self.__current: int = 0

    def ajouterCase(self, case: list):
        caseAJoutee = Case(case[0], case[1], case[2], case[3], case[4])
        self.__listCase[1].append(caseAJoutee)
        
    def getAllPosition(self) -> list:
        positionList = []
        for case in self.__listCase[1]:
            positionList.append(case.getPosition())
        return positionList
        
    def ajouterArticle(self, articles: dict):
        positionList = self.getAllPosition()
        if(self.currentCase not in positionList):
            color : str 
            if self.category in self.categoryColors:
                color = self.categoryColors[self.category]
            else:
                color = "purple"
            self.ajouterCase([self.currentCase, {}, None,color , False])
                
        for case in self.__listCase[1]:
            if case.getPosition() == self.currentCase:
                case.ajouterArticle(articles)
                break
            
    def supprimerCase(self):
        for case in self.__listCase[1]:
            if case.getPosition() == self.currentCase:
                self.__listCase[1].remove(case)
                break
    
    def supprimerArticle(self, nom_article: str):
        for case in self.__listCase[1]:
            if case.getPosition() == self.currentCase:
                if nom_article in case.articles:
                    del case.articles[nom_article]
                    break
    
    def nextArticle(self) -> int:
        self.__current = (self.__current + 1) % len(self.__listeCase[1])
        
    def PreviousArticle(self) -> int:
        self.__current = (self.__current - 1) % len(self.__listeCase[1])
        
    def setArticleIndex(self, index: int) -> None:
        self.__current = index
        
    def changerImage(self, image : str) -> None:
        self.grille.setImage(image)
    
    def getProductsJson(self) -> dict:
        with open('liste_produits.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        return self.data
    
    def getArticlesJson(self, nomCategory : str) -> list:
        dict_product = self.getProductsJson()
        
        return dict_product[nomCategory]
        
    def getCategoryJson(self) -> list:
        dict_product = self.getProductsJson()
        
        return dict_product.keys()
    
    def getArticlesCase(self) -> dict:
        for case in self.__listCase[1]:
            if case.getPosition() == self.currentCase:
                return case.getArticles()
    
    # Get all of the case who are not empty     
    def getUsedCase(self) -> dict:
        caseList : dict = {} 
        for case in self.__listCase[1]:
            caseList[case.getPosition()] = case.getColor()
        return caseList
            
    
    def changerQuant(self, nomArticle : str, quantite: int) -> str | None:
                    
        for case in self.__listCase[1]:
            if case.getPosition() == self.currentCase:
                if (case.getArticles()[nomArticle][1] == True ):
                    return ("Quantité verrouillée")
                elif (quantite > 0):
                    case.getArticles()[nomArticle][0] = quantite
                else :
                    return ("Quantité invalide")
        return ("Case non définie")
            
    def clearArticle(self) -> None:
        for case in self.__listCase[1]:
            if case.getPosition() == self.currentCase:
                case.setArticles({})
            
    def load(self, filename: str):
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

    def save(self, filename: str):
        # Convertir la grille en dictionnaire
        grille_dict = {
            "image": self.grille.getImage(),
            "tailleGrille": self.grille.getTailleGrille(),
            "pas": self.grille.pas,
            "decalage": self.grille.decalage,
            "verrouiller": self.grille.getVerouiller()
        }
        
        # Convertir les cases en liste de dictionnaires
        cases_dict = []
        for case in self.__listCase[1]:
            if case.getPosition() == self.currentCase:
                case.setArticles({})
                
    def RemoveSave(filepath: str):
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


if __name__ == '__main__':
    # Example instances
    position_vegetable = (2, 5)
    vegetable_articles = {'carotte': [8, False], 'tomate': [12, True]}
    vegetable_category = 'Légumes'
    vegetable_color = 'vert'
    vegetable_status = True

    vegetable_case = Case(position_vegetable, vegetable_articles, vegetable_category, vegetable_color, vegetable_status)

    position_dairy = (1, 3)
    dairy_articles = {'lait': [6, False], 'fromage': [15, True]}
    dairy_category = 'Produits laitiers'
    dairy_color = 'blanc'
    dairy_status = False

    dairy_case = Case(position_dairy, dairy_articles, dairy_category, dairy_color, dairy_status)

    position_hygiene = (0, 0)
    hygiene_articles = {'savon': [10, True], 'dentifrice': [8, True]}
    hygiene_category = 'Produits d\'hygiène'
    hygiene_color = 'bleu'
    hygiene_status = False

    ma_case = Case(position_vegetable, vegetable_articles, vegetable_category, vegetable_color, vegetable_status)
    ma_case2 = Case(position_dairy, dairy_articles, dairy_category, dairy_color, dairy_status)
    list_case = ma_case.getListe()
    list_case2 = ma_case2.getListe()
    print(list_case)
    magasin = ModelMagasin()
    
    magasin.ajouterCase(list_case)
    magasin.ajouterCase(list_case2)
    magasin.ajouterArticle(position_vegetable, hygiene_articles)
    
    print("test des classes : \n")
    print(ma_case)
    print("\n\n")
    print(magasin)
    
    magasin.supprimerArticle(position_vegetable, 'dentifrice')
    print(magasin)
    
    # Save the state of the store to a JSON file
    magasin.save('saves/etat_magasin.json')
    