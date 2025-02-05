import os
import requests
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
from dotenv import load_dotenv

class HuggingFaceModelsAPI(QThread):
    dataFetched = pyqtSignal(list)
    triggerFetch = pyqtSignal(str)

    def __init__(self):
        super(HuggingFaceModelsAPI, self).__init__()
        load_dotenv()
        self._is_running = True
        self.API_TOKEN = os.getenv('HUGGING_FACE_API_TOKEN')
        if not self.API_TOKEN:
            raise EnvironmentError('API token not found')
        self.triggerFetch.connect(self.fetchData)
        
    @pyqtSlot(str)
    def fetchData(self, query):
        self.query = query
        headers = {
            'Authorization': f'Bearer {self.API_TOKEN}',
            'Content-Type': 'application/json'
        }

        url = f'https://huggingface.co/api/models?search={self.query}' if self.query else 'https://huggingface.co/api/models'
        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()

            # Only return text-generation models
            text_gen_models = [model for model in data if model.get("pipeline_tag") == "text-generation"]

            if text_gen_models:
                model_names = [model["id"] for model in text_gen_models[:30]]  # First 30 models
            else:
                model_names = ["No text-generation models found."]
        except requests.exceptions.Timeout:
            model_names = ["Error: Request timed out."]
        except requests.exceptions.RequestException as e:
            model_names = [f"Error: {str(e)}"]
        except Exception:
            model_names = ["Error: Failed to fetch data."]
        self.dataFetched.emit(model_names)
    
    def run(self):
        while self._is_running:
            self.sleep(1)

    def stop(self):
        self._is_running = False