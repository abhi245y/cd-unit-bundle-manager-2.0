from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMenu
from PyQt6.QtCore import Qt
import sys

class TableWidgetDemo(QWidget):
    def __init__(self):
        super().__init__()

        # Set up layout
        layout = QVBoxLayout()

        # Create table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)  # Set number of columns
        self.table_widget.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])

        # Enable right-click context menu
        self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.open_context_menu)

        # Add table widget to the layout
        layout.addWidget(self.table_widget)

        self.setLayout(layout)
        self.setWindowTitle("Table Widget POC - Right-click to add row")

    def open_context_menu(self, position):
        # Create the context menu
        menu = QMenu()

        # Add 'Add New Row' option to the context menu
        add_new_action = menu.addAction("Add New Row")
        add_new_action.triggered.connect(self.add_new_row)

        # Show the context menu at the mouse position
        menu.exec(self.table_widget.viewport().mapToGlobal(position))

    def add_new_row(self):
        # Get the current row count and add a new row
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        # Optionally, set default values for the new row
        self.table_widget.setItem(row_position, 0, QTableWidgetItem(f"Item {row_position+1} - 1"))
        self.table_widget.setItem(row_position, 1, QTableWidgetItem(f"Item {row_position+1} - 2"))
        self.table_widget.setItem(row_position, 2, QTableWidgetItem(f"Item {row_position+1} - 3"))

# Run the application
app = QApplication(sys.argv)
window = TableWidgetDemo()
window.show()
sys.exit(app.exec())
