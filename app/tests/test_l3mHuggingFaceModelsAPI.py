import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from l3m.l3mHuggingFaceModelsAPI import HuggingFaceModelsAPI

def test_import_huggingface_models_api():
    """Basic test to ensure HuggingFaceModelsAPI imports correctly."""
    assert HuggingFaceModelsAPI is not None 
