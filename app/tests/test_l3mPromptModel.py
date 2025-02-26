import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from l3m.l3mPromptModel import PromptModel

def test_import_prompt_model():
    """Basic test to ensure PromptModel imports correctly."""
    assert PromptModel is not None 
