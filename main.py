import sys
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow, QPushButton, QFileDialog)
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLayout, QSizePolicy
from PyQt6 import QtCore, QtGui
from Process import FileProcessor

class FileDialogDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_processor = FileProcessor()
        self.resize(400,200)
        self.setWindowTitle("Report Data Extracter")
        # Enable drag-and-drop on the main window
        self.setAcceptDrops(True)
        # Create central widget and layout
        # Create layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)
        # Create button
        button = QPushButton("Upload")
        button.setToolTip("Please upload files")
        button.clicked.connect(self.open_file_dialog)
        button.setIcon(QtGui.QIcon("images/dragdrop.png"))
        button.setIconSize(QtCore.QSize(50,50))
        button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        button.setFixedSize(100, 50)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        # Add button to layout with stretch factors
        layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)
        layout.addStretch(1)  # Add stretch before button
        layout.addWidget(button)  # Add button
        layout.addStretch(1)  # Add stretch after button
        
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

    def open_file_dialog(self):
        # Create open file dialog
        default_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.DocumentsLocation)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileDialogDemo()
    window.show()
    sys.exit(app.exec())
