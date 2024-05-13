class Case:
    def __init__(self, position, articles, categorie, couleur, statut):
        self.position = position
        self.articles = articles
        self.categorie = categorie
        self.couleur = couleur
        self.statut = statut
        
    def getposition(self):
        return self.position
        
class Grille:
    def __init__(self, image : str, tailleGrille : tuple, verrouiller : bool):
        self.image = image
        self.tailleGrille = tailleGrille
        self.verouiller = verrouiller

class ModelMagasin:
    def __init__(self, jsonFile : (str|None) = None) -> None:
        # attributs
        self.__listCase : list[Grille, list[Case]] = []
        self.__current : (tuple|None) = None
        
        # si un fichier est fourni : on charge 
        # if jsonFile: self.open(jsonFile)
        
    def ajouterCase(self, case : list):
        caseAJoutee = Case(case[0], case[1], case[2], case[3], case[4], case[5])
        self.__listCase[1].append(caseAJoutee)
        
    def ajouterArticle(self, positionCase : tuple, articles : dict):
        index = 0
        for position in self.__listCase[1].getposition():
            if position == positionCase:
                self.__listCase[1]
            index += 1
            
if __name__ == '__main__':
    # Exemple d'utilisation :
    position = (3, 4)
    articles = {'pomme': [5, False], 'banane': [10, True]}
    categorie = 'Fruits'
    couleur = 'rouge'
    statut = True

    ma_case = Case(position, articles, categorie, couleur, statut)

    # Accès aux attributs de la case
    print("Position:", ma_case.position)
    print("Articles:", ma_case.articles)
    print("Catégorie:", ma_case.categorie)
    print("Couleur:", ma_case.couleur)
    print("Statut:", ma_case.statut)
