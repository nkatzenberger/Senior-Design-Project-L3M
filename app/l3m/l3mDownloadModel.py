import os
import shutil
import json
from PyQt6.QtCore import QThread, pyqtSignal
from utils.path_utils import get_models_path
from utils.logging_utils import log_message

class DownloadModel(QThread):
    model_download_complete = pyqtSignal(bool, str, dict)

    def __init__(self, model_metadata: dict):
        super(DownloadModel, self).__init__()
        self._is_running = True

        #Set model install destination
        self.model_metadata = model_metadata
        self.model_id = model_metadata["Model ID"]
        self.folder_name = self.model_id.replace("/", "-")

        models_dir = get_models_path()
        self.model_folder = os.path.join(models_dir, self.folder_name)

    def run(self):
        try:
            from utils.torch_loader import TorchLoader
            torch, _ = TorchLoader.load()
            from utils.device_utils import DeviceManager
            from transformers import AutoModel, AutoTokenizer, AutoConfig

            # Ensure the save directory exists
            os.makedirs(self.model_folder, exist_ok=True)
            log_message("info", f"Downloading model: {self.model_id}")

            if not self._is_running: # Stop before starting download
                return
            
            # Download the model, tokenizer, and config
            model = AutoModel.from_pretrained(
                self.model_id, 
                low_cpu_mem_usage=True, # Prevents entire model being loaded into ram
                device_map="auto",  # Automatically offloads model parts to disk if needed
                trust_remote_code=True, #allows more models to be downloaded
                torch_dtype=DeviceManager.get_best_dtype()
            )

            if not self._is_running: # Stop after download
                return
            
            # Download the model, tokenizer, and config
            tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            config = AutoConfig.from_pretrained(self.model_id)

            if not self._is_running: # Stop before saving
                return
            
            #Save the model, tokenizer, and config
            model.save_pretrained(self.model_folder)
            tokenizer.save_pretrained(self.model_folder)
            config.save_pretrained(self.model_folder)

            # Save metadata as JSON
            metadata_path = os.path.join(self.model_folder, "metadata.json")
            with open(metadata_path, "w") as f:
                json.dump(self.model_metadata, f, indent=4)
            
            log_message("info", f"Model {self.model_id} saved at {self.model_folder}")

            # Emit download was successful to GUI
            self.model_download_complete.emit(True, self.model_id, {})

        except Exception as e:
            log_message("error", f"Failed to download {self.model_id}: {e}")

            # If the folder exists and is partially downloaded, delete it
            if os.path.exists(self.model_folder):
                shutil.rmtree(self.model_folder) 
                log_message("warning", f"Deleted partial model files at {self.model_folder}")

            # Emit failure with error details
            self.model_download_complete.emit(False, self.model_id, {
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
   