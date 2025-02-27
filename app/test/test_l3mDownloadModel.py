#Test cases for DownloadModel Class
from l3m.l3mDownloadModel import DownloadModel

def test_import_download_model():
    """Basic test to ensure DownloadModel imports correctly."""
    assert DownloadModel is not None  # ✅ Passes if import works
