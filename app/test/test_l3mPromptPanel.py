from l3m.l3mPromptPanel import PromptPanel
from l3m.l3mPromptModel import PromptModel
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QApplication, QVBoxLayout, QScrollArea, QFrame, QLabel
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
    mock = MagicMock()
    mock.current_tokenizer = None  # Set some default values if needed
    mock.current_model = None
    return mock

@pytest.fixture
def prompt_panel(main_gui_mock):
    """Create an instance of the PromptPanel with the necessary mocks."""
    # Create the PromptPanel and pass the mocked main_gui_mock
    panel = PromptPanel(main_gui_mock)
    
    # Mock necessary UI components in PromptPanel
    panel.chat_layout = QVBoxLayout()  # Assuming QVBoxLayout for chat layout
    panel.scroll_area = MagicMock(spec=QScrollArea)
    panel.chat_container = MagicMock()  # In case adjustSize() is called
    
    # Mock input_field if used in tests
    panel.input_field = MagicMock()
    return panel

def test_import_prompt_panel():
    """Basic test to ensure PromptPanel imports correctly."""
    assert PromptPanel is not None

def test_add_message_user(app, prompt_panel):
    # Call add_message with user message
    prompt_panel.add_message("Hello", alignment=Qt.AlignmentFlag.AlignRight, user=True)
    
    # Check that the chat layout has one message container (user's message)
    assert prompt_panel.chat_layout.count() == 1
    
    # Get the message container
    message_container = prompt_panel.chat_layout.itemAt(0).widget()
    assert isinstance(message_container, QFrame)
    
    # Print out the items in the message container layout
    message_layout = message_container.layout()
    
    # Check that the message label is in the layout
    message_label = message_layout.itemAt(1).widget()
    
    # Ensure the correct message label and style
    assert isinstance(message_label, QLabel)
    assert message_label.text() == "Hello"
    assert "background-color: #e1f5fe;" in message_label.styleSheet()

def test_add_message_model_response(app,prompt_panel):
    
    # Call the method to add the message (for a user)
    prompt_panel.add_message("Hello", alignment=Qt.AlignmentFlag.AlignLeft, user=False)

    # Check that the chat layout has one message container (user's message)
    assert prompt_panel.chat_layout.count() == 1
    
    # Get the message container
    message_container = prompt_panel.chat_layout.itemAt(0).widget()
    assert isinstance(message_container, QFrame)
    
    # Print out the items in the message container layout
    message_layout = message_container.layout()
    
    # Check that the message label is in the layout
    message_label = message_layout.itemAt(0).widget()
    
    # Ensure the correct message label and style
    assert isinstance(message_label, QLabel)
    assert message_label.text() == "Hello"
    assert "background-color: #c8e6c9;" in message_label.styleSheet()

def test_send_message_no_model_selected(app,prompt_panel, main_gui_mock):
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

def test_send_message_with_model_selected(app,prompt_panel, main_gui_mock):
    #Test that send_message sends the message to the model.
    prompt_panel.input_field.text = MagicMock(return_value="Hello")
    
    # Mock the clear method to track its call
    prompt_panel.input_field.clear = MagicMock()
    
    # Mock the model and tokenizer
    main_gui_mock.current_tokenizer = MagicMock()
    main_gui_mock.current_model = MagicMock()
    
    # Patch the signal and pool start
    with patch.object(PromptModel, "signals", create=True) as mock_signals, patch.object(main_gui_mock.pool, "start") as mock_start:
        mock_signals.result.connect = MagicMock()  # Mock the connect method

        # Simulate sending the message
        prompt_panel.send_message()

        # Ensure the message is added to the chat layout
        assert prompt_panel.chat_layout.count() == 1
        
        # Get the message container and label
        message_container = prompt_panel.chat_layout.itemAt(0).widget()
        message_label = message_container.layout().itemAt(1).widget()
        
        # Assert that the message text in the label is correct
        assert message_label.text() == "Hello"
        
        # Ensure the pool start method is called
        mock_start.assert_called_once()

        # Ensure input field is cleared after sending
        prompt_panel.input_field.clear.assert_called_once()  # Verify clear() was called

def test_respond_to_message(app,prompt_panel):
    """Test that respond_to_message correctly adds the model's response to the chat."""
    prompt_panel.respond_to_message("Model response")
    
    # Check that the model response was added to the chat window
    assert prompt_panel.chat_layout.count() == 1
    message_container = prompt_panel.chat_layout.itemAt(0).widget()
    message_label = message_container.layout().itemAt(0).widget()
    assert message_label.text() == "Model response"