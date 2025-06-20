from logging import exception

from PyQt5.QtWidgets import *
import sys
from main import *

class mainwindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 400)
        layout = QVBoxLayout()

        # try:
        #     # with open("register_style.css", "r") as f:
        #     #     app.setStyleSheet(f.read())
        # except FileNotFoundError:
        #     print("Файл style.css не найден")

        self.mainlabel = QLabel("Welcome to register window!", self)
        layout.addWidget(self.mainlabel)

        self.register_but = QPushButton("Авторизоваться", self)
        self.register_but.clicked.connect(self.open_auth_window)
        layout.addWidget(self.register_but)

        self.login_but = QPushButton("Логин", self)
        self.login_but.clicked.connect(self.open_login)
        layout.addWidget(self.login_but)

        self.setLayout(layout)

    def open_auth_window(self):
        self.auth_window = AuthWindow()
        self.auth_window.show()

    def open_login(self):
        self.loginwindow = LogWindow()
        self.loginwindow.show()
class AuthWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 400)
        self.setWindowTitle("Окно авторизации")
        qwidget = QWidget()
        layout = QVBoxLayout()

        self.authlabel = QLabel("Авторизация")
        layout.addWidget(self.authlabel)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Логин")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Пароль")
        self.email = QLineEdit()
        self.email.setPlaceholderText("Почта (@)")
        self.Authorize = QPushButton("Авторизоваться")
        self.Authorize.clicked.connect(self.open_game)
        layout.addWidget(self.name_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.email)
        layout.addWidget(self.Authorize)

        qwidget.setLayout(layout)
        self.setCentralWidget(qwidget)

        self.game = ClickerWindow()

    def open_game(self):
        try:
            self.password = self.pass_input.text()
            self.name = self.name_input.text()
            self.gmail = self.email.text()
            self.game.show()
        except Exception as e:
            print(e)


class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 400)
        self.setWindowTitle("Логин")
        qwidget = QWidget()
        layout = QVBoxLayout()
        self.logLabel = QLabel("Логин")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Логин")
        self.pass_edit = QLineEdit()
        self.pass_edit.setPlaceholderText("Пароль")
        self.log_button = QPushButton("Login")
        layout.addWidget(self.logLabel)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.pass_edit)
        layout.addWidget(self.log_button)

        qwidget.setLayout(layout)
        self.setCentralWidget(qwidget)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())