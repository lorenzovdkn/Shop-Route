# -*- coding: utf-8 -*-
'''
:Titre : Module de classe Case(), Grille()
:Auteur : L. Conoir
:Date : 05/2020
'''
from filepile import File
import json
import random

class Case(object) :
    '''Classe définissant une case à partir de sa position : x, y.

Un objet, instance de cette classe, possède plusieurs méthodes :

    construireMur() : construit un mur de la case
    detruireMur() : détruit un mur de la case
    getContenu() : renvoie le contenu de la case
    setContenu() : affecte le contenu de la case
    getposition() : renvoie la position de la case
    getMurs() : renvoie la liste des murs de la case'''
    
    
    def __init__(self, x: int, y: int,lock : bool = False):
        '''Méthode dédiée, constructeur de la classe'''
        
        self.__position: tuple = x, y
        self.__est_vide: bool = True
        self.__contenu = None
        self.__locked = False
        


    def setContenu(self, cakechose: any) -> None:
        '''Méthode publique, affecte le contenu de l'objet.'''
        self.__contenu = cakechose


    def getContenu(self) -> any:
        '''Méthode publique, renvoie le contenu de l'objet.'''
        return self.__contenu


    def getPosition(self) -> tuple:
        '''Méthode publique, renvoie la position de l'objet : tuple (x, y)'''
        return self.__position

    def setLock(self,choice : bool) -> None:
        self.__locked = choice

    def isLocked(self):
        return self.__locked
        
       
class Grille(object) :
    '''Classe définissant une grille à partir de ses dimensions
           largeur : nombre de cases en largeur
           hauteur : nombre de cases en longueur

Un objet, instance de cette classe, possède plusieurs méthodes :

    construireBordure() : construit les murs sur le contour de la grille
    detruireBordure() : détruit les murs sur le contour de la grille
    afficheGrilleVide() : affiche la grille (sans contenu) avec tous les murs
    affichePlateau() : affiche le plateau (avec contenu et murs éventuels des cases)'''
    
    def __init__(self,largeur,hauteur):
        self.__largeur: int = largeur
        self.__hauteur: int = hauteur
        self.__cases: list = self.__creationGrille()
    
    def __creationGrille(self) -> list:
        '''Méthode privée, crée et renvoie la liste des cases'''
        liste_cases: list = []
        
        for y in range(self.__hauteur) :
            
            ligne_cases: list = []
        
            for x in range(self.__largeur) :
                nouvelle_case = Case(x, y)
                ligne_cases.append(nouvelle_case)
            
            liste_cases.append(ligne_cases)
        
        return liste_cases


    def getCases(self) -> list:
        '''Méthode publique, renvoie la liste des cases.'''
        return self.__cases


    def setContenu(self, position: tuple, cakechose: any) -> None:
        '''Méthode publique, affecte le contenu de la case à la position prévue.'''
        self.__cases[position[1]][position[0]].setContenu(cakechose)


    def getContenu(self, position: tuple) -> any:
        '''Méthode publique, renvoie le contenu de la case à la position prévue.'''
        return self.__cases[position[1]][position[0]].getContenu()

    def setLockGrid(self, position: tuple, choice: bool) -> None:
        self.__cases[position[1]][position[0]].setLock(choice)

    def effaceContenu(self) -> None:
        '''Méthode publique, efface le contenu de toutes les cases.'''
        for y in range(self.__hauteur):
            for x in range(self.__largeur):
                self.__cases[y][x].setContenu(None)
    
    def afficheGrille(self) -> None:
        '''Cette méthode affiche la grille et le contenu des cases'''
        for ligne in range(self.__hauteur):
            print('+---' * self.__largeur + '+')
            for colonne in range(self.__largeur):
                contenu: any = self.__cases[ligne][colonne].getContenu()
                if contenu is not None:
                    contenu = str(contenu)[0]
                else:
                    contenu = ' '
                print(f'| {contenu} ', end='')
            print('|')
        print('+---' * self.__largeur + '+\n')

    #Fait le parcours min entre un point de depart et son arrivée
    def parcours_min(self, depart: tuple, arrivee: tuple) -> list:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]       
        f = File(100)
        f.enfiler(depart)
        dico = {depart: None}
        while not f.est_vide():
            current = f.defiler()
            #On prend le produit si le client se situe en haut,à droite,à gauche,ou en bas
            if current == (arrivee[0]+1,arrivee[1]) or current == (arrivee[0]-1,arrivee[1]) or current == (arrivee[0],arrivee[1]+1) or current == (arrivee[0],arrivee[1]-1):
                chemin = []
                # Revenir en arrière depuis la destination jusqu'à la position de départ
                while current:
                    chemin.append(current)
                    self.setContenu(current,"X")
                    current = dico[current]
                chemin.reverse() # Inverser le chemin pour l'avoir de la position de départ à la destination
                print(f"Chemin trouvé : {chemin}")
                return chemin
            for direction in directions:
                next_case = (current[0] + direction[0], current[1] + direction[1])
                if 0 <= next_case[0] < self.__largeur and 0 <= next_case[1] < self.__hauteur:
                    case_obj = self.__cases[next_case[1]][next_case[0]]
                    # Si la prochaine position n'est pas verrouillée et n'a pas encore été visitée
                    if not case_obj.isLocked() and next_case not in dico:
                        f.enfiler(next_case)
                        dico[next_case] = current

        return None
    
