from l3m.l3mGenerateTextResponse import GenerateTextResponse
from l3m.l3mChatMessage import ChatMessage, LoadingMessage
from PyQt6.QtWidgets import (
    QPushButton, QScrollArea, QLineEdit, QHBoxLayout, QWidget, QVBoxLayout, QMessageBox,
    QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt


class PromptModel(QWidget):
    def __init__(self, main_gui):
        super().__init__()
        self.main_gui = main_gui  # Store reference to GUI

        # Setup Chat Area
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setContentsMargins(0, 0, 0, 0)

        self.chat_container = QWidget()
        self.chat_container.setLayout(self.chat_layout)
        self.chat_container.setContentsMargins(0, 80, 0, 60)

        # Wrap chat_container in a container so it's centered inside scroll_area
        self.chat_wrapper = QWidget()
        self.chat_wrapper.setContentsMargins(0, 0, 0, 0)

        self.chat_wrapper_layout = QVBoxLayout(self.chat_wrapper)
        self.chat_wrapper_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.chat_wrapper_layout.setSpacing(0)
        self.chat_wrapper_layout.addWidget(self.chat_container)

        # Set chat_container in a scrollable, centered widget
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.chat_wrapper)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }                          

            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
                margin: 0;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: #888;
                min-height: 20px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical:hover {
                background: #aaa;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                subcontrol-origin: margin;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        # Setup Input Area
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.returnPressed.connect(self.send_message)
        self.input_field.setStyleSheet("""
            QLineEdit {
                background: transparent;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 6px 12px;
                font-size: 14pt;
            }
            QLineEdit:focus {
                outline: none;
            }
        """)

        self.send_button = QPushButton("Send")
        self.send_button.setFixedSize(36, 36)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #aaaaaa;
                border: none;
                border-radius: 18px;
            }
            QPushButton:hover {
                background-color: #cccccc;
            }
        """)

        input_row = QHBoxLayout()
        input_row.setContentsMargins(8, 8, 8, 8)
        input_row.setSpacing(8)
        input_row.addWidget(self.input_field)
        input_row.addWidget(self.send_button)

        self.input_container = QWidget()
        self.input_container.setLayout(input_row)
        self.input_container.setMinimumWidth(400)
        self.input_container.setStyleSheet("""
            background-color: #4f4f4f;
            border-radius: 24px;
        """)

        # Define Layout for Prompt Panel
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.input_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        main_layout.addItem(QSpacerItem(0, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            background-color: #2c2c2c;
        """)

    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.parent():
            scrollbar_width = self.scroll_area.verticalScrollBar().sizeHint().width()
            new_width = int(self.parent().width() * 0.5)
            self.chat_container.setFixedWidth(new_width + 8 + scrollbar_width)
            self.input_container.setFixedWidth(new_width)

            # Apply left margin to compensate for scrollbar
            self.chat_wrapper_layout.setContentsMargins(scrollbar_width, 0, 0, 0)

    #Function for adding users prompt to chat window
    def add_message(self, message: str, alignment: Qt.AlignmentFlag, user: bool = False):
        msg_widget = ChatMessage(message, is_user=user)
        self.chat_layout.addWidget(msg_widget)
        self.chat_container.adjustSize()
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )


    # Function that sends users prompt to the model
    def send_message(self):
        user_message = self.input_field.text().strip()
        if not user_message:
            return

        if not self.main_gui.current_tokenizer or not self.main_gui.current_model:
            QMessageBox.warning(self, "No Model Selected", "Please select a model first")
            return

        self.add_message(user_message, alignment=Qt.AlignmentFlag.AlignRight, user=True)

        self.loading_widget = LoadingMessage()
        self.chat_layout.addWidget(self.loading_widget)
        self.chat_container.adjustSize()
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

        prompt_model = GenerateTextResponse(user_message, self.main_gui)
        prompt_model.signals.result.connect(self.respond_to_message)
        self.main_gui.pool.start(prompt_model)

        self.input_field.clear()

    # Function for adding models response to chat window
    def respond_to_message(self, message: str):
        if self.loading_widget:
            self.chat_layout.removeWidget(self.loading_widget)
            self.loading_widget.setParent(None)
            self.loading_widget = None

        self.add_message(message, alignment=Qt.AlignmentFlag.AlignLeft, user=False)

