from PyQt6.QtCore import QRunnable, QObject, pyqtSignal
from utils.torch_loader import TorchLoader
from utils.logging_utils import log_message
import time

class PromptSignals(QObject):
    result = pyqtSignal(str)

class PromptModel(QRunnable):
    def __init__(self, prompt, main_gui):
        super().__init__()
        self.torch, _ = TorchLoader.load()
        from utils.device_utils import DeviceManager
        from transformers import logging
        logging.set_verbosity_error()
        self.max_length = 500
        self.prompt = prompt
        self.device = DeviceManager.get_best_device()
        self.signals = PromptSignals()

        # Strong references to avoid GC issues
        self.tokenizer = main_gui.current_tokenizer
        self.model = main_gui.current_model
        self.metadata = main_gui.current_metadata
    
    def run(self):
        try:
            log_message("info", "PromptModel thread started...")
            start = time.time()
            
            
            log_message("info", "Tokenizing prompt...")
            inputs = self.tokenizer(
                self.prompt,
                return_tensors="pt",
                padding=True,
                truncation=True
            )
            log_message("info", f"Inputs created on device: {self.model.device}")
            
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            pad_token_id = self.tokenizer.pad_token_id or self.tokenizer.eos_token_id
            eos_token_id = self.tokenizer.eos_token_id

            log_message("debug", f"Model ref: {self.model}")
            log_message("debug", f"Tokenizer ref: {self.tokenizer}")
            log_message("debug", f"pad_token_id: {pad_token_id}, eos_token_id: {eos_token_id}")
            log_message("debug", f"input_ids: {inputs['input_ids'].shape}")
            log_message("debug", f"attention_mask: {inputs['attention_mask'].shape}")
            log_message("debug", f"input_ids tensor: {inputs['input_ids']}")
            log_message("debug", f"attention_mask tensor: {inputs['attention_mask']}")

            try:
                log_message("info", "Running model.generate()...")
                outputs = self.model.generate(
                    inputs["input_ids"],
                    attention_mask=inputs["attention_mask"],
                    max_length=inputs["input_ids"].shape[1] + 50,
                    pad_token_id=pad_token_id,
                    eos_token_id=eos_token_id,)
                log_message("info", f"Model.generate() completed in {time.time() - start:.2f}s")
            except Exception as e:
                log_message("error", f"model.generate() crashed: {e}")
                self.signals.result.emit(f"⚠️ Model crashed during generation: {e}")
                return

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            log_message("info", f"Decoded response: {response[:10]}...")

        except Exception as e:
            log_message("error", f"Exception in PromptModel: {e}")
            response = f'Error: Failed to Prompt Model; {e}'

        self.signals.result.emit(response)
        return