import sys

from PyQt5.QtWidgets import QLineEdit, QApplication
from game import *
from database import *

with open("style.css", "r") as stylesheet:
    APP_STYLE = stylesheet.read()

class AuthWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Авторизація")
        self.setFixedSize(300, 250)
        self.setStyleSheet(APP_STYLE)
        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setSpacing(12)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Ім'я користувача")

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Пароль")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Увійти")
        self.login_button.clicked.connect(self.handle_login)

        layout.addWidget(QLabel("Авторизація", alignment=Qt.AlignCenter))
        layout.addWidget(self.login_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        name = self.login_input.text()
        password = self.pass_input.text()
        user_id = login_user(name, password)
        if user_id:
            self.close()
            self.main_window.close()
            self.game_window = GameWindow(user_id)
            self.game_window.show()
        else:
            QMessageBox.warning(self, "Помилка", "Невірні дані")

class RegisterWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Реєстрація")
        self.setFixedSize(300, 300)
        self.setStyleSheet(APP_STYLE)
        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setSpacing(12)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ім'я користувача")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Пароль")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Зареєструватись")
        self.register_button.clicked.connect(self.handle_register)

        layout.addWidget(QLabel("Реєстрація", alignment=Qt.AlignCenter))
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def handle_register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.pass_input.text()
        success = register_user(name, password, email)
        if success:
            user_id = login_user(name, password)
            self.close()
            self.main_window.close()
            self.game_window = GameWindow(user_id)
            self.game_window.show()
        else:
            QMessageBox.warning(self, "Помилка", "Користувач вже існує")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Меню")
        self.setFixedSize(300, 200)
        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        layout.addWidget(QLabel("Ласкаво просимо!", alignment=Qt.AlignCenter))

        self.login_button = QPushButton("Авторизуватись")
        self.login_button.clicked.connect(self.open_login)

        self.register_button = QPushButton("Зареєструватись")
        self.register_button.clicked.connect(self.open_register)

        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def open_login(self):
        self.auth_window = AuthWindow(self)
        self.auth_window.show()

    def open_register(self):
        self.register_window = RegisterWindow(self)
        self.register_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
