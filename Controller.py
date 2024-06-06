# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import QApplication
from ModeleAppBis import Modele
from VueAPP2 import VueProjet,Grid  # Assurez-vous que le fichier contenant la classe VueProjet est nommé vue.py
from PyQt6.QtWidgets import QApplication, QTreeWidgetItem


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

        # Charger les articles depuis le modèle
        self.vue.afficherArticles(self.modele.getArticle())
        self.vue.grid.setCasePrive(self.modele.getCasesLock())

    def update_position(self, pos):
        # Vérifie si la case est privée
        print(self.modele.getAllCasesLock())
        if [pos.x(), pos.y()] in self.modele.getAllCasesLock():
            # Affiche un message à l'utilisateur pour lui indiquer que la case est privée
            self.vue.definirPosition()
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
        #self.vue.liste_course.takeTopLevelItem(self.vue.liste_course.indexOfTopLevelItem(item))

    def analyser_parcours(self):
        # Analyse le parcours et met à jour la grille
        chemin = self.modele.coordonneeChemin()
        print(chemin)
        print(self.modele.getListeCourse())
        self.vue.grid.setParcours(chemin)

    def creation_liste_random(self):
        self.modele.random_course()
        produit = self.modele.article_priorite()
        produits_couleurs = [(i, self.modele.colorAttribution(i)) for i in produit]
        self.vue.grid.setProduit(produits_couleurs)
        liste = self.modele.getListeCourse()
        self.vue.afficher_liste_course(liste)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.vue.show()
    sys.exit(app.exec())
