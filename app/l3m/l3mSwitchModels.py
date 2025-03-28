import os
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
        #lazy Load
        import gc
        import json
        from utils.torch_loader import TorchLoader
        self.torch, self.device = TorchLoader.load() #need to load torch before importing transformers
        from transformers import AutoModelForCausalLM, AutoTokenizer

        # Unload existing model
        if self.main_gui.current_model:
            log_message("info", "Waiting for running tasks to complete before switching model...")
            self.main_gui.pool.waitForDone(3000)  # waits up to 3s

            del self.main_gui.current_model
            del self.main_gui.current_tokenizer
            gc.collect()
            if self.torch.cuda.is_available():
                self.torch.cuda.empty_cache()
            log_message("info", 'Unloaded existing model')

        # Error check models folder
        model_path = os.path.join(self.models_dir, self.model_name)
        if not os.path.exists(model_path):
            log_message("error", 'Model path doesn\'t exist')
            return

        # Load new model + tokenizer
        self.main_gui.current_tokenizer = AutoTokenizer.from_pretrained(model_path)
        model_selected = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=self.torch.float16,
            low_cpu_mem_usage=True
        ).to(self.device)

        # Inject pad token early if needed
        if self.main_gui.current_tokenizer.pad_token is None:
            log_message("info", "Pad token is None — injecting during model switch")
            try:
                self.main_gui.current_tokenizer.add_special_tokens({'pad_token': '[PAD]'})
                if hasattr(model_selected, "resize_token_embeddings"):
                    model_selected.resize_token_embeddings(len(self.main_gui.current_tokenizer))
                    if hasattr(model_selected, "tie_weights"):
                        model_selected.tie_weights()
                log_message("info", "Pad token injected and model updated.")
            except Exception as e:
                log_message("error", f"Failed to inject pad token during model switch: {e}")

        '''
        # Try torch.compile for performance boost
        try:
            model_selected = torch.compile(model_selected)
            log_message("info", "Compiled model with torch.compile()")
        except Exception as e:
            log_message("warning", "Could not compile model: {e}")
        '''

        self.main_gui.current_model = model_selected

        log_message("info", f'Current model is now {model_path}')
        log_message("info", f"Model loaded to {self.device}")

        # Load metadata
        metadata = {}
        metadata_path = os.path.join(model_path, "metadata.json")
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                    log_message("info", f"Loaded metadata: {metadata}")
            except Exception as e:
                log_message("error", f"Failed to load metadata: {e}")
        
        self.main_gui.current_metadata = metadata

        self.main_gui.repaint()
        self.signals.finished.emit() 
