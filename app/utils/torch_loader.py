import os
import sys

class TorchLoader:
    _torch = None
    _device = None

    @classmethod
    def _get_path(cls, folder):
        base_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
        return os.path.abspath(os.path.join(base_dir, "..", "lib", folder))

    @classmethod
    def load(cls):
        if cls._torch:
            return cls._torch, cls._device

        cuda_path = cls._get_path("torch_cuda")
        cpu_path = cls._get_path("torch_cpu")

        try:
            sys.path.insert(0, cuda_path)
            raise RuntimeError("CPU for testing")
            import torch
            sys.modules["torch"] = torch
            if torch.cuda.is_available():
                cls._torch = torch
                cls._device = torch.device("cuda")
                print("Using GPU torch")
            raise RuntimeError("CUDA not available")
        except Exception as e:
            print(f"Falling back to CPU torch: {e}")
            sys.path.remove(cuda_path)
            sys.path.insert(0, cpu_path)
            import torch
            sys.modules["torch"] = torch
            cls._torch = torch
            cls._device = torch.device("cpu")
        
        return cls._torch, cls._device
