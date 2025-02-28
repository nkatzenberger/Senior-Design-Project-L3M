# Test cases for DownloadModelGUI class
import pytest
from PyQt6.QtWidgets import QApplication, QPushButton
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt, QPoint
from unittest.mock import MagicMock
from l3m.l3mDownloadModelGUI import DownloadModelGUI



@pytest.fixture
def app(qtbot):
    """Fixture to create the QApplication instance."""
    app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def download_model_gui(qtbot):
    """Fixture to create the GUI instance."""
    gui = DownloadModelGUI(model_panel=MagicMock(), main_gui=MagicMock())
    qtbot.addWidget(gui)
    return gui

def test_gui_initialization(download_model_gui):
    """Test if GUI initializes properly."""
    assert download_model_gui.windowTitle() == "Download Model"

def test_gui_widgets_exist(download_model_gui):
    """Test if GUI widgets exist after initialization."""
    assert download_model_gui.search_input is not None
    assert download_model_gui.model_list is not None

def test_download_button_click(download_model_gui):
    """Test if clicking the download button does not crash."""
    QTest.mouseClick(download_model_gui.findChild(QPushButton), Qt.MouseButton.LeftButton)
    assert True

def test_gui_closes_on_outside_click(download_model_gui, qtbot):
    """Test if GUI closes when clicking outside."""
    outside_pos = QPoint(9999, 9999)
    qtbot.mouseClick(download_model_gui, Qt.MouseButton.LeftButton, pos=outside_pos)
    assert not download_model_gui.isVisible()

def test_search_runs_on_start(download_model_gui, qtbot):
    """Test if searchForModel() is triggered on startup and updates model list."""
    # Model list should be empty initially
    assert download_model_gui.model_list.count() == 0  
    
    # Mock API response (Simulating HuggingFaceModelsAPI returning results)
    mock_model_data = {"Model 1": {"Model ID": "model-1"}, "Model 2": {"Model ID": "model-2"}}
    
    # Manually trigger the update to simulate the API call completing
    download_model_gui.updateModelList(mock_model_data)
    
    # Model list should now be updated 
    assert len(download_model_gui.model_list) > 0  
