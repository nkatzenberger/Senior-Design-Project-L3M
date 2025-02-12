import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QEvent, QThreadPool
from PyQt6.QtGui import QTextCursor
from typing import Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
from l3mPromptModel import PromptModel
from l3mDownloadModelGUI import DownloadModelGUI
from l3mModelPanel import ModelPanel

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize Model
        self.prompt_model = None
        self.pool = QThreadPool.globalInstance()
        self.model_selected()  

        # Set up the window
        self.setWindowTitle("L3M GUI")
        self.setGeometry(100, 100, 1280, 720)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        panelLayout = QHBoxLayout() #overall layout
        self.leftPanel = QVBoxLayout() #everything at the left
        self.rightPanel = QVBoxLayout() #everything at the right

        self.leftPanel.setSpacing(10)
        self.leftPanel.setContentsMargins(10, 10, 10, 10)
        self.leftPanel.setAlignment(Qt.AlignmentFlag.AlignTop)


        #LEFT PANEL CHAT WINDOW STUFF ################################################################################

        # Create a layout specifically for the dynamically generated model buttons
        self.modelButtonLayout = QVBoxLayout()
        self.modelButtonLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.leftPanel.addLayout(self.modelButtonLayout)

        for i in ModelPanel.modelButtons:
            self.modelButtonLayout.addWidget(ModelPanel.modelButtons[i])

        self.leftPanel.addWidget(ModelPanel.downloadModelButton)

        #RIGHT PANEL CHAT WINDOW STUFF ################################################################################
        # Scrollable chat area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_container.setLayout(self.chat_layout)

        self.scroll_area.setWidget(self.chat_container)
        self.rightPanel.addWidget(self.scroll_area)

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
        self.rightPanel.addLayout(input_layout)

        # add layouts to central panel layout and add to main widget
        panelLayout.addLayout(self.leftPanel)
        panelLayout.addLayout(self.rightPanel)
        central_widget.setLayout(panelLayout)


#functions that are called with buttons etc..
    


    #Function for adding a new message in chat window

    def model_selected(self):
        # Gets path to selected model
        script_directory = os.path.dirname(os.path.abspath(__file__))
        model_name = "openai-community-gpt2" #hardcoded selected model for now
        model_path = os.path.join(script_directory, "models", model_name)
        #Initialize selected model
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)



    



#entry point for testing, code inside is how you would start GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec())

