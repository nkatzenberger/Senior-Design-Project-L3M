import os
from unittest.mock import MagicMock, patch
import pytest
from l3m.l3mModelPanel import ModelPanel

@pytest.fixture
def main_gui_mock():
    """Mock the main GUI object."""
    return MagicMock()

@pytest.fixture
def model_panel(main_gui_mock):
    """Fixture to create a ModelPanel instance with cleanup."""
    return ModelPanel(main_gui_mock)

def test_import_model_panel():
    """Basic test to ensure ModelPanel imports correctly."""
    assert ModelPanel is not None 

def test_create_acronyms():
    """Test the creation of acronyms from model names."""
    model_names = ["my_model", "another_example_model", "test_model"]
    expected_acronyms = {
        "AEM": "another_example_model",
        "MML": "my_model",
        "TML": "test_model",
    }

    acronyms = ModelPanel.createAcronyms(model_names)

    assert acronyms == expected_acronyms

def test_get_model_names_existing():
    """Test getModelNames() with existing models."""
    # Patch os.path.exists and os.listdir in the correct location (l3m.l3mModelPanel)
    with patch("l3m.l3mModelPanel.os.path.exists", return_value=True), \
         patch("l3m.l3mModelPanel.os.listdir", return_value=["model1", "model2"]), \
         patch("l3m.l3mModelPanel.os.path.isdir", return_value=True):
        
        # Call the method you are testing
        model_names =ModelPanel.getModelNames()

    # Assert that the model names returned are correct
    assert model_names == ["model1", "model2"]

def test_get_model_names_no_models():
    """Test getModelNames() with existing models."""
    # Patch os.path.exists and os.listdir in the correct location (l3m.l3mModelPanel)
    with patch("l3m.l3mModelPanel.os.path.exists", return_value=True), \
         patch("l3m.l3mModelPanel.os.listdir", return_value=[]), \
         patch("l3m.l3mModelPanel.os.path.isdir", return_value=True):
        
        # Call the method you are testing
        model_names = ModelPanel.getModelNames()

    # Assert that the model names returned are correct
    assert model_names == []       

def test_get_model_names_directory_not_exist(): 
    """Test getModelNames() with existing models."""
    # Patch os.path.exists and os.listdir in the correct location (l3m.l3mModelPanel)
    with patch("l3m.l3mModelPanel.os.path.exists", return_value=False) as mock_exists:
        # Call the method you are testing
        model_names = ModelPanel.getModelNames()

    # Assert that the model names returned are correct
    assert model_names == []   

@patch("l3m.l3mModelPanel.AnimateIcon")
@patch("l3m.l3mModelPanel.switchModel")
def test_model_button_clicked(mock_switch, mock_icon_class, main_gui_mock, qtbot):
    mock_icon_instance = MagicMock()
    mock_icon_class.return_value = mock_icon_instance

    mock_switch_instance = MagicMock()
    # Don't call stop_animation (yet) to inspect overlay
    mock_switch_instance.signals.finished.connect = MagicMock()
    mock_switch.return_value = mock_switch_instance

    # Mock the GUI's thread pool too
    mock_pool = MagicMock()
    main_gui_mock.pool = mock_pool

    panel = ModelPanel(main_gui_mock)
    qtbot.addWidget(panel.downloadModelButton)

    model_name = "test_model"
    panel.modelButtonClicked(model_name)

    # Assert overlay was set before signal completes
    assert panel.overlay == mock_icon_instance
    mock_icon_instance.setWindowFlag.assert_called_once()
    mock_icon_instance.show.assert_called_once()
    mock_switch.assert_called_once_with(main_gui_mock, model_name=model_name)
    mock_pool.start.assert_called_once_with(mock_switch_instance)

def test_on_model_download_complete_success(model_panel):
    """Test the functionality when model download completes successfully."""
    with patch.object(model_panel, "refreshModelButtons") as mock_refresh:
        model_panel.onModelDownloadComplete(success=True)
        mock_refresh.assert_called_once()

def test_on_model_download_complete_failure(main_gui_mock):
    """Test the functionality when model download fails."""
    model_panel = ModelPanel(main_gui_mock)
    
    # Simulate a failed download with an error dictionary
    error = {"code": "404", "kind": "Not Found", "message": "Model not found."}
    
    with patch("PyQt6.QtWidgets.QMessageBox.warning") as mock_warning:
        model_panel.onModelDownloadComplete(success=False, error=error)
        mock_warning.assert_called_once_with(
            None,
            "Download Failed",
            "Code: 404\nKind: Not Found\nDetails: Model not found."
        )
