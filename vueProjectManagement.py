from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QInputDialog, QMessageBox, QFileDialog
from PyQt6.QtCore import pyqtSignal, Qt
import os
import json

class Project(QWidget):
    projectLoadedSignal = pyqtSignal(str, str, str, str, dict)
    projectSelectedSignal = pyqtSignal(str, str)
    projectCreatedSignal = pyqtSignal(str)
    projectDetailsSignal = pyqtSignal(str, str, str, str)
    projectDeleteSignal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.layout1 = QVBoxLayout()
        self.setLayout(self.layout1)
        self.project = None
        self.projectDetails = None

        project_label = QLabel("Projet :")
        self.projectsList = QListWidget()
        self.addButton = QPushButton('Ajouter un projet')
        self.removeButton = QPushButton('Supprimer un projet')

        self.layout1.addWidget(project_label)
        self.layout1.addWidget(self.projectsList)
        self.layout1.addWidget(self.addButton)
        self.layout1.addWidget(self.removeButton)

        self.projectsList.itemClicked.connect(self.projectClicked)
        self.projectsList.itemDoubleClicked.connect(self.editProjectDoubleClicked)
        self.addButton.clicked.connect(self.addProject)
        self.removeButton.clicked.connect(self.removeProjectClicked)

    def addProject(self):
        name, ok = QInputDialog.getText(self, 'Ajouter un projet', 'Nom du projet:')
        if ok and name:
            self.projectCreatedSignal.emit(name)

    def setProject(self, project: str):
        self.project = project

    def getProject(self):
        return self.project

    def projectClicked(self, item):
        project_name = item.text()
        self.projectSelectedSignal.emit(project_name, self.projectDetails)

    def editProjectDoubleClicked(self, item):
        project = item.text()
        edit_project, ok = QInputDialog.getText(self, 'Modifier un projet', 'Modifier le projet:', text=project)
        if ok and edit_project:
            self.projectDetailsSignal.emit(self.project, edit_project)

    def removeProjectClicked(self):
        selected = self.projectsList.currentRow()
        if selected >= 0:
            project = self.projectsList.takeItem(selected).text()
            self.projectDeleteSignal.emit(project)

    def addProjectToList(self, name: str):
        self.projectsList.addItem(name)

    def removeProject(self, name: str):
        items = self.projectsList.findItems(name, Qt.MatchFlag.MatchExactly)
        for item in items:
            row = self.projectsList.row(item)
            self.projectsList.takeItem(row)

    def loadProject(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Charger un projet", os.getcwd(), "JSON Files (*.json)")

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    project_data = json.load(file)
                    project_name = os.path.basename(file_path).split('.')[0]
                    project_details = project_data['details']
                    self.projectLoadedSignal.emit(project_name, project_details, file_path, project_data)
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement du projet: {e}")
