import os
import requests
from transformers import AutoModel, AutoTokenizer, AutoConfig
from dotenv import load_dotenv

class DownloadModel:
    def __init__(self, model_name):
        self.model_name = model_name
        script_directory = os.path.dirname(os.path.abspath(__file__))
        models_folder = os.path.join(script_directory, "models")
        self.model_folder = os.path.join(models_folder, model_name.replace("/", "-"))
        self.download_huggingface_model()

    def download_huggingface_model(self):
        # Ensure the save directory exists
        os.makedirs(self.model_folder, exist_ok=True)
        
        # Download the model, tokenizer, and config
        model = AutoModel.from_pretrained(self.model_name)
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        config = AutoConfig.from_pretrained(self.model_name)
        
        #Save the model, tokenizer, and config
        model.save_pretrained(self.model_folder)
        tokenizer.save_pretrained(self.model_folder)
        config.save_pretrained(self.model_folder)
        
        print(f"Model {self.model_name} successfully downloaded and saved in {self.model_folder}.")
   