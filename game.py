import os
from datetime import date
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
from database import *
import random

with open("style.css", "r") as stylesheet:
    APP_STYLE = stylesheet.read()

class GameWindow(QWidget):
    def __init__(self, user_id: int) -> None:
        super().__init__()
        self.setWindowTitle("Гра Клікер")
        self.setStyleSheet(APP_STYLE)
        self.setFixedSize(400, 500)

        self.user_id = user_id
        self.coins = 0
        self.passive_income = 0
        self.upgrade_cost = 100
        self.click_value = 1
        self.auto_clicker = 0
        self.bonus = 0
        self.double_click = 1
        self.upgrade_discount = 0
        self.bonus_multiplier = 1

        layout = QVBoxLayout()

        self.leaderboard_button = QPushButton("Показати рейтинг")
        self.leaderboard_button.clicked.connect(self.show_leaderboard)
        layout.addWidget(self.leaderboard_button)

        layout.addWidget(QLabel(f"Вітаємо в грі! Ваш ID: {user_id}", alignment=Qt.AlignCenter))
        self.coins_label = QLabel(f"Монети: {self.coins}")
        self.coins_label.setAlignment(Qt.AlignCenter)
        self.coins_label.setStyleSheet("font-size: 18px;")

        self.click_button = QPushButton("🚀 Клікни!")
        self.click_button.setObjectName("clickButton")
        self.click_button.clicked.connect(self.handle_click)

        self.upgrade_button = QPushButton(f"Покращення (Ціна: {self.upgrade_cost} монет)")
        self.upgrade_button.setStyleSheet("font-size: 14px;")
        self.upgrade_button.clicked.connect(self.handle_upgrade)

        self.passive_income_label = QLabel(f"Пасивний дохід: {self.passive_income}/с")
        self.passive_income_label.setAlignment(Qt.AlignCenter)

        self.auto_clicker_button = QPushButton("Автоклікер (Ціна: 500 монет)")
        self.auto_clicker_button.clicked.connect(self.handle_auto_clicker)

        self.double_click_button = QPushButton("Подвоїти монети за клік (Ціна: 1000 монет)")
        self.double_click_button.clicked.connect(self.handle_double_click)

        self.upgrade_discount_button = QPushButton("Знижка на покращення (Ціна: 1500 монет)")
        self.upgrade_discount_button.clicked.connect(self.handle_upgrade_discount)

        self.bonus_button = QPushButton("Отримати бонус")
        self.bonus_button.clicked.connect(self.handle_bonus)
        self.daily_bonus_button = QPushButton("Отримати щоденний бонус")
        self.daily_bonus_button.clicked.connect(self.claim_daily_bonus)

        if not self.check_daily_bonus_available():
            self.daily_bonus_button.setEnabled(False)
            self.daily_bonus_button.setText("Щоденний бонус вже отримано")

        self.save_button = QPushButton("😀 Зафіксувати результат")
        self.save_button.clicked.connect(self.save_progress)

        layout.addWidget(self.daily_bonus_button)
        layout.addWidget(self.coins_label)
        layout.addWidget(self.click_button)
        layout.addWidget(self.upgrade_button)
        layout.addWidget(self.auto_clicker_button)
        layout.addWidget(self.double_click_button)
        layout.addWidget(self.upgrade_discount_button)
        layout.addWidget(self.bonus_button)
        layout.addWidget(self.passive_income_label)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start(1000)

    def show_leaderboard(self) -> None:
        try:
            leaderboard = get_leaderboard()
            if not leaderboard:
                QMessageBox.information(self, "Рейтинг", "Немає даних для рейтингу.")
                return

            message = "Топ гравців:\n"
            for i, (uid, score) in enumerate(leaderboard, 1):
                message += f"{i}. ID {uid} — {score} монет\n"

            QMessageBox.information(self, "Рейтинг", message)
        except Exception as e:
            QMessageBox.warning(self, "Помилка", f"Не вдалося завантажити рейтинг.\n{str(e)}")

    def check_daily_bonus_available(self) -> bool:
        today = str(date.today())
        if os.path.exists("last_bonus.txt"):
            with open("last_bonus.txt", "r") as file:
                last_date = file.read().strip()
                return last_date != today
        return True

    def claim_daily_bonus(self) -> None:
        if self.check_daily_bonus_available():
            bonus = random.randint(100, 300)
            self.coins += bonus
            self.coins_label.setText(f"Монети: {self.coins}")
            with open("last_bonus.txt", "w") as file:
                file.write(str(date.today()))
            self.daily_bonus_button.setText(f"Бонус отримано: {bonus} монет")
            self.daily_bonus_button.setEnabled(False)
        else:
            QMessageBox.information(self, "Інформація", "Ви вже отримали щоденний бонус сьогодні.")

    def handle_click(self) -> None:
        self.coins += self.click_value * self.double_click
        self.coins_label.setText(f"Монети: {self.coins}")

    def handle_upgrade(self) -> None:
        if self.coins >= self.upgrade_cost:
            self.coins -= self.upgrade_cost
            self.passive_income += 1
            self.coins_label.setText(f"Монети: {self.coins}")
            self.passive_income_label.setText(f"Пасивний дохід: {self.passive_income}/с")
            self.upgrade_cost = int(self.upgrade_cost * 1.5) * (1 - self.upgrade_discount)
            self.upgrade_button.setText(f"Покращення (Ціна: {self.upgrade_cost} монет)")
        else:
            QMessageBox.warning(self, "Помилка", "Не вистачає монет для покращення!")

    def handle_auto_clicker(self) -> None:
        if self.coins >= 500:
            self.coins -= 500
            self.auto_clicker += 1
            self.coins_label.setText(f"Монети: {self.coins}")
            self.auto_clicker_button.setText(f"Автоклікер (Кількість: {self.auto_clicker})")
        else:
            QMessageBox.warning(self, "Помилка", "Не вистачає монет для автоклікера!")

    def handle_double_click(self) -> None:
        if self.coins >= 1000:
            self.coins -= 1000
            self.double_click = 2
            self.coins_label.setText(f"Монети: {self.coins}")
            self.double_click_button.setText("Подвоїти монети за клік (Виконано)")

    def handle_upgrade_discount(self) -> None:
        if self.coins >= 1500:
            self.coins -= 1500
            self.upgrade_discount = 0.5
            self.coins_label.setText(f"Монети: {self.coins}")
            self.upgrade_discount_button.setText("Знижка на покращення (Виконано)")

    def handle_bonus(self) -> None:
        bonus = random.randint(10, 100) * self.bonus_multiplier
        self.coins += bonus
        self.coins_label.setText(f"Монети: {self.coins}")
        self.bonus_button.setText(f"Отримано бонус: {bonus} монет")

    def save_progress(self) -> None:
        try:
            update_score(self.user_id, self.coins)
            QMessageBox.information(self, "Збереження", "Прогрес успішно збережено!")
        except Exception as e:
            QMessageBox.warning(self, "Помилка", f"Не вдалося зберегти прогрес.\n{str(e)}")

    def game_loop(self) -> None:
        self.coins += self.passive_income + (self.auto_clicker * 1)
        self.coins_label.setText(f"Монети: {self.coins}")
