import torch
import time
import threading
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal
from transformers import TextIteratorStreamer, logging
from utils.logging_utils import LogManager

class PromptSignals(QObject):
    token_stream = pyqtSignal(str)
    finished = pyqtSignal(str)

class GenerateTextResponse(QRunnable):
    def __init__(self, prompt, main_gui):
        super().__init__()
        logging.set_verbosity_error()
        self.prompt = prompt
        self.signals = PromptSignals()
        self._stop_requested = False

        # Strong references to avoid GC issues
        self.tokenizer = main_gui.current_tokenizer
        self.model = main_gui.current_model
        self.metadata = main_gui.current_metadata
    
    def run(self):
        # Sampling controls
        MAX_STREAM_TOKENS = 512
        TEMPERATURE = 0.9
        TOP_K = 50
        TOP_P = 0.95

        try:
            LogManager.log("info", "GenerateTextResponse thread started...")
            start = time.time()

            # Get max context len(Prompt + Response) for specific model
            # Divide by two for prompt and leave rest for response
            max_context_len = getattr(self.model.config, "max_position_embeddings", 1024)
            max_prompt_len = max_context_len // 2
            
            # Tokenize input
            inputs = self.tokenizer(
                self.prompt,
                return_tensors="pt",                # Output as PyTorch tensors
                truncation=True,                    # Truncate if prompt is too long
                max_length=max_prompt_len,          # Set based on your model’s context window
                add_special_tokens=True,            # Adds <BOS>, <EOS>, etc., depending on model
                return_attention_mask=True          # Needed for attention masking during generation
            )
            LogManager.log("info", f"Inputs created on device: {self.model.device}")

            # Ensure that tokens and inputs on on proper device
            model_device = next(self.model.parameters()).device
            inputs = {k: v.to(model_device) for k, v in inputs.items()}
            
            # Available space for output
            prompt_len = inputs["input_ids"].shape[1]
            max_allowed_output = min(MAX_STREAM_TOKENS, max_context_len - prompt_len)
            
            # Set up Hugging Face streaming
            streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)

            generation_kwargs = {
                "input_ids": inputs["input_ids"],
                "attention_mask": inputs["attention_mask"],
                "max_new_tokens": max_allowed_output,
                "temperature": TEMPERATURE,
                "top_k": TOP_K,
                "top_p": TOP_P,
                "do_sample": True,
                "streamer": streamer,
                "repetition_penalty": 1.2,                      # Avoid loops and rambling
                "eos_token_id": self.tokenizer.eos_token_id,    # Stop at end-of-sequence
                "num_beams": 1,                                 # Greedy search (shorter, more factual)
            }

            thread = threading.Thread(target=self.model.generate, kwargs=generation_kwargs)
            thread.start()

            full_response = ""
            for new_text in streamer:
                if self._stop_requested:
                    break
                full_response += new_text
                self.signals.token_stream.emit(new_text)

            LogManager.log("info", f"Full generation finished in {time.time() - start:.2f}s")
        except Exception as e:
            LogManager.log("error", f"Exception in GenerateTextResponse: {e}")
            full_response = f"Error: Failed to Generate Text Response; {e}"

        self.signals.finished.emit(full_response)

    def stop(self):
        self._stop_requested = True