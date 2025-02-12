import os
from typing import Optional
from PyQt6.QtWidgets import QPushButton, QMessageBox
from l3mDownloadModelGUI import DownloadModelGUI

class ModelPanel():

    def __init__(self):
        modelDict = self.createAcronyms(self.getModelNames())
        self.modelButtons = self.assembleModelIcons(modelDict)


        self.downloadModelButton = QPushButton("Download Model", self)
        self.downloadModelButton.setStyleSheet(
            "background-color: #222222; color: white; font-size: 12pt; padding: 8px; border-radius: 5px;"
        )
        self.downloadModelButton.clicked.connect(self.downloadModelButtonClicked)

    #takes in array of model names then returns a dictionary of acronyms with associated model names, acronyms should be 3 characters long
        #dictionary in form of {acronym: modelName}
    def createAcronyms(self, modelNames: list[str]):
        #eventually this numbering logic will be replaced with real acronyms for the models
            #as of writing we chose to put the specifics of how this will be done to be decided later
        acronyms = {}
        for i,name in enumerate(modelNames):
            acronyms[i + 1] = name
        return acronyms
    
    #looks inside of model directory and gets names of subfolders associated with distinct models, returns array of names
    def getModelNames(self):
        if not os.path.exists('./models'):
            raise FileNotFoundError(f"The directory './models' does not exist.")
        
        return [name for name in os.listdir('./models') if os.path.isdir(os.path.join('./models', name))]
    
    #creates the icons for the left panel of the GUI based on the assembled acronyms
    def assembleModelIcons(self, modelAcronyms: dict):
        group = []
        for acronym, modelName in modelAcronyms.items():
            btn = QPushButton(str(acronym))
            btn.clicked.connect(lambda checked, a = modelName: self.onModelSelect(a))

            #button formatting
            btn.setToolTip(modelName)
            btn.setFixedSize(50,50)
            #TODO need to remove border on this style after model selecting is implemented
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
            """)

            #add to layout
            group.append(btn)

        return group
    
    #TODO: function that is called when user selects an installed model from the left side-panel
    def onModelSelect(self,model:str):
        print(model)

    def downloadModelButtonClicked(self):
        #QMessageBox.information(self, "Button Clicked", "You clicked the left panel button!")
        self.download_model_widget = DownloadModelGUI(self)
        self.download_model_widget.show()

    def refreshModelList(self):
        modelDict = self.createAcronyms(self.getModelNames())  # Refresh model list
        modelButtons = self.assembleModelIcons(modelDict)
        
        # Clear the old model buttons and update the left panel
        while self.modelButtonLayout.count():
            item = self.modelButtonLayout.takeAt(0)  # Get the first item
            if item.widget():
                item.widget().deleteLater()
        self.modelButtonLayout.addLayout(modelButtons)

    def onModelDownloadComplete(self, success: bool, error: Optional[dict] = None):
        if success: # Refresh list of available models
            self.refreshModelList()
        else: # Display error
            QMessageBox.warning(
                self, 
                "Download Failed", 
                f"Code: {error.get('code', 'N/A')}\nKind: {error.get('kind', 'Unknown Error')}\nDetails: {error.get('message', 'No details')}"
            )