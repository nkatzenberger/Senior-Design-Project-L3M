import os
import shutil
from PyQt6.QtCore import QThread, pyqtSignal
from transformers import AutoModel, AutoTokenizer, AutoConfig

class DownloadModel(QThread):
    model_download_complete = pyqtSignal(bool, str, dict)

    def __init__(self, model_name):
        super(DownloadModel, self).__init__()
        self._is_running = True

        #Set model install destination
        self.model_name = model_name
        script_directory = os.path.dirname(os.path.abspath(__file__))
        models_folder = os.path.join(script_directory, "models")
        self.model_folder = os.path.join(models_folder, model_name.replace("/", "-"))

    def run(self):
        try:
            # Ensure the save directory exists
            os.makedirs(self.model_folder, exist_ok=True)

            if not self._is_running: # Stop before starting download
                return
            
            # Download the model, tokenizer, and config
            AutoModel.from_pretrained(
                self.model_name, 
                low_cpu_mem_usage=True, # Prevents entire model being loaded into ram
                device_map="auto"  # Automatically offloads model parts to disk if needed
            )

            if not self._is_running: # Stop after download
                return
            
            # Download the model, tokenizer, and config
            model = AutoModel.from_pretrained(self.model_name)
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            config = AutoConfig.from_pretrained(self.model_name)

            if not self._is_running: # Stop before saving
                return
            
            #Save the model, tokenizer, and config
            model.save_pretrained(self.model_folder)
            tokenizer.save_pretrained(self.model_folder)
            config.save_pretrained(self.model_folder)
            
            print(f"Model {self.model_name} successfully downloaded and saved in {self.model_folder}.")

            # Emit download was successful to GUI
            self.model_download_complete.emit(True, self.model_name, {})

        except Exception as e:
            print(f"Error downloading model: {e}")

            # If the folder exists and is partially downloaded, delete it
            if os.path.exists(self.model_folder):
                shutil.rmtree(self.model_folder) 
                print(f"Deleted incomplete model files at {self.model_folder}")

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
            print(f"Stopped download and deleted partial files at {self.model_folder}")
   