import asyncio
import httpx
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal
from huggingface_hub import HfApi

class APISignals(QObject):
    result = pyqtSignal(dict)

class HuggingFaceModelsAPI(QRunnable):
    def __init__(self, query):
        super(HuggingFaceModelsAPI, self).__init__()
        self.query = query
        self.signals = APISignals()
        self.api = HfApi()

    async def fetch_model_info(self, session, model_id):
        #Fetch detailed model info asynchronously.
        url = f"https://huggingface.co/api/models/{model_id}"
        try:
            response = await session.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"Model ID": model_id, "Error": f"HTTP {e.response.status_code}"}
        except Exception as e:
            return {"Model ID": model_id, "Error": str(e)}

    async def get_all_model_info(self, model_ids):
        #Fetches all model info in a single batch request.
        model_data = {}

        async with httpx.AsyncClient() as session:
            tasks = [self.fetch_model_info(session, model_id) for model_id in model_ids]
            results = await asyncio.gather(*tasks)

            # Process results
            for model_info in results:
                if "Error" in model_info:
                    continue  # Skip failed requests
                
                for model_info in results:
                    model_id = model_info.get("modelId", "Unknown")  # Ensure model_id is defined

                    if model_info.get("gated", False) or model_info.get("disabled", False):
                        continue  # Skip gated or disabled models

                    model_name = model_info.get("Model Name", model_id.split("/")[-1])  # Extract model name
                                
                    model_data[model_name] = {  # Use model name as the dictionary key
                        "Model ID": model_id,  # Store the model ID inside the dictionary for downloading
                        "Author": model_info.get("author", "Unknown"),
                        "Library Name": model_info.get("library_name", "Unknown"),
                        "Pipeline Tag": model_info.get("pipeline_tag", "Unknown"),
                        "Used Storage (GB)": round(model_info.get("usedStorage", 0) / (1024 * 1024 * 1024), 2),
                        "Likes": model_info.get("likes", 0),
                        "Downloads": model_info.get("downloads", 0),
                        "Trending Score": model_info.get("trending_score", "Unknown"),
                        "Gated": model_info.get("gated", "Unknown"),
                        "Disabled": model_info.get("disabled", "Unknown"),
                        "Security Repo Status": model_info.get("security_repo_status", "Unknown")
                    }
            return model_data

    def run(self):
        try:
            # Fetch the base model list
            models = self.api.list_models(
                search=self.query,
                library="transformers",
                pipeline_tag="text-generation",
                limit=50 
            )

            model_ids = [model.modelId for model in models]

            # Fetch all model details in a single batch
            model_data = asyncio.run(self.get_all_model_info(model_ids))

        except Exception as e:
            model_data = {"Error": f"Unexpected error - {str(e)}"}

        # Signal to the UI that the API call is complete
        self.signals.result.emit(model_data)
