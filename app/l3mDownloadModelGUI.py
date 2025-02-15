import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QEvent, QThreadPool
from l3mDownloadModel import DownloadModel
from l3mHuggingFaceModelsAPI import HuggingFaceModelsAPI

class DownloadModelGUI(QDialog):
    def __init__(self, model_panel, main_gui, parent=None):
        super().__init__(parent)
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

        if main_gui:
            main_gui.installEventFilter(self)
        self.query = None
        self.download_model_thread = None
        self.setupUi()
        self.pool = QThreadPool.globalInstance()
        self.searchForModel()
        self.main_gui = main_gui
        self.model_panel = model_panel

    def setupUi(self):
        layout = QVBoxLayout()
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Enter search query...")
        self.search_input.returnPressed.connect(self.searchForModel)
        layout.addWidget(self.search_input)

        self.model_list = QListWidget()
        layout.addWidget(self.model_list)

        download_button = QPushButton("Download")
        download_button.clicked.connect(self.downloadSelectedModel)
        layout.addWidget(download_button)
        self.setLayout(layout)

    #Triggers API to run on thread
    def searchForModel(self):
        self.query = self.search_input.text().strip()
        # Start QRunnable and set signal listener to update when response comes back
        self.search = HuggingFaceModelsAPI(self.query)
        self.search.signals.result.connect(self.updateModelList)
        self.pool.start(self.search)

    #Updates list everytime thread emits the API is done
    def updateModelList(self, model_ids):
        self.model_list.clear()
        self.model_list.addItems(model_ids)

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

