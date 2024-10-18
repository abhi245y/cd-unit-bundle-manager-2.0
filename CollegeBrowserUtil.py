import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMessageBox
from CollegeBrowserUI import Ui_CollegeBrowserUI
from AddNewCollegeDialogueBox import Ui_AddNewCollege
from db_operations import DbOps
from PyQt6.QtCore import QThread, pyqtSignal
from types import SimpleNamespace


class ButtonCreationThread(QThread):
    buttonCreated = pyqtSignal(int)

    def __init__(self, rows_count):
        super().__init__()
        self.rows_count = rows_count

    def run(self):
        for row in range(self.rows_count):
            self.buttonCreated.emit(row)
            self.msleep(10)


class CollegeBrowserApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_CollegeBrowserUI()
        self.ui.setupUi(self)
        self.configUI()
        self.db = DbOps()
        self.populateComboBoxes()
        self.connectSignals()

    def configUI(self):
        collegeTableHeader = self.ui.collegeDataTable.horizontalHeader()
        collegeTableHeader.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        collegeTableHeader.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        collegeTableHeader.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        collegeTableHeader.setSectionResizeMode(
            3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        collegeTableHeader.setSectionResizeMode(
            4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        self.ui.courseCB.setEnabled(False)
        self.ui.collegeTypeCB.setEnabled(False)
        self.ui.routeCB.setEnabled(False)
        self.ui.collegeCodelineEdit.setEnabled(False)

    def connectSignals(self):
        self.ui.getALLPB.clicked.connect(self.getAllColleges)
        self.ui.searchPB.clicked.connect(self.searchCollege)
        self.ui.courseIncludeRB.toggled.connect(self.on_radio_button_toggled)
        self.ui.collegeTypeIncludeRB.toggled.connect(self.on_radio_button_toggled)
        self.ui.routeIncludeRB.toggled.connect(self.on_radio_button_toggled)
        self.ui.collegCodeIncludeCheckBox.toggled.connect(self.on_radio_button_toggled)
        self.ui.addNewPB.clicked.connect(self.showAddNewCollegeDialog)
        self.ui.viewAllCoursesPB.clicked.connect(self.viewCourses)
        self.ui.viewAllMessengersPB.clicked.connect(self.viewMessengers)
        self.ui.viewAllRoutesPB.clicked.connect(self.viewRoutes)

    def on_radio_button_toggled(self):
        self.ui.courseCB.setEnabled(self.ui.courseIncludeRB.isChecked())
        self.ui.collegeTypeCB.setEnabled(self.ui.collegeTypeIncludeRB.isChecked())
        self.ui.routeCB.setEnabled(self.ui.routeIncludeRB.isChecked())
        self.ui.collegeCodelineEdit.setEnabled(
            self.ui.collegCodeIncludeCheckBox.isChecked()
        )

    def showAddNewCollegeDialog(self):
        dialog = QtWidgets.QDialog(self)
        ui = Ui_AddNewCollege()
        ui.setupUi(dialog)

        self.populateAddNewCollegeDialog(ui)
        ui.addCollegeDialogePB.accepted.connect(lambda: self.addNewCollege(ui, dialog))

        dialog.exec()

    def populateAddNewCollegeDialog(self, ui):
        otherDatas = self.db.getOtherData()
        for otherData in otherDatas:
            ui.routeCB.addItems(otherData.routes)
        from database_setup import CollegeType as college_type

        for type in college_type:
            ui.collgeTypeCB.addItem(type.value, type)
        courses = self.db.getAllCourses()
        for course in courses:
            item = QtWidgets.QListWidgetItem(course.name)
            item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            ui.courseList.addItem(item)

    def addNewCollege(self, ui, dialog):
        college_code = ui.collegeCodeLE.text()
        college_name = ui.collegeNameLE.text()
        selected_route = ui.routeCB.currentText()
        college_type = ui.collgeTypeCB.currentData()

        selected_courses_code = []
        for i in range(ui.courseList.count()):
            item = ui.courseList.item(i)
            if item.checkState() == QtCore.Qt.CheckState.Checked:
                course_code = self.db.getCourseByCourseName(item.text()).code
                selected_courses_code.append(course_code)
        # print(college_code, college_name, route, college_type,selected_courses_code)
        college_data = SimpleNamespace(
            code=college_code,
            name=college_name,
            route=selected_route,
            type=college_type,
            courses=selected_courses_code,
        )
        success = self.db.add_new_college(college_data)
        if success:
            QtWidgets.QMessageBox.information(
                self, "Success", "New college added successfully!"
            )
            dialog.accept()
            self.getAllColleges()
        else:
            QtWidgets.QMessageBox.warning(
                self, "Error", "Failed to add new college. Please try again."
            )

    def populateComboBoxes(self):
        from database_setup import CollegeType as college_type

        otherDatas = self.db.getOtherData()
        courses = self.db.getAllCourses()

        for course in courses:
            self.ui.courseCB.addItem(course.name)

        for otherData in otherDatas:
            self.ui.routeCB.addItems(otherData.routes)

        for type in college_type:
            self.ui.collegeTypeCB.addItem(type.value, type)

    def populateCollegeTable(self, datas):
        self.ui.collegeDataTable.blockSignals(True)
        self.ui.collegeDataTable.setRowCount(0)

        for data in datas:
            rowPosition = self.ui.collegeDataTable.rowCount()
            clg_name = data.name
            clg_code = data.code
            clg_type = (
                data.college_type.value if data.college_type is not None else "Pending"
            )
            clg_route = data.route if data.route is not None else "Pending"

            self.ui.collegeDataTable.insertRow(rowPosition)
            self.ui.collegeDataTable.setItem(
                rowPosition, 0, QtWidgets.QTableWidgetItem(clg_name)
            )
            self.ui.collegeDataTable.setItem(
                rowPosition, 1, QtWidgets.QTableWidgetItem(str(clg_code))
            )
            self.ui.collegeDataTable.setItem(
                rowPosition, 2, QtWidgets.QTableWidgetItem(clg_type)
            )
            self.ui.collegeDataTable.setItem(
                rowPosition, 4, QtWidgets.QTableWidgetItem(clg_route)
            )

        self.startButtonCreationThread(len(datas))

    def startButtonCreationThread(self, rows_count):
        self.button_thread = ButtonCreationThread(rows_count)
        self.button_thread.buttonCreated.connect(self.addButtonToTable)
        self.button_thread.start()

    def addButtonToTable(self, row):
        button = QtWidgets.QPushButton("Show Courses")
        self.ui.collegeDataTable.setCellWidget(row, 3, button)
        button.clicked.connect(lambda: self.handleButtonClicked(row))

    def handleButtonClicked(self, row):
        clg_code = self.ui.collegeDataTable.item(row, 1).text()
        courses = self.db.getCoursesByCollegeCode(int(clg_code))
        self.showPopupWithList(courses)

    def showPopupWithList(self, courses):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Course Details")
        list_widget = QtWidgets.QListWidget()
        for course in courses:
            list_widget.addItem(course.name)
        dialog_layout = QtWidgets.QVBoxLayout(dialog)
        dialog_layout.addWidget(list_widget)
        dialog.exec()

    def getAllColleges(self):
        colleges = self.db.getAllColleges()
        self.populateCollegeTable(colleges)

    def populateOtherDataTable(self, datas):
        # self.ui.otherDataTable.blockSignals(True)
        print(datas[0])
        self.ui.otherDataTable.clearContents()
        self.ui.otherDataTable.setRowCount(0)
        column_names = [
            key for key in vars(datas[0]).keys() if not key.startswith("_sa")
        ]
        # print(column_names)
        self.ui.otherDataTable.setColumnCount(len(column_names))
        self.ui.otherDataTable.setHorizontalHeaderLabels(column_names)

        self.ui.otherDataTable.setRowCount(len(datas))

        for row_idx, course in enumerate(datas):
            for col_idx, col_name in enumerate(column_names):
                cell_value = getattr(course, col_name, "N/A")
                if cell_value is None:
                    cell_value = "N/A"
                else:
                    cell_value = str(cell_value)
                self.ui.otherDataTable.setItem(
                    row_idx, col_idx, QtWidgets.QTableWidgetItem(cell_value)
                )
        self.ui.otherDataTable.resizeColumnsToContents()

    def viewCourses(self):
        courses = self.db.getAllCourses()
        self.populateOtherDataTable(courses)

    def viewMessengers(self):
        messengers = self.db.getMessengers()
        self.populateOtherDataTable(messengers)

    def viewRoutes(self):
        otherData = self.db.getOtherData()
        self.populateOtherDataTable(otherData)

    def searchCollege(self):
        inlcude_course = self.ui.courseIncludeRB.isChecked()
        include_college_type = self.ui.collegeTypeIncludeRB.isChecked()
        include_route = self.ui.routeIncludeRB.isChecked()
        include_colleg_code = self.ui.collegCodeIncludeCheckBox.isChecked()

        if (
            inlcude_course
            or include_college_type
            or include_route
            or include_colleg_code
        ):
            result = self.db.serachColleges(
                inlcude_course,
                include_college_type,
                include_route,
                include_colleg_code,
                self.ui.courseCB.currentText(),
                self.ui.collegeTypeCB.currentData(),
                self.ui.routeCB.currentText(),
                self.ui.collegeCodelineEdit.text(),
            )

            self.populateCollegeTable(result)
        else:
            QtWidgets.QMessageBox.warning(
                self, "No Filter Selected", "Please select at least one filter"
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CollegeBrowserApp()
    window.show()
    sys.exit(app.exec())
