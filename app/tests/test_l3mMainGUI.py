import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from l3m.l3mMainGUI import GUI

def test_import_main_gui():
    """Basic test to ensure GUI imports correctly."""
    assert GUI is not None 
