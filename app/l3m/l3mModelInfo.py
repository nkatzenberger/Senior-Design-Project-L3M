from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QToolButton, QScrollArea, QSizePolicy, QFrame, QAbstractScrollArea
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

class ModelInfo(QWidget):
    def __init__(self, main_gui, title="", parent=None):
        super().__init__(parent)
        # Store reference to main GUI and get metadata
        self.main_gui = main_gui
        self.metadata = self.main_gui.current_metadata if self.main_gui.current_metadata else {}
        title = self.metadata.get('Model ID', 'Select A Model')

        self.toggle_button = QToolButton(text=title, checkable=True, checked=False)
        self.toggle_button.setStyleSheet("QToolButton { font-weight: bold; }")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.ArrowType.RightArrow)
        self.toggle_button.clicked.connect(self.on_toggle)

        self.content_area = QScrollArea()
        self.content_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.content_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.content_area.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        self.content_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)
        self.content_area.setFrameShape(QFrame.Shape.NoFrame)

        self.toggle_animation = QPropertyAnimation(self.content_area, b"maximumHeight")
        self.toggle_animation.setDuration(150)
        self.toggle_animation.setEasingCurve(QEasingCurve.Type.InOutQuart)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.toggle_button)
        main_layout.addWidget(self.content_area)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(self.toggle_button, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        

    def setContentLayout(self, content_layout):
         # Wrap content in a widget and force it to take only necessary space
        content = QWidget()
        content.setLayout(content_layout)
        content.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum))
        content.setMinimumHeight(0)
        content.setMaximumHeight(content.sizeHint().height())

        # ✅ Important fix: setSizeAdjustPolicy ensures it only takes as much space as needed
        self.content_area.setWidget(content)
        self.content_area.setWidgetResizable(True)
        self.content_area.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)  # 🔥

        # Reset height
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)

        # Update animation target to actual content height
        self.toggle_animation.setStartValue(0)
        self.toggle_animation.setEndValue(content.sizeHint().height())

    def on_toggle(self, checked):
        self.toggle_button.setArrowType(Qt.ArrowType.DownArrow if checked else Qt.ArrowType.RightArrow)
        if self.content_area.widget():
            full_height = self.content_area.widget().sizeHint().height()
            self.toggle_animation.setDirection(
                QPropertyAnimation.Direction.Forward if checked else QPropertyAnimation.Direction.Backward
            )
            self.toggle_animation.setEndValue(full_height if checked else 0)
            self.toggle_animation.start()

    def create_model_info_section(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(QLabel(f"Author: {self.metadata.get('Author', 'N/A')}"))
        layout.addWidget(QLabel(f"Model Type: {self.metadata.get('Pipeline Tag', 'N/A')}"))
        layout.addWidget(QLabel(f"Library: {self.metadata.get('Library Name', 'N/A')}"))
        layout.addWidget(QLabel(f"Size: {str(self.metadata.get('Used Storage (GB)', 'N/A'))} GB"))
        return layout
    
    def refresh(self):
        self.metadata = self.main_gui.current_metadata if self.main_gui.current_metadata else {}

        # Extract the model_id from metadata
        full_model_id = self.metadata.get("Model ID", "Select A Model")

        # Get the substring after the last '/'
        model_name = full_model_id.split('/')[-1]

        # Update the toggle button text
        self.toggle_button.setText(model_name)

        # Replace the content layout with the updated metadata
        content_layout = self.create_model_info_section()
        self.setContentLayout(content_layout)

        # Optional: keep it collapsed when refreshed
        self.toggle_button.setChecked(False)
        self.content_area.setMaximumHeight(0)