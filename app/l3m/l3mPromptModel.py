from PyQt6.QtCore import QRunnable, QObject, pyqtSignal
from transformers import logging
from utils.device_utils import DeviceManager
from utils.logging_utils import log_message
import time

class PromptSignals(QObject):
    result = pyqtSignal(str)

class PromptModel(QRunnable):
    def __init__(self, prompt, main_gui):
        super().__init__()
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

            context_length = getattr(self.model.config, "max_position_embeddings", 1024)
            
            inputs = self.tokenizer(
                self.prompt,
                return_tensors="pt",             # Output as PyTorch tensors
                padding=True,            # Pad to a fixed length (so model input is consistent)
                truncation=True,                 # Truncate if prompt is too long
                max_length=context_length,     # Set based on your model’s context window
                add_special_tokens=True,         # Adds <BOS>, <EOS>, etc., depending on model
                return_attention_mask=True       # Needed for attention masking during generation
            )
            log_message("info", f"Inputs created on device: {self.model.device}")
            
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            try:
                outputs = self.model.generate(
                    input_ids=inputs["input_ids"],
                    attention_mask=inputs["attention_mask"],
                    max_new_tokens=512,
                    do_sample=True,
                    top_p=0.9,
                    temperature=0.8,
                    repetition_penalty=1.1,
                    eos_token_id=self.tokenizer.eos_token_id,
                    pad_token_id=self.tokenizer.pad_token_id
                )
                log_message("info", f"Model.generate() completed in {time.time() - start:.2f}s")
            except Exception as e:
                log_message("error", f"model.generate() crashed: {e}")
                self.signals.result.emit(f"Model crashed during generation: {e}")
                return

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            log_message("info", f"Decoded response: {response[:10]}...")

        except Exception as e:
            log_message("error", f"Exception in PromptModel: {e}")
            response = f'Error: Failed to Prompt Model; {e}'

        self.signals.result.emit(response)
        return