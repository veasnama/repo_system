from PyQt6.QtWidgets import (QLabel,QWidget, QSizePolicy, QFileDialog, QVBoxLayout,QPushButton)
from PyQt6.QtCore import Qt, QSize,QStandardPaths

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        button = QPushButton("Upload")
        button.setToolTip("Please upload files")
        button.clicked.connect(self.open_file_dialog)
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        button.setStyleSheet("""
        QPushButton {
                color: white; /* White text */
                font-family: Arial, sans-serif; /* Font */
                font-size: 14px; /* Font size */
                font-weight: bold; /* Bold text */
                border: none; /* No border */
                border-radius: 5px; /* Rounded corners */
                width: 100px; /* Fixed width */
                height: 40px; /* Fixed height */
                padding: 5px; /* Inner padding */
            }            
        
            QPushButton:hover {
                background-color: #2196F3; /* Blue background on hover */
                color: #FFFFFF; /* Keep text white (or change if desired) */
            }
            QPushButton:pressed {
                background-color: #1976D2; /* Darker blue when pressed */
            }
                                         """)
        
        layout1 = QVBoxLayout()
        label = QLabel("Welcome to Tab 1!\nThis is a simple label.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)        
        layout1.addWidget(label)
        layout1.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)
        layout1.addWidget(button,alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout1)
    def open_file_dialog(self):
        # Create open file dialog
        default_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        file_dialog = QFileDialog(self)
        file_dialog.setDirectory(default_path)
        file_dialog.setWindowFilePath(default_path)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)

        file_dialog.setNameFilter(
            "Supported files (*.txt, *.zip, *.tar.gz);;"
            "Text files (*.txt);;"
            "Archive files (*.tar.gz *.zip);;"
        )

        # Show dialog and get selected file
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            path = selected_files[0]
            # set file path
            #
            self.file_processor.set_file_path(path)
            results = []
            for file_path in selected_files:
                self.file_processor.set_file_path(file_path)
                if self.file_processor.is_valid_file():
                    result = self.file_processor.process_file()
                    results.append(f"{file_path}: {result}")
                else:
                    results.append(f"{file_path}: Invalid file")


