import os
import sys
import json
from PyQt6.QtCore import Qt, pyqtSignal, QDate, QSize
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QDateEdit, QFormLayout,
    QWidget, QScrollArea, QGridLayout, QSizePolicy, QSpacerItem, QFileDialog
)
from PyQt6.QtGui import QPixmap

class ProjectDetailsDialog(QDialog):
    signalDeleteSave = pyqtSignal()
    def __init__(self, project_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Projet")
        self.layout = QVBoxLayout(self)

        self.details_label = QLabel(self.format_project_details(project_data), self)
        self.layout.addWidget(self.details_label)

        self.buttons_layout = QHBoxLayout()
        
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.buttons_layout.addItem(spacer)

        self.open_button = QPushButton("Ouvrir", self)
        self.open_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.open_button)

        self.delete_button = QPushButton("Supprimer", self)
        self.delete_button.clicked.connect(self.removeSave)
        self.buttons_layout.addWidget(self.delete_button)

        self.cancel_button = QPushButton("Annuler", self)
        self.cancel_button.clicked.connect(self.close)
        self.buttons_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.buttons_layout)
        
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.buttons_layout.addItem(spacer)
        
    def removeSave(self):
        self.signalDeleteSave.emit()
        self.reject()

    def format_project_details(self, project_data):
        data_projet = project_data.get('data_projet', {}) # Extrait le sous-dictionnaire data_projet de project_data.
        
        name = data_projet.get('nom_projet', 'Inconnu')
        authors = data_projet.get('auteurs', 'Inconnu')
        store_name = data_projet.get('nom_magasin', 'Inconnu')
        creation_date = data_projet.get('date', 'Inconnu')

        return (f"Nom: {name}\n"
                f"Auteurs: {authors}\n"
                f"Magasin: {store_name}\n"
                f"Date: {creation_date}")

