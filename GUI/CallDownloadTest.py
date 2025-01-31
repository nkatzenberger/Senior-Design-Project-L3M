from modelDownload import DownloadModel

# Hardcoded model name
MODEL_NAME = "openai-community/gpt2"

if __name__ == "__main__":
    # Initialize and download the model
    downloader = DownloadModel(MODEL_NAME)