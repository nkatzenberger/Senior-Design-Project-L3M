import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QEvent  # Import Qt for alignment flags
from PyQt6.QtGui import QTextCursor
from modelPrompt import PromptModel
from modelDownload import DownloadModelWidget

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize Model
        self.prompt_model = None
        #self.model_selected()  

        # Set up the window
        self.setWindowTitle("L3M GUI")
        self.setGeometry(100, 100, 1280, 720)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        panelLayout = QHBoxLayout() #overall layout
        leftPanel = QVBoxLayout() #everything at the left
        rightPanel = QVBoxLayout() #everything at the right

        leftPanel.setSpacing(10)
        leftPanel.setContentsMargins(10, 10, 10, 10)
        leftPanel.setAlignment(Qt.AlignmentFlag.AlignTop)
        #LEFT PANEL CHAT WINDOW STUFF ################################################################################
        modelDict = self.createAcronyms(self.getModelNames())
        modelButtons = self.assembleModelIcons(modelDict)
        leftPanel.addLayout(modelButtons)

        self.downloadModelButton = QPushButton("Download Model", self)
        self.downloadModelButton.setStyleSheet(
            "background-color: #222222; color: white; font-size: 12pt; padding: 8px; border-radius: 5px;"
        )
        self.downloadModelButton.clicked.connect(self.downloadModelButtonClicked)
        leftPanel.addWidget(self.downloadModelButton)



        #RIGHT PANEL CHAT WINDOW STUFF ################################################################################
        # Scrollable chat area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_container.setLayout(self.chat_layout)

        self.scroll_area.setWidget(self.chat_container)
        rightPanel.addWidget(self.scroll_area)

        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        send_button = QPushButton("Send", self)
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)

        #add the chat layout to the right panel
        rightPanel.addLayout(input_layout)

        # add layouts to central panel layout and add to main widget
        panelLayout.addLayout(leftPanel)
        panelLayout.addLayout(rightPanel)
        central_widget.setLayout(panelLayout)

#functions for assembling/updating the page dynamically

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
        group = QVBoxLayout()
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
            group.addWidget(btn)

        return group


#functions that are called with buttons etc..
    #TODO: function that is called when user selects an installed model from the left side-panel
    def onModelSelect(self,model:str):
        print(model)

    def downloadModelButtonClicked(self):
        #QMessageBox.information(self, "Button Clicked", "You clicked the left panel button!")
        self.download_model_widget = DownloadModelWidget(self)
        self.download_model_widget.show()

    #function that captures user text input
    def send_message(self):
        user_message = self.input_field.text().strip()
        if user_message:
            self.add_message(user_message, alignment=Qt.AlignmentFlag.AlignRight, user=True)
            self.respond_to_message(user_message) #THIS IS WHERE USER QUERRY GETS SENT TO MODEL
            self.input_field.clear()

    #Function for adding a new message in chat window
    def add_message(self, message, alignment, user=False):
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet(
            "background-color: #e1f5fe; padding: 8px; border-radius: 5px; font-size: 16pt; color: black;" if user else
            "background-color: #c8e6c9; padding: 8px; border-radius: 5px; font-size: 16pt; color: black;"
        )

        message_layout = QHBoxLayout()
        if alignment == Qt.AlignmentFlag.AlignRight:
            message_layout.addStretch()
            message_layout.addWidget(message_label)
        else:
            message_layout.addWidget(message_label)
            message_layout.addStretch()

        message_container = QFrame()
        message_container.setLayout(message_layout)

        self.chat_layout.addWidget(message_container)
        self.chat_container.adjustSize()
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

    #def model_selected(self):
        #Gets path to selected model
        #script_directory = os.path.dirname(os.path.abspath(__file__))
        #model_name = "openai-community-gpt2" #hardcoded selected model for now
        #model_path = os.path.join(script_directory, "models", model_name)

        # Initialize the model
        #self.prompt_model = PromptModel(model_path)

    def respond_to_message(self, message): 
        #if self.prompt_model is None:
            #raise ValueError("Model not initialized. Call 'model_selected' first.")
        #response = f'{self.prompt_model.generate_response(message)}'

        ##DUMMY RESPONSE FOR TESTING
        response = "Dummy Response!!"
        self.add_message(response, alignment=Qt.AlignmentFlag.AlignLeft, user=False)



#entry point for testing, code inside is how you would start GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec())

