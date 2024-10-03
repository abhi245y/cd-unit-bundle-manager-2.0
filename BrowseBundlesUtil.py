import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QPen
from PyQt6.QtWidgets import QMessageBox
from BundleBrowserUI import Ui_BundleBrowser  # Import the generated UI class
from db_operations import DbOps
from pprint import pprint
from dateutil import parser


class BundleBrowserApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_BundleBrowser()
        self.ui.setupUi(self)
        self.configUI()
        self.connectSignals()
        self.db = DbOps()
        self.populateComboBoxes()
        self.changed_items = {}

    def configUI(self):
        self.ui.advancedSearchGroupBox.hide()
        self.ui.entryDateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.receviedDateEdit.setMinimumDate(QtCore.QDate(2024, 9, 14))
        self.ui.tableWidget.setColumnHidden(8, True)

        collegeTableHeader = self.ui.colegeTableWidget.horizontalHeader()
        collegeTableHeader.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch
        )

        mainTableHeader = self.ui.tableWidget.horizontalHeader()
        mainTableHeader.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        mainTableHeader.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        mainTableHeader.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        mainTableHeader.setSectionResizeMode(
            3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        mainTableHeader.setSectionResizeMode(
            4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        mainTableHeader.setSectionResizeMode(
            5, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        mainTableHeader.setSectionResizeMode(
            6, QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        mainTableHeader.setSectionResizeMode(
            7, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )

    def connectSignals(self):
        # Connect signals to interact with the UI elements as needed
        # For example, a button click can trigger a function
        self.ui.showAdvancedPB.clicked.connect(self.showHideAdvSeach)
        self.ui.searchPB.clicked.connect(self.startSearch)
        self.ui.routeCB.currentIndexChanged.connect(self.on_route_selected)
        self.ui.advancedsearchPB.clicked.connect(self.advanced_search)
        self.ui.clearPB.clicked.connect(self.clearFilter)
        self.ui.tableWidget.itemChanged.connect(self.track_changes)
        self.ui.updatePB.clicked.connect(self.update_data)
        self.ui.deletePB.clicked.connect(self.delete_selected_items)
        self.ui.actionShow_ID.triggered.connect(self.toggle_id_column)
        self.ui.aiSearchPB.clicked.connect(self.attemptAISearch)
        pass

    def mousePressEvent(self, event):
        clicked_widget = self.childAt(event.position().toPoint())
        if clicked_widget is not self.ui.colegeTableWidget:
            self.ui.colegeTableWidget.clearSelection()
        super().mousePressEvent(event)

    def populateComboBoxes(self):
        # Populating routeComboBox, messengerComboBox, and collegeComboBox from the database
        # self.cursor.execute("SELECT route_name FROM routes")

        messengers = self.db.getMessengers()
        otherDatas = self.db.getOtherData()

        for messenger in messengers:
            self.ui.messengersCB.addItem(messenger.name)

        for otherData in otherDatas:
            self.ui.routeCB.addItems(otherData.routes)

        # for college in colleges:
        #     self.ui.collegeComboBox.addItem(college[0])

    def setDateEdit(self, date):
        # Sets the dateEdit widget to a specific date
        self.ui.dateEdit.setDate(date)

    # def collectUserInput(self):
    #     # Collect data from the UI elements and update the database
    #     selected_date = self.ui.dateEdit.date().toString("yyyy-MM-dd")
    #     selected_route = self.ui.routeComboBox.currentText()
    #     selected_messenger = self.ui.messengerComboBox.currentText()
    #     selected_college = self.ui.collegeComboBox.currentText()

    # Example of updating the database with collected data

    # def closeEvent(self, event):
    #     # Close the database connection when the window is closed
    #     self.conn.close()
    #     event.accept()

    def populateTable(self, datas):
        self.ui.tableWidget.blockSignals(True)
        self.ui.tableWidget.setRowCount(0)
        for data in datas:
            id = data.id
            qp_series = data.qp_series
            qp_code = data.qp_code
            messenger = data.messenger_name
            college_name = self.db.getCollegeNameByCode(data.college_code).name
            remarks = data.remarks
            received_date = data.received_date
            date_of_entry = data.date_of_entry
            is_nill = data.is_nill

            rowPosition = self.ui.tableWidget.rowCount()

            self.ui.tableWidget.insertRow(rowPosition)
            self.ui.tableWidget.setItem(
                rowPosition, 0, QtWidgets.QTableWidgetItem(str(received_date))
            )
            self.ui.tableWidget.setItem(
                rowPosition, 1, QtWidgets.QTableWidgetItem(qp_series)
            )
            self.ui.tableWidget.setItem(
                rowPosition, 2, QtWidgets.QTableWidgetItem(qp_code)
            )
            self.ui.tableWidget.setItem(
                rowPosition, 3, QtWidgets.QTableWidgetItem(str(is_nill))
            )
            self.ui.tableWidget.setItem(
                rowPosition, 4, QtWidgets.QTableWidgetItem(str(date_of_entry))
            )
            self.ui.tableWidget.setItem(
                rowPosition, 5, QtWidgets.QTableWidgetItem(messenger)
            )
            self.ui.tableWidget.setItem(
                rowPosition, 6, QtWidgets.QTableWidgetItem(college_name)
            )
            self.ui.tableWidget.setItem(
                rowPosition, 7, QtWidgets.QTableWidgetItem(remarks)
            )
            self.ui.tableWidget.setItem(rowPosition, 8, QtWidgets.QTableWidgetItem(id))
        self.ui.tableWidget.blockSignals(False)

    def showHideAdvSeach(self):
        if self.ui.advancedSearchGroupBox.isVisible():
            self.ui.advancedSearchGroupBox.hide()
        else:
            self.ui.advancedSearchGroupBox.show()

    def clearFilter(self):
        self.ui.colegeTableWidget.setRowCount(0)
        self.ui.routeCB.setCurrentIndex(-1)
        self.ui.messengersCB.setCurrentIndex(-1)
        self.ui.qpCodeLineEdit.clear()

    def startSearch(self):
        entryDate = self.ui.entryDateEdit.date().toPyDate()
        received_date = self.ui.receviedDateEdit.date().toPyDate()
        print(self.ui.receviedDateRB.isChecked(), self.ui.entryDateRB.isChecked())
        if (
            not self.ui.receviedDateRB.isChecked()
            and not self.ui.entryDateRB.isChecked()
        ):
            print("Select at least one date")
        else:
            result = self.db.searchBundles(
                entryDate,
                received_date,
                self.ui.receviedDateRB.isChecked(),
                self.ui.entryDateRB.isChecked(),
            )
            self.populateTable(result)

    def on_route_selected(self):
        selected_route = self.ui.routeCB.currentText()
        colleges_data = self.db.getCollegesByRoute(selected_route)

        self.ui.colegeTableWidget.setRowCount(0)
        for college in colleges_data:
            rowPosition = self.ui.colegeTableWidget.rowCount()

            self.ui.colegeTableWidget.insertRow(rowPosition)
            self.ui.colegeTableWidget.setItem(
                rowPosition, 0, QtWidgets.QTableWidgetItem(college.name)
            )

    def advanced_search(self):
        messenger = (
            self.ui.messengersCB.currentText()
            if self.ui.messengersCB.currentText()
            else None
        )
        qp_code_input = (
            self.ui.qpCodeLineEdit.text() if self.ui.qpCodeLineEdit.text() else None
        )
        college_code = (
            self.db.getCollegeByName(
                self.ui.colegeTableWidget.currentItem().text()
            ).code
            if self.ui.colegeTableWidget.currentItem()
            else None
        )
        date_of_entry = self.ui.entryDateEdit.date().toPyDate()
        received_date = self.ui.receviedDateEdit.date().toPyDate()

        # pprint(f'{messenger, qp_code_input, college_code, date_of_entry, received_date, self.ui.receviedDateRB.isChecked(), self.ui.entryDateRB.isChecked()}')
        self.populateTable(
            self.db.adv_search(
                messenger=messenger,
                qp_code_input=qp_code_input,
                college_code=college_code,
                date_of_entry=date_of_entry,
                received_date=received_date,
                received_date_check=self.ui.receviedDateRB.isChecked(),
                date_of_entry_check=self.ui.entryDateRB.isChecked(),
            )
        )

    def track_changes(self, item):
        row = item.row()
        column = item.column()
        new_value = item.text()

        # Get the ID for the row, assuming ID is in the last column (column index 8)
        bundle_id = self.ui.tableWidget.item(row, 8).text()
        if bundle_id:
            # Track the change in the form of {row: {column: value}}
            if bundle_id not in self.changed_items:
                self.changed_items[bundle_id] = {}

            if column == 0 or column == 4:
                parsed_date = parser.parse(new_value)
                formatted_date = parsed_date.strftime("%Y-%m-%d")
                self.changed_items[bundle_id][column] = formatted_date
            else:
                self.changed_items[bundle_id][column] = new_value

        pprint(self.changed_items)

    def update_data(self):
        confirmation = QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to save the changes?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            self.db.save_changes_to_db(new_data=self.changed_items)
            QMessageBox.information(self, "Success", "Changes saved successfully!")

    def delete_selected_items(self):
        selected_items = self.ui.tableWidget.selectedItems()

        if not selected_items:
            QtWidgets.QMessageBox.warning(
                self, "No Selection", "Please select rows to delete."
            )
            return
        selected_rows = set(item.row() for item in selected_items)
        confirmation = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            f"Are you sure you want to delete {len(selected_rows)} Bundle(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        try:
            for row in sorted(selected_rows, reverse=True):
                bundle_id = self.ui.tableWidget.item(row, 8).text()
                self.db.delete_bundle(bundle_id=bundle_id)
                self.ui.tableWidget.removeRow(row)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Error", f"Failed to delete record: {str(e)}"
            )
            return

        QtWidgets.QMessageBox.information(
            self, "Success", f"{len(selected_rows)} row(s) deleted successfully."
        )

    def toggle_id_column(self):
        """
        Toggles the visibility of the ID column in the table.
        """
        id_column_index = 8

        if self.ui.tableWidget.isColumnHidden(id_column_index):
            self.ui.tableWidget.setColumnHidden(id_column_index, False)
            self.ui.actionShow_ID.setChecked(True)
        else:
            self.ui.tableWidget.setColumnHidden(id_column_index, True)
            self.ui.actionShow_ID.setChecked(False)

    def attemptAISearch(self):
        user_query = self.ui.searchLineEdit.text()
        print(user_query)
        if user_query is not None or user_query != "":
            self.ui.aiSearchPB.setEnabled(False)
            self.ui.aiSearchPB.setText("Searching...")
            QtCore.QCoreApplication.processEvents()

            result = self.db.execute_custom(user_query=user_query)
            if result is not None:
                print(result)
                self.populateTable(result)

            self.ui.aiSearchPB.setEnabled(True)
            self.ui.aiSearchPB.setText("AI Search")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BundleBrowserApp()
    window.show()
    sys.exit(app.exec())
