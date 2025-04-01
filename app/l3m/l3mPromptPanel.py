from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from l3m.l3mModelInfo import ModelInfo
from l3m.l3mPromptModel import PromptModel


class PromptPanel(QWidget):
    def __init__(self, main_gui):
        super().__init__()
        self.main_gui = main_gui  # Store reference to GUI

        # Top-level horizontal layout: left vs right
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Left panel: model info + placeholder
        left_panel = QVBoxLayout()
        left_panel.setSpacing(10)

        self.model_info = ModelInfo(main_gui)
        model_info_section = self.model_info.create_model_info_section()
        self.model_info.setContentLayout(model_info_section)
        left_panel.addWidget(self.model_info)

        # Placeholder at bottom-left
        self.placeholder = QWidget()
        left_panel.addWidget(self.placeholder)

        # Right panel: full PromptModel
        self.prompt_model = PromptModel(main_gui)

        # Add left and right to main layout
        main_layout.addLayout(left_panel, 1)  # 1/6 width
        main_layout.setAlignment(left_panel, Qt.AlignmentFlag.AlignTop)          
        main_layout.addWidget(self.prompt_model, 5)     # 5/6 width

        # Set layout
        self.setLayout(main_layout)