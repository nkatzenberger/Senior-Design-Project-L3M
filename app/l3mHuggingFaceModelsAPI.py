import httpx
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal
from huggingface_hub import HfApi

class WorkerSignals(QObject):
    result = pyqtSignal(list)

class HuggingFaceModelsAPI(QRunnable):
    def __init__(self, query):
        super(HuggingFaceModelsAPI, self).__init__()
        self._is_running = True
        self.query = query
        self.signals = WorkerSignals()
        self.api = HfApi()
        
    
    def run(self):
        try:
            # Filter the api 
            models = self.api.list_models(
                author=None,
                search=self.query,
                library="transformers",
                pipeline_tag="text-generation",
                limit=100)
            
            # Filter out gated and disabled models
            filtered_models = [model for model in models if not model.gated and not model.disabled]

            model_data = []

            for model in filtered_models:
                model_info = self.api.model_info(model.modelId)

                # Extract model info
                model_id = model_info.modelId
                model_name = model_id.split("/")[-1]  # Extract model name from model ID
                author = model_info.author if model_info.author else "Unknown"
                library_name = model_info.library_name if model_info.library_name else "Unknown"
                pipeline_tag = model_info.pipeline_tag if model_info.pipeline_tag else "Unknown"
                used_storage = model_info.usedStorage if hasattr(model_info, "usedStorage") else 0
                used_storage_gb = used_storage / (1024 * 1024 * 1024)  # Convert to MB
                likes = model_info.likes if model_info.likes else 0
                downloads = model_info.downloads if model_info.downloads else 0
                trending_score = model_info.trending_score if hasattr(model_info, "trending_score") else "Unknown"
                gated = model_info.gated if hasattr(model_info, "gated") else "Unknown"
                disabled = model_info.disabled if hasattr(model_info, "disabled") else "Unknown"
                security_status = model_info.security_repo_status if hasattr(model_info, "security_repo_status") else "Unknown"

                # Store data in dictionary with model name as the key
                model_data.append({
                    "Model Name": model_name,
                    "Author": author,
                    "Model ID": model_id,
                    "Library Name": library_name,
                    "Pipeline Tag": pipeline_tag,
                    "Used Storage (GB)": round(used_storage_gb, 2),
                    "Likes": likes,
                    "Downloads": downloads,
                    "Trending Score": trending_score,
                    "Gated": gated,
                    "Disabled": disabled,
                    "Security Repo Status": security_status
                })

            # If no models were found, return a default message
            if not model_data:
                model_data.append({"message": "No text-generation models found."})
    
        except httpx.TimeoutException:
            model_data = [{"Error": "Request timed out."}]
        except httpx.HTTPStatusError as e:
            model_data = [{"Error": f"API responded with {e.response.status_code}"}]
        except httpx.RequestError as e:
            model_data = [{"Error": f"API request failed - {str(e)}"}]
        except Exception as e:
            model_data = [{"Error": f"Unexpected error - {str(e)}"}]
    
    # Signal to the DownloadModelGUI that the API is done
        self.signals.result.emit(model_data)
