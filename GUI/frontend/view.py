import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt  # Import Qt for alignment flags
from PyQt6.QtGui import QTextCursor

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("L3M GUI")
        self.setGeometry(100, 100, 1280, 720)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        panelLayout = QHBoxLayout() #overall layout
        leftPanel = QVBoxLayout() #everything at the left
        rightPanel = QVBoxLayout() #everything at the right

        #LEFT PANEL CHAT WINDOW STUFF ################################################################################
        #TODO: these are just examples for the side panel. can be replaced with buttons, sub layouts, whatever
        self.exampleLabel1 = QLabel("I am an example")
        self.exampleLabel2 = QLabel("I am an example")
        self.exampleLabel3 = QLabel("I am an example")

        self.exampleLabel1.setStyleSheet(
            "background-color: #blue; padding: 8px; border-radius: 5px; font-size: 16pt; color: black;"
        )
        self.exampleLabel2.setStyleSheet(
            "background-color: #red; padding: 8px; border-radius: 5px; font-size: 16pt; color: black;"
        )
        self.exampleLabel3.setStyleSheet(
            "background-color: #green; padding: 8px; border-radius: 5px; font-size: 16pt; color: black;"
        )
        leftPanel.addWidget(self.exampleLabel1)
        leftPanel.addWidget(self.exampleLabel2)
        leftPanel.addWidget(self.exampleLabel3)



        #RIGHT PANEL CHAT WINDOW STUFF ################################################################################
        # Scrollable chat area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_container.setLayout(self.chat_layout)

        self.scroll_area.setWidget(self.chat_container)
        rightPanel.addWidget(self.scroll_area)

        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        send_button = QPushButton("Send", self)
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)

        #add the chat layout to the right panel
        rightPanel.addLayout(input_layout)

        # add layouts to central panel layout and add to main widget
        panelLayout.addLayout(leftPanel)
        panelLayout.addLayout(rightPanel)
        central_widget.setLayout(panelLayout)



#functions that are called with buttons etc..

    #function that captures user text input
    def send_message(self):
        user_message = self.input_field.text().strip()
        if user_message:
            self.add_message(user_message, alignment=Qt.AlignmentFlag.AlignRight, user=True)
            self.respond_to_message(user_message) #THIS IS WHERE USER QUERRY GETS SENT TO MODEL
            self.input_field.clear()

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

    def respond_to_message(self, message):
        #TODO: dummy response, just repeats back to you for now, write logic here to get response from model
        response = f"(Model Name): you said '{message}'"
        self.add_message(response, alignment=Qt.AlignmentFlag.AlignLeft, user=False)



#entry point for testing, code inside is how you would start GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec())