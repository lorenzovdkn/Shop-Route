import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import pyqtSlot

import vue
import modele

class Controller:
    def __init__(self):
        self.model = modele.ModelMagasin()
        self.view = vue.MainWindow()

        # self.view.case_widget.type_case_combo.currentTextChanged.connect(self.on_type_case_changed)
        # self.view.contenu_widget.addButton.clicked.connect(self.on_add_product)
        # self.view.contenu_widget.removeButton.clicked.connect(self.on_remove_product)
        # self.view.contenu_widget.editButton.clicked.connect(self.on_edit_product)
        # self.view.contenu_widget.productClickedSignal.connect(self.on_product_clicked)
        self.view.contenu_widget.signalAddProduct.connect(self.on_add_productClick)
        
    def on_add_productClick(self):
        list_category = self.model.getCategoryJson()
        self.view.contenu_widget.addProduct(list_category)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.view.show()
    sys.exit(app.exec())
    
