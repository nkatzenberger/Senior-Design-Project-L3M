from l3mPromptModel import *
from PyQt6.QtWidgets import QPushButton, QScrollArea, QLineEdit, QHBoxLayout,QLabel,QFrame
class PromptPanel():

    def __init__(self):
        # Scrollable chat area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Input area
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)


    #Function for adding a new message in chat window
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

    #function that captures user text input
    def send_message(self):
        user_message = self.input_field.text().strip()
        if user_message:
            self.add_message(user_message, alignment=Qt.AlignmentFlag.AlignRight, user=True)
            prompt_model = PromptModel(user_message, self.tokenizer, self.model)
            prompt_model.signals.result.connect(self.respond_to_message)
            self.pool.start(prompt_model) #THIS IS WHERE USER QUERRY GETS SENT TO MODEL
            self.input_field.clear()

    def respond_to_message(self, message): 
        ##DUMMY RESPONSE FOR TESTING
        #message = "Dummy Response!!"
        self.add_message(message, alignment=Qt.AlignmentFlag.AlignLeft, user=False)

