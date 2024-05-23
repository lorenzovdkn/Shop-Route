# -*- coding: utf-8 -*-
'''
:Titre : Module de classe Case(), Grille()
:Auteur : L. Conoir
:Date : 05/2020
'''
from filepile import File
import json

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
    
    def __init__(self, largeur: int, hauteur: int):
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
        f = File()
        f.enfiler(depart)
        dico = {depart: None}

        while not f.est_vide():
            current = f.defiler()
            if current == arrivee:
                chemin = []
                # Revenir en arrière depuis la destination jusqu'à la position de départ
                while current:
                    chemin.append(current)
                    self.setContenu(current,"X")
                    current = dico[current]
                chemin.reverse() # Inverser le chemin pour l'avoir de la position de départ à la destination
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


    def __init__(self,position,largeur,hauteur) -> None:
        self.position = position
        self.grille = Grille(largeur,hauteur)
        self.liste_course = ["savon","fromage"]
        self.information = {}
        self.lireJson("InformationApp.json")

    #Méthode pour lire les données d'un fichier JSON et les stocker dans l'objet
    def lireJson(self,fichier : str ):
        with open(fichier, 'r', encoding='utf-8') as f:
            self.information = json.load(f)

    #Definir la liste de course
    def setListeCourse(self,produit):
        if produit not in self.liste_course:
            self.liste_course.append(produit)

    #Supprime un produit dans la liste de course
    def deleteProduct(self,produit):
        if produit in self.liste_course:
            self.liste_course.remove(produit)

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
    
    #Calcule la distance entre 2 points
    def distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    #Liste des coordonées des produits du plus proche au plus loin de la position initial 
    def chemin_priorite(self) -> list:
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

    #TEST
    def definir_chemin(self): 
        chemin = self.chemin_priorite()
        for i in chemin:
            position = self.position
            self.grille.parcours_min(position,i)
            position = i
    
    # Definir toutes les coordonnées du chemin pour faire les courses
    def coordonneeChemin(self) -> list:
        chemin = self.chemin_priorite()
        liste = []
        for i in chemin:
            position = self.position
            liste.append(self.grille.parcours_min(position,i))
            position = i
        return liste
            

        

########### Exemple d'utilisation ######################################################################################
if __name__ == '__main__' :
    
    modele = Modele((0,0),8,8)
    print(modele.getArticle())
    print(modele.coordonneeChemin())
    modele.grille.afficheGrille()
    
    