import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from l3m.l3mModelPanel import ModelPanel

def test_import_model_panel():
    """Basic test to ensure ModelPanel imports correctly."""
    assert ModelPanel is not None 
