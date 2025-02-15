from huggingface_hub import HfApi

api = HfApi()
models = api.list_models()

counter = 0
with open("HuggingFaceModels.txt", "w", encoding="utf-8") as f:
    for model in models:
        if counter < 50:
            model_info = api.model_info(model.modelId)
            
            # Extract model info safely
            model_id = model_info.modelId
            author = model_info.author if model_info.author else "Unknown"
            library_name = model_info.library_name if model_info.library_name else "Unknown"
            pipeline_tag = model_info.pipeline_tag if model_info.pipeline_tag else "Unknown"
            used_storage = model_info.usedStorage if hasattr(model_info, "usedStorage") else 0
            used_storage_mb = used_storage / (1024 * 1024)  # Convert to MB
            likes = model_info.likes if model_info.likes else 0
            downloads = model_info.downloads if model_info.downloads else 0
            trending_score = model_info.trending_score if hasattr(model_info, "trending_score") else "Unknown"
            gated = model_info.gated if hasattr(model_info, "gated") else "Unknown"
            disabled = model_info.disabled if hasattr(model_info, "disabled") else "Unknown"
            security_status = model_info.security_repo_status if hasattr(model_info, "security_repo_status") else "Unknown"

            # Write to file
            f.write("="*50 + "\n")
            f.write(f"Author: {author}\n")
            f.write(f"Model Name: {model_id.split('/')[-1]}\n")
            f.write(f"Model ID: {model_id}\n")
            f.write(f"Library Name: {library_name}\n")
            f.write(f"Pipeline Tag: {pipeline_tag}\n")
            f.write(f"Used Storage: {used_storage_mb:.2f} MB\n")
            f.write(f"Likes: {likes}\n")
            f.write(f"Downloads: {downloads}\n")
            f.write(f"Trending Score: {trending_score}\n")
            f.write(f"Gated: {gated}\n")
            f.write(f"Disabled: {disabled}\n")
            f.write(f"Security Repo Status: {security_status}\n")
            f.write("="*50 + "\n\n")
            
            counter += 1
        else:
            break
print(dir(model_info))
f.close()