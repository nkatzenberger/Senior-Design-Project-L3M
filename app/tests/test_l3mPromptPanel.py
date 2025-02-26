import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from l3m.l3mPromptPanel import PromptPanel

def test_import_prompt_panel():
    """Basic test to ensure PromptPanel imports correctly."""
    assert PromptPanel is not None
