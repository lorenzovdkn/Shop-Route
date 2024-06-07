# view.py
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QDialog, QDialogButtonBox, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize, pyqtSignal

class LoginDialog(QDialog):
    signalLoginAccepted = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.username_label = QLabel('Username:')
        layout.addWidget(self.username_label)
        self.username_edit = QLineEdit()
        layout.addWidget(self.username_edit)

        self.password_label = QLabel('Password:')
        layout.addWidget(self.password_label)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def accept(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()

        self.signalLoginAccepted.emit(username, password)
        super().accept()

class View(QWidget):
    signalOpenAppClient = pyqtSignal()
    signalIdentifiants = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Application')
        self.setGeometry(100, 100, 300, 200)

        layout = QHBoxLayout()

        # Client button
        self.clientButton = QPushButton()
        self.clientButton.setIcon(QIcon('client.png'))
        self.clientButton.setIconSize(QSize(100, 100))  # Taille de l'icône
        self.clientButton.setFixedSize(150, 150)  # Taille du bouton
        self.clientButton.setStyleSheet("QPushButton::icon { margin-bottom: -20px; }")  # Ajuster la position de l'icône
        layout.addWidget(self.clientButton)

        # Manager button
        self.managerButton = QPushButton()
        self.managerButton.setIcon(QIcon('avatar-du-manager.png'))
        self.managerButton.setIconSize(QSize(100, 100))  # Taille de l'icône
        self.managerButton.setFixedSize(150, 150)  # Taille du bouton
        self.managerButton.setStyleSheet("QPushButton::icon { margin-bottom: -20px; }")  # Ajuster la position de l'icône
        layout.addWidget(self.managerButton)

        self.setLayout(layout)

        # Connecter les signaux aux slots
        self.clientButton.clicked.connect(self.signalOpenAppClient.emit)
        self.managerButton.clicked.connect(self.show_manager_login)

    def show_manager_login(self):
        login_dialog = LoginDialog()
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            # Les identifiants sont émis via le signalIdentifiants
            username = login_dialog.username_edit.text().strip()
            password = login_dialog.password_edit.text().strip()
            self.signalIdentifiants.emit(username, password)
