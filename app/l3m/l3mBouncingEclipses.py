from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer

class BouncingElipses(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(4)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.dots = []
        self.styles = [
            "font-size: 16px; color: grey;",
            "font-size: 24px; color: grey;",
            "font-size: 16px; color: grey;"
        ]

        for i in range(3):
            dot = QLabel(".")
            dot.setStyleSheet(self.styles[0])
            dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(dot)
            self.dots.append(dot)

        self.current = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_next)
        self.timer.start(300)

    def animate_next(self):
        for i, dot in enumerate(self.dots):
            if i == self.current:
                dot.setStyleSheet(self.styles[1])  # Enlarge
            else:
                dot.setStyleSheet(self.styles[0])  # Reset
        self.current = (self.current + 1) % 3
