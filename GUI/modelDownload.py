import os
from transformers import AutoModel, AutoTokenizer, AutoConfig

def download_huggingface_model(model_name: str, save_directory: str):
    """
    Downloads a model, tokenizer, and config from Hugging Face and saves them locally.

    Args:
        model_name (str): Name of the model on Hugging Face (e.g., 'bert-base-uncased').
        save_directory (str): Path to save the downloaded files.
    """
    # Ensure the save directory exists
    os.makedirs(save_directory, exist_ok=True)
    
    print(f"Downloading model: {model_name}...")
    
    # Download the model, tokenizer, and config
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    config = AutoConfig.from_pretrained(model_name)
    
    print("Saving model...")
    model.save_pretrained(save_directory)
    
    print("Saving tokenizer...")
    tokenizer.save_pretrained(save_directory)
    
    print("Saving config...")
    config.save_pretrained(save_directory)
    
    print(f"Model {model_name} successfully downloaded and saved in {save_directory}.")

if __name__ == "__main__":
    model_name = "openai-community/gpt2"  # Model to Download
    script_directory = os.path.dirname(os.path.abspath(__file__))
    models_folder = os.path.join(script_directory, "models")
    model_folder = os.path.join(models_folder, model_name.replace("/", "-"))
    download_huggingface_model(model_name, model_folder)