import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QEvent, QThreadPool
from l3mDownloadModel import DownloadModel
from l3mHuggingFaceModelsAPI import HuggingFaceModelsAPI

class DownloadModelGUI(QDialog):
    def __init__(self, model_panel, main_gui, parent=None):
        super().__init__(parent)
        # Create references to other classes so it can make updates to them
        self.main_gui = main_gui
        self.model_panel = model_panel

        # Connect event filter to mainGUI
        main_gui.installEventFilter(self)

        # Initialize threadpool for api to use
        self.pool = QThreadPool.globalInstance()

        #Initialize variables and get default list of models for when this gui opens
        self.query = None
        self.download_model_thread = None

        #Set up window
        self.setWindowTitle("Download Model")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setGeometry(400, 267, 400, 200)
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

        # Set layout for window
        layout = QVBoxLayout()

        # Create search bar
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Enter search query...")
        self.search_input.returnPressed.connect(self.searchForModel)

        # Create list for models
        self.model_list = QListWidget()

        # Create download button
        download_button = QPushButton("Download")
        download_button.clicked.connect(self.downloadSelectedModel)

        # Add elements to window
        layout.addWidget(self.search_input)
        layout.addWidget(self.model_list)
        layout.addWidget(download_button)
        self.setLayout(layout)


        # Get default list of models
        self.searchForModel()


    #Triggers API to run on thread
    def searchForModel(self):
        self.query = self.search_input.text().strip()
        # Start QRunnable and set signal listener to update when response comes back
        self.search = HuggingFaceModelsAPI(self.query)
        self.search.signals.result.connect(self.updateModelList)
        self.pool.start(self.search)

    #Updates list everytime thread emits the API is done
    def updateModelList(self, model_data):
        model_names = [model["Model Name"] for model in model_data if "Model Name" in model]
        self.model_list.addItems(model_names)

    #Allow users to select model from the list and install them
    def downloadSelectedModel(self):
        selected_items = self.model_list.selectedItems()
        if selected_items:
            selected_model = selected_items[0].text()
            self.download_model_thread = DownloadModel(selected_model)
            self.download_model_thread.model_download_complete.connect(self.model_panel.onModelDownloadComplete)
            self.download_model_thread.start()
            #TODO:
            #disable button
            #update button to say downloading...
            #wait 2 seconds
            #self.close()
        else:
            print("No model selected!")

    #Closes GUI if user clicks outside of its geometry
    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if not self.geometry().contains(event.globalPosition().toPoint()):
                self.close()
        return super().eventFilter(source, event)

