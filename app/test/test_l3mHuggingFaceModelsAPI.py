import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from l3m.l3mHuggingFaceModelsAPI import HuggingFaceModelsAPI

@pytest.fixture
def mock_hf_api():
    """Mock Hugging Face API list_models call."""
    with patch("l3m.l3mHuggingFaceModelsAPI.HfApi.list_models") as mock_list_models:
        mock_list_models.return_value = [
            MagicMock(modelId="test-model-1"),
            MagicMock(modelId="test-model-2"),
        ]
        yield mock_list_models

@pytest.fixture
def mock_httpx_client():
    """Mock httpx AsyncClient for fetching model info."""
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        async def mock_fetch(url, timeout):
            if "test-model-1" in url:
                return MagicMock(status_code=200, json=lambda: {
                    "modelId": "test-model-1",
                    "author": "user1",
                    "library_name": "transformers",
                    "pipeline_tag": "text-generation",
                    "usedStorage": 2000000000,
                    "likes": 100,
                    "downloads": 5000,
                    "trending_score": 0.95,
                    "gated": False,
                    "disabled": False,
                })
            elif "test-model-2" in url:
                return MagicMock(status_code=200, json=lambda: {
                    "modelId": "test-model-2",
                    "author": "user2",
                    "library_name": "transformers",
                    "pipeline_tag": "text-generation",
                    "usedStorage": 3000000000,
                    "likes": 200,
                    "downloads": 8000,
                    "trending_score": 1.2,
                    "gated": False,
                    "disabled": False,
                })
            return MagicMock(status_code=404, json=lambda: {"Error": "Not Found"})
        
        mock_get.side_effect = mock_fetch
        yield mock_get

@pytest.fixture
def huggingface_api():
    """Fixture to create a HuggingFaceModelsAPI instance."""
    return HuggingFaceModelsAPI(query="test-query")

@pytest.mark.asyncio
async def test_get_all_model_info(huggingface_api, mock_httpx_client):
    """Test fetching all model info asynchronously."""
    model_ids = ["test-model-1", "test-model-2"]
    result = await huggingface_api.get_all_model_info(model_ids)

    assert "test-model-1" in result
    assert result["test-model-1"]["Author"] == "user1"
    assert result["test-model-1"]["Used Storage (GB)"] == 1.86  # 2GB rounded

    assert "test-model-2" in result
    assert result["test-model-2"]["Author"] == "user2"
    assert result["test-model-2"]["Used Storage (GB)"] == 2.79  # 3GB rounded

def test_run_success(huggingface_api, mock_hf_api, mock_httpx_client):
    """Test running the Hugging Face API call."""
    mock_emit = MagicMock()
    huggingface_api.signals.result.connect(mock_emit)

    huggingface_api.run()

    mock_hf_api.assert_called_once_with(
        search="test-query",
        library="transformers",
        pipeline_tag="text-generation",
        limit=50
    )

    mock_emit.assert_called_once()
    result_data = mock_emit.call_args[0][0]
    assert "test-model-1" in result_data
    assert "test-model-2" in result_data

def test_run_with_exception(huggingface_api):
    """Test API call failure handling."""
    with patch("l3m.l3mHuggingFaceModelsAPI.HfApi.list_models", side_effect=Exception("API Error")):
        mock_emit = MagicMock()
        huggingface_api.signals.result.connect(mock_emit)

        huggingface_api.run()

        mock_emit.assert_called_once()
        result_data = mock_emit.call_args[0][0]
        assert "Error" in result_data
        assert "Unexpected error" in result_data["Error"]
