import os
import sys
import platform
import traceback
from utils.logging_utils import LogManager

class TorchLoader:
    _torch = None
    _device = None

    @classmethod
    def _get_base_dir(cls):
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        return base_dir
    
    @classmethod
    def _try_import(cls, path, device_type):
        if path not in sys.path:
            sys.path.insert(0, path)
        
        import torch
        cls._torch = torch
        cls._device = torch.device(device_type)
        LogManager.log("info", f"Using {device_type.upper()} torch from: {path}")

        try:
            import torchvision
            LogManager.log("info", f"TorchVision version: {torchvision.__version__}, from: {torchvision.__file__}")
        except Exception as e:
            LogManager.log("warning", f"torchvision import failed: {e}")

        try:
            import torchaudio
            LogManager.log("info", f"TorchAudio version: {torchaudio.__version__}, from: {torchaudio.__file__}")
        except Exception as e:
            LogManager.log("warning", f"torchAudio import failed: {e}")

    @classmethod
    def load(cls):
        try:
            base_dir = cls._get_base_dir()
            LogManager.log("debug", f"Resolved base_dir: {base_dir}")

            is_macos = platform.system() == "Darwin"
            force_cpu = os.environ.get("FORCE_CPU_TORCH") == "1"

            cpu_path = os.path.join(base_dir, "lib", "torch_cpu")
            gpu_path = os.path.join(base_dir, "lib", "torch_cuda")

            if is_macos:
                import torch
                cls._torch = torch
                cls._device = torch.device("cpu")
                LogManager.log("info", "macOS detected: using system torch (CPU only)")
                return


            if not force_cpu:
                LogManager.log("debug", "Attempting GPU torch load...")
                try:
                    cls._try_import(gpu_path, "cuda")
                    if not cls._torch.cuda.is_available():
                        raise RuntimeError("CUDA unavailable at runtime")
                except Exception as e:
                    LogManager.log("warning", f"GPU torch load failed: {e}")
                    cls._try_import(cpu_path, "cpu")
            else:
                LogManager.log("debug", "GPU torch not used or unavailable")
                cls._try_import(cpu_path, "cpu")

            sys.modules["torch"] = cls._torch
            LogManager.log("info", f"Torch successfully initialized: {cls._torch.__version__}, Device: {cls._device}")

        except Exception:
            LogManager.log("error", "Fatal error in TorchLoader:\n" + traceback.format_exc())
            print("A fatal error occurred. Check logs/L3M.log for details.")

TorchLoader.load()
