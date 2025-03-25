import os
import shutil
import glob
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal
from huggingface_hub import HUGGINGFACE_HUB_CACHE
from utils.path_utils import get_models_path
from utils.logging_utils import log_message

class DeleteModelSignal(QObject):
    finished = pyqtSignal()

class DeleteModel(QRunnable):
    def __init__(self, main_gui):
        super().__init__()
        self.models_dir = get_models_path()
        self.model_name = main_gui.current_model_name
        self.signals = DeleteModelSignal()
    
    def run(self):
        if not self.model_name:
            log_message("info", f"No Model Selected for deletion")
            return
        
        # Delete from models folder
        model_path = os.path.join(self.models_dir, self.model_name)
        if os.path.exists(model_path):
            try:
                shutil.rmtree(model_path)
                log_message("info", f"Model '{model_path}' successfully deleted.")
                self.main_gui.current_model = None
                self.main_gui.current_tokenizer = None
                self.main_gui.current_model_name = None

            except Exception as e:
                log_message("error", f"Error deleting model: {e}")
        else:
            log_message("warning", f"Model path does not exist: {model_path}")

        # Delete from hugging face cache folder
        try:
            hf_cache_dir = os.path.expanduser(HUGGINGFACE_HUB_CACHE)
            matching_dirs = glob.glob(os.path.join(hf_cache_dir, "**", f"*{self.model_name}*"), recursive=True)

            for path in matching_dirs:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    log_message("info", f"Deleted from Hugging Face cache: {path}")
                elif os.path.isfile(path):
                    os.remove(path)
                    log_message("info", f"Deleted file from Hugging Face cache: {path}")

        except Exception as e:
            log_message("error", f"Error deleting from Hugging Face cache: {e}")

        self.signals.finished.emit()
