# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import QApplication
from ModeleAppBis import Modele
from VueAPP2 import VueProjet  # Assurez-vous que le fichier contenant la classe VueProjet est nommé vue.py
from PyQt6.QtWidgets import QApplication, QTreeWidgetItem


class Controller:
    def __init__(self):
        self.modele = Modele((0, 0))  # Initialiser le modèle avec une position de départ par défaut
        self.vue = VueProjet()  # Initialiser la vue
        
        # Connecter les signaux et les slots
        self.vue.ajoutClicked.connect(self.ajouter_article)
        self.vue.supprimerClicked.connect(self.supprimer_article)
        self.vue.analyseClicked.connect(self.analyser_parcours)
        self.vue.fnameOpen.connect(self.ouvrir_fichier)
        self.vue.grid.positionSignal.connect(self.update_position)

        # Charger les articles depuis le modèle
        self.vue.afficherArticles(self.modele.getArticle())

    def update_position(self, pos):
        # Met à jour la position de départ dans le modèle lorsque l'utilisateur clique sur la grille
        self.modele.setPosition((pos.x(), pos.y()))

    def ouvrir_fichier(self, chemin):
        # Ouvre un fichier et met à jour les informations dans le modèle
        self.modele.lireJson(chemin)
        self.vue.afficherArticles(self.modele.getArticle())

    def ajouter_article(self, produit):
        # Add a product to the shopping list in the model
        if produit not in self.modele.getListeCourse():
            self.modele.setListeCourse(produit)
            self.vue.liste_course.clear()
            for item in self.modele.getListeCourse():
                self.vue.liste_course.addTopLevelItem(QTreeWidgetItem([item]))

    def supprimer_article(self):
        # Supprime un produit de la liste de course dans le modèle
        item = self.vue.liste_course.currentItem()
        if item:
            product_name = item.text(0)
            self.modele.deleteProduct(product_name)
            self.vue.liste_course.takeTopLevelItem(self.vue.liste_course.indexOfTopLevelItem(item))

    def analyser_parcours(self):
        # Analyse le parcours et met à jour la grille
        chemin = self.modele.coordonneeChemin()
        print(chemin)
        print(self.modele.getListeCourse())
        self.vue.set_parcours(chemin)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.vue.show()
    sys.exit(app.exec())
