from flask import Flask

# Initialize the Flask app with the correct template folder
app = Flask(__name__, template_folder='../frontend/templates')