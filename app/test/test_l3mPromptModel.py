import pytest
from unittest.mock import MagicMock
from l3m.l3mPromptModel import PromptModel

@pytest.fixture
def mock_tokenizer():
    tokenizer = MagicMock()
    tokenizer.pad_token = None
    tokenizer.pad_token_id = 0
    tokenizer.eos_token_id = 1
    tokenizer.add_special_tokens = MagicMock()
    tokenizer.resize_token_embeddings = MagicMock()
    tokenizer.return_tensors = "pt"

    # Mock the tokenizer __call__ to return input_ids and attention_mask
    tokenizer.side_effect = lambda text, return_tensors, padding, truncation: {
        "input_ids": [[1, 2, 3]], 
        "attention_mask": [[1, 1, 1]]
    }
    tokenizer.decode = MagicMock(return_value="Generated response")
    return tokenizer

@pytest.fixture
def mock_model():
    model = MagicMock()
    model.generate = MagicMock(return_value=[[4, 5, 6]])
    return model

def test_prompt_model_initialization(mock_tokenizer, mock_model):
    """Test if PromptModel initializes correctly."""
    prompt_text = "Test prompt"
    prompt_model = PromptModel(prompt_text, mock_tokenizer, mock_model)

    assert prompt_model.prompt == prompt_text
    assert prompt_model.tokenizer == mock_tokenizer
    assert prompt_model.model == mock_model

def test_prompt_model_run(mock_tokenizer, mock_model):
    """Test the run method for successful execution."""
    prompt_text = "Test prompt"
    prompt_model = PromptModel(prompt_text, mock_tokenizer, mock_model)

    mock_emit = MagicMock()
    prompt_model.signals.result.connect(mock_emit)  # Connect mock to signal

    prompt_model.run()

    # Verify tokenizer was called
    mock_tokenizer.assert_called_once_with(
        prompt_text, return_tensors="pt", padding=True, truncation=True
    )
    # Ensure model generate was called
    mock_model.generate.assert_called_once()
    # Ensure tokenizer decode was called
    mock_tokenizer.decode.assert_called_once()
    # Ensure the expected signal was emitted
    mock_emit.assert_called_once_with("Generated response")

def test_prompt_model_run_with_exception(mock_tokenizer, mock_model):
    """Test run method when an exception occurs."""
    prompt_text = "Test prompt"
    prompt_model = PromptModel(prompt_text, mock_tokenizer, mock_model)

    # Force an exception in model.generate
    mock_model.generate.side_effect = Exception("Model error")

    mock_emit = MagicMock()
    prompt_model.signals.result.connect(mock_emit)  # Connect mock to signal

    prompt_model.run()

    # Ensure the error message was emitted
    mock_emit.assert_called_once()
    emitted_message = mock_emit.call_args[0][0]
    assert "Error: Failed to Prompt Model" in emitted_message
