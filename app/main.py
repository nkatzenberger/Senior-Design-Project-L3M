import os
import sys
from PyQt6.QtWidgets import QApplication
from l3m.l3mMainGUI import GUI
from utils.path_utils import get_models_path

# App startup configurations
def setup_environment():
    print("Setting up environment...")

    # Disable tokenizer parallelism warnings
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # Check for or Create required directories
    models_dir = get_models_path()
    print(f"Created directory: {models_dir}")

def main():
    app = QApplication(sys.argv)
    
    # Create the main window (GUI)
    window = GUI()
    window.show()

    # Run the application loop
    sys.exit(app.exec())

# Entry point for running the app
if __name__ == "__main__":
    setup_environment() #Run setup before launching GUI
    main()