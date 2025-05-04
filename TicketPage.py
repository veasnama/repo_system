from PyQt6.QtWidgets import QApplication,QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QTimeEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel
from PyQt6.QtCore import QDateTime, QDate, QTime
from PyQt6.QtGui import QFont
import sys

class TaskNoteWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Note Widget")
        self.setGeometry(100, 100, 600, 400)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)


        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tasks...")
        self.search_input.textChanged.connect(self.search_tasks)
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)

        # Clear search button
        self.clear_search_button = QPushButton("Clear Search")
        self.clear_search_button.clicked.connect(self.clear_search)
        search_layout.addWidget(self.clear_search_button)

        main_layout.addLayout(search_layout)

        # Input form layout
        form_layout = QVBoxLayout()
        font = QFont()
        font.setPixelSize(18)
        font.setWordSpacing(1.2)

        # Task name
        self.task_name_input = QLineEdit()
        self.task_name_input.setFont(font)
        self.task_name_input.setPlaceholderText("Enter task name")
        task_label =QLabel("Task Name:")
        task_label.setFont(font)
        form_layout.addWidget(task_label)
        form_layout.addWidget(self.task_name_input)

        # Customer (dropdown)
        self.customer_input = QComboBox()
        self.customer_input.setFont(font)
        self.customer_input.addItems(["ABA", "ACLEDA", "HATTHA", "PHILLIP", "CAB"])
        customer_label = QLabel("Customer")
        customer_label.setFont(font)
        form_layout.addWidget(customer_label)
        form_layout.addWidget(self.customer_input)

        # Task type
        self.task_type_input = QComboBox()
        self.task_type_input.setFont(font)
        self.task_type_input.addItems(["Onsite", "Remote", "Zoom", "MSTeam", "Docx"])

        type_label = QLabel("Customer")
        type_label.setFont(font)
        form_layout.addWidget(type_label)
        form_layout.addWidget(self.task_type_input)

        # Start time
        self.start_date = QDate.currentDate()  # Store fixed date
        self.start_time_input = QTimeEdit()
        self.start_time_input.setFont(font)
        self.start_time_input.setDisplayFormat("hh:mm:ss")
        self.start_time_input.setTime(QTime.currentTime())
        form_layout.addWidget(QLabel("Start Time:"))
        form_layout.addWidget(self.start_time_input)

        # End time
        self.end_date = QDate.currentDate()  # Store fixed date
        self.end_time_input = QTimeEdit()
        self.end_time_input.setFont(font)
        self.end_time_input.setDisplayFormat("hh:mm:ss")
        self.end_time_input.setTime(QTime.currentTime())
        form_layout.addWidget(QLabel("End Time:"))
        form_layout.addWidget(self.end_time_input)

        # Add task button
        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.add_task)
        form_layout.addWidget(self.add_task_button)

        # Add form to main layout
        main_layout.addLayout(form_layout)

        # Task table
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(5)
        self.task_table.setHorizontalHeaderLabels(["Task Name", "Customer", "Task Type", "Start DateTime", "End DateTime"])
        self.task_table.setFont(font)
        self.task_table.setRowCount(0)
        self.task_table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.task_table)

    def search_tasks(self, query):
        query = query.lower().strip()
        for row in range(self.task_table.rowCount()):
            match = False
            for col in range(self.task_table.columnCount()):
                item = self.task_table.item(row, col)
                if item and query in item.text().lower():
                    match = True
                    break
            self.task_table.setRowHidden(row, not match)

    def clear_search(self):
        # Clear search input and show all rows
        self.search_input.clear()
        for row in range(self.task_table.rowCount()):
            self.task_table.setRowHidden(row, False)
    def add_task(self):
        # Get input values
        task_name = self.task_name_input.text().strip()
        customer = self.customer_input.currentText()
        task_type = self.task_type_input.currentText()

        # Combine fixed date with user-entered time
        start_time = self.start_time_input.time()
        start_datetime = QDateTime(self.start_date, start_time)
        start_datetime_str = start_datetime.toString("yyyy-MM-dd hh:mm:ss")

        end_time = self.end_time_input.time()
        end_datetime = QDateTime(self.end_date, end_time)
        end_datetime_str = end_datetime.toString("yyyy-MM-dd hh:mm:ss")

        # Validate inputs
        if not task_name:
            return  # Ignore empty task name

        # Add new row to table
        row_count = self.task_table.rowCount()
        self.task_table.insertRow(row_count)

        # Populate table with task data
        self.task_table.setItem(row_count, 0, QTableWidgetItem(task_name))
        self.task_table.setItem(row_count, 1, QTableWidgetItem(customer))
        self.task_table.setItem(row_count, 2, QTableWidgetItem(task_type))
        self.task_table.setItem(row_count, 3, QTableWidgetItem(start_datetime_str))
        self.task_table.setItem(row_count, 4, QTableWidgetItem(end_datetime_str))

        # Clear input fields
        self.task_name_input.clear()
        self.customer_input.setCurrentIndex(0)
        self.task_type_input.setCurrentIndex(0)
        self.start_time_input.setTime(QTime.currentTime())
        self.end_time_input.setTime(QTime.currentTime())

        
        self.search_tasks(self.search_input.text())
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TaskNoteWidget()
    window.show()
    sys.exit(app.exec())
