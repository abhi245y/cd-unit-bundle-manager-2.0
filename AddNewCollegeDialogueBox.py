# Form implementation generated from reading ui file './Other Files/AddNewCollegeDialogue.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AddNewCollege(object):
    def setupUi(self, AddNewCollege):
        AddNewCollege.setObjectName("AddNewCollege")
        AddNewCollege.resize(505, 445)
        self.horizontalLayout = QtWidgets.QHBoxLayout(AddNewCollege)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.collegeCodeLE = QtWidgets.QLineEdit(parent=AddNewCollege)
        self.collegeCodeLE.setObjectName("collegeCodeLE")
        self.verticalLayout.addWidget(self.collegeCodeLE)
        self.collegeNameLE = QtWidgets.QLineEdit(parent=AddNewCollege)
        self.collegeNameLE.setObjectName("collegeNameLE")
        self.verticalLayout.addWidget(self.collegeNameLE)
        self.routeCB = QtWidgets.QComboBox(parent=AddNewCollege)
        self.routeCB.setObjectName("routeCB")
        self.verticalLayout.addWidget(self.routeCB)
        self.collgeTypeCB = QtWidgets.QComboBox(parent=AddNewCollege)
        self.collgeTypeCB.setObjectName("collgeTypeCB")
        self.verticalLayout.addWidget(self.collgeTypeCB)
        self.groupBox = QtWidgets.QGroupBox(parent=AddNewCollege)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.courseList = QtWidgets.QListWidget(parent=self.groupBox)
        self.courseList.setObjectName("courseList")
        self.verticalLayout_2.addWidget(self.courseList)
        self.verticalLayout.addWidget(self.groupBox)
        self.addCollegeDialogePB = QtWidgets.QDialogButtonBox(parent=AddNewCollege)
        self.addCollegeDialogePB.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.addCollegeDialogePB.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.addCollegeDialogePB.setObjectName("addCollegeDialogePB")
        self.verticalLayout.addWidget(self.addCollegeDialogePB)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(AddNewCollege)
        self.addCollegeDialogePB.accepted.connect(AddNewCollege.accept) # type: ignore
        self.addCollegeDialogePB.rejected.connect(AddNewCollege.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(AddNewCollege)

    def retranslateUi(self, AddNewCollege):
        _translate = QtCore.QCoreApplication.translate
        AddNewCollege.setWindowTitle(_translate("AddNewCollege", "Add New College"))
        self.collegeCodeLE.setPlaceholderText(_translate("AddNewCollege", "Enter Colleg Code/ Center Code"))
        self.collegeNameLE.setPlaceholderText(_translate("AddNewCollege", "Enter College Name"))
        self.routeCB.setPlaceholderText(_translate("AddNewCollege", "Select Route"))
        self.collgeTypeCB.setPlaceholderText(_translate("AddNewCollege", "Select College Type"))
        self.groupBox.setTitle(_translate("AddNewCollege", "Select Available Courses"))
