import os
import logging
import random
import requests
from huggingface_hub import HfApi
import httpx
import asyncio
from flask import render_template, request, jsonify, send_file
from config import app

# Load API token from environment variables
HUGGING_FACE_API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', default="", type=str)
    limit = 6
    page = request.args.get('page', default=1, type=int)

    api = HfApi()

    try:
        # Step 1: Fetch model list (basic info)
        models = api.list_models(
            search=query,
            library="transformers",
            pipeline_tag="text-generation",
            limit=50
        )

        # Step 2: Extract model IDs
        model_ids = [model.modelId for model in models]

        # Step 3: Fetch detailed model info
        async def fetch_all_details(model_ids):
            async with httpx.AsyncClient() as session:
                tasks = [
                    fetch_model_info(session, model_id)
                    for model_id in model_ids
                ]
                results = await asyncio.gather(*tasks)
                return [r for r in results if "Error" not in r and not r.get("gated", False) and not r.get("disabled", False)]

        async def fetch_model_info(session, model_id):
            url = f"https://huggingface.co/api/models/{model_id}"
            try:
                response = await session.get(url, timeout=10.0)
                response.raise_for_status()
                return response.json()
            except Exception:
                return {"Model ID": model_id, "Error": "Failed to fetch"}

        model_infos = asyncio.run(fetch_all_details(model_ids))

        # Step 4: Manual pagination
        total_models = min(len(model_infos), 100)
        total_pages = (total_models // limit) + (1 if total_models % limit > 0 else 0)

        start_index = (page - 1) * limit
        end_index = start_index + limit
        paginated_models = model_infos[start_index:end_index]

        return jsonify({
            "models": paginated_models,
            "totalPages": total_pages
        })

    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        return jsonify({'error': 'Error fetching models'}), 500

@app.route('/about')
def About():
    return render_template('aboutUs.html')

@app.route('/about-llms')
def llms():
    return render_template('aboutllms.html',)

@app.route('/download', methods=['GET'])
def download_installer():
    """Serve the GUI installer file for download."""
    try:
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../public/L3M_Installer.zip"))
        return send_file(file_path, as_attachment=True, download_name="L3M_Installer.zip")
    except Exception as e:
        logger.error(f"Error serving file: {e}")
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)

