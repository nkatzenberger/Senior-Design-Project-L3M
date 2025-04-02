import os
import gc
import json
import torch
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject
from transformers import AutoModelForCausalLM, AutoTokenizer
from utils.device_utils import DeviceManager
from utils.path_utils import PathManager
from utils.logging_utils import LogManager


class WorkerSignal(QObject):
    finished = pyqtSignal()  # Signal to notify when work is done

class switchModel(QRunnable):

    def __init__(self, main_gui, model_name):
        super().__init__()
        self.main_gui = main_gui
        self.models_dir = PathManager.get_models_path()
        self.model_name = model_name
        self.signals = WorkerSignal()

    def run(self):
        # Unload existing model
        if self.main_gui.current_model:
            LogManager.log("info", "Waiting for running tasks to complete before switching model...")
            self.main_gui.pool.waitForDone(3000)  # waits up to 3s

            del self.main_gui.current_model
            del self.main_gui.current_tokenizer
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            LogManager.log("info", 'Unloaded existing model')

        # Error check models folder
        model_path = os.path.join(self.models_dir, self.model_name)
        if not os.path.exists(model_path):
            LogManager.log("error", 'Model path doesn\'t exist')
            return

        # Load new model + tokenizer
        self.main_gui.current_tokenizer = AutoTokenizer.from_pretrained(model_path)
        model_selected = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=DeviceManager.get_best_dtype(),
            low_cpu_mem_usage=True,
            device_map="auto"
        )

        # Inject pad token early if needed
        if self.main_gui.current_tokenizer.pad_token is None:
            LogManager.log("info", "Pad token is None — injecting during model switch")
            try:
                self.main_gui.current_tokenizer.add_special_tokens({'pad_token': '[PAD]'})
                if hasattr(model_selected, "resize_token_embeddings"):
                    model_selected.resize_token_embeddings(len(self.main_gui.current_tokenizer))
                    if hasattr(model_selected, "tie_weights"):
                        model_selected.tie_weights()
                LogManager.log("info", "Pad token injected and model updated.")
            except Exception as e:
                LogManager.log("error", f"Failed to inject pad token during model switch: {e}")

        '''
        # Try torch.compile for performance boost
        try:
            model_selected = torch.compile(model_selected)
            LogManager.log("info", "Compiled model with torch.compile()")
        except Exception as e:
            LogManager.log("warning", "Could not compile model: {e}")
        '''

        self.main_gui.current_model = model_selected

        LogManager.log("info", f'Current model is now {model_path}')
        LogManager.log("info", f"Model loaded to device: {next(model_selected.parameters()).device}")

        # Load metadata
        metadata = {}
        metadata_path = os.path.join(model_path, "metadata.json")
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                    LogManager.log("info", f"Loaded metadata: {metadata}")
            except Exception as e:
                LogManager.log("error", f"Failed to load metadata: {e}")
        
        self.main_gui.current_metadata = metadata

        self.main_gui.repaint()
        self.signals.finished.emit() 
