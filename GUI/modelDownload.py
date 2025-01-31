import os
import requests
import json
from dotenv import load_dotenv
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
        self.download_huggingface_model()

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

        #Get list of models
        self.model_ids = self.modelsAPI()

        # Set up the subwindow
        self.setWindowTitle("Download Model")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setGeometry(300, 200, 300, 150)

        self.setStyleSheet("""
            QDialog {
                background-color: #2E3B4E;
                border: 2px solid #1ABC9C;
                border-radius: 10px;
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #1ABC9C;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
        """)

        # Add content to the floating dialog
        layout = QVBoxLayout()


        # List Widget
        self.model_list = QListWidget()
        self.model_list.addItems(self.model_ids)  # Add model names to the list
        layout.addWidget(self.model_list)

        #Download Button
        download_button = QPushButton("Download")
        download_button.clicked.connect(self.download_selected_model)
        layout.addWidget(download_button)

        #Set Layout
        self.setLayout(layout)

        if parent:
            parent.installEventFilter(self)

    def eventFilter(self, source, event):
        #Close the dialog if the user clicks outside.
        if event.type() == QEvent.Type.MouseButtonPress:
            if not self.geometry().contains(event.globalPosition().toPoint()):
                self.close()
        return super().eventFilter(source, event)
    
    #Function for selecting model to download user to select model 
    def download_selected_model(self):
        selected_items = self.model_list.selectedItems()
        if selected_items:
            selected_model = selected_items[0].text()
            print(f"Downloading model: {selected_model}")
            DownloadModel(selected_model)
        else:
            print("No model selected!")
    
    #API Call to get and list models available for download
    def modelsAPI(self, sort_by=None):
        #valid sort keys are "likes", "downloads", "id", "trendingScore"

        #Load API Token
        load_dotenv()
        API_TOKEN = os.getenv('HUGGING_FACE_API_TOKEN')
        if not API_TOKEN:
            print("Error: API Token not found!")
            return []
        
        #API Call
        headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'
        }
        response = requests.get('https://huggingface.co/api/models', headers=headers)

        if response.status_code == 200:
            data = response.json()

            #Only returns text-generation models
            text_gen_models = [model for model in data if model.get("pipeline_tag") == "text-generation"]
            if not text_gen_models:
                print("No text-generation models found.")
                return []

            #Sorts models by sort_by
            if sort_by:
                text_gen_models = sorted(text_gen_models, key=lambda x: x.get(sort_by, 0), reverse=True)
            
            #Returns 1st 30 models
            return [model["id"] for model in text_gen_models[:30]]
        else:
            print(f'Error: {response.status_code}' - {response.text})
            return []

        
    