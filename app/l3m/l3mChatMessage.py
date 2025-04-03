from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy
from PyQt6.QtCore import Qt, QTimer
from l3m.l3mBouncingEclipses import BouncingElipses

class ChatMessage(QWidget):
    def __init__(self, message="", is_user=False):
        super().__init__()
        self.is_user = is_user
        self.setStyleSheet("background-color: rgba(255,0,0,0.1);") if is_user else self.setStyleSheet("background-color: rgba(255,0,255,0.1);")

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setContentsMargins(0,0,0,0)

        QTimer.singleShot(0, self.update_label_width)

        self.bubble = QFrame()
        self.bubble.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.bubble.setContentsMargins(0,0,0,0)
        self.bubble.setStyleSheet(f"""
            QFrame {{
                background-color: {"#4f4f4f" if is_user else "transparent"};
                border-radius: 6px;
                padding: {"8px" if is_user else "0px"};
            }}
        """)
        
        # Set up QLabel
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.label.setContentsMargins(0,0,0,0)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.label.setWordWrap(False)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                font-family: Consolas, monospace;
                font-size: 14pt;
                background-color: transparent;
            }
        """)
        self.label.setText(message)

        # Bubble layout
        self.bubble_layout = QVBoxLayout(self.bubble)
        self.bubble_layout.setContentsMargins(0, 0, 0, 0)
        self.bubble_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.bubble_layout.addWidget(self.label)

        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        if is_user:
            layout.addStretch(1)
            layout.addWidget(self.bubble)
        else:
            layout.addWidget(self.bubble)
            layout.addStretch(1)

    def append_text(self, text: str):
        current = self.label.text()
        self.label.setText(current + text)
    
    def update_label_width(self):
        parent = self.parentWidget()
        if not parent:
            return
        
        container_width = parent.width()
        max_bubble_width = int(container_width * 0.75) if self.is_user else container_width

        self.bubble.setMaximumWidth(max_bubble_width)
        self.label.setMaximumWidth(max_bubble_width)

        # Measure the actual rendered text width
        font_metrics = self.label.fontMetrics()
        text_width = font_metrics.horizontalAdvance(self.label.text())
        buffer = 20

        if text_width > (max_bubble_width-buffer):
            self.label.setWordWrap(True)
            self.label.setFixedWidth(max_bubble_width)
        else:
            self.label.setWordWrap(False)
            self.label.setMinimumWidth(0)

    
    def resizeEvent(self, event):
        self.update_label_width()

    
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