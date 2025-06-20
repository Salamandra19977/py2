import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer

class ClickerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Clicker")
        self.resize(400, 300)
        try:
            with open("style.css", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Файл style.css не найден. Продолжение без внешнего стиля.")

        # Изначальная стата
        self.clicks = 0
        self.click_value = 1
        self.autoclick_rate = 0
        self.temp_multiplier = 1
        self.temp_timer = None

        # Стоимость улучшений
        self.cost_plus1 = 10
        self.cost_x2 = 100
        self.cost_x5 = 500
        self.cost_autoclick = 1000
        self.cost_temp_x9 = 2000

        # Основные виджеты
        self.click_label = QLabel(f"Clicks: {self.clicks}")
        self.click_label.setStyleSheet("font-size: 24px;")

        self.autolabel = QLabel(f"Autoclick: {self.autoclick_rate}")
        self.autolabel.setStyleSheet("font-size: 24px;")

        self.click_button = QPushButton("Click!")
        self.click_button.setStyleSheet("font-size: 20px; padding: 10px;")
        self.click_button.clicked.connect(self.handle_click)
        self.click_button.setObjectName("aba")

        # Кнопки-улучшения
        self.btn_plus1 = QPushButton(f"+1 клик\nCost: {self.cost_plus1}")
        self.btn_plus1.clicked.connect(self.buy_plus1)

        self.btn_x2 = QPushButton(f"x2 клик\nCost: {self.cost_x2}")
        self.btn_x2.clicked.connect(self.buy_x2)

        self.btn_x5 = QPushButton(f"x5 клик\nCost: {self.cost_x5}")
        self.btn_x5.clicked.connect(self.buy_x5)

        self.btn_autoclick = QPushButton(f"Автокликер\nCost: {self.cost_autoclick}")
        self.btn_autoclick.clicked.connect(self.buy_autoclick)

        self.btn_temp = QPushButton(f"Бонус x9 (10с)\nCost: {self.cost_temp_x9}")
        self.btn_temp.clicked.connect(self.buy_temp)

        # Отображение
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.click_label)
        main_layout.addWidget(self.autolabel)
        main_layout.addWidget(self.click_button)

        upgrades_layout = QHBoxLayout()
        for btn in (self.btn_plus1, self.btn_x2, self.btn_x5, self.btn_autoclick, self.btn_temp):
            upgrades_layout.addWidget(btn)
        main_layout.addLayout(upgrades_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Autoclick timer
        self.autoclick_timer = QTimer(self)
        self.autoclick_timer.timeout.connect(self.handle_autoclick)
        self.autoclick_timer.start(1000)

    def game_loop(self):
        self.click_label.setText(f"Clicks: {self.clicks}")
        self.autolabel.setText(f"Autoclick: {self.autoclick_rate}")

    def handle_click(self):
        gained = self.click_value * self.temp_multiplier
        self.clicks += gained
        self.game_loop()

    def handle_autoclick(self):
        if self.autoclick_rate > 0:
            self.clicks += self.autoclick_rate * self.temp_multiplier
            self.game_loop()

    def buy_plus1(self):
        if self.spend_clicks(self.cost_plus1):
            self.click_value += 1
            # Optional: cost scaling
            self.cost_plus1 = int(self.cost_plus1 * 3)
            self.btn_plus1.setText(f"+1 Click\nCost: {self.cost_plus1}")

    def buy_x2(self):
        if self.spend_clicks(self.cost_x2):
            self.click_value *= 2
            self.cost_x2 = int(self.cost_x2 * 3)
            self.btn_x2.setText(f"x2 Clicks\nCost: {self.cost_x2}")

    def buy_x5(self):
        if self.spend_clicks(self.cost_x5):
            self.click_value *= 5
            self.cost_x5 = int(self.cost_x5 * 3)
            self.btn_x5.setText(f"x5 Clicks\nCost: {self.cost_x5}")

    def buy_autoclick(self):
        if self.spend_clicks(self.cost_autoclick):
            self.autoclick_rate += 1
            self.cost_autoclick = int(self.cost_autoclick * 2)
            self.btn_autoclick.setText(f"Autoclicker\nCost: {self.cost_autoclick}")


    def buy_temp(self):
        if self.temp_multiplier > 1:
            QMessageBox.information(self, "Бонус активен")
            return
        if self.spend_clicks(self.cost_temp_x9):
            self.activate_temp_multiplier()


    def activate_temp_multiplier(self):
        self.temp_multiplier = 9
        self.btn_temp.setEnabled(False)
        self.temp_timer = QTimer(self)
        self.temp_timer.setSingleShot(True)
        self.temp_timer.timeout.connect(self.deactivate_temp_multiplier)
        self.temp_timer.start(10000)

    def deactivate_temp_multiplier(self):
        self.temp_multiplier = 1
        self.btn_temp.setEnabled(True)
        self.game_loop()


    def spend_clicks(self, amount):
        if self.clicks >= amount:
            self.clicks -= amount
            self.game_loop()
            return True
        else:
            QMessageBox.warning(self, "Error", "Соберите больше кликов!")
            return False


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ClickerWindow()
#     window.show()
#     sys.exit(app.exec_())
