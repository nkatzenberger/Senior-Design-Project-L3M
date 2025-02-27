from l3m.l3mPromptPanel import PromptPanel
from l3m.l3mPromptModel import PromptModel
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QApplication
from unittest.mock import MagicMock, patch

# Initialize the QApplication to test Qt widgets
@pytest.fixture(scope="module")
def app():
    app = QApplication([])
    yield app
    app.quit()


@pytest.fixture
def main_gui_mock():
    """Mock the main GUI object."""
    return MagicMock()

@pytest.fixture
def prompt_panel(main_gui_mock):
    """Create an instance of the PromptPanel."""
    return PromptPanel(main_gui_mock)

def test_import_prompt_panel():
    """Basic test to ensure PromptPanel imports correctly."""
    assert PromptPanel is not None

def test_add_message_user(prompt_panel):
    """Test that the add_message function correctly adds a user message."""
    prompt_panel.add_message("Hello", alignment=Qt.AlignmentFlag.AlignRight, user=True)
    
    # Check that the chat layout has one message container (user's message)
    assert prompt_panel.chat_layout.count() == 1
    message_container = prompt_panel.chat_layout.itemAt(0).widget()
    
    # Check that the message label contains the expected text
    message_label = message_container.layout().itemAt(0).widget()
    assert message_label.text() == "Hello"
    
    # Ensure that the user message has the correct style
    assert "background-color: #e1f5fe;" in message_label.styleSheet()

def test_add_message_model_response(prompt_panel):
    """Test that the add_message function correctly adds a model response."""
    prompt_panel.add_message("Response from model", alignment=Qt.AlignmentFlag.AlignLeft, user=False)
    
    # Check that the chat layout has one message container (model's response)
    assert prompt_panel.chat_layout.count() == 1
    message_container = prompt_panel.chat_layout.itemAt(0).widget()
    
    # Check that the message label contains the expected text
    message_label = message_container.layout().itemAt(0).widget()
    assert message_label.text() == "Response from model"
    
    # Ensure that the model response has the correct style
    assert "background-color: #c8e6c9;" in message_label.styleSheet()

def test_send_message_no_input(prompt_panel):
    """Test that send_message doesn't do anything if there's no input."""
    prompt_panel.input_field.setText("")
    
    # Mock the QMessageBox to ensure no warning appears
    with patch.object(QMessageBox, "warning") as mock_warning:
        prompt_panel.send_message()
        mock_warning.assert_not_called()

def test_send_message_no_model_selected(prompt_panel, main_gui_mock):
    """Test that send_message shows a warning if no model is selected."""
    prompt_panel.input_field.setText("Hello")
    
    # Simulate no model selected
    main_gui_mock.current_tokenizer = None
    main_gui_mock.current_model = None
    
    with patch.object(QMessageBox, "warning") as mock_warning:
        prompt_panel.send_message()
        mock_warning.assert_called_once_with(
            None,
            "No Model Selected",
            "Please select a model first"
        )

def test_send_message_with_model_selected(prompt_panel, main_gui_mock):
    """Test that send_message sends the message to the model."""
    prompt_panel.input_field.setText("Hello")
    
    # Mock the model and tokenizer
    main_gui_mock.current_tokenizer = MagicMock()
    main_gui_mock.current_model = MagicMock()
    
    with patch.object(PromptModel, "signals", create=True) as mock_signals, patch.object(main_gui_mock.pool, "start") as mock_start:
        mock_signals.result.connect = MagicMock()  # Mock connect method
        
        # Simulate sending the message
        prompt_panel.send_message()
        
        # Check that the message was added to the chat window
        assert prompt_panel.chat_layout.count() == 1
        message_container = prompt_panel.chat_layout.itemAt(0).widget()
        message_label = message_container.layout().itemAt(0).widget()
        assert message_label.text() == "Hello"
        
        # Check that the model was triggered
        mock_start.assert_called_once()

def test_respond_to_message(prompt_panel):
    """Test that respond_to_message correctly adds the model's response to the chat."""
    prompt_panel.respond_to_message("Model response")
    
    # Check that the model response was added to the chat window
    assert prompt_panel.chat_layout.count() == 1
    message_container = prompt_panel.chat_layout.itemAt(0).widget()
    message_label = message_container.layout().itemAt(0).widget()
    assert message_label.text() == "Model response"


# Example test for checking the signal connection (you can skip this if the test framework doesn't support signal testing)
def test_send_message_signal_connection(prompt_panel, main_gui_mock):
    """Test that the send_message method properly connects to the model."""
    prompt_panel.input_field.setText("Test message")
    
    # Mock the tokenizer and model
    main_gui_mock.current_tokenizer = MagicMock()
    main_gui_mock.current_model = MagicMock()

    with patch.object(PromptModel, "signals", create=True) as mock_signals:
        mock_signals.result.connect = MagicMock()  # Mock connect method

        # Run send_message
        prompt_panel.send_message()

        # Check that the signal connection was made
        mock_signals.result.connect.assert_called_once()