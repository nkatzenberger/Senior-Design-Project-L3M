import sys
from tqdm.auto import tqdm
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from transformers.utils import logging as hf_logging
class StreamRedirector(QObject):
    new_text = pyqtSignal(str)

    def write(self, text):
        if text.strip():
            self.new_text.emit(text)

    def flush(self):
        pass
""""
class QTextEditTqdmOutput:
    def __init__(self, emit_func):
        self.emit = emit_func

    def write(self, s):
        # Detect and replace the progress bar
        if '\r' in s:  # If there's a carriage return (typical of tqdm)
            progress = s.split('\r')[-1].strip()  # Get the last progress bar string
            progress = progress.strip()
            # Replace # with solid █ blocks (or any other character you'd like)
            progress_bar = progress.replace('#', '█')
            self.emit(progress)
        else:
            self.emit(s.strip())
    def flush(self):
        pass
"""
class DownloadWindow(QWidget):
    download_complete = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Model Installer")
        self.resize(600, 400)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        font = QFont("Cascadia Code", 10)  # Monospaced fonts are best for progress bars
        self.text_edit.setFont(font)
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
        
        self.redirector = StreamRedirector()
        self.redirector.new_text.connect(self.text_edit.append)
        sys.stdout = self.redirector
        sys.stderr = self.redirector
        
        self.download_complete.connect(self.close)
        