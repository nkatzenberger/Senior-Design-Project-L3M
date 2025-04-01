from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QToolButton, QScrollArea, QSizePolicy, QFrame
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

class ModelInfo(QWidget):
    def __init__(self, main_gui, title="", parent=None):
        super().__init__(parent)
        # Store reference to main GUI and get metadata
        self.main_gui = main_gui
        self.metadata = self.main_gui.current_metadata
        title = self.metadata.get('model_id', 'N/A')

        self.toggle_button = QToolButton(text=title, checkable=True, checked=False)
        self.toggle_button.setStyleSheet("QToolButton { font-weight: bold; }")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.clicked.connect(self.on_toggle)

        self.content_area = QScrollArea()
        self.content_area.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)
        self.content_area.setFrameShape(QFrame.NoFrame)

        self.toggle_animation = QPropertyAnimation(self.content_area, b"maximumHeight")
        self.toggle_animation.setDuration(150)
        self.toggle_animation.setEasingCurve(QEasingCurve.InOutQuart)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.toggle_button)
        main_layout.addWidget(self.content_area)
        main_layout.setContentsMargins(0, 0, 0, 0)

    def setContentLayout(self, content_layout):
        content = QWidget()
        content.setLayout(content_layout)
        self.content_area.setWidget(content)
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)
        self.toggle_animation.setStartValue(0)
        self.toggle_animation.setEndValue(content.sizeHint().height())

    def on_toggle(self, checked):
        self.toggle_button.setArrowType(Qt.DownArrow if checked else Qt.RightArrow)
        if self.content_area.widget():
            full_height = self.content_area.widget().sizeHint().height()
            self.toggle_animation.setDirection(
                QPropertyAnimation.Forward if checked else QPropertyAnimation.Backward
            )
            self.toggle_animation.setEndValue(full_height if checked else 0)
            self.toggle_animation.start()

    def create_model_info_section(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Author: {self.metadata.get('Author', 'N/A')}"))
        layout.addWidget(QLabel(f"Model Type: {self.metadata.get('Pipeline Tag', 'N/A')}"))
        layout.addWidget(QLabel(f"Library: {self.metadata.get('Library Name', 'N/A')}"))
        layout.addWidget(QLabel(f"Size: {str(self.metadata.get('Used Storage (GB)', 'N/A'))} GB"))
        layout.addStretch()
        return layout