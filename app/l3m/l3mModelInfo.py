from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QSizePolicy, QFrame, QAbstractScrollArea, QSpacerItem
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

class ModelInfo(QWidget):
    def __init__(self, main_gui, title="", parent=None):
        super().__init__(parent)
        # Store reference to main GUI and get metadata
        self.main_gui = main_gui
        self.metadata = self.main_gui.current_metadata if self.main_gui.current_metadata else {}
        self.title = self.metadata.get('Model ID', 'Select A Model')

        self.toggle_button = QWidget()
        self.toggle_button.setFixedHeight(50)
        self.toggle_button.setFixedWidth(250)

        toggle_layout = QHBoxLayout(self.toggle_button)
        toggle_layout.setContentsMargins(12,0,12,0)
        toggle_layout.setSpacing(0)

        self.label_title = QLabel(self.title)
        self.label_title.setStyleSheet("color: white; font-weight: bold; font-size: 12pt;")
        self.label_title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.label_title.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.label_arrow = QLabel("▶")
        self.label_arrow.setStyleSheet("color: white; font-size: 12pt;")
        self.label_arrow.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)

        toggle_layout.addWidget(self.label_title)
        toggle_layout.addWidget(self.label_arrow)

        self.expanded = False
        
        self.toggle_button.mousePressEvent = self.handle_click

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
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        main_layout.setAlignment(self.toggle_button, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.setContentLayout(self.create_model_info_section())
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)
        self.setFixedWidth(250)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            background-color: #1f1f1f;
        """)

    # Handle click event
    def handle_click(self, event):
        self.expanded = not self.expanded
        self.on_toggle()
        

    def setContentLayout(self, content_layout):
         # Wrap content in a widget and force it to take only necessary space
        content = QWidget()
        content.setLayout(content_layout)
        content.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        content.setMinimumHeight(0)
        content.setMaximumHeight(content.sizeHint().height())
        content.setContentsMargins(0,0,0,0)
        content.setStyleSheet("""
                QLabel {
                    color: #e2e2e2;
                    font-size: 10pt;
                    font-weight: bold;
                }
            """)

        # Important fix: setSizeAdjustPolicy ensures it only takes as much space as needed
        self.content_area.setWidget(content)
        self.content_area.setWidgetResizable(True)
        self.content_area.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

        # Reset height
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)

        # Update animation target to actual content height
        self.toggle_animation.setStartValue(0)
        self.toggle_animation.setEndValue(content.sizeHint().height())

    def on_toggle(self):
        arrow = "▼" if self.expanded else "▶"
        self.label_arrow.setText(arrow)

        if self.content_area.widget():
            full_height = self.content_area.widget().sizeHint().height()
            self.toggle_animation.setDirection(
                QPropertyAnimation.Direction.Forward if self.expanded else QPropertyAnimation.Direction.Backward
            )
            self.toggle_animation.setEndValue(full_height if self.expanded else 0)
            self.toggle_animation.start()

    def create_model_info_section(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(6)
        layout.setContentsMargins(12, 0, 12, 0)

        layout.addWidget(QLabel(f"Author: {self.metadata.get('Author', 'N/A')}"))
        layout.addWidget(QLabel(f"Model Type: {self.metadata.get('Pipeline Tag', 'N/A')}"))
        layout.addWidget(QLabel(f"Library: {self.metadata.get('Library Name', 'N/A')}"))
        layout.addWidget(QLabel(f"Size: {str(self.metadata.get('Used Storage (GB)', 'N/A'))} GB"))
        layout.addItem(QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        return layout
    
    def refresh(self):
        self.metadata = self.main_gui.current_metadata if self.main_gui.current_metadata else {}
        full_model_id = self.metadata.get("Model ID", "Select A Model")
        model_name = full_model_id.split('/')[-1]

        # Update the toggle button text
        self.expanded = False
        arrow = "▶"
        self.label_title.setText(model_name)
        self.label_title.setToolTip(model_name)
        self.label_arrow.setText(arrow)

        # Replace the content layout with the updated metadata
        content_layout = self.create_model_info_section()
        self.setContentLayout(content_layout)