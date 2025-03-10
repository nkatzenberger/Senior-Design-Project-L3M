import os
import shutil
from PyQt6.QtCore import QThread, pyqtSignal
from transformers import AutoModel, AutoTokenizer, AutoConfig
from utils.path_utils import get_models_path
from utils.logging_utils import log_message

class DownloadModel(QThread):
    model_download_complete = pyqtSignal(bool, str, dict)

    def __init__(self, model_name):
        super(DownloadModel, self).__init__()
        self._is_running = True

        #Set model install destination
        self.model_name = model_name
        models_dir = get_models_path()
        self.model_folder = os.path.join(models_dir, model_name.replace("/", "-"))

    def run(self):
        try:
            # Ensure the save directory exists
            os.makedirs(self.model_folder, exist_ok=True)
            log_message("info", f"Downloading model: {self.model_name}")

            if not self._is_running: # Stop before starting download
                return
            
            # Download the model, tokenizer, and config
            model = AutoModel.from_pretrained(
                self.model_name, 
                low_cpu_mem_usage=True, # Prevents entire model being loaded into ram
                device_map="auto",  # Automatically offloads model parts to disk if needed
                trust_remote_code=True #allows more models to be downloaded
            )

            if not self._is_running: # Stop after download
                return
            
            # Download the model, tokenizer, and config
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            config = AutoConfig.from_pretrained(self.model_name)

            if not self._is_running: # Stop before saving
                return
            
            #Save the model, tokenizer, and config
            model.save_pretrained(self.model_folder)
            tokenizer.save_pretrained(self.model_folder)
            config.save_pretrained(self.model_folder)
            
            log_message("info", f"Model {self.model_name} saved at {self.model_folder}")

            # Emit download was successful to GUI
            self.model_download_complete.emit(True, self.model_name, {})

        except Exception as e:
            log_message("error", f"Failed to download {self.model_name}: {e}")

            # If the folder exists and is partially downloaded, delete it
            if os.path.exists(self.model_folder):
                shutil.rmtree(self.model_folder) 
                log_message("warning", f"Deleted partial model files at {self.model_folder}")

            # Emit failure with error details
            self.model_download_complete.emit(False, self.model_name, {
                "code": getattr(e, "errno", "Unknown"),
                "kind": type(e).__name__,
                "message": str(e)
            })

    def stop(self):
        self._is_running = False

        # If the folder exists and is partially downloaded, delete it
        if os.path.exists(self.model_folder):
            shutil.rmtree(self.model_folder)
            log_message("warning", f"Deleted partial model files at {self.model_folder}")
   