import sys
import os
from l3m.l3mModelPanel import ModelPanel
from l3m.l3mPromptPanel import PromptPanel
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThreadPool
from typing import Optional

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        #Initialize thread pool for PromptModel and HuggingFaceModelsAPI
        self.pool = QThreadPool.globalInstance() 

        # Initialize ModelPanel
        self.ref_model_panel = ModelPanel(self) # Pass reference to GUI so ModelPanel can update GUI

        # Initialize PromptPanel
        self.ref_prompt_panel = PromptPanel(self) # Pass reference to GUI so PromptPanel can update GUI

        # Store Global Variables
        self.current_tokenizer = None
        self.current_model = None

        # Set up the main window
        self.setWindowTitle("L3M GUI V 1.0.0")
        self.setGeometry(100, 100, 1280, 720)

        # Central widget that holds all UI Elements
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Overall layout within central window
        panelLayout = QHBoxLayout() 

        # Add layouts to central panel layout
        panelLayout.addLayout(self.ref_model_panel.modelPanel)
        panelLayout.addLayout(self.ref_prompt_panel.promptPanel)
        central_widget.setLayout(panelLayout)
