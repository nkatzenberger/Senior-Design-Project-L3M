import os
from flask import render_template, send_file
from config import app  # Import the Flask app object

# Define the route for the home page
@app.route('/')
def hello_world():
    return render_template('views/index.html')

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