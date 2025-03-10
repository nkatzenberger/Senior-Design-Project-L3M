from flask import Flask

# Initialize the Flask app with the correct template folder
<<<<<<< HEAD
app = Flask(__name__, template_folder='../frontend/templates')
=======
app = Flask(__name__, static_folder="../static/", template_folder='../templates/')
>>>>>>> origin/webServer-refactoring
