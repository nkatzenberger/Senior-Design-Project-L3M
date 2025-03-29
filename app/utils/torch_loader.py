import os
import sys

class TorchLoader:
    @classmethod
    def _get_path(cls, folder):
        base_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
        return os.path.abspath(os.path.join(base_dir, "..", "lib", folder))

    @classmethod
    def load(cls):
        cuda_path = cls._get_path("torch_cuda")
        cpu_path = cls._get_path("torch_cpu")

        try:
            sys.path.insert(0, cuda_path)
            import torch
            if torch.cuda.is_available():
                cls._torch = torch
                cls._device = torch.device("cuda")
                print("Using GPU torch")
            else:
                raise RuntimeError("CUDA not available")
        except Exception as e:
            print(f"⚠️ Falling back to CPU torch: {e}")
            if cuda_path in sys.path:
                sys.path.remove(cuda_path)
            sys.path.insert(0, cpu_path)
            import torch
            cls._torch = torch
            cls._device = torch.device("cpu")
            print("Using CPU torch")

        # Make sure every other module gets the same torch
        sys.modules["torch"] = cls._torch

# Automatically run on import
TorchLoader.load()