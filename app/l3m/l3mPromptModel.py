from PyQt6.QtCore import QRunnable, QObject, pyqtSignal, Qt
from transformers import logging
from utils.device_utils import DeviceManager

class PromptSignals(QObject):
    result = pyqtSignal(str)

class PromptModel(QRunnable):
    def __init__(self, prompt, tokenizer, model):
        super().__init__()
        logging.set_verbosity_error()
        self.max_length = 500
        self.prompt = prompt
        self.tokenizer = tokenizer
        self.model = model
        self.device = DeviceManager.get_best_device()
        self.signals = PromptSignals()
    
    def run(self):
        try:
            if self.tokenizer.pad_token is None:
                self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
                self.model.resize_token_embeddings(len(self.tokenizer))

            inputs = self.tokenizer(
                self.prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
            )
            
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            pad_token_id = self.tokenizer.pad_token_id or self.tokenizer.eos_token_id

            outputs = self.model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_length = self.max_length,
                num_return_sequences=1,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3,
                pad_token_id=pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            response = f'Error: Failed to Prompt Model; {e}'

        self.signals.result.emit(response)