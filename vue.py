import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout,QMainWindow
from PyQt6.QtWidgets import QPushButton,QFileDialog,QComboBox,QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

class Case(QWidget):
    

    def __init__(self):
        super().__init__()
        self.layout1 = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()
        self.layout4 = QHBoxLayout()

        self.setLayout(self.layout1)
        self.resize(800, 600) 
        titre = QLabel("Mode Edition de plan")

        self.layout1.addWidget(titre)
        titre_font = QFont()
        titre_font.setPointSize(30)
        titre.setFont(titre_font)

        case = QLabel("Case")
        case_font = QFont()
        case_font.setPointSize(20)
        case.setFont(case_font)
        self.layout1.addWidget(case)
        self.layout1.addLayout(self.layout2)
        self.layout1.addLayout(self.layout3)
        type_case_label = QLabel("Type de case:")
        self.layout2.addWidget(type_case_label)
        self.type_case_combo = QComboBox()
        self.type_case_combo.addItems(["publique", "privé"])
        self.layout2.addWidget(self.type_case_combo)
        category_label = QLabel("Catégorie de la case:")
        self.layout3.addWidget(category_label)
        self.category_combo = QComboBox()
        self.category_combo.addItems( ["Légumes","Poissons","Viandes","Épicerie","Épicerie sucrée","Petit déjeuner","Fruits","Rayon frais","Crèmerie","Conserves","Apéritifs","Boissons","Articles Maison","Hygiène","Bureau","Animaux"])
        self.layout3.addWidget(self.category_combo)
            
        # Alignement des layouts
        self.layout1.setAlignment(Qt.AlignmentFlag.AlignTop)

class Contenu(QWidget):
    def __init__(self):
        super().__init__()
        self.layout1 = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    vue = Case() 
    vue.show()
    sys.exit(app.exec())
