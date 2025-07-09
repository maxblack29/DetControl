from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtCore import Qt

import sys

class GreenLed(QWidget):
    def __init__(self, parent=None, diameter=20):
        super().__init__(parent)
        self.diameter = diameter
        self.setFixedSize(diameter, diameter)
        self.is_on = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.is_on:
            color = QColor(0, 255, 0)  # bright green
        else:
            color = QColor(0, 50, 0)   # dim green (off)
        
        brush = QBrush(color)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        
        painter.drawEllipse(0, 0, self.diameter, self.diameter)

    def turn_on(self):
        self.is_on = True
        self.update()

    def turn_off(self):
        self.is_on = False
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    led = GreenLed(diameter=30)
    led.show()
    
    # Example usage: turn on after 2 seconds
    from PyQt6.QtCore import QTimer
    QTimer.singleShot(2000, led.turn_on)
    
    sys.exit(app.exec())