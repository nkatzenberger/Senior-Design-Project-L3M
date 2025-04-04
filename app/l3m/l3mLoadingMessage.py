from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame
from PyQt6.QtCore import Qt, QPropertyAnimation, QTimer, QRect

class LoadingMessage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Chat bubble frame
        self.bubble_frame = QFrame()
        self.bubble_frame.setStyleSheet("background-color: transparent;")
        self.bubble_layout = QHBoxLayout(self.bubble_frame)
        self.bubble_layout.setSpacing(0)  # Adjust spacing here
        self.bubble_layout.setContentsMargins(0, 0, 0, 0)
        self.bubble_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        main_layout.addWidget(self.bubble_frame, alignment=Qt.AlignmentFlag.AlignLeft)

        self.dots = []
        for _ in range(3):
            dot = QLabel("•")
            dot.setStyleSheet("font-size: 30px; color: white; background-color: transparent;")
            dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dot.setFixedSize(10, 36)  # Force layout to behave

            self.bubble_layout.addWidget(dot)
            self.dots.append(dot)

        self.animations = []
        self.current_index = 0
        QTimer.singleShot(0, self.store_original_geometries)
        QTimer.singleShot(0, self.animate_next_dot)

    def store_original_geometries(self):
        self.original_geometries = [dot.geometry() for dot in self.dots]

    def animate_next_dot(self):
        dot = self.dots[self.current_index]
        original_rect = dot.geometry()

        # Animate geometry up
        up_anim = QPropertyAnimation(dot, b"geometry")
        up_anim.setDuration(250)
        up_anim.setStartValue(original_rect)
        up_anim.setEndValue(QRect(
            original_rect.x(),
            original_rect.y() - 10,
            original_rect.width(),
            original_rect.height()
        ))

        # Animate geometry down
        down_anim = QPropertyAnimation(dot, b"geometry")
        down_anim.setDuration(250)
        down_anim.setStartValue(up_anim.endValue())
        down_anim.setEndValue(original_rect)

        up_anim.finished.connect(down_anim.start)
        QTimer.singleShot(250, self.animate_next_dot)

        self.animations.extend([up_anim, down_anim])
        up_anim.start()

        self.current_index = (self.current_index + 1) % len(self.dots)