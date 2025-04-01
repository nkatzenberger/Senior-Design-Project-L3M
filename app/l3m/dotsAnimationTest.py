from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint

class ChatBubble(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Chat bubble frame
        self.bubble_frame = QFrame()
        self.bubble_frame.setStyleSheet("background-color: #c8e6c9; padding: 8px; border-radius: 5px; font-size: 16pt; color: black;")
        self.bubble_layout = QHBoxLayout(self.bubble_frame)
        main_layout.addWidget(self.bubble_frame, alignment=Qt.AlignmentFlag.AlignLeft)

        # Three dots (QLabels)
        self.dots = []
        for i in range(3):
            dot = QLabel(".")
            dot.setStyleSheet("font-size: 24px; color: black;")
            dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.bubble_layout.addWidget(dot)
            self.dots.append(dot)

        for i, dot in enumerate(self.dots):
            fixed_start_pos = QPoint(15 + (i * 30), 17)  # Example coordinates
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



if __name__ == '__main__':
    app = QApplication([])
    window = ChatBubble()
    window.show()
    app.exec()