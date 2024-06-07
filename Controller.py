# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import QApplication
from ModeleAppBis import Modele
from VueAPP2 import VueProjet,Grid  # Assurez-vous que le fichier contenant la classe VueProjet est nommé vue.py
from PyQt6.QtWidgets import QApplication, QTreeWidgetItem
import time

class Controller:
    def __init__(self):
        self.modele = Modele()  # Initialiser le modèle avec une position de départ par défaut
        self.vue = VueProjet()  # Initialiser la vue
        # Connecter les signaux et les slots
        self.vue.ajoutClicked.connect(self.ajouter_article)
        self.vue.supprimerClicked.connect(self.supprimer_article)
        self.vue.analyseClicked.connect(self.analyser_parcours)
        self.vue.fnameOpen.connect(self.ouvrir_fichier)
        self.vue.grid.positionSignal.connect(self.update_position)
        self.vue.dicoAleatoireClicked.connect(self.creation_liste_random)
        self.vue.indexClicked.connect(self.cheminContinu)
        self.vue.grid.indexReset.connect(self.indexReset)

        # Definir:
        self.vue.afficherArticles(self.modele.getArticle())
        self.vue.grid.setCasePrive(self.modele.getCasesLock())
        self.vue.grid.setCaisses(self.modele.getCaisses())

    def update_position(self, pos):
        # Vérifie si la case est privée
        if [pos.x(), pos.y()] in self.modele.getAllCasesLock():
            # Affiche un message à l'utilisateur pour lui indiquer que la case est privée
            #self.vue.definirPosition()
            print("OOOH")
        else:
        # Met à jour la position de départ dans le modèle lorsque l'utilisateur clique sur la grille
            self.modele.setPosition((pos.x(), pos.y()))
            self.vue.grid.setPosition([(pos.x(), pos.y())])

    def ouvrir_fichier(self, chemin):
        # Ouvre un fichier et met à jour les informations dans le modèle
        self.modele.lireJson(chemin)
        self.vue.afficherArticles(self.modele.getArticle())

    def ajouter_article(self, produit):
        if produit not in self.modele.getListeCourse():
            self.modele.setListeCourse(produit)
            produit_prioritaire = self.modele.article_priorite()
            produits_couleurs = [(i, self.modele.colorAttribution(i)) for i in produit_prioritaire]
            self.vue.grid.setProduit(produits_couleurs)
            liste = self.modele.getListeCourse()
            self.vue.afficher_liste_course(liste)
            
    def supprimer_article(self,produit):
        # Supprime un produit de la liste de course dans le modèle
        self.modele.deleteProduct(produit)
        liste = self.modele.getListeCourse()
        produit = self.modele.article_priorite()
        self.vue.grid.setProduit(produit)
        self.vue.afficher_liste_course(liste)

    def analyser_parcours(self):
        # Analyse le parcours et met à jour la grille
        self.vue.afficherArticles(self.modele.getArticle())
        if  self.vue.grid.parcours:
            self.modele.indexZero()
            self.vue.grid.setIndex(self.modele.getIndex())

        chemins = self.modele.coordonneeChemin()
        self.vue.cocheCourse(self.modele.getListeCourse(),self.modele.getProduitCoche())
        self.vue.grid.setParcours(chemins)
        self.vue.setpos.setVisible(True)

    def continu_parcours(self):
        chemins = self.modele.coordonneeChemin()
        self.vue.cocheCourse(self.modele.getListeCourse(),self.modele.getProduitCoche())
        self.vue.grid.setParcours(chemins)

    def creation_liste_random(self):
        self.modele.random_course()
        produit = self.modele.article_priorite()
        produits_couleurs = [(i, self.modele.colorAttribution(i)) for i in produit]
        self.vue.grid.setProduit(produits_couleurs)
        liste = self.modele.getListeCourse()
        self.vue.afficher_liste_course(liste)

    def cheminContinu(self):

        self.modele.plusUnIndex()
        self.vue.grid.setIndex(self.modele.getIndex())
        self.continu_parcours()

    def indexReset(self):
        self.vue.setpos.setVisible(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.vue.show()
    sys.exit(app.exec())
