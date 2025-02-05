from transformers import AutoModelForCausalLM, AutoTokenizer, logging

class PromptModel:
    _model_cache = {}

    def __init__(self, model_path):
        logging.set_verbosity_error()
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)

    def generate_response(self, prompt, max_length=500):
        if self.tokenizer.pad_token is None:
            self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
            self.model.resize_token_embeddings(len(self.tokenizer))

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )

        pad_token_id = self.tokenizer.pad_token_id or self.tokenizer.eos_token_id

        outputs = self.model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=max_length,
            num_return_sequences=1,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3,
            pad_token_id=pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
        )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    @classmethod
    def get_or_create_model(cls, model_path):
        if model_path not in cls._model_cache:
            cls._model_cache[model_path] = cls(model_path)
        return cls._model_cache[model_path]

    @classmethod
    def prompt_model(cls, model_path: str, prompt: str):
        handler = cls.get_or_create_model(model_path)
        return handler.generate_response(prompt)