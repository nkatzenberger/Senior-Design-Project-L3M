from l3m.l3mPromptModel import PromptModel
from PyQt6.QtWidgets import QPushButton, QScrollArea, QLineEdit, QHBoxLayout, QLabel, QFrame, QWidget, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation

class BouncingElipses(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.bubble_frame = QFrame()
            self.bubble_frame.setStyleSheet("background-color: #c8e6c9; padding: 8px; border-radius: 5px; font-size: 16pt; color: black;")
            self.bubble_layout = QHBoxLayout(self.bubble_frame)
            
            self.dots = []
            for i in range(3):
                dot = QLabel(".")
                dot.setStyleSheet("font-size: 24px; color: red;")
                dot.setAlignment(Qt.AlignmentFlag.AlignLeft)
                self.dots.append(dot)
            for i, dot in enumerate(self.dots):
                fixed_start_pos = QPoint(15 + (i * 30), 17)  # starting coordinates
                dot.move(fixed_start_pos.x(), fixed_start_pos.y())
            self.animations = []
            self.current_index = 0  # Track which dot is currently animating
            self.animate_next_dot()

        def animate_next_dot(self):
            if self.current_index >= len(self.dots):  # Check if all dots have been animated
                self.current_index = 0
            
            dot = self.dots[self.current_index]
            start_pos = dot.pos()
            end_pos = QPoint(start_pos.x(), start_pos.y()-10)  # Adjust position vertically
            Upanimation = QPropertyAnimation(dot, b"pos")
            Upanimation.setDuration(500)
            Upanimation.setStartValue(start_pos)
            Upanimation.setEndValue(end_pos)
            Downanimation = QPropertyAnimation(dot, b"pos")
            Downanimation.setDuration(500)
            Downanimation.setStartValue(end_pos)
            Downanimation.setEndValue(start_pos)
            Downanimation.finished.connect(self.animate_next_dot)

            Upanimation.start()
            Downanimation.start()
            self.animations.append(Upanimation)
            self.animations.append(Downanimation)
            self.current_index += 1

class PromptPanel(QWidget):
    def __init__(self, main_gui):
        super().__init__()
        self.main_gui = main_gui  # Store reference to GUI

        # Define Layout for Prompt Panel
        self.promptPanel = QVBoxLayout()

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
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.returnPressed.connect(self.send_message)

        # Button to send Prompt to model
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        # Set Layout for Input Area
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        
        # Add everything to Prompt Panel Layout
        self.promptPanel.addWidget(self.scroll_area)
        self.promptPanel.addLayout(input_layout)

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
            AnimatedElipses = BouncingElipses()
            self.add_message(AnimatedElipses, alignment=Qt.AlignmentFlag.AlignLeft, user = False)
            """AnimatedElipses = BouncingElipses()
            self.chat_layout.addWidget(AnimatedElipses)"""
            prompt_model = PromptModel(user_message, self.main_gui.current_tokenizer, self.main_gui.current_model)
            prompt_model.signals.result.connect(self.respond_to_message)
            self.main_gui.pool.start(prompt_model) #THIS IS WHERE USER QUERRY GETS SENT TO MODEL
            self.input_field.clear()

    # Function for adding models response to chat window
    def respond_to_message(self, message): 
        self.add_message(message, alignment=Qt.AlignmentFlag.AlignLeft, user=False)

    