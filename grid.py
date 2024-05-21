# -*- coding: utf-8 -*-
'''
:Titre : Module de classe Case(), Grille()
:Auteur : L. Conoir
:Date : 05/2020
'''

class Case(object) :
    '''Classe définissant une case à partir de sa position : x, y.

Un objet, instance de cette classe, possède plusieurs méthodes :

    construireMur() : construit un mur de la case
    detruireMur() : détruit un mur de la case
    getContenu() : renvoie le contenu de la case
    setContenu() : affecte le contenu de la case
    getposition() : renvoie la position de la case
    getMurs() : renvoie la liste des murs de la case'''
    
    
    def __init__(self, x: int, y: int):
        '''Méthode dédiée, constructeur de la classe'''
        
        self.__position: tuple = x, y
        self.__est_vide: bool = True
        self.__contenu = None
        self.__murs: list = ['N', 'S', 'E', 'W']


    def construireMur(self, mur: str) -> None:
        '''Méthode publique, construit un mur de l'objet.'''
        if mur not in self.__murs :
            self.__murs.append(mur)


    def detruireMur(self, mur: str) -> None:
        '''Méthode publique, détruit un mur de l'objet.'''
        if mur in self.__murs :
            self.__murs.remove(mur)


    def setContenu(self, cakechose: any) -> None:
        '''Méthode publique, affecte le contenu de l'objet.'''
        self.__contenu = cakechose


    def getContenu(self) -> any:
        '''Méthode publique, renvoie le contenu de l'objet.'''
        return self.__contenu


    def getPosition(self) -> tuple:
        '''Méthode publique, renvoie la position de l'objet : tuple (x, y)'''
        return self.__position


    def getMurs(self) -> list:
        '''Méthode publique, renvoie la liste des murs.'''
        return self.__murs


    def __setMurs(self) -> None:
        '''Méthode privée, construit les 4 murs de l'objet.'''
        self.__murs = ['N', 'S', 'W', 'E']



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


    def effaceContenu(self) -> None:
        '''Méthode publique, efface le contenu de toutes les cases.'''
        for y in range(self.__hauteur):
            for x in range(self.__largeur):
                self.__cases[y][x].setContenu(None)


    def construireAvecGraphe(self, graphe: dict) -> None:
        '''Méthode publique, définit les murs à partir d'un graphe.'''
        for case, voisines in graphe.items():
            x1, y1 = case

            for case_voisine in voisines:
                
                x2, y2 = case_voisine

                if y1 == y2 :
                    if x1 < x2 :
                        self.__cases[y1][x1].detruireMur('E')
                    else: 
                        self.__cases[y1][x1].detruireMur('W')
                else :
                    if y1 < y2 :
                        self.__cases[y1][x1].detruireMur('S')
                    else: 
                        self.__cases[y1][x1].detruireMur('N')


    def construireBordure(self) -> None:
        '''Méthode publique, définit une bordure extérieure de la grille.'''
        for colonne in range(self.__largeur) :
            self.__cases[0][colonne].construireMur('N')
            self.__cases[self.__hauteur - 1][colonne].construireMur('S')
        
        for ligne in range(self.__hauteur) :
            self.__cases[ligne][0].construireMur('W')
            self.__cases[ligne][self.__largeur - 1].construireMur('E')
    
    
    def detruireBordure(self) -> None:
        '''Méthode publique, enlève une bordure extérieure de la grille.'''
        for colonne in range(self.__largeur) :
            self.__cases[0][colonne].detruireMur('N')
            self.__cases[self.__hauteur - 1][colonne].detruireMur('S')
        
        for ligne in range(self.__hauteur) :
            self.__cases[ligne][0].detruireMur('W')
            self.__cases[ligne][self.__largeur - 1].detruireMur('E')
    
    
    def afficheGrilleVide(self) -> None:
        '''Méthode publique, affiche la grille vide avec tous les murs.'''                                
        for ligne in range(self.__hauteur) :
            print('+---' * self.__largeur + '+')
            print('|   ' * self.__largeur + '|')
            
        print('+---' * self.__largeur + '+\n')


    def __str__(self) :
        '''Méthode dédiée, affiche la grille avec son contenu et les murs existants.'''
        affichage: str = ''
        
        for ligne in range(self.__hauteur) :
        
            affiche_ligne1: str = ''
            affiche_ligne2: str = ''
        
            for colonne in range(self.__largeur) :
            
                liste_murs: list = self.__cases[ligne][colonne].getMurs()
                
                if 'N' in liste_murs :
                    affiche_ligne1 = affiche_ligne1 + '+---'
                else :
                    affiche_ligne1 = affiche_ligne1 + '+   '
                
                contenu: any = self.__cases[ligne][colonne].getContenu()
                
                if contenu != None :
                    contenu = str(contenu)[0]
                else :
                    contenu = ' '
                
                if 'W' in liste_murs :
                    affiche_ligne2 = affiche_ligne2 + '| ' + contenu + ' '
                else :
                    affiche_ligne2 = affiche_ligne2 + '  ' + contenu + ' '

            if 'E' in liste_murs :
                affiche_ligne2 = affiche_ligne2 + '|'
            
            affichage = affichage + affiche_ligne1 + '+\n' + affiche_ligne2 + '\n'
            
        affiche_ligne1 = ''
            
        for colonne in range(self.__largeur) :
            
            liste_murs = self.__cases[self.__hauteur - 1][colonne].getMurs()
                
            if 'S' in liste_murs :
                affiche_ligne1 = affiche_ligne1 + '+---'
            else :
                affiche_ligne1 = affiche_ligne1 + '+   '
                
        affichage = affichage + affiche_ligne1 + '+\n'
        
        return affichage


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


    def effaceContenu(self) -> None:
        '''Méthode publique, efface le contenu de toutes les cases.'''
        for y in range(self.__hauteur):
            for x in range(self.__largeur):
                self.__cases[y][x].setContenu(None)


    def construireAvecGraphe(self, graphe: dict) -> None:
        '''Méthode publique, définit les murs à partir d'un graphe.'''
        for case, voisines in graphe.items():
            x1, y1 = case

            for case_voisine in voisines:
                
                x2, y2 = case_voisine

                if y1 == y2 :
                    if x1 < x2 :
                        self.__cases[y1][x1].detruireMur('E')
                    else: 
                        self.__cases[y1][x1].detruireMur('W')
                else :
                    if y1 < y2 :
                        self.__cases[y1][x1].detruireMur('S')
                    else: 
                        self.__cases[y1][x1].detruireMur('N')


    def construireBordure(self) -> None:
        '''Méthode publique, définit une bordure extérieure de la grille.'''
        for colonne in range(self.__largeur) :
            self.__cases[0][colonne].construireMur('N')
            self.__cases[self.__hauteur - 1][colonne].construireMur('S')
        
        for ligne in range(self.__hauteur) :
            self.__cases[ligne][0].construireMur('W')
            self.__cases[ligne][self.__largeur - 1].construireMur('E')
    
    
    def detruireBordure(self) -> None:
        '''Méthode publique, enlève une bordure extérieure de la grille.'''
        for colonne in range(self.__largeur) :
            self.__cases[0][colonne].detruireMur('N')
            self.__cases[self.__hauteur - 1][colonne].detruireMur('S')
        
        for ligne in range(self.__hauteur) :
            self.__cases[ligne][0].detruireMur('W')
            self.__cases[ligne][self.__largeur - 1].detruireMur('E')
    
    
    def afficheGrilleVide(self) -> None:
        '''Méthode publique, affiche la grille vide avec tous les murs.'''                                
        for ligne in range(self.__hauteur) :
            print('+---' * self.__largeur + '+')
            print('|   ' * self.__largeur + '|')
            
        print('+---' * self.__largeur + '+\n')


    def __str__(self) :
        '''Méthode dédiée, affiche la grille avec son contenu et les murs existants.'''
        affichage: str = ''
        
        for ligne in range(self.__hauteur) :
        
            affiche_ligne1: str = ''
            affiche_ligne2: str = ''
        
            for colonne in range(self.__largeur) :
            
                liste_murs: list = self.__cases[ligne][colonne].getMurs()
                
                if 'N' in liste_murs :
                    affiche_ligne1 = affiche_ligne1 + '+---'
                else :
                    affiche_ligne1 = affiche_ligne1 + '+   '
                
                contenu: any = self.__cases[ligne][colonne].getContenu()
                
                if contenu != None :
                    contenu = str(contenu)[0]
                else :
                    contenu = ' '
                
                if 'W' in liste_murs :
                    affiche_ligne2 = affiche_ligne2 + '| ' + contenu + ' '
                else :
                    affiche_ligne2 = affiche_ligne2 + '  ' + contenu + ' '

            if 'E' in liste_murs :
                affiche_ligne2 = affiche_ligne2 + '|'
            
            affichage = affichage + affiche_ligne1 + '+\n' + affiche_ligne2 + '\n'
            
        affiche_ligne1 = ''
            
        for colonne in range(self.__largeur) :
            
            liste_murs = self.__cases[self.__hauteur - 1][colonne].getMurs()
                
            if 'S' in liste_murs :
                affiche_ligne1 = affiche_ligne1 + '+---'
            else :
                affiche_ligne1 = affiche_ligne1 + '+   '
                
        affichage = affichage + affiche_ligne1 + '+\n'
        
        return affichage
        


