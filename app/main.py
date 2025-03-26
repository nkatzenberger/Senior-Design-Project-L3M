import os
import sys
import importlib.util
from PyQt6.QtWidgets import QApplication
from l3m.l3mMainGUI import GUI
from utils.path_utils import get_models_path

def check_torch_installed():
    if importlib.util.find_spec("torch") is None:
        print("❌ torch is not installed. Please run post_install.py or reinstall.")
        sys.exit(1)

def setup_environment():
    print("Setting up environment...")

    import torch  # Now safe to import
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name()}")

    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    models_dir = get_models_path()
    print(f"Created directory: {models_dir}")

def main():
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    check_torch_installed()
    setup_environment()
    main()