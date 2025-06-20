from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.coins = 0
        self.speed = 500
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start(self.speed)
        self.label = QLabel(self)

        self.show()

    def game_loop(self) -> None:
        self.coins += 1
        self.label.setText(f"Монети: {self.coins}")

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())