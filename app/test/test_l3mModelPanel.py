from unittest.mock import MagicMock, patch
from l3m.l3mModelPanel import ModelPanel

def test_import_model_panel():
    """Basic test to ensure ModelPanel imports correctly."""
    assert ModelPanel is not None 

def test_create_acronyms():
    model_panel = ModelPanel(None)  # Mocking main_gui for this test
    
    model_names = ["my_model", "another_example_model", "test_model"]
    expected_acronyms = {
        "MM": "my_model",
        "AEM": "another_example_model",
        "TM": "test_model"
    }
    
    acronyms = model_panel.createAcronyms(model_names)
    
    assert acronyms == expected_acronyms

def test_get_model_names_existing():
    model_panel = ModelPanel(None)  # Mocking main_gui for this test
    
    # Mocking os.listdir and os.path.exists
    with patch("os.path.exists", return_value=True), patch("os.listdir", return_value=["model1", "model2"]):
        model_names = model_panel.getModelNames()
        assert model_names == ["model1", "model2"]

def test_get_model_names_no_models():
    model_panel = ModelPanel(None)  # Mocking main_gui for this test
    
    # Mocking os.listdir and os.path.exists
    with patch("os.path.exists", return_value=True), patch("os.listdir", return_value=[]):
        model_names = model_panel.getModelNames()
        assert model_names == []

def test_get_model_names_directory_not_exist():
    model_panel = ModelPanel(None)  # Mocking main_gui for this test
    
    # Mocking os.path.exists
    with patch("os.path.exists", return_value=False):
        model_names = model_panel.getModelNames()
        assert model_names == []

def test_model_button_clicked():
    model_panel = ModelPanel(None)  # Mocking main_gui for this test
    model_name = "test_model"
    
    # Mocking the AutoTokenizer and AutoModelForCausalLM classes
    with patch("transformers.AutoTokenizer.from_pretrained") as mock_tokenizer, patch("transformers.AutoModelForCausalLM.from_pretrained") as mock_model:
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()

        # Simulating a valid model path
        with patch("os.path.exists", return_value=True):
            model_panel.modelButtonClicked(model_name)
            
            # Verifying that AutoTokenizer and AutoModelForCausalLM are called correctly
            mock_tokenizer.assert_called_with(f"models/{model_name}")
            mock_model.assert_called_with(f"models/{model_name}")

def test_download_model_button_clicked():
    main_gui_mock = MagicMock()
    model_panel = ModelPanel(main_gui_mock)
    
    # Ensure that the download model button creates and shows a DownloadModelGUI instance
    with patch("l3m.l3mDownloadModelGUI.DownloadModelGUI") as mock_downloadModelGUI:
        mock_downloadModelGUI.return_value = MagicMock()
        
        model_panel.downloadModelButtonClicked()
        
        # Check that the download model GUI is shown
        mock_downloadModelGUI.return_value.show.assert_called_once()

def test_on_model_download_complete_success():
    main_gui_mock = MagicMock()
    model_panel = ModelPanel(main_gui_mock)
    
    with patch.object(model_panel, "refreshModelButtons") as mock_refresh:
        model_panel.onModelDownloadComplete(success=True)
        mock_refresh.assert_called_once()

def test_on_model_download_complete_failure():
    main_gui_mock = MagicMock()
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