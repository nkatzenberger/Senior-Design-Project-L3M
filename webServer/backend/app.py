import os
import logging
import random
import requests
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

    url = "https://huggingface.co/api/models"
    headers = {
        'Authorization': f'Bearer {HUGGING_FACE_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    params = {
        "limit": 50
    }
    if query:
        params["search"] = query

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        models = response.json()

        # Apply manual pagination within the 100 models
        total_models = min(len(models), 100)  # Ensure we don't exceed 100
        total_pages = (total_models // limit) + (1 if total_models % limit > 0 else 0)

        start_index = (page - 1) * limit
        end_index = start_index + limit
        paginated_models = models[start_index:end_index]

        return jsonify({
            "models": paginated_models,
            "totalPages": total_pages
        })

    except requests.exceptions.RequestException as e:
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
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../public/L3M_Installer.exe"))
        return send_file(file_path, as_attachment=True, download_name="L3M_Installer.exe")
    except Exception as e:
        logger.error(f"Error serving file: {e}")
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)

