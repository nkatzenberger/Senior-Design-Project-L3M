import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QGraphicsScene,
                             QGraphicsView, QGraphicsEllipseItem, QVBoxLayout)
from PyQt6.QtCore import QPropertyAnimation, QRectF, QEasingCurve, Qt, QObject, pyqtProperty
from PyQt6.QtGui import QBrush, QColor

class LoadingCircle(QGraphicsEllipseItem, QObject):
    def __init__(self, rect, parent=None):
        super().__init__(rect)
        self._start_angle = 0  # Initial angle
        self.span_angle = 120  # Length of the arc (degrees)
        self.setBrush(QBrush(QColor(0, 120, 215)))

    def set_start_angle(self, angle):
        self._start_angle = angle
        self.update()

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.brush()) 
        painter.drawArc(self.rect(), 0, 50 * 16)
        
class LoadingAnimation(QObject):
    def __init__(self, target, parent=None):
        super().__init__(parent)
        self._start_angle = 0
        self.target = target  # The QGraphicsEllipseItem to update

    def get_start_angle(self):
        return self._start_angle
    
    def set_start_angle(self, angle):
        self._start_angle = angle
        self.target.setStartAngle(angle)
        self.target.scene().update()

    start_angle = pyqtProperty(int, get_start_angle, set_start_angle)

class AnimateIcon(QWidget):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(-50, -50, 100, 100)
        self.view = QGraphicsView(self.scene)
        self.view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(200, 200)

        self.circle_rect = QRectF(-50, -50, 100, 100)
        self.loading_circle = LoadingCircle(self.circle_rect)
        self.scene.addItem(self.loading_circle)
        self.scene.setSceneRect(self.circle_rect)

        self.animation_object = LoadingAnimation(self.loading_circle)

        self.animation = QPropertyAnimation(self.animation_object, b"start_angle")
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setDuration(1000) 
        self.animation.setLoopCount(-1)
        self.animation.setEasingCurve(QEasingCurve.Type.Linear)
        
        self.animation.start()

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
        self.setLayout(layout)
    
    def stopAnimation(self):
        self.animation.stop()
        #self.close()
       