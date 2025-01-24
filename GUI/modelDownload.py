import os
from transformers import AutoModel, AutoTokenizer, AutoConfig
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QEvent

#Class Responsible for downloading the selected model
class DownloadModel:
    def __init__(self, model_name):
        self.model_name = model_name
        script_directory = os.path.dirname(os.path.abspath(__file__))
        models_folder = os.path.join(script_directory, "models")
        self.model_folder = os.path.join(models_folder, model_name.replace("/", "-"))

    def download_huggingface_model(self):
        # Ensure the save directory exists
        os.makedirs(self.model_folder, exist_ok=True)
        
        # Download the model, tokenizer, and config
        model = AutoModel.from_pretrained(self.model_name)
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        config = AutoConfig.from_pretrained(self.model_name)
        
        #Save the model, tokenizer, and config
        model.save_pretrained(self.model_folder)
        tokenizer.save_pretrained(self.model_folder)
        config.save_pretrained(self.model_folder)
        
        print(f"Model {self.model_name} successfully downloaded and saved in {self.model_folder}.")

#Class responsible for showing and selecting available models for download in the gui
class DownloadModelWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up the subwindow
        self.setWindowTitle("Floating Dialog")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setGeometry(300, 200, 300, 150)

        self.setStyleSheet("""
            QDialog {
                background-color: #2E3B4E;  /* Dark blue background */
                border: 2px solid #1ABC9C; /* Aqua border */
                border-radius: 10px;
            }
            QLabel {
                color: white;             /* White text */
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #1ABC9C; /* Aqua button background */
                color: white;              /* White button text */
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #16A085; /* Slightly darker aqua on hover */
            }
        """)

        # Add content to the floating dialog
        layout = QVBoxLayout()
        label = QLabel("List models for download here")
        close_button = QPushButton("Download")
        close_button.clicked.connect(self.close)

        layout.addWidget(label)
        layout.addWidget(close_button)
        self.setLayout(layout)

        if parent:
            parent.installEventFilter(self)

    def eventFilter(self, source, event):
        #Close the dialog if the user clicks outside.
        if event.type() == QEvent.Type.MouseButtonPress:
            if not self.geometry().contains(event.globalPosition().toPoint()):
                self.close()
        return super().eventFilter(source, event)

        
    