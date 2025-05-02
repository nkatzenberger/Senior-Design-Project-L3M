import os
import sys
import traceback
import utils.torch_utils
from PyQt6.QtWidgets import QApplication
from l3m.l3mMainGUI import GUI

from utils.path_utils import PathManager

def setup_environment():
    print("Setting up environment...")

    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    models_dir = PathManager.get_models_path()
    print(f"Created directory: {models_dir}")

def main():
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    try:
        setup_environment()
        main()
    except Exception:
        with open("error.log", "w") as f:
            traceback.print_exc(file=f)
        sys.exit(1)