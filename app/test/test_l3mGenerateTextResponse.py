import pytest
from unittest.mock import MagicMock
from l3m.l3mGenerateTextResponse import GenerateTextResponse

@pytest.fixture
def mock_tokenizer():
    tokenizer = MagicMock()

    # Simulate tokenizer output with tensors that support .to()
    tokenizer.return_value = {
        "input_ids": MagicMock(to=MagicMock(return_value="input_ids_tensor")),
        "attention_mask": MagicMock(to=MagicMock(return_value="attention_mask_tensor"))
    }

    tokenizer.decode.return_value = "Generated response"
    tokenizer.eos_token_id = 2
    tokenizer.pad_token_id = 0

    return tokenizer

@pytest.fixture
def mock_model():
    model = MagicMock()
    model.generate.return_value = [["Generated", "response"]]
    model.device = "cpu"  # Mocking device for logs
    return model

@pytest.fixture
def mock_main_gui(mock_tokenizer, mock_model):
    gui = MagicMock()
    gui.current_tokenizer = mock_tokenizer
    gui.current_model = mock_model
    gui.current_metadata = {}
    return gui

def test_prompt_model_initialization(mock_main_gui):
    """Test if PromptModel initializes correctly."""
    prompt_text = "Test prompt"
    prompt_model = GenerateTextResponse(prompt_text, mock_main_gui)

    assert prompt_model.prompt == prompt_text
    assert prompt_model.tokenizer == mock_main_gui.current_tokenizer
    assert prompt_model.model == mock_main_gui.current_model

def test_prompt_model_run(mock_main_gui):
    prompt_text = "Test prompt"
    prompt_model = GenerateTextResponse(prompt_text, mock_main_gui)

    mock_emit = MagicMock()
    prompt_model.signals.result.connect(mock_emit)

    prompt_model.run()

    # Confirm expected calls
    prompt_model.tokenizer.assert_called()
    prompt_model.model.generate.assert_called_once()
    prompt_model.tokenizer.decode.assert_called_once()
    mock_emit.assert_called_once_with("Generated response")

def test_prompt_model_run_with_exception(mock_main_gui):
    prompt_text = "Test prompt"
    prompt_model = GenerateTextResponse(prompt_text, mock_main_gui)

    # Force generate to raise
    prompt_model.model.generate.side_effect = Exception("Model error")

    mock_emit = MagicMock()
    prompt_model.signals.result.connect(mock_emit)

    prompt_model.run()

    mock_emit.assert_called_once()
    assert "Model crashed during generation" in mock_emit.call_args[0][0]
