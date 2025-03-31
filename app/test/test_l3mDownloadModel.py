import pytest
import os
import shutil
import torch
from unittest.mock import MagicMock, patch
from l3m.l3mDownloadModel import DownloadModel
from utils.device_utils import DeviceManager

@pytest.fixture
def mock_hf_objects():
    """Fixture to mock Hugging Face model, tokenizer, and config."""
    with patch("l3m.l3mDownloadModel.AutoModel.from_pretrained") as mock_model, \
         patch("l3m.l3mDownloadModel.AutoTokenizer.from_pretrained") as mock_tokenizer, \
         patch("l3m.l3mDownloadModel.AutoConfig.from_pretrained") as mock_config:

        mock_model.return_value = MagicMock()
        mock_tokenizer.return_value = MagicMock()
        mock_config.return_value = MagicMock()

        yield mock_model, mock_tokenizer, mock_config

@pytest.fixture
def mock_os_functions():
    """Fixture to mock OS-related functions."""
    with patch("os.makedirs") as mock_makedirs, \
         patch("shutil.rmtree") as mock_rmtree, \
         patch("os.path.exists", return_value=True):  # Ensure deletion happens
        yield mock_makedirs, mock_rmtree

@pytest.fixture
def mock_get_models_path():
    """Fixture to mock get_models_path to return a fake directory."""
    with patch("utils.path_utils.PathManager.get_models_path", return_value="/fake/path"):
        yield

@pytest.fixture
def download_model(mock_get_models_path):
    """Fixture to create a DownloadModel instance with fake metadata."""
    fake_metadata = {
        "Model ID": "fake-model"
    }
    return DownloadModel(fake_metadata)

def test_download_model_initialization(download_model):
    """Test initialization of DownloadModel."""
    assert download_model.model_id == "fake-model"
    assert download_model.model_folder == os.path.join("/fake/path", "fake-model")

def test_successful_download(download_model, mock_hf_objects, mock_os_functions):
    """Test successful model download and saving."""
    mock_model, mock_tokenizer, mock_config = mock_hf_objects
    mock_makedirs, mock_rmtree = mock_os_functions
    # Patch out metadata saving to avoid FileNotFoundError
    download_model._save_metadata = MagicMock()

    mock_emit = MagicMock()
    download_model.model_download_complete.connect(mock_emit)

    download_model.run()

    # Verify download was attempted
    mock_model.assert_called_once_with(
        "fake-model", 
        low_cpu_mem_usage=True, 
        device_map="auto", 
        trust_remote_code=True,
        torch_dtype=DeviceManager.get_best_dtype()
    )
    mock_tokenizer.assert_called_once_with("fake-model")
    mock_config.assert_called_once_with("fake-model")

    # Ensure save methods were called
    mock_model.return_value.save_pretrained.assert_called_once_with(download_model.model_folder)
    mock_tokenizer.return_value.save_pretrained.assert_called_once_with(download_model.model_folder)
    mock_config.return_value.save_pretrained.assert_called_once_with(download_model.model_folder)

    # Verify that the successful signal was emitted
    mock_emit.assert_called_once_with(True, "fake-model", {})

def test_download_failure(download_model, mock_hf_objects, mock_os_functions):
    """Test handling of model download failure."""
    mock_model, _, _ = mock_hf_objects
    mock_makedirs, mock_rmtree = mock_os_functions

    # Simulate failure
    mock_model.side_effect = Exception("Download error")

    mock_emit = MagicMock()
    download_model.model_download_complete.connect(mock_emit)

    download_model.run()

    # Verify cleanup was called
    mock_rmtree.assert_called_once_with(download_model.model_folder)

    # Verify failure signal emitted with error details
    mock_emit.assert_called_once()
    emitted_args = mock_emit.call_args[0]
    assert emitted_args[0] is False  # Download failed
    assert emitted_args[1] == "fake-model"  # Model name
    assert "Download error" in emitted_args[2]["message"]  # Error message

def test_download_stop(download_model, mock_os_functions):
    """Test stopping the download process."""
    mock_makedirs, mock_rmtree = mock_os_functions

    download_model.stop()

    assert not download_model._is_running
    mock_rmtree.assert_called_once_with(download_model.model_folder)
