import os
from l3m.l3mDownloadModelGUI import DownloadModelGUI
from l3m.l3mLoadingIcon import AnimateIcon
from l3m.l3mSwitchModels import switchModel
from l3m.l3mDeleteModel import DeleteModel
from typing import Optional
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QMessageBox, QButtonGroup
from PyQt6.QtCore import Qt
from transformers import AutoModelForCausalLM, AutoTokenizer
from utils.path_utils import get_models_path
from utils.logging_utils import log_message

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

        # Create Download Model button
        self.downloadModelButton = QPushButton("Download Model")
        self.downloadModelButton.setStyleSheet(
            "background-color: #222222; color: white; font-size: 12pt; padding: 8px; border-radius: 5px;"
        )
        self.downloadModelButton.clicked.connect(self.downloadModelButtonClicked)

        # Create Delete Model button
        self.deleteModelButton = QPushButton("Delete Model")
        self.deleteModelButton.setStyleSheet(
            "background-color: #222222; color: white; font-size: 12pt; padding: 8px; border-radius: 5px;"
        )
        self.deleteModelButton.clicked.connect(self.deleteModelButtonClicked)

        # Add buttons to layout
        self.modelPanel.addLayout(self.modelButtonLayout)
        self.modelPanel.addWidget(self.downloadModelButton)
        self.modelPanel.addWidget(self.deleteModelButton)

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
            if len(finalAcro) == 2:
                if len(name) > 1:
                    finalAcro += name[len(name)-1].upper()
                else:
                    finalAcro += '_'
            if len(finalAcro) == 1:
                if len(name) > 2:
                    finalAcro += name[len(name)-2].upper()
                    finalAcro += name[len(name)-1].upper()
                else:
                    finalAcro += '__'

            acronyms[finalAcro] = name
        return acronyms

    # Get the names of all installed models
    def getModelNames(self):
        models_dir = get_models_path()
        
        if not os.path.exists(models_dir):
            print("Models directory does not exist!")
            return []  #return an empty list

        model_names = [name for name in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, name))]
        return model_names
    
    # Create model button for each model installed
    def createModelButtons(self, modelAcronyms: dict):
        # Create a QButtonGroup to manage the buttons
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)  # Ensure only one button is checked at a time

        for acronym, modelName in modelAcronyms.items():
            # Create Button and add to button group
            btn = QPushButton(str(acronym))
            btn.setCheckable(True)
            self.button_group.addButton(btn)

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
                }
            """)

            # Use lambda to pass parameters
            btn.clicked.connect(lambda checked, modelName=modelName: self.modelButtonClicked(modelName))

            # Add buttons to layout
            self.modelButtonLayout.addWidget(btn)

    # Recreate model buttons list to add new model button
    def refreshModelButtons(self):
        # Clear the old model buttons
        while self.modelButtonLayout.count():
            item = self.modelButtonLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Refresh list
        modelNames = self.getModelNames()
        modelDict = self.createAcronyms(modelNames)
        self.createModelButtons(modelDict)

    # Store current Model and Tokenizer in GUI so Prompt panel can access
    def modelButtonClicked(self, model_name: str):
        self.overlay = AnimateIcon()
        self.overlay.setWindowFlag(Qt.WindowType.Tool)
        self.overlay.show()
        self.Switch = switchModel(self.main_gui, model_name = model_name)
        self.Switch.signals.finished.connect(self.stop_animation)
        self.main_gui.pool.start(self.Switch)
        """
        model_name = str(model_name)
        models_dir = get_models_path()
        model_path = os.path.join(models_dir, model_name)
        #add loading spinner
        if not os.path.exists(model_path):
            print("Error: Model path does not exist!")
            return  # Prevent further errors

        self.main_gui.current_tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.main_gui.current_model = AutoModelForCausalLM.from_pretrained(model_path)
        self.main_gui.repaint()"""
    def stop_animation(self):
        if self.overlay:
            self.overlay.stopAnimation()
            self.overlay = None  # Clean up

    # Opens Download Model GUI
    def downloadModelButtonClicked(self):
        self.download_model_widget = DownloadModelGUI(self, self.main_gui)
        self.download_model_widget.show()

    # Deletes current selected model
    def deleteModelButtonClicked(self):
        if not self.main_gui.current_model:
            QMessageBox.warning(None, "Warning", "No model selected")
        else:
            confirm = QMessageBox.question(
                None,
                "Confirm Deletion",
                f"Are you sure you want to delete the model '{self.main_gui.current_model_name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

        if confirm == QMessageBox.StandardButton.Yes:
            delete_worker = DeleteModel(self.main_gui)
            delete_worker.signals.finished.connect(self.refreshModelButtons)
            self.main_gui.pool.start(delete_worker)

    # Updates model buttons after a new model is installed
    def onModelDownloadComplete(self, success: bool, error: Optional[dict] = None):
        if success:
            self.refreshModelButtons()
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