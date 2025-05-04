from PyQt6.QtWidgets import (QListWidgetItem, QListWidget,QLabel,QWidget, QSizePolicy, QFileDialog, QVBoxLayout,QPushButton)
from PyQt6.QtCore import Qt, QSize,QStandardPaths
from PyQt6.QtGui import QFont, QIcon
from Process import FileProcessor
class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        button = QPushButton( QIcon("images/file.png"), "Upload")
        button.setIconSize(QSize(32, 32))
        self.file_processor = FileProcessor()
        button.setToolTip("Please upload files")
        button.clicked.connect(self.open_file_dialog)
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        button.setStyleSheet("""
        QPushButton {
                color: white; /* White text */
                text-transform: uppercase;
                font-family: Arial, sans-serif; /* Font */
                font-size: 18px; /* Font size */
                font-weight: bold; /* Bold text */
                border: none; /* No border */
                border-radius: 5px; /* Rounded corners */
                width: 120px; /* Fixed width */
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
        label = QLabel("Please upload logs for Health Check Analysis")
        label.setStyleSheet("font-size:16px; text-transform:uppercase; font-weight: bold")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)        
        
        self.list_widget = QListWidget()        
        self.list_widget.setStyleSheet("""
            QListWidget::indicator {
                border: 2px solid white;  /* Red border for checkboxes */
                width: 16px;
                height: 16px;
            }
            QListWidget::indicator:checked {
                background-color: #2196F3;  /* Optional: Background when checked */
            }
            QListWidget::indicator:unchecked {
                background-color: white;  /* Optional: Background when unchecked */
            }
        """)
        #Add items to the list
        items = ["SPARC Server", "X86-64 Server", "ZFS STORAGE", "Exadata", "ODA"]
        # Define a custom font size
        font = QFont()
        font.setPointSize(18)
        for item_text in items:
            item = QListWidgetItem(item_text)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setFont(font)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.list_widget.addItem(item)        
        
        # Connect selection change signal
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        
        self.list_widget.itemChanged.connect(self.on_item_checked)        
        
        layout1.addWidget(label)
        layout1.addWidget(self.list_widget)
        layout1.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)
        layout1.addWidget(button,alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout1)
    
    def on_selection_changed(self):
        # Get selected items
        selected_items = [item.text() for item in self.list_widget.selectedItems()]
        print("Selected items:", selected_items)    
    
    def on_item_checked(self, item):
        # Handle checkbox state change
        state = "Checked" if item.checkState() == Qt.CheckState.Checked else "Unchecked"
        index = self.list_widget.row(item)
        print(f"Item at index {index} {item.text()} is {state}")    
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


