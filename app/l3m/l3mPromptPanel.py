from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from l3m.l3mModelInfo import ModelInfo
from l3m.l3mPromptModel import PromptModel
from l3m.l3mChatHistory import ChatHistory


class PromptPanel(QWidget):
    def __init__(self, main_gui):
        super().__init__()
        self.main_gui = main_gui  # Store reference to GUI

        # Top-level horizontal layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # LEFT SIDE: just a QVBoxLayout, not a QWidget
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        # Model Info
        self.model_info = ModelInfo(main_gui)
        left_layout.addWidget(self.model_info)

        # Chat History (styled directly)
        self.chat_history = ChatHistory(main_gui)
        left_layout.addWidget(self.chat_history)

        # Right panel: full PromptModel
        self.prompt_model = PromptModel(main_gui)

        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.prompt_model, 1)

        # Set layout
        self.setLayout(main_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.layout().invalidate()
        self.layout().update()