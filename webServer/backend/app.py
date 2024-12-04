import sys
sys.path.append('backend')  # Ensure 'backend' folder is in the path
import index
from config import app  # Import the Flask app object from config

# Start the app
if __name__ == '__main__':
    app.run(host="localhost", port=3000)