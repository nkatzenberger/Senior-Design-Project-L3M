from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt

class ChatHistory(QWidget):
    def __init__(self, main_gui):
        super().__init__()
        self.main_gui = main_gui

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 10, 12, 10)
        main_layout.setSpacing(6)

        title = QLabel('History')
        title.setObjectName('History')
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        main_layout.addWidget(title)
        main_layout.addStretch(1)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.setMinimumHeight(150)
        self.setFixedWidth(250)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("chatHistory")
        self.setStyleSheet("""
            #chatHistory {
                background-color: #1f1f1f;
                border: 2px solid transparent;
                border-top-color: #444444;
            }
            QLabel#History {
                    color: white;
                    font-size: 12pt;
                    font-weight: bold;
                }
        """)