########### Exemple d'utilisation ######################################################################################
if __name__ == '__main__' :
    
    laby = Grille(8,8)
    print('Grille de dimensions 8 x 8 avec bordure (par défaut) :')
    print(laby)
    input("Appuyer sur 'Entrée'")
    
    print('\nSans bordure :')
    laby.detruireBordure()
    print(laby)
    input("Appuyer sur 'Entrée'")
    
    print("\nAvec bordure, c'est mieux pour la suite...")
    laby.construireBordure()
    print(laby)
    input("Appuyer sur 'Entrée'")

    graphe: dict = {(0, 0): {(0, 1): 1, (1, 0): 1}, (0, 1): {(0, 0): 1, (1, 1): 1}, (0, 2): {(1, 2): 1}, 
                    (0, 3): {(0, 4): 1, (1, 3): 1}, (0, 4): {(0, 3): 1, (0, 5): 1},
                    (0, 5): {(0, 4): 1, (0, 6): 1}, (0, 6): {(0, 5): 1, (0, 7): 1}, (0, 7): {(0, 6): 1}, 
                    (1, 0): {(0, 0): 1, (2, 0): 1}, (1, 1): {(0, 1): 1, (2, 1): 1},
                    (1, 2): {(0, 2): 1, (2, 2): 1}, (1, 3): {(0, 3): 1, (1, 4): 1}, (1, 4): {(1, 3): 1, (2, 4): 1}, 
                    (1, 5): {(1, 6): 1, (2, 5): 1}, (1, 6): {(1, 5): 1, (1, 7): 1}, (1, 7): {(1, 6): 1, (2, 7): 1}, 
                    (2, 0): {(1, 0): 1, (2, 1): 1, (3, 0): 1}, (2, 1): {(1, 1): 1, (2, 0): 1, (3, 1): 1}, 
                    (2, 2): {(1, 2): 1, (2, 3): 1}, (2, 3): {(2, 2): 1, (2, 4): 1}, 
                    (2, 4): {(1, 4): 1, (2, 3): 1, (2, 5): 1}, (2, 5): {(1, 5): 1, (2, 4): 1, (3, 5): 1}, 
                    (2, 6): {(2, 7): 1, (3, 6): 1}, (2, 7): {(1, 7): 1, (2, 6): 1, (3, 7): 1}, 
                    (3, 0): {(2, 0): 1, (4, 0): 1}, (3, 1): {(2, 1): 1, (3, 2): 1}, 
                    (3, 2): {(3, 1): 1, (3, 3): 1, (4, 2): 1}, (3, 3): {(3, 2): 1, (3, 4): 1}, 
                    (3, 4): {(3, 3): 1, (3, 5): 1}, (3, 5): {(2, 5): 1, (3, 4): 1}, (3, 6): {(2, 6): 1, (4, 6): 1}, 
                    (3, 7): {(2, 7): 1, (4, 7): 1},
                    (4, 0): {(3, 0): 1, (5, 0): 1}, (4, 1): {(5, 1): 1}, (4, 2): {(3, 2): 1, (5, 2): 1}, (4, 3): {(4, 4): 1}, 
                    (4, 4): {(4, 3): 1, (4, 5): 1, (5, 4): 1}, (4, 5): {(4, 4): 1, (4, 6): 1, (5, 5): 1}, 
                    (4, 6): {(3, 6): 1, (4, 5): 1}, (4, 7): {(3, 7): 1, (5, 7): 1}, 
                    (5, 0): {(4, 0): 1, (6, 0): 1}, (5, 1): {(4, 1): 1, (6, 1): 1}, (5, 2): {(4, 2): 1, (5, 3): 1, (6, 2): 1},
                    (5, 3): {(5, 2): 1, (5, 4): 1, (6, 3): 1}, (5, 4): {(4, 4): 1, (5, 3): 1, (6, 4): 1}, 
                    (5, 5): {(4, 5): 1, (5, 6): 1}, (5, 6): {(5, 5): 1, (5, 7): 1},
                    (5, 7): {(4, 7): 1, (5, 6): 1, (6, 7): 1}, 
                    (6, 0): {(5, 0): 1, (6, 1): 1}, (6, 1): {(5, 1): 1, (6, 0): 1, (7, 1): 1}, (6, 2): {(5, 2): 1, (7, 2): 1}, 
                    (6, 3): {(5, 3): 1, (7, 3): 1}, (6, 4): {(5, 4): 1, (6, 5): 1, (7, 4): 1}, 
                    (6, 5): {(6, 4): 1, (6, 6): 1}, (6, 6): {(6, 5): 1}, (6, 7): {(5, 7): 1, (7, 7): 1}, 
                    (7, 0): {(7, 1): 1}, (7, 1): {(6, 1): 1, (7, 0): 1, (7, 2): 1}, (7, 2): {(6, 2): 1, (7, 1): 1}, 
                    (7, 3): {(6, 3): 1}, (7, 4): {(6, 4): 1, (7, 5): 1}, (7, 5): {(7, 4): 1, (7, 6): 1},
                    (7, 6): {(7, 5): 1, (7, 7): 1}, (7, 7): {(6, 7): 1, (7, 6): 1}}
    
    print("\nConstruction avec un graphe :")
    laby.construireAvecGraphe(graphe)
    print(laby)