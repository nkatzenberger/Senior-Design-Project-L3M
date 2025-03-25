from PyQt6.QtCore import QRunnable, pyqtSignal, QObject
import os
from transformers import AutoModelForCausalLM, AutoTokenizer

class WorkerSignal(QObject):
    finished = pyqtSignal()  # Signal to notify when work is done

class switchModel(QRunnable):

    def __init__(self, main_gui, callback=None, path=None, model_name = str, ):
        super().__init__()
        self.main_gui = main_gui
        self.callback = callback  # Function to call when work is done
        self.models_dir = path
        self.model_name = model_name
        self.signals = WorkerSignal()

    def run(self):
        model_path = os.path.join(self.models_dir, self.model_name)
        if not os.path.exists(model_path):
            print("Error: Model path does not exist!")
            return  # Prevent further errors

        self.main_gui.current_tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.main_gui.current_model = AutoModelForCausalLM.from_pretrained(model_path)
        self.main_gui.repaint()
        
        if self.callback:
            self.callback()
        self.signals.finished.emit() 
