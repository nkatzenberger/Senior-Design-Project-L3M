import sys
import os
import pytest
from PyQt6.QtWidgets import QApplication

# Add 'app/' to sys.path if not already present
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Create single QApplication to share for all tests
@pytest.fixture(scope="session")
def app():
    """Ensure a single QApplication instance across all tests."""
    app = QApplication.instance() or QApplication(sys.argv)
    yield app

# Automatically set the asyncio mode to "auto" for all tests
pytest_plugins = "pytest_asyncio"

def pytest_configure(config):
    config.addinivalue_line("markers", "asyncio: mark a test as an asyncio test.")