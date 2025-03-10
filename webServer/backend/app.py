<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify, send_file
import requests
import logging
import random
import sys
import os
from config import app
#sys.path.append('backend')
# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
STATIC_DIR = os.path.abspath('../static')

# Replace with your actual Hugging Face API token
HUGGING_FACE_API_TOKEN = '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'

@app.route('/')
def index():
    
    # Fetch all models from Hugging Face API
    headers = {
        'Authorization': f'Bearer {HUGGING_FACE_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get('https://huggingface.co/api/models', headers=headers)
    print(response.text)
    

    if response.ok:
        all_models = response.json()
        # Randomly select 5-10 models
        random_models = random.sample(all_models, min(len(all_models), 10))  # Limit to 10 if there are more than 10
        return render_template('views/index.html', models=random_models)
    else:
        logger.error(f"Error fetching models: {response.status_code} - {response.text}")
        return render_template('views/index.html', models=[])


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    limit = request.args.get('limit', default=50, type=int)

    if not query:
        return jsonify({'error': 'No query provided'}), 400

=======
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
>>>>>>> origin/webServer-refactoring
    headers = {
        'Authorization': f'Bearer {HUGGING_FACE_API_TOKEN}',
        'Content-Type': 'application/json'
    }
<<<<<<< HEAD
    logger.info(f"Received search query: {query} with limit: {limit}")

    try:
        response = requests.get(f'https://huggingface.co/api/models?search={query}', headers=headers)
        response.raise_for_status()  # Raise an exception for error HTTP statuses

        models = response.json()
        return jsonify(models)
        
=======
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
>>>>>>> origin/webServer-refactoring

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching models: {e}")
        return jsonify({'error': 'Error fetching models'}), 500

<<<<<<< HEAD
@app.route('/AboutUs')
def About():
    return render_template('views/aboutUs.html')



@app.route('/Aboutllms')
def llms():
    return render_template('views/aboutllms.html',)

@app.route('/download', methods=['GET'])
def download_file():
    try:
        # Path to the file to be served
        base_dir = os.path.abspath(os.path.dirname(__file__))  # Path to 'backend' folder
        file_path = os.path.join(base_dir, "..", "frontend", "public", "files", "lorem.txt")  # Adjust path to reach the file
        # send_file serves the file for download
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"An error occurred: {e}", 500


if __name__ == '__main__':
    app.run(host="localhost", port=5000)
=======
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
    app.run(host="0.0.0.0", port=5000, debug=True)
>>>>>>> origin/webServer-refactoring

