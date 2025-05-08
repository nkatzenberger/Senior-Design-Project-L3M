from flask import Flask

# Initialize the Flask app with the correct template folder
app = Flask(__name__, static_folder="../static/", template_folder='../templates/')
