#Test cases for DownloadModel Class
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from l3m.l3mDownloadModel import DownloadModel

def test_import_download_model():
    """Basic test to ensure DownloadModel imports correctly."""
    assert DownloadModel is not None  # ✅ Passes if import works
