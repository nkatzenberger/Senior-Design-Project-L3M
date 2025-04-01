import os
import shutil
import json
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal
from utils.path_utils import PathManager
from utils.logging_utils import LogManager

class DeleteModelSignal(QObject):
    finished = pyqtSignal()

class DeleteModel(QRunnable):
    def __init__(self, main_gui):
        super().__init__()
        self.main_gui = main_gui
        self.signals = DeleteModelSignal()
        self.models_dir = PathManager.get_models_path()
        model_id = self.main_gui.current_metadata.get("Model ID", "")
        self.model_folder_name = model_id.replace("/", "-")
    
    def run(self):
        try:
            # Get Model ID from metadata
            model_path = os.path.join(self.models_dir, self.model_folder_name)

            metadata = self.main_gui.current_metadata
            model_id = metadata.get("Model ID", "")

            if not model_id or "/" not in model_id:
                LogManager.log("error", f"Invalid or missing model ID in metadata: {model_id}")
                return

            author, model_name = model_id.split("/", 1)
            
            # 1. Delete the model folder itself
            if os.path.exists(model_path):
                shutil.rmtree(model_path)
                LogManager.log("info", f"Deleted model folder: {model_path}")
            
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
                    LogManager.log("info", f"Deleted: {path}")

        except Exception as e:
            LogManager.log("error", f"Error during deletion: {e}")
        
        self.main_gui.current_model = None
        self.main_gui.current_tokenizer = None
        self.main_gui.current_model_name = None

        self.signals.finished.emit()
