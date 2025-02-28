import os
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication
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

def test_create_acronyms(model_panel):
    """Test the creation of acronyms from model names."""
    model_names = ["my_model", "another_example_model", "test_model"]
    expected_acronyms = {
        "AEM": "another_example_model",
        "MML": "my_model",
        "TML": "test_model",
    }
    
    acronyms = ModelPanel.createAcronyms(None,model_names)
    
    assert acronyms == expected_acronyms

def test_get_model_names_existing(main_gui_mock):
    """Test getModelNames() with existing models."""
    model_panel = ModelPanel(main_gui_mock)

    # Patch os.path.exists and os.listdir in the correct location (l3m.l3mModelPanel)
    with patch("l3m.l3mModelPanel.os.path.exists", return_value=True) as mock_exists, \
         patch("l3m.l3mModelPanel.os.listdir", return_value=["model1", "model2"]) as mock_listdir, \
         patch("l3m.l3mModelPanel.os.path.isdir", return_value=True) as mock_isdir:
        
        # Call the method you are testing
        model_names = model_panel.getModelNames()

    # Assert that the model names returned are correct
    assert model_names == ["model1", "model2"]

def test_get_model_names_no_models():
    """Test getModelNames() with existing models."""
    model_panel = ModelPanel(main_gui_mock)

    # Patch os.path.exists and os.listdir in the correct location (l3m.l3mModelPanel)
    with patch("l3m.l3mModelPanel.os.path.exists", return_value=True) as mock_exists, \
         patch("l3m.l3mModelPanel.os.listdir", return_value=[]) as mock_listdir, \
         patch("l3m.l3mModelPanel.os.path.isdir", return_value=True) as mock_isdir:
        
        # Call the method you are testing
        model_names = model_panel.getModelNames()

    # Assert that the model names returned are correct
    assert model_names == []       

def test_get_model_names_directory_not_exist(): 
    """Test getModelNames() with existing models."""
    model_panel = ModelPanel(main_gui_mock)

    # Patch os.path.exists and os.listdir in the correct location (l3m.l3mModelPanel)
    with patch("l3m.l3mModelPanel.os.path.exists", return_value=False) as mock_exists:
        # Call the method you are testing
        model_names = model_panel.getModelNames()

    # Assert that the model names returned are correct
    assert model_names == []   

def test_model_button_clicked(main_gui_mock):
    """Test the model button click functionality."""
    model_panel = ModelPanel(main_gui_mock)  # Mocking main_gui for this test
    model_name = "test_model"
    
    # Mocking the AutoTokenizer and AutoModelForCausalLM classes
    with patch("transformers.AutoTokenizer.from_pretrained") as mock_tokenizer, patch("transformers.AutoModelForCausalLM.from_pretrained") as mock_model:
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()

        # Simulating a valid model path
        with patch("os.path.exists", return_value=True):
            model_panel.modelButtonClicked(model_name)

            app_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            expected_model_path = os.path.join(app_directory, "models", model_name)
            # Verifying that AutoTokenizer and AutoModelForCausalLM are called correctly
            mock_tokenizer.assert_called_with(expected_model_path)
            mock_model.assert_called_with(expected_model_path)

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
