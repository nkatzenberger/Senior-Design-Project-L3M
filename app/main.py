import os
import sys
import subprocess
import importlib.util

# -----------------------------------------------------------------------------
# Torch Auto-Installer
# -----------------------------------------------------------------------------

def has_gpu():
    try:
        result = subprocess.run(["nvidia-smi"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_torch_if_needed():
    if importlib.util.find_spec("torch") is not None:
        print("✅ torch is already installed.")
        return

    if has_gpu():
        print("💻 GPU detected — installing torch with CUDA...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "torch==2.6.0+cu118",
            "--extra-index-url", "https://download.pytorch.org/whl/cu118"
        ])
    else:
        print("🖥️ No GPU detected — installing CPU-only torch...")
        subprocess.check_call(["pip", "install", "torch==2.6.0"])

# -----------------------------------------------------------------------------
# Main App Imports (after torch is guaranteed installed)
# -----------------------------------------------------------------------------

install_torch_if_needed()

import torch
from PyQt6.QtWidgets import QApplication
from l3m.l3mMainGUI import GUI
from utils.path_utils import get_models_path

# -----------------------------------------------------------------------------
# App startup configurations
# -----------------------------------------------------------------------------

def setup_environment():
    print("Setting up environment...")

    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name()}")

    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    models_dir = get_models_path()
    print(f"Created directory: {models_dir}")

# -----------------------------------------------------------------------------
# Launch the GUI
# -----------------------------------------------------------------------------

def main():
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec())

# -----------------------------------------------------------------------------
# Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    setup_environment()
    main()