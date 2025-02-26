import os
import sys
from PyQt6.QtWidgets import QApplication
from l3m.l3mMainGUI import GUI  # Import directly from the package

# App startup configurations
def setup_environment():
    print("Setting up environment...")

    # Disable tokenizer parallelism warnings
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # Check for or Create required directories
    required_dirs = ["models", "logs", "offload"]
    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def main():
    setup_environment() #Run setup before launching GUI
    app = QApplication(sys.argv)
    
    # Create the main window (GUI)
    window = GUI()
    window.show()

    # Run the application loop
    sys.exit(app.exec())

# Entry point for running the app
if __name__ == "__main__":
    main()