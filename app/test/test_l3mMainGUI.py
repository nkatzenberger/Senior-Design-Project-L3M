import pytest
from l3m.l3mMainGUI import GUI
from l3m.l3mModelPanel import ModelPanel
from l3m.l3mPromptModel import PromptModel

@pytest.fixture
def gui(app, qtbot):
    #Fixture to set up the GUI instance and add it to the qtbot.
    gui = GUI()  # Create the GUI instance
    qtbot.addWidget(gui)  # Add the GUI to qtbot
    return gui

def test_import_main_gui():
    #Basic test to ensure GUI imports correctly.
    assert GUI is not None 

def test_window_title(gui):
    #Test that the window title contains title of application
    assert "L3M GUI" in gui.windowTitle()


def test_window_geometry(gui):
    #Test that the window geometry is set correctly.
    x, y, width, height = gui.geometry().getRect()
    assert isinstance(x, int) and x >= 0
    assert isinstance(y, int) and y >= 0
    assert isinstance(width, int) and width > 0
    assert isinstance(height, int) and height > 0 


def test_model_panel_rendered(gui):
    #Test that the ModelPanel is rendered correctly in the layout.
    model_panel = gui.ref_model_panel
    assert model_panel is not None
    # Check if the model panel layout is present and contains widgets
    assert model_panel.modelPanel.count() > 0


def test_prompt_panel_rendered(gui):
    #Test that the PromptModel is rendered correctly in the layout.
    prompt_panel = gui.ref_prompt_panel
    assert prompt_panel is not None
    assert prompt_panel.promptModelLayout.count() > 0


def test_layout_contains_model_and_prompt_panels(gui):
    #Test that the main window layout contains both ModelPanel and PromptModel.
    layout = gui.centralWidget().layout()
    assert layout is not None
    assert layout.count() == 2  # It should contain two panels


def test_thread_pool_initialized(gui):
    #Test that the QThreadPool instance is correctly initialized.
    assert gui.pool is not None
    assert gui.pool.activeThreadCount() == 0  # Assuming no active threads initially


def test_current_model_and_tokenizer(gui):
    #Test that the current model and tokenizer are initialized as None.
    assert gui.current_model is None
    assert gui.current_tokenizer is None