class Modele(object):

    def __init__(self) -> None:
        self.information = {}
        self.position = ()
        self.grille = Grille(10,10)
        self.liste_course = []
        self.index = 0
        self.produit_coche = []
        

    #Méthode pour lire les données d'un fichier JSON et les stocker dans l'objet
    def lireJson(self,fichier : str ):
        with open(fichier, 'r', encoding='utf-8') as f:
            self.information = json.load(f)
        self.grille = Grille(self.setLargeur(),self.setHauteur())
    #Definir la liste de course
    def setListeCourse(self,produit):
        if produit not in self.liste_course:
            self.liste_course.append(produit)

    def plusUnIndex(self):
        self.index +=1

    def indexZero(self):
        self.index = 0

    def getIndex(self):
        return self.index
    #Supprime un produit dans la liste de course
    def deleteProduct(self,produit):
        if produit in self.liste_course:
            self.liste_course.remove(produit)

    def setLargeur(self):
        return self.information["grille"]["tailleGrille"][0]
    
    def setHauteur(self):
        return self.information["grille"]["tailleGrille"][1]

    #Retourne la liste de course
    def getListeCourse(self):
        return self.liste_course
    
    #Definir la position de départ 
    def setPosition(self,position):
        self.position = position

    def getPosition(self):
        return self.position
    
    def getCasesProducts(self):
        return self.information["cases"]
    
    def getPositions(self):
        listePos = []
        liste = self.getCasesProducts()
        for i in liste:
            listePos.append(i["position"])
        return listePos
    
    #Renvoie les articles du magasins sous formes de {'Légumes': ['carotte', 'tomate', 'savon'], 'Produits laitiers': ['lait', 'fromage']}
    def getArticle(self) -> dict:
        cases = self.getCasesProducts()
        dico_categorie = {}

        for case in cases:
            categorie = case['categorie']
            articles = case['articles']

            if categorie not in dico_categorie:
                dico_categorie[categorie] = []

            for article,(quantite,x) in articles.items():
                if quantite > 0:
                    dico_categorie[categorie].append(article)
    
        return dico_categorie
    
    def getArticlesList(self) -> list:
        cases = self.getCasesProducts()
        articles_list = []

        for case in cases:
            articles = case['articles']

            for article, (quantite, x) in articles.items():
                if quantite > 0:
                    articles_list.append(article)

        return articles_list
    
    #Calcule la distance entre 2 points
    def distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    #Liste des coordonées des produits du plus proche au plus loin de la position initial 
    def article_priorite(self) -> list:
        cases = self.getCasesProducts()
        def distance_case(case):
            return self.distance(self.position, case["position"])
        sorted_cases = sorted(cases,key=distance_case)
        produits_tries = []
        for case in sorted_cases:
            for produit, (quantite, x) in case["articles"].items():
                #Si le produit est dans la liste de course et que la quantite en stock est supérieur à 0 alors on peut ajouter dans le chemin
                if produit in self.liste_course and quantite > 0:
                    #On regroupe les produits si ils sont au même endroit
                    if tuple(case["position"]) not in produits_tries:
                        produits_tries.append(tuple(case["position"])) 
        return produits_tries 
    
    def trier_positions_par_distance_avec_chemin(self, position_donnee, liste_positions):
        chemins_avec_distances = []

        for position in liste_positions:
            chemin = self.grille.parcours_min(position_donnee, position)
            if chemin:
                chemins_avec_distances.append((position, len(chemin)))

        # Trier les chemins par longueur
        chemins_avec_distances.sort(key=lambda x: x[1])

        # Extraire les positions triées
        positions_triees = [position for position, distance in chemins_avec_distances]

        return positions_triees
                
                

    # Retourne toutes les coordonnées du chemin pour faire les courses et ensuite aller ) à la caisse 
    def coordonneeChemin(self) -> list:
        chemin = self.article_priorite()
        self.casesLock()
        liste = []
        position = self.position
        while chemin:
            chemin = self.trier_positions_par_distance_avec_chemin(position,chemin)
            element = chemin[0]
            final = self.grille.parcours_min(position, element)
            liste.append(final)
            position = final[-1]
            
            chemin_a_supprimer = []  # Liste temporaire pour les éléments à supprimer
            #Faire en sorte de supprimer la destination du produit si on est déjà passer devant en allant chercher un autre produit
            for destination in chemin:
                cells_to_check = [
                    (destination[0] - 1, destination[1]),
                    (destination[0] + 1, destination[1]),
                    (destination[0], destination[1] - 1),
                    (destination[0], destination[1] + 1)
                ]
                if any(cell in sublist for sublist in liste for cell in cells_to_check):
                    chemin_a_supprimer.append(destination)  # Ajouter à la liste de suppression
            produit_coche = []    
            for destination in chemin_a_supprimer:
                produit_coche.append(destination)
                chemin.remove(destination)  # Supprimer les éléments de la liste d'origine
            #determiner les produit à cocher en meme temps
            self.determineProduitCoche(produit_coche)

        if self.getCaisses():
            caisse = self.trier_positions_par_distance_avec_chemin(position,self.getCaisses())
            liste.append(self.grille.parcours_min(position,caisse[0]))
        return liste

    # Definir les cases que le client ne peut pas accéder
    def casesLock(self) -> list:
        cases = self.getCasesProducts()
        for case in cases:
            if case["statut"] == "Privé" or case["statut"] == "Publique":
                self.grille.setLockGrid(tuple(case["position"]),True)
            if case["statut"] == "Publique":
                self.grille.getCases()[case["position"][1]][case["position"][0]].setContenu("Produit")

    def getCasesLock(self):
        liste = []
        cases = self.getCasesProducts()
        for case in cases:
            if case["statut"] == "Privé":
                liste.append(case["position"])
        return liste
            
    def getAllCasesLock(self):
        liste = []
        cases = self.getCasesProducts()
        for case in cases:
            if case["statut"] == "Privé" or case["statut"] == "Publique":
                liste.append(case["position"])
        return liste

    def random_course(self):
        self.liste_course = []
        article_list = self.getArticlesList()
        if len(article_list) < 20:
            self.liste_course = article_list
        else:
            self.liste_course = random.sample(article_list, 20)

    def colorAttribution(self, coordonnee):
        article_list = self.getCasesProducts()
        for case in article_list:
            if list(coordonnee) == case["position"]:
                return case["couleur"]
        return None
    
    def getCaisses(self):
        liste = []
        article_list = self.getCasesProducts()
        for case in article_list:
            if case["categorie"] == "Caisse":
                liste.append(case["position"])
        return liste
    
    def determineProduitCoche(self,element):
        liste = []
        article_list = self.getCasesProducts()
        for case in article_list:
            if case["statut"] == "Publique":
                for position in element:
                    if list(position) == case["position"]:
                        for article,_ in case["articles"].items():
                            if article in self.liste_course:
                                liste.append(article)
        self.produit_coche.append(liste)

    def getEntree(self):
        liste = []
        article_list = self.getCasesProducts()
        for case in article_list:
            if case["categorie"] == "Entree":
                liste.append(case["position"])
        return liste

    def getProduitCoche(self):
        return self.produit_coche




########### Exemple d'utilisation ######################################################################################
if __name__ == '__main__' :
    modele = Modele()
    modele.grille.afficheGrille()