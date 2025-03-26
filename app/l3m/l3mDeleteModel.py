import os
import shutil
import glob
import json
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal
from utils.path_utils import get_models_path
from utils.logging_utils import log_message

class DeleteModelSignal(QObject):
    finished = pyqtSignal()

class DeleteModel(QRunnable):
    def __init__(self, main_gui):
        super().__init__()
        self.main_gui = main_gui
        self.signals = DeleteModelSignal()
        self.models_dir = get_models_path()
        self.model_folder_name = self.main_gui.current_model_name 
    
    def run(self):
        try:
            # Reconstruct full model path
            model_path = os.path.join(self.models_dir, self.model_folder_name)
            metadata_path = os.path.join(model_path, "metadata.json")

            if not os.path.exists(metadata_path):
                log_message("error", f"No metadata.json found in: {model_path}")
                return
            
            # Read original model ID from metadata
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                model_id = metadata.get("Model ID", "")
                if "/" not in model_id:
                    log_message("error", f"Invalid model ID: {model_id}")
                    return
                author, model_name = model_id.split("/", 1)
            
            # 1. Delete the model folder itself
            if os.path.exists(model_path):
                shutil.rmtree(model_path)
                log_message("info", f"Deleted model folder: {model_path}")
            
            # 2. Delete Hugging Face cached folders
            hf_cache_dir = os.path.expanduser(os.getenv("HF_HOME", "~/.cache/huggingface"))
            cache_paths = [
                os.path.join(hf_cache_dir, "hub", f"models--{author}--{model_name}"),
                os.path.join(hf_cache_dir, "hub", ".locks", f"models--{author}--{model_name}")
            ]
            
            for path in cache_paths:
                if os.path.exists(path):
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                    log_message("info", f"Deleted: {path}")

        except Exception as e:
            log_message("error", f"Error during deletion: {e}")
        
        self.main_gui.current_model = None
        self.main_gui.current_tokenizer = None
        self.main_gui.current_model_name = None

        self.signals.finished.emit()
