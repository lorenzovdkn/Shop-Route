import sys
from PyQt6.QtWidgets import QApplication
from view import View
from model import Model
import os

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.signalOpenAppClient.connect(self.open_client_app)
        self.view.signalIdentifiants.connect(self.check_login)

    def open_client_app(self):
        self.model.open_client_app()
        self.view.close()
        sys.exit(0)

    def check_login(self, username, password):
        check = self.model.validate_user(username, password)
        if check:
            self.model.open_manager_app()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = Model()
    view = View()
    controller = Controller(model, view)
    view.show()
    sys.exit(app.exec())
