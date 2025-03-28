import os
import shutil
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
            # Get Model ID from metadata
            model_path = os.path.join(self.models_dir, self.model_folder_name)

            metadata = self.main_gui.current_metadata
            model_id = metadata.get("Model ID", "")

            if not model_id or "/" not in model_id:
                log_message("error", f"Invalid or missing model ID in metadata: {model_id}")
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
