from l3m.l3mGenerateTextResponse import GenerateTextResponse
from PyQt6.QtWidgets import QPushButton, QScrollArea, QLineEdit, QHBoxLayout, QLabel, QFrame, QWidget, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt


class PromptModel(QWidget):
    def __init__(self, main_gui):
        super().__init__()
        self.main_gui = main_gui  # Store reference to GUI

        # Define Layout for Prompt Panel
        self.promptModelLayout = QVBoxLayout()

        # Define the scrollable chat area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_container.setLayout(self.chat_layout)

        self.scroll_area.setWidget(self.chat_container) # Add chat contaier to scroll area

        # Prompt input feild
        self.input_field = QLineEdit()
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
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.returnPressed.connect(self.send_message)

        # Button to send Prompt to model
        self.send_button = QPushButton("Send")
        self.send_button.setFixedSize(36, 36)  # Circle size
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
        self.send_button.clicked.connect(self.send_message)

       # Create horizontal row for input field + send button
        input_row = QHBoxLayout()
        input_row.setContentsMargins(8, 8, 8, 8)
        input_row.setSpacing(8)
        input_row.addWidget(self.input_field)
        input_row.addWidget(self.send_button)

        # Create container for the row
        self.input_container = QWidget()
        self.input_container.setLayout(input_row)
        self.input_container.setStyleSheet("""
            background-color: #4f4f4f;
            border-radius: 24px;
        """)
        self.input_container.setMinimumWidth(400)

        # Add scroll area and input container to main layout
        self.promptModelLayout.addWidget(self.scroll_area)
        self.promptModelLayout.addWidget(self.input_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.promptModelLayout)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Set input container to 80% of total panel width
        parent_width = self.parent().width()
        desired_width = int(parent_width * 0.7)

        self.input_container.setFixedWidth(desired_width)

    #Function for adding users prompt to chat window
    def add_message(self, message, alignment, user=False):
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet(
            "background-color: #e1f5fe; padding: 8px; border-radius: 5px; font-size: 16pt; color: black;" if user else
            "background-color: #c8e6c9; padding: 8px; border-radius: 5px; font-size: 16pt; color: black;"
        )

        message_layout = QHBoxLayout()
        if alignment == Qt.AlignmentFlag.AlignRight:
            message_layout.addStretch()
            message_layout.addWidget(message_label)
        else:
            message_layout.addWidget(message_label)
            message_layout.addStretch()

        message_container = QFrame()
        message_container.setLayout(message_layout)

        self.chat_layout.addWidget(message_container)
        self.chat_container.adjustSize()
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

    # Function that sends users prompt to the model
    def send_message(self):
        user_message = self.input_field.text().strip()
        
        if not user_message:
            return  # Avoid triggering if there's no user input
        elif not self.main_gui.current_tokenizer or not self.main_gui.current_model:
            QMessageBox.warning(
                None, 
                "No Model Selected", 
                "Please select a model first"
            )
        elif user_message:
            self.add_message(user_message, alignment=Qt.AlignmentFlag.AlignRight, user=True)
            prompt_model = GenerateTextResponse(user_message, self.main_gui)
            prompt_model.signals.result.connect(self.respond_to_message)
            self.main_gui.pool.start(prompt_model) #THIS IS WHERE USER QUERRY GETS SENT TO MODEL
            self.input_field.clear()

    # Function for adding models response to chat window
    def respond_to_message(self, message): 
        self.add_message(message, alignment=Qt.AlignmentFlag.AlignLeft, user=False)

