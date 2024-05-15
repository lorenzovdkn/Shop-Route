class Case:
    def __init__(self, position, articles, categorie, couleur, statut):
        self.position = position
        self.articles = articles
        self.categorie = categorie
        self.couleur = couleur
        self.statut = statut
        
    def getposition(self):
        return self.position
    
    def getListe(self) -> list:
        return [self.position, self.articles, self.categorie, self.couleur, self.statut]
    
    def ajouterArticle(self, article):
        self.articles.update(article)

    
    def __str__(self):
        articles_str = ', '.join([f"{key}: {value}" for key, value in self.articles.items()])
        return f"Position: {self.position}\nArticles: {articles_str}\nCatégorie: {self.categorie}\nCouleur: {self.couleur}\nStatut: {self.statut}"

        
class Grille:
    def __init__(self, image : str, tailleGrille : tuple, verrouiller : bool):
        self.image = image
        self.tailleGrille = tailleGrille
        self.verouiller = verrouiller

class ModelMagasin:
    def __init__(self, jsonFile : (str|None) = None) -> None:
        # attributs
        self.__listCase = [Grille, []]
        self.__current : (tuple|None) = None
        
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
    print("\n\n")
    print(magasin)
    
    magasin.supprimerArticle(position_vegetable, 'dentifrice')
    print(magasin)
