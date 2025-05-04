import sys
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow, QPushButton, QFileDialog)
from PyQt6.QtWidgets import (QVBoxLayout, QWidget, QLayout,
      QLabel, QLineEdit, QSizePolicy,QTableWidget, QTableWidgetItem, QTabWidget)
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QTransform
from Process import FileProcessor
from HomePage import HomePage
class FileDialogDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.home_page = HomePage()
        self.resize(800,400)
        self.file_processor = FileProcessor()
        # Create the tab widget
        tabs = QTabWidget()
        tabs.setIconSize(QtCore.QSize(32,32))
        tabs.setStyleSheet("""
         /* Style the QTabWidget (content area) */
    QTabWidget::pane {
        border-radius: 5px; /* Rounded corners */
    }

    /* Style the tab bar */
    QTabBar::tab {
        background-color: #4CAF50; /* Green background like the button */
        color: white; /* White text */
        font-family: Arial, sans-serif;
        font-size: 24px;
        text-transform: uppercase;
        border: none; /* No border */
        padding: 8px 16px; /* Padding for tab size */
        margin-right: 4px; /* Space between tabs */
        min-width: 124px; /* Match button width */
        height: 64px; /* Match button height */
    }
    /* Hover effect for tabs */
    QTabBar::tab:hover {
        background-color: #2196F3; /* Blue background on hover */
        color: #FFFFFF; /* White text */
    }

    /* Selected tab */
    QTabBar::tab:selected {
        background-color: #1976D2; /* Darker blue for active tab */
        color: white;
    }                          
                               
                           """)
        
        # Style the tabs for better appearance
        self.setCentralWidget(tabs)
        self.setWindowTitle("Report Data Extracter")
        # Enable drag-and-drop on the main window
        self.setAcceptDrops(True)

        # layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        # # Add button to layout with stretch factors
        # layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)
        # layout.addStretch(1)  # Add stretch before button
        # layout.addWidget(button)  # Add button
        # layout.addStretch(1)  # Add stretch after button       
      # Tab 1: Simple Label
        tabs.addTab(self.home_page, QtGui.QIcon("images/home-button.png"), "Home") 
        # Create central widget and layout
        
        
        # Tab 2: Input and Button
        tab2 = QWidget()
        layout2 = QVBoxLayout()
        # Kindly add custom widget in between
        tab2.setLayout(layout2)
        tabs.addTab(tab2, "Input")        # Create layout        
        # Tab 3: Table
        tab3 = QWidget()
        layout3 = QVBoxLayout()
        # kindly add widget in between        
        tab3.setLayout(layout3)
        tabs.addTab(tab3, QtGui.QIcon("images/dragdrop.png"), "Table")        # layout = QVBoxLayout()
        
        # Create button

    def on_button_click(sefl, text):
        print(f"You input {text}")
        
    def dragEnterEvent(self, event):
        """Handle drag enter event to accept file drops."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        """Handle drag move event to accept file drops."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop event to process dropped files."""
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            # Get list of dropped file paths
            file_paths = [url.toLocalFile()
                          for url in mime_data.urls() if url.isLocalFile()]

            # Process each dropped file
            results = []
            for file_path in file_paths:
                self.file_processor.set_file_path(file_path)
                print(file_path)
                if self.file_processor.is_valid_file():
                    result = self.file_processor.process_file()
                    results.append(f"{file_path}: {result}")
                else:
                    results.append(f"{file_path}: Invalid file")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileDialogDemo()
    window.show()
    sys.exit(app.exec())
