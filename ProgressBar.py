from PyQt6.QtWidgets import QApplication, QMainWindow, QProgressBar, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QThread, pyqtSignal
import sys
import time

class TaskThread(QThread):
    progress_updated = pyqtSignal(int)  # Signal to update progress
    task_finished = pyqtSignal()       # Signal when task is complete

    def __init__(self, duration):
        super().__init__()
        self.duration = duration

    def run(self):
        # Simulate a time-consuming task
        for i in range(100):
            time.sleep(self.duration / 100)  # Simulate work for duration/100 seconds per step
            self.progress_updated.emit(i + 1)  # Emit progress (1 to 100)
        self.task_finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Threaded Progress Bar Task Tracker")
        self.setGeometry(100, 100, 400, 200)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        # Create start button
        self.start_button = QPushButton("Start Task")
        self.start_button.clicked.connect(self.start_task)

        # Add widgets to layout
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.start_button)

        # Initialize task variables
        self.task_duration = 5  # Task duration in seconds
        self.task_thread = None

    def start_task(self):
        # Disable button during task
        self.start_button.setEnabled(False)
        self.progress_bar.setValue(0)

        # Create and start the task thread
        self.task_thread = TaskThread(self.task_duration)
        self.task_thread.progress_updated.connect(self.progress_bar.setValue)
        self.task_thread.task_finished.connect(self.on_task_finished)
        self.task_thread.start()

    def on_task_finished(self):
        # Re-enable button when task is complete
        self.start_button.setEnabled(True)
        self.progress_bar.setValue(100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
