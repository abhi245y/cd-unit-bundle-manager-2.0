import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMessageBox, QProgressDialog
from BundleBrowserUI import Ui_BundleBrowser
from db_operations import DbOps
from pprint import pprint
from dateutil import parser
from PyQt6.QtCore import QThread, pyqtSignal


class SearchWorker(QThread):
    finished = pyqtSignal(list)

    def __init__(self, db, populateTable, search_params, search_mode):
        super().__init__()
        self.db = db
        self.mode = search_mode
        self.populateTable = populateTable
        self.search_params = search_params
        self.result = None

    def run(self):
        if self.mode == "Normal":
            self.result = self.db.searchBundles(**self.search_params)
        elif self.mode == "Advanced":
            self.result = self.db.adv_search(**self.search_params)

        if len(self.result) != 0:
            self.populateTable(self.result)
        else:
            print("No Result Found")
        self.finished.emit(self.result)


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
        self.search_worker = None

    def configUI(self):
        self.ui.advancedSearchGroupBox.hide()
        self.ui.entryFromDateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.entryToDateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.receviedFromDateEdit.setDateTime(
            QtCore.QDateTime.currentDateTime().addDays(-2)
        )
        self.ui.receivedToDateEdit.setDateTime(QtCore.QDateTime.currentDateTime())

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
        self.ui.fetchEnteredPB.clicked.connect(self.fetchRecentEntered)
        self.ui.fetchReceivedPB.clicked.connect(self.fetchRecentReceived)

    def mousePressEvent(self, event):
        clicked_widget = self.childAt(event.position().toPoint())
        if clicked_widget is not self.ui.colegeTableWidget:
            self.ui.colegeTableWidget.clearSelection()
        super().mousePressEvent(event)

    def populateComboBoxes(self):
        messengers = self.db.getMessengers()
        otherDatas = self.db.getOtherData()

        for messenger in messengers:
            self.ui.messengersCB.addItem(messenger.name)

        for otherData in otherDatas:
            self.ui.routeCB.addItems(otherData.routes)

    def populateTable(self, datas):
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

    def fetchRecentEntered(self):
        entryDate = QtCore.QDateTime.currentDateTime().toPyDateTime().date()
        result = self.db.fetchRecentBundles(
            entryDate,
            None,
            False,
            True,
        )
        if len(result) == 0:
            print("No Result Found")
        self.populateTable(result)

    def fetchRecentReceived(self):
        receivedDate = (
            QtCore.QDateTime.currentDateTime().addDays(-2).toPyDateTime().date()
        )
        result = self.db.fetchRecentBundles(
            None,
            receivedDate,
            True,
            False,
        )
        if len(result) == 0:
            print("No Result Found")
        self.populateTable(result)

    # def startSearch(self):
    #     entryDateFrom = self.ui.entryFromDateEdit.date().toPyDate()
    #     entryDateTo = self.ui.entryToDateEdit.date().toPyDate()
    #     received_date_from = self.ui.receviedFromDateEdit.date().toPyDate()
    #     received_date_to = self.ui.receivedToDateEdit.date().toPyDate()

    #     print(self.ui.receviedDateRB.isChecked(), self.ui.entryDateRB.isChecked())
    #     if (
    #         not self.ui.receviedDateRB.isChecked()
    #         and not self.ui.entryDateRB.isChecked()
    #     ):
    #         print("Select at least one date")
    #     else:
    #         result = self.db.searchBundles(
    #             entryDateFrom,
    #             entryDateTo,
    #             received_date_from,
    #             received_date_to,
    #             self.ui.receviedDateRB.isChecked(),
    #             self.ui.entryDateRB.isChecked(),
    #         )
    #         if len(result) == 0:
    #             print("No Result Found")
    #         self.populateTable(result)

    def startSearch(self):
        self.ui.tableWidget.clearContents()
        entryDateFrom = self.ui.entryFromDateEdit.date().toPyDate()
        entryDateTo = self.ui.entryToDateEdit.date().toPyDate()
        received_date_from = self.ui.receviedFromDateEdit.date().toPyDate()
        received_date_to = self.ui.receivedToDateEdit.date().toPyDate()

        if (
            not self.ui.receviedDateRB.isChecked()
            and not self.ui.entryDateRB.isChecked()
        ):
            print("Select at least one date")
            return

        search_params = {
            "entryDateFrom": entryDateFrom,
            "entryDateTo": entryDateTo,
            "received_date_from": received_date_from,
            "received_date_to": received_date_to,
            "received_date_check": self.ui.receviedDateRB.isChecked(),
            "date_of_entry_check": self.ui.entryDateRB.isChecked(),
        }
        self.ui.tableWidget.blockSignals(True)
        self.ui.tableWidget.setVisible(False)
        self.progress_dialog = QProgressDialog("Searching...", "Cancel", 0, 0, self)
        self.progress_dialog.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.canceled.connect(self.cancelSearch)

        self.search_worker = SearchWorker(
            self.db, self.populateTable, search_params, "Normal"
        )
        self.search_worker.finished.connect(self.searchFinished)

        self.search_worker.start()
        self.progress_dialog.show()

    def cancelSearch(self):
        if self.search_worker and self.search_worker.isRunning():
            self.search_worker.terminate()
            self.search_worker.wait()
            self.search_worker = None

    def searchFinished(self, result):
        self.search_worker.quit()
        self.search_worker.wait()
        self.progress_dialog.close()
        self.ui.tableWidget.blockSignals(False)
        self.ui.tableWidget.setVisible(True)
        if len(result) == 0:
            QMessageBox.warning(self, "Warnning", "No Bundles Found")
        self.search_worker = None

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
        date_of_entry = self.ui.entryFromDateEdit.date().toPyDate()
        received_date = self.ui.receviedFromDateEdit.date().toPyDate()

        search_params = {
            "messenger": messenger,
            "qp_code_input": qp_code_input,
            "college_code": college_code,
            "date_of_entry": date_of_entry,
            "received_date": received_date,
            "received_date_check": self.ui.receviedDateRB.isChecked(),
            "date_of_entry_check": self.ui.entryDateRB.isChecked(),
        }
        self.ui.tableWidget.blockSignals(True)
        self.ui.tableWidget.setVisible(False)
        self.progress_dialog = QProgressDialog("Searching...", "Cancel", 0, 0, self)
        self.progress_dialog.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.canceled.connect(self.cancelSearch)

        self.search_worker = SearchWorker(
            self.db, self.populateTable, search_params, "Advanced"
        )
        self.search_worker.finished.connect(self.searchFinished)

        self.search_worker.start()
        self.progress_dialog.show()

    def track_changes(self, item):
        row = item.row()
        column = item.column()
        new_value = item.text()

        bundle_id = self.ui.tableWidget.item(row, 8).text()
        if bundle_id:
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

            result, e = self.db.execute_custom(user_query=user_query)
            if result is not None:
                self.populateTable(result)
            elif "Connection error" in str(e):
                QMessageBox.critical(
                    self, "No Internet", "Please Check your network connetion"
                )

            self.ui.aiSearchPB.setEnabled(True)
            self.ui.aiSearchPB.setText("AI Search")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BundleBrowserApp()
    window.show()
    sys.exit(app.exec())
