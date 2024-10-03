from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QTimer
import sys

class LoadingButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        # Create a QLabel to hold the loading animation
        self.loading_label = QLabel(self)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setGeometry(0, 0, 18, 18)  # Size of the loading animation

        # Load the loading gif
        self.loading_gif = QMovie("loading.gif")
        self.loading_gif.setScaledSize(self.loading_label.size())  # Scale the gif size

        # Set QLabel to show the QMovie (animated gif)
        self.loading_label.setMovie(self.loading_gif)
        self.loading_label.hide()  # Initially hide the loading gif

    def start_loading(self):
        self.setEnabled(False)
        self.loading_label.show()
        self.loading_gif.start()

    def stop_loading(self):
        self.setEnabled(True)
        self.loading_gif.stop()
        self.loading_label.hide()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Create the button with loading
        self.button = LoadingButton("Submit")
        self.button.clicked.connect(self.start_task)

        layout.addWidget(self.button)
        self.setLayout(layout)

    def start_task(self):
        # Start loading animation
        self.button.start_loading()

        # Simulate a long task
        QTimer.singleShot(3000, self.button.stop_loading)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
