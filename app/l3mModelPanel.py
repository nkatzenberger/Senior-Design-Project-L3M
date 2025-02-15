import os
from typing import Optional
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from l3mDownloadModelGUI import DownloadModelGUI
from transformers import AutoModelForCausalLM, AutoTokenizer

class ModelPanel():
    def __init__(self, main_gui):
        self.main_gui = main_gui # Store reference to GUI
        self.tokenizer = None
        self.model = None

        # Define Layout for Model Panel
        self.modelPanel = QVBoxLayout()

        # Config items within Model Panel
        self.modelPanel.setSpacing(10)
        self.modelPanel.setContentsMargins(10, 10, 10, 10)
        self.modelPanel.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create layout for Model Buttons within Model Panel
        self.modelButtonLayout = QVBoxLayout()
        self.modelButtonLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Create model buttons
        modelDict = self.createAcronyms(self.getModelNames())
        self.createModelButtons(modelDict)

        # Create Download Model button
        self.downloadModelButton = QPushButton("Download Model")
        self.downloadModelButton.setStyleSheet(
            "background-color: #222222; color: white; font-size: 12pt; padding: 8px; border-radius: 5px;"
        )
        self.downloadModelButton.clicked.connect(self.downloadModelButtonClicked)

        # Add download buttons to layout
        self.modelPanel.addLayout(self.modelButtonLayout)
        self.modelPanel.addWidget(self.downloadModelButton)

    #Creates acronyms for model buttons
    def createAcronyms(self, modelNames: list[str]):
        #TODO: Replace numeric logic with real acronyms
        acronyms = {}
        for i,name in enumerate(modelNames):
            acronyms[i + 1] = name
        return acronyms
    
    # Get the names of all installed models
    def getModelNames(self):
        #TODO: Create models folder if one doesn't already exist.
        if not os.path.exists('./models'):
            raise FileNotFoundError(f"The directory './models' does not exist.")
        
        return [name for name in os.listdir('./models') if os.path.isdir(os.path.join('./models', name))]
    
    # Create model button for each model installed
    def createModelButtons(self, modelAcronyms: dict):
        for acronym, modelName in modelAcronyms.items():
            # Create Button
            btn = QPushButton(str(acronym))
            btn.clicked.connect(lambda: self.modelButtonClicked(modelName))

            # Format button
            btn.setToolTip(modelName)
            btn.setFixedSize(50,50)
            btn.setStyleSheet("""
                QPushButton{
                    background-color: gray;
                    border-radius: 25px;
                    border: 2px solid #27F2FA;
                    font-size: 14pt;
                    font-weight:bold;
                    color: black;   
                    text-align:center;
                }
                
                QToolTip {
                }
            """)#TODO need to remove border on this style after model selecting is implemented

            # Add button to model button layout
            self.modelButtonLayout.addWidget(btn)

    # Recreate model buttons list to add new model button
    def refreshModelButtons(self):
        # Clear the old model buttons
        while self.modelButtonLayout.count():
            item = self.modelButtonLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Refresh list
        modelDict = self.createAcronyms(self.getModelNames())
        self.createModelButtons(modelDict)

    # In main GUI, curr_tokenizer and curr_model inherit tokenizer and model, 
    # then passes to prompt so prompt uses current selected model.
    def modelButtonClicked(self, model_name:str):
        print(model_name)
        
        #Sets tokenizer and model to model clicked
        script_directory = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_directory, "models", model_name)
        self.main_gui.current_tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.main_gui.current_model = AutoModelForCausalLM.from_pretrained(model_path)

    # Opens Download Model GUI
    def downloadModelButtonClicked(self):
        self.download_model_widget = DownloadModelGUI(self, self.main_gui)
        self.download_model_widget.show()

    # Updates model buttons after a new model is installed
    def onModelDownloadComplete(self, success: bool, error: Optional[dict] = None):
        if success:
            self.refreshModelButtons()
        else:
            QMessageBox.warning(
                None, 
                "Download Failed", 
                f"Code: {error.get('code', 'N/A')}\nKind: {error.get('kind', 'Unknown Error')}\nDetails: {error.get('message', 'No details')}"
            )