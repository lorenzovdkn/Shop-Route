# model.py
import os, sys

class Model:
    def __init__(self):
        self.users = {
            'admin': 'admin'  # Utilisateur de test
        }
        
    def open_client_app(self):
        client_controller_path = os.path.abspath('AppClient/Controller.py')
        os.system(f'{sys.executable} "{client_controller_path}" &')
        
    def open_manager_app(self):
        manager_controller_path = os.path.abspath("AppCreation/Controller.py")
        os.system(f'{sys.executable} "{manager_controller_path}" &')

    def validate_user(self, username, password):
        if username in self.users and self.users[username] == password:
            return True
        else:
            return False