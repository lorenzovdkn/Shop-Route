# -*- coding: utf-8 -*-
'''
:Titre : Module de classe Case(), Grille()
:Auteur : L. Conoir
:Date : 05/2020
'''
from filepile import File

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
        


##########################################################################################       
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

    def parcours_min(self, depart: tuple, arrivee: tuple) -> list:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]       
        f = File()
        f.enfiler(depart)
        dico = {depart: None}

        while not f.est_vide():
            current = f.defiler()
            if current == arrivee:
                chemin = []
                while current:
                    chemin.append(current)
                    current = dico[current]
                chemin.reverse()
                return chemin

            for direction in directions:
                next_case = (current[0] + direction[0], current[1] + direction[1])
                if 0 <= next_case[0] < self.__largeur and 0 <= next_case[1] < self.__hauteur:
                    case_obj = self.__cases[next_case[1]][next_case[0]]
                    if not case_obj.isLocked() and next_case not in dico:
                        f.enfiler(next_case)
                        dico[next_case] = current
            

        return None



########### Exemple d'utilisation ######################################################################################
if __name__ == '__main__' :
    
    laby = Grille(8,8)
    print('Grille de dimensions 8 x 8 avec bordure (par défaut) :')
    print(laby.afficheGrille())
    