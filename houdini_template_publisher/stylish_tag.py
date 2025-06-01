from PySide2.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PySide2.QtCore import QTimer, QPropertyAnimation, Qt, QPoint

class Toast(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        self.setLayout(QVBoxLayout())
        self.label = QLabel(self)
        self.label.setStyleSheet("""
            background-color: #333333;
            color: white;
            padding: 10px;
            border-radius: 5px;
        """)
        self.layout().addWidget(self.label)
        self.layout().setContentsMargins(0, 0, 0, 0)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide)
        
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
    
    def show_toast(self, message, duration=3000):
        self.label.setText(message)
        self.label.adjustSize()
        self.adjustSize()
        
        # Position at bottom right of parent or screen
        parent_geometry = self.parent().geometry() if self.parent() else QApplication.desktop().availableGeometry()
        self.move(parent_geometry.right() - self.width() - 20, 
                 parent_geometry.bottom() - self.height() - 20)
        
        self.show()
        
        # Fade in animation
        self.animation.stop()
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        
        self.timer.start(duration)
    
    def hide(self):
        # Fade out animation
        self.animation.stop()
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.finished.connect(super().hide)
        self.animation.start()
        
        self.timer.stop()

from PySide2.QtWidgets import QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Toast Notification Example")
        self.setGeometry(100, 100, 400, 300)
        
        self.toast = Toast(self)
        
        button = QPushButton("Show Toast", self)
        button.clicked.connect(self.show_toast_notification)
        button.move(150, 130)
    
    def show_toast_notification(self):
        self.toast.show_toast("This is a toast notification!", 2000)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()