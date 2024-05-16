import json

class Case:
    def __init__(self, position, articles, categorie, couleur, statut):
        self.position = position
        self.articles = articles
        self.categorie = categorie
        self.couleur = couleur
        self.statut = statut # False = public ; True = private
        
    def getposition(self):
        return self.position
    
    def getArticles(self) -> dict:
        return self.articles
    
    def getCategorie(self) -> str:
        return self.categorie
    
    def getCouleur(self) -> str:
        return self.couleur
    
    def getStatut(self) -> str:
        return self.statut
    
    def getListe(self) -> list:
        return [self.position, self.articles, self.categorie, self.couleur, self.statut]
    
    
    # setters
    def setposition(self, position : tuple):
        self.position = position
        
    def setArticles(self, articles : dict):
        self.articles = articles
        
    def setCategorie(self, categorie : str):
        self.categorie = categorie
        
    def setCouleur(self, couleur : str):
        self.couleur = couleur
        
    def setStatut(self, statut : str):
        self.statut = statut
    
    
    def __str__(self):
        articles_str = ', '.join([f"{key}: {value}" for key, value in self.articles.items()])
        return f"Position: {self.position}\nArticles: {articles_str}\nCatégorie: {self.categorie}\nCouleur: {self.couleur}\nStatut: {self.statut}"

        
class Grille:
    def __init__(self, image : str, tailleGrille : tuple, verrouiller : bool):
        self.image : str = image
        self.tailleGrille : tuple = tailleGrille
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
    def __init__(self, jsonFile : (str|None) = None) -> None:
        # attributs
        self.grille = Grille('/media/lorenzo/Disque secondaire/BUT-IUT/BUT1/SAE/SAE_C12/sae_C12/plan11.jpg', (10, 20), False)
        self.__listCase = [self.grille, []]
        self.__current : int = 0
        
        # si un fichier est fourni : on charge 
        # if jsonFile: self.open(jsonFile)
        
    def ajouterCase(self, case : list):
        caseAJoutee = Case(case[0], case[1], case[2], case[3], case[4])
        self.__listCase[1].append(caseAJoutee)
        
    def ajouterArticle(self, positionCase: tuple, articles: dict):
        for case in self.__listCase[1]:
            if case.getposition() == positionCase:
                case.ajouterArticle(articles)
                break
            
    def supprimerCase(self, positionCase: tuple):
        for case in self.__listCase[1]:
            if case.getposition() == positionCase:
                self.__listCase[1].remove(case)
                break
    
    def supprimerArticle(self, positionCase: tuple, nom_article: str):
        for case in self.__listCase[1]:
            if case.getposition() == positionCase:
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
        
    
    def __str__(self):
        listCases : list = []
        if self.__listCase[1]:
            for case in self.__listCase[1]:
                listCases.append(case.getListe())
        
        return str(listCases)
    
    def changerQuant(self, position : tuple, nomArticle : str, quantite: int) -> str | None:
        for case in self.__listCase[1]: 
            if case.getPosition() == position:
                if (case.getArticles()[nomArticle][1] == True ):
                    return ("Quantité verrouillée")
                elif (quantite > 0):
                    case.getArticles()[nomArticle][0] = quantite
                else : 
                    return ("Quantité invalide")
            else:
                return ("Article non trouvé")
        
    def changerVerrouillage(self, position : tuple, nomArticle : str) -> None:
        for case in self.__listCase[1]:
            if case.getPosition() == position:
                if (case.getArticles()[nomArticle][1] == False ):
                    case.getArticles()[nomArticle][1] = True
                else : 
                    case.getArticles()[nomArticle][1] = False
            else:
                return ("Article non trouvé")
            
    def modifierArticle(self, positionCase : tuple, nomArticle : str, quantite: (int|bool)) -> None:
            for case in self.__listCase[1]:
                if case.getPosition() == positionCase:
                    if isinstance(quantite, bool):
                        self.changerVerrouillage(positionCase, nomArticle)
                    else:
                        self.changerQuant(positionCase, nomArticle, quantite)  
                else:
                    return ("Article non trouvé")
 
             
            
if __name__ == '__main__':
    # Exemple 1 : Case de légumes
    position_vegetable = (2, 5)
    vegetable_articles = {'carotte': [8, False], 'tomate': [12, True]}
    vegetable_category = 'Légumes'
    vegetable_color = 'vert'
    vegetable_status = True

    vegetable_case = Case(position_vegetable, vegetable_articles, vegetable_category, vegetable_color, vegetable_status)

    # Exemple 2 : Case de produits laitiers
    position_dairy = (1, 3)
    dairy_articles = {'lait': [6, False], 'fromage': [15, True]}
    dairy_category = 'Produits laitiers'
    dairy_color = 'blanc'
    dairy_status = False

    dairy_case = Case(position_dairy, dairy_articles, dairy_category, dairy_color, dairy_status)

    # Exemple 3 : Case de produits d'hygiène
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
    magasin.modifierArticle((2,5), 'carotte', 18)

    magasin.modifierArticle((2,5), 'carotte', True)
    
    print('changement verrouillage : \n')
    print(ma_case)
    magasin.modifierArticle((2,5), 'carotte', 10)
    print(ma_case)
    
    print('changement verrouillage : \n')
    print(ma_case)
    magasin.modifierArticle((2,5), 'carotte', 10)
    print(ma_case)
    print("\n\n")
    print(magasin)
    
    magasin.supprimerArticle(position_vegetable, 'dentifrice')
    print(magasin)
    
