import os
from typing import Optional
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QMessageBox, QButtonGroup
from PyQt6.QtCore import Qt
from l3mDownloadModelGUI import DownloadModelGUI
from transformers import AutoModelForCausalLM, AutoTokenizer

class ModelPanel():
    def __init__(self, main_gui):
        self.main_gui = main_gui # Store reference to GUI

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
        print(modelDict)
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
        acronyms = {}
        for name in modelNames:
            # Initialize acronym with the first character
            finalAcro = name[0].upper()

            # Add additional characters after special delimiters
            delimiters = ['-', '_', '/']
            for i in range(1, len(name)):
                if len(finalAcro) >= 3:
                    break
                if name[i-1] in delimiters:
                    finalAcro += name[i].upper()

            # Ensure the acronym is at least 3 characters long
            while len(finalAcro) < 3:
                finalAcro += name[len(finalAcro)].upper()

            acronyms[finalAcro] = name
        print("Acronyms created:", acronyms)
        return acronyms

    # Get the names of all installed models
    def getModelNames(self):
        #TODO: Create models folder if one doesn't already exist.
        models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
        if not os.path.exists(models_dir):
            raise FileNotFoundError(f"The directory './models' does not exist.")
        
        return [name for name in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, name))]
    
    # Create model button for each model installed
    def createModelButtons(self, modelAcronyms: dict):
        # Create a QButtonGroup to manage the buttons
        self.button_group = QButtonGroup()  # Store in self to prevent garbage collection
        self.button_group.setExclusive(True)  # Ensure only one button is checked at a time

        for acronym, modelName in modelAcronyms.items():
            # Create a checkable button
            btn = QPushButton(str(acronym))
            btn.setCheckable(True)  # Allows toggling
            self.button_group.addButton(btn)  # Add to group

            # Apply styles
            btn.setToolTip(modelName)
            btn.setFixedSize(50, 50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: gray;
                    border-radius: 25px;
                    border: none;
                    font-size: 14pt;
                    font-weight: bold;
                    color: black;
                    text-align: center;
                }
                QPushButton:checked {
                    border: 2px solid #27F2FA;
                    background-color: lightblue;
                }
            """)

            # Helper function to handle button click
            def handleButtonClick(modelName, btn):
                self.modelButtonClicked(modelName)
                self.main_gui.repaint()  # Force UI update

            # Use lambda to pass parameters
            btn.clicked.connect(lambda checked, modelName=modelName, btn=btn: handleButtonClick(modelName, btn))

            self.modelButtonLayout.addWidget(btn)

        # Ensure the first button is selected by default (optional)
        if self.button_group.buttons():
            self.button_group.buttons()[0].setChecked(True)

    # Recreate model buttons list to add new model button
    def refreshModelButtons(self):
        # Clear the old model buttons
        while self.modelButtonLayout.count():
            item = self.modelButtonLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Refresh list
        modelNames = self.getModelNames()
        print(modelNames)
        modelDict = self.createAcronyms(modelNames)
        print(modelDict)
        self.createModelButtons(modelDict)
        print("createModelButtons")

    # Store current Model and Tokenizer in GUI so Prompt panel can access
    def modelButtonClicked(self, model_name:str):
        model_name = str(model_name)
        print(model_name)
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
            print("refresh")
        else:
            if not error:
                code = "N/A"
                kind = "Unknown Error"
                message = "No details provided."

            # Handle the case where error is a dict
            if isinstance(error, dict):
                code = error.get('code', 'N/A')
                kind = error.get('kind', 'Unknown Error')
                message = error.get('message', 'No details')

            QMessageBox.warning(
                None, 
                "Download Failed", 
                f"Code: {code}\nKind: {kind}\nDetails: {message}"
            )