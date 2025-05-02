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
        self.model_name = model_name
        self.models_dir = PathManager.get_models_path()
        self.signals = WorkerSignal()
        self.model_path = os.path.join(self.models_dir, self.model_name)

    def run(self):
        try:
            LogManager.log("info", f"Starting model switch to: {self.model_name}")
            self._unload_current_model()
            if not self._validate_model_path():
                return

            tokenizer = self._load_tokenizer()
            model = self._load_model()

            if tokenizer is None or model is None:
                return

            self._inject_pad_token_if_needed(tokenizer, model)
            self._set_current_model(tokenizer, model)
            self._load_metadata()
            self.main_gui.repaint()
            self.signals.finished.emit()
        except Exception as e:
            LogManager.log("critical", f"Unhandled exception during model switch: {e}")

    def _unload_current_model(self):
        if self.main_gui.current_model:
            try:
                LogManager.log("info", "Waiting for running tasks to complete before switching model...")
                self.main_gui.pool.waitForDone(3000)
                del self.main_gui.current_model
                del self.main_gui.current_tokenizer
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                LogManager.log("info", "Unloaded existing model")
            except Exception as e:
                LogManager.log("error", f"Error unloading model: {e}")

    def _validate_model_path(self):
        if not os.path.exists(self.model_path):
            LogManager.log("error", f"Model path does not exist: {self.model_path}")
            return False
        return True

    def _load_tokenizer(self):
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            LogManager.log("info", f"Loaded tokenizer from {self.model_path}")
            return tokenizer
        
        except Exception as e:
            LogManager.log("error", f"Failed to load tokenizer: {e}")
            return None

    def _load_model(self):
        try:
            LogManager.log("debug", "Preparing to call AutoModelForCausalLM.from_pretrained")

            model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=DeviceManager.get_best_dtype(),
                low_cpu_mem_usage=True,
                device_map="auto"
            )

            LogManager.log("info", f"Loaded model from {self.model_path}")
            LogManager.log("info", f"Model device: {next(model.parameters()).device}")
            return model
        
        except Exception as e:
            LogManager.log("error", f"Failed to load model: {e}")
            return None

    def _inject_pad_token_if_needed(self, tokenizer, model):
        if tokenizer.pad_token is None:
            try:
                LogManager.log("info", "Pad token is None — injecting...")
                tokenizer.add_special_tokens({'pad_token': '[PAD]'})
                if hasattr(model, "resize_token_embeddings"):
                    model.resize_token_embeddings(len(tokenizer))
                    if hasattr(model, "tie_weights"):
                        model.tie_weights()
                LogManager.log("info", "Injected pad token and updated model.")
            except Exception as e:
                LogManager.log("error", f"Failed to inject pad token: {e}")

    def _set_current_model(self, tokenizer, model):
        self.main_gui.current_tokenizer = tokenizer
        self.main_gui.current_model = model

    def _load_metadata(self):
        metadata_path = os.path.join(self.model_path, "metadata.json")
        metadata = {}
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                LogManager.log("info", f"Loaded metadata: {metadata}")
            except Exception as e:
                LogManager.log("error", f"Failed to load metadata: {e}")
        else:
            LogManager.log("warning", "No metadata.json found.")
        self.main_gui.current_metadata = metadata