class LoadProjectWindow(QWidget):
    signalOpenProject = pyqtSignal(str)
    signalCreateProject = pyqtSignal(str, str, str, str, str, str)
    signalDeleteProject = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setStyleSheet(open("AppCreation/styles/qssSelect.qss").read())
        self.setWindowTitle('Charger ou Créer un Projet')
        self.setMinimumSize(1000, 400)
        self.setMaximumSize(1200, 800)

        self.layoutMain = QHBoxLayout(self)
        self.layoutText = QVBoxLayout()
        self.layoutMain.addLayout(self.layoutText)
        self.layoutButtons = QVBoxLayout()
        self.layoutMain.addLayout(self.layoutButtons)


        self.titleButton = QLabel("Sélectionner un projet ou en créer un nouveau")
        self.layoutButtons.addWidget(self.titleButton)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layoutButtons.addWidget(self.scroll_area)

        self.scroll_widget = QWidget()
        self.project_layout = QGridLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        
        

        self.load_projects()

    def load_projects(self):
        # Nettoyer la grille avant de recharger les projets
        for i in reversed(range(self.project_layout.count())): 
            widget_to_remove = self.project_layout.itemAt(i).widget()
            if widget_to_remove:
                self.project_layout.removeWidget(widget_to_remove)
                widget_to_remove.deleteLater()

        saves_folder = "AppCreation/saves"
        if not os.path.exists(saves_folder):
            os.makedirs(saves_folder)
        
        row, col = 0, 0
        max_columns = 5  # Nombre maximal de colonnes
        button_size = QSize(200, 200)  # Taille des boutons
        button_spacing = 10  # Espacement entre les boutons

        for file_name in os.listdir(saves_folder):
            project_button = QPushButton(file_name.split("-")[0][:-4])
            project_button.setStyleSheet("font-family: Roboto; font-size: 18px;")
            project_button.setFixedSize(button_size)
            project_button.clicked.connect(self.create_project_selected_callback(file_name))
            self.project_layout.addWidget(project_button, row, col * 2)

            col += 1
            if col >= max_columns:
                col = 0
                row += 1

            # Ajouter un espacement horizontal entre les boutons
            if col < max_columns:
                hspacer = QSpacerItem(button_spacing, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
                self.project_layout.addItem(hspacer, row, col * 2 + 1)

        # Bouton pour créer un nouveau projet
        create_button = QPushButton('+')
        create_button.setStyleSheet('font-size: 30px; font-weight: bold; border-radius: 60;')

        create_button.setFixedSize(QSize(160, 160) )
        create_button.clicked.connect(self.create_project)

        # Ajouter le bouton de création en bas à droite de la grille
        if col == 0:
            self.project_layout.addWidget(create_button, row, col * 2)
        else:
            self.project_layout.addWidget(create_button, row, col * 2)

        # Mettre à jour la géométrie du widget de défilement
        self.scroll_widget.setGeometry(self.project_layout.geometry())

    def create_project_selected_callback(self, file_name):
        def callback():
            self.project_selected(file_name)
        return callback

    def create_project(self):
        dialog = CreateProjectDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, authors, store_name, store_address, creation_date, file_name = dialog.get_project_details()
            self.signalCreateProject.emit(name, authors, store_name, store_address, creation_date, file_name)

    def project_selected(self, project_name):
        saves_folder = "AppCreation/saves"
        file_path = os.path.join(saves_folder, project_name)

        with open(file_path, 'r', encoding='utf-8') as file:
            project_data = json.load(file)

        dialog = ProjectDetailsDialog(project_data, self)
        dialog.signalDeleteSave.connect(lambda: self.deleteSave(file_path))
        
        ret = dialog.exec()

        if ret == QDialog.DialogCode.Accepted:
            print("Accepté")
            self.signalOpenProject.emit(file_path)
        elif ret == QDialog.DialogCode.Rejected:
            print("Rejeté")

    def deleteSave(self, file_path):
        if file_path:
            print("Suppression de la sauvegarde :", file_path)
            self.signalDeleteProject.emit(file_path)
            self.load_projects()          

class CreateProjectDialog(QDialog):
    signalCreateProject = pyqtSignal(str, str, str, str, str, str) # name, authors, store_name, store_address, creation_date, file_name
    signalOpenImage = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_name = None
        self.setWindowTitle('Créer un Projet')
        self.layout = QVBoxLayout(self)
        
        self.form_layout = QFormLayout()
        
        self.name_input = QLineEdit(self)
        self.authors_input = QLineEdit(self)
        self.store_name_input = QLineEdit(self)
        self.store_address_input = QLineEdit(self)
        self.creation_date_input = QDateEdit(self)
        self.creation_date_input.setCalendarPopup(True)
        self.creation_date_input.setDate(QDate.currentDate())
        self.image_label = QLabel(self)
        self.image_label.setText("Aucune image sélectionnée")
        self.image_button = QPushButton("Sélectionner une image", self)
        self.image_button.clicked.connect(self.select_image)
        
        self.form_layout.addRow("Nom du projet:", self.name_input)
        self.form_layout.addRow("Auteurs:", self.authors_input)
        self.form_layout.addRow("Nom du magasin:", self.store_name_input)
        self.form_layout.addRow("Adresse du magasin:", self.store_address_input)
        self.form_layout.addRow("Date de création:", self.creation_date_input)
        self.form_layout.addRow("Image du projet:", self.image_button)
        self.form_layout.addRow("", self.image_label)
        
        self.layout.addLayout(self.form_layout)
        
        self.buttons_layout = QHBoxLayout()
        
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.buttons_layout.addItem(spacer)

        self.ok_button = QPushButton("OK")
        self.ok_button.setEnabled(False)
        self.ok_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.cancel_button)
        
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.buttons_layout.addItem(spacer)
        
        self.layout.addLayout(self.buttons_layout)
        
        self.name_input.textChanged.connect(self.validate_fields)
        self.authors_input.textChanged.connect(self.validate_fields)
        self.store_name_input.textChanged.connect(self.validate_fields)
        self.store_address_input.textChanged.connect(self.validate_fields)
        self.creation_date_input.dateChanged.connect(self.validate_fields)
        self.signalOpenImage.connect(self.update_image_label)
    
    def select_image(self):
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner une image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)")
        if self.file_name:
            self.signalOpenImage.emit(self.file_name)
        else:
            self.image_label.setText("Aucune image sélectionnée")
            self.file_name = None
        self.validate_fields()

    def update_image_label(self, file_name):
        self.image_label.setText("")
        self.file_name = file_name

    def validate_fields(self):
        fields_filled = (
            bool(self.name_input.text().strip()) and
            bool(self.authors_input.text().strip()) and
            bool(self.store_name_input.text().strip()) and
            bool(self.store_address_input.text().strip()) and
            self.creation_date_input.date().isValid() and
            self.file_name is not None
        )
        self.ok_button.setEnabled(fields_filled)
    
    def get_project_details(self):
        name = self.name_input.text().strip()
        authors = self.authors_input.text().strip()
        store_name = self.store_name_input.text().strip()
        store_address = self.store_address_input.text().strip()
        creation_date = self.creation_date_input.date().toString('yyyy-MM-dd')
        file_name = self.file_name
        return name, authors, store_name, store_address, creation_date, file_name

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoadProjectWindow()
    window.show()
    sys.exit(app.exec())
