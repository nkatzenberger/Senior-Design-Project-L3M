import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject
from utils.path_utils import get_models_path
from utils.logging_utils import log_message

class WorkerSignal(QObject):
    finished = pyqtSignal()  # Signal to notify when work is done

class switchModel(QRunnable):

    def __init__(self, main_gui, model_name):
        super().__init__()
        self.main_gui = main_gui
        self.models_dir = get_models_path()
        self.model_name = model_name
        self.signals = WorkerSignal()

    def run(self):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_path = os.path.join(self.models_dir, self.model_name)
        if not os.path.exists(model_path):
            print("Error: Model path does not exist!")
            return  # Prevent further errors

        self.main_gui.current_tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.main_gui.current_model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16).to(device)
        self.main_gui.current_model_name = self.model_name
        self.main_gui.repaint()

        log_message("info", f'Current model is now {model_path}')
        log_message("info", f"Model loaded to {device}")

        self.signals.finished.emit() 
