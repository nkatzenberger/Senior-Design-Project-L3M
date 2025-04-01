from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from l3m.l3mBouncingEclipses import BouncingElipses

class ChatMessage(QWidget):
    def __init__(self, message, is_user=False):
        super().__init__()

        self.bubble = QFrame()
        self.bubble.setStyleSheet(
            "background-color: #e1f5fe; padding: 8px; border-radius: 5px; font-size: 16pt; color: black;" if is_user else
            "background-color: #c8e6c9; padding: 8px; border-radius: 5px; font-size: 16pt; color: black;"
        )

        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.bubble_layout = QHBoxLayout(self.bubble)
        self.bubble_layout.addWidget(self.label)

        layout = QHBoxLayout(self)
        if is_user:
            layout.addStretch()
            layout.addWidget(self.bubble)
        else:
            layout.addWidget(self.bubble)
            layout.addStretch()

class LoadingMessage(QWidget):
    def __init__(self):
        super().__init__()

        self.bubble = QFrame()
        self.bubble.setStyleSheet("background-color: #c8e6c9; padding: 8px; border-radius: 5px;")
        self.bubble_layout = QHBoxLayout(self.bubble)

        self.loading_widget = BouncingElipses()
        self.bubble_layout.addWidget(self.loading_widget)

        layout = QHBoxLayout(self)
        layout.addWidget(self.bubble)
        layout.addStretch()