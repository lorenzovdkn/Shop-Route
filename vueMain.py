from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from vueGrid import Grid
from vueCase import Case
from vueContenu import Contenu
from vueProjectManagement import Project

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.grid = Grid()
        self.case = Case()
        self.contenu = Contenu()
        self.project = Project()

        self.layout.addWidget(self.grid)
        self.layout.addWidget(self.case)
        self.layout.addWidget(self.contenu)
        self.layout.addWidget(self.project)

        self.grid.positionSignal.connect(self.case.setCase)
        self.contenu.signalAddProduct.connect(self.addProduct)
        self.contenu.signalProductClick.connect(self.handleProductClick)
        self.contenu.signalDeleteProduct.connect(self.handleDeleteProduct)
        self.contenu.signalEditProduct.connect(self.handleEditProduct)
        self.project.projectCreatedSignal.connect(self.createProject)
        self.project.projectSelectedSignal.connect(self.loadProject)
        self.project.projectDetailsSignal.connect(self.updateProjectDetails)
        self.project.projectDeleteSignal.connect(self.deleteProject)
        self.project.projectLoadedSignal.connect(self.loadProject)

    def addProduct(self):
        current_category = self.case.currentCategory()
        self.contenu.addProduct(['Product1', 'Product2', 'Product3'], current_category)

    def handleProductClick(self, data):
        # Handle product click event
        pass

    def handleDeleteProduct(self, product_name):
        # Handle product delete event
        pass

    def handleEditProduct(self, product_data):
        # Handle product edit event
        pass

    def createProject(self, project_name):
        self.project.addProjectToList(project_name)

    def loadProject(self, project_name, project_details):
        self.project.setProject(project_name)
        self.project.projectDetails = project_details

    def updateProjectDetails(self, old_name, new_name):
        # Update project details
        pass

    def deleteProject(self, project_name):
        self.project.removeProject(project_name)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
