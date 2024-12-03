from flask import render_template
from config import app  # Import the Flask app object

# Define the route for the home page
@app.route('/')
def hello_world():
    return render_template('views/index.html')