from flask import Flask, render_template, request, jsonify
import requests
import logging
import random

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        return render_template('index.html', models=random_models)
    else:
        logger.error(f"Error fetching models: {response.status_code} - {response.text}")
        return render_template('index.html', models=[])


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    limit = request.args.get('limit', default=50, type=int)

    if not query:
        return jsonify({'error': 'No query provided'}), 400

    headers = {
        'Authorization': f'Bearer {HUGGING_FACE_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    logger.info(f"Received search query: {query} with limit: {limit}")

    try:
        response = requests.get(f'https://huggingface.co/api/models?search={query}', headers=headers)
        response.raise_for_status()  # Raise an exception for error HTTP statuses

        models = response.json()
        return jsonify(models)
        

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching models: {e}")
        return jsonify({'error': 'Error fetching models'}), 500

if __name__ == '__main__':
    app.run(debug=True)

