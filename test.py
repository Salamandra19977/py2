from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self) -> None:
        layout = QVBoxLayout()
        self.coins = 0
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start(100)

        self.label1 = QLabel(f"Clicks: {self.coins}", self)
        self.clicker_title = QLabel("Sigma clicker game!", self)
        layout.addWidget(self.clicker_title)
        layout.addWidget(self.label1)

        self.setLayout(layout)

    def game_loop(self) -> None:
        self.coins += 1
        print(self.coins)
        self.label1.setText(f"Монети: {self.coins}")




App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())