# Form implementation generated from reading ui file './Other Files/CollegeBrowserUI.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_CollegeBrowserUI(object):
    def setupUi(self, CollegeBrowserUI):
        CollegeBrowserUI.setObjectName("CollegeBrowserUI")
        CollegeBrowserUI.resize(809, 560)
        self.centralwidget = QtWidgets.QWidget(parent=CollegeBrowserUI)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidgetPage1 = QtWidgets.QWidget()
        self.tabWidgetPage1.setObjectName("tabWidgetPage1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabWidgetPage1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.routeIncludeRB = QtWidgets.QCheckBox(parent=self.tabWidgetPage1)
        self.routeIncludeRB.setObjectName("routeIncludeRB")
        self.gridLayout.addWidget(self.routeIncludeRB, 2, 2, 1, 1)
        self.courseIncludeRB = QtWidgets.QCheckBox(parent=self.tabWidgetPage1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.courseIncludeRB.sizePolicy().hasHeightForWidth())
        self.courseIncludeRB.setSizePolicy(sizePolicy)
        self.courseIncludeRB.setObjectName("courseIncludeRB")
        self.gridLayout.addWidget(self.courseIncludeRB, 0, 2, 1, 1)
        self.collegeCodelineEdit = QtWidgets.QLineEdit(parent=self.tabWidgetPage1)
        self.collegeCodelineEdit.setObjectName("collegeCodelineEdit")
        self.gridLayout.addWidget(self.collegeCodelineEdit, 3, 0, 1, 1)
        self.courseCB = QtWidgets.QComboBox(parent=self.tabWidgetPage1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.courseCB.sizePolicy().hasHeightForWidth())
        self.courseCB.setSizePolicy(sizePolicy)
        self.courseCB.setObjectName("courseCB")
        self.gridLayout.addWidget(self.courseCB, 0, 0, 1, 1)
        self.collegeTypeIncludeRB = QtWidgets.QCheckBox(parent=self.tabWidgetPage1)
        self.collegeTypeIncludeRB.setObjectName("collegeTypeIncludeRB")
        self.gridLayout.addWidget(self.collegeTypeIncludeRB, 1, 2, 1, 1)
        self.collegeTypeCB = QtWidgets.QComboBox(parent=self.tabWidgetPage1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.collegeTypeCB.sizePolicy().hasHeightForWidth())
        self.collegeTypeCB.setSizePolicy(sizePolicy)
        self.collegeTypeCB.setObjectName("collegeTypeCB")
        self.gridLayout.addWidget(self.collegeTypeCB, 1, 0, 1, 1)
        self.routeCB = QtWidgets.QComboBox(parent=self.tabWidgetPage1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.routeCB.sizePolicy().hasHeightForWidth())
        self.routeCB.setSizePolicy(sizePolicy)
        self.routeCB.setObjectName("routeCB")
        self.gridLayout.addWidget(self.routeCB, 2, 0, 1, 1)
        self.collegCodeIncludeCheckBox = QtWidgets.QCheckBox(parent=self.tabWidgetPage1)
        self.collegCodeIncludeCheckBox.setObjectName("collegCodeIncludeCheckBox")
        self.gridLayout.addWidget(self.collegCodeIncludeCheckBox, 3, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.searchPB = QtWidgets.QPushButton(parent=self.tabWidgetPage1)
        self.searchPB.setObjectName("searchPB")
        self.horizontalLayout.addWidget(self.searchPB)
        self.getALLPB = QtWidgets.QPushButton(parent=self.tabWidgetPage1)
        self.getALLPB.setObjectName("getALLPB")
        self.horizontalLayout.addWidget(self.getALLPB)
        self.addNewPB = QtWidgets.QPushButton(parent=self.tabWidgetPage1)
        self.addNewPB.setObjectName("addNewPB")
        self.horizontalLayout.addWidget(self.addNewPB)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.collegeDataTable = QtWidgets.QTableWidget(parent=self.tabWidgetPage1)
        self.collegeDataTable.setObjectName("collegeDataTable")
        self.collegeDataTable.setColumnCount(5)
        self.collegeDataTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.collegeDataTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.collegeDataTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.collegeDataTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.collegeDataTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.collegeDataTable.setHorizontalHeaderItem(4, item)
        self.verticalLayout_2.addWidget(self.collegeDataTable)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton = QtWidgets.QPushButton(parent=self.tabWidgetPage1)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_5.addWidget(self.pushButton)
        self.savePB = QtWidgets.QPushButton(parent=self.tabWidgetPage1)
        self.savePB.setObjectName("savePB")
        self.horizontalLayout_5.addWidget(self.savePB)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.viewAllMessengersPB = QtWidgets.QPushButton(parent=self.tab_5)
        self.viewAllMessengersPB.setObjectName("viewAllMessengersPB")
        self.horizontalLayout_4.addWidget(self.viewAllMessengersPB)
        self.viewAllCoursesPB = QtWidgets.QPushButton(parent=self.tab_5)
        self.viewAllCoursesPB.setObjectName("viewAllCoursesPB")
        self.horizontalLayout_4.addWidget(self.viewAllCoursesPB)
        self.viewAllRoutesPB = QtWidgets.QPushButton(parent=self.tab_5)
        self.viewAllRoutesPB.setObjectName("viewAllRoutesPB")
        self.horizontalLayout_4.addWidget(self.viewAllRoutesPB)
        self.viewAllQPSeriesPB = QtWidgets.QPushButton(parent=self.tab_5)
        self.viewAllQPSeriesPB.setObjectName("viewAllQPSeriesPB")
        self.horizontalLayout_4.addWidget(self.viewAllQPSeriesPB)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.otherDataTable = QtWidgets.QTableWidget(parent=self.tab_5)
        self.otherDataTable.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.otherDataTable.setObjectName("otherDataTable")
        self.otherDataTable.setColumnCount(0)
        self.otherDataTable.setRowCount(0)
        self.verticalLayout_3.addWidget(self.otherDataTable)
        self.otherDataSavePB = QtWidgets.QPushButton(parent=self.tab_5)
        self.otherDataSavePB.setObjectName("otherDataSavePB")
        self.verticalLayout_3.addWidget(self.otherDataSavePB)
        self.tabWidget.addTab(self.tab_5, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        CollegeBrowserUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=CollegeBrowserUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 809, 24))
        self.menubar.setObjectName("menubar")
        CollegeBrowserUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=CollegeBrowserUI)
        self.statusbar.setObjectName("statusbar")
        CollegeBrowserUI.setStatusBar(self.statusbar)
        self.actionAdd_Item = QtGui.QAction(parent=CollegeBrowserUI)
        self.actionAdd_Item.setObjectName("actionAdd_Item")

        self.retranslateUi(CollegeBrowserUI)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CollegeBrowserUI)

    def retranslateUi(self, CollegeBrowserUI):
        _translate = QtCore.QCoreApplication.translate
        CollegeBrowserUI.setWindowTitle(_translate("CollegeBrowserUI", "College Browser"))
        self.routeIncludeRB.setText(_translate("CollegeBrowserUI", "Include This"))
        self.courseIncludeRB.setText(_translate("CollegeBrowserUI", "Include This"))
        self.collegeCodelineEdit.setPlaceholderText(_translate("CollegeBrowserUI", "Enter College Code"))
        self.courseCB.setPlaceholderText(_translate("CollegeBrowserUI", "Select Course"))
        self.collegeTypeIncludeRB.setText(_translate("CollegeBrowserUI", "Include This"))
        self.collegeTypeCB.setPlaceholderText(_translate("CollegeBrowserUI", "Select College Type"))
        self.routeCB.setPlaceholderText(_translate("CollegeBrowserUI", "Select Route"))
        self.collegCodeIncludeCheckBox.setText(_translate("CollegeBrowserUI", "Include This"))
        self.searchPB.setText(_translate("CollegeBrowserUI", "Search"))
        self.getALLPB.setText(_translate("CollegeBrowserUI", "Get All Colleges"))
        self.addNewPB.setText(_translate("CollegeBrowserUI", "Add New"))
        item = self.collegeDataTable.horizontalHeaderItem(0)
        item.setText(_translate("CollegeBrowserUI", "College Name"))
        item = self.collegeDataTable.horizontalHeaderItem(1)
        item.setText(_translate("CollegeBrowserUI", "Code"))
        item = self.collegeDataTable.horizontalHeaderItem(2)
        item.setText(_translate("CollegeBrowserUI", "College Type"))
        item = self.collegeDataTable.horizontalHeaderItem(3)
        item.setText(_translate("CollegeBrowserUI", "Route"))
        item = self.collegeDataTable.horizontalHeaderItem(4)
        item.setText(_translate("CollegeBrowserUI", "Courses"))
        self.pushButton.setText(_translate("CollegeBrowserUI", "Delete Selected Colleges"))
        self.savePB.setText(_translate("CollegeBrowserUI", "Save Changes"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), _translate("CollegeBrowserUI", "View/Edit College Details "))
        self.viewAllMessengersPB.setText(_translate("CollegeBrowserUI", "View All Messengers"))
        self.viewAllCoursesPB.setText(_translate("CollegeBrowserUI", "View Courses"))
        self.viewAllRoutesPB.setText(_translate("CollegeBrowserUI", "View All Routes"))
        self.viewAllQPSeriesPB.setText(_translate("CollegeBrowserUI", "View All QP Series"))
        self.otherDataSavePB.setText(_translate("CollegeBrowserUI", "Save Changes"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("CollegeBrowserUI", "View/Edit Other Data"))
        self.actionAdd_Item.setText(_translate("CollegeBrowserUI", "Add Item"))
        self.actionAdd_Item.setToolTip(_translate("CollegeBrowserUI", "<html><head/><body><svg fill=\"#000000\" version=\"1.1\" id=\"Capa_1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" width=\"800px\" height=\"800px\" viewBox=\"0 0 45.402 45.402\" xml:space=\"preserve\">\n"
"<g>\n"
"    <path d=\"M41.267,18.557H26.832V4.134C26.832,1.851,24.99,0,22.707,0c-2.283,0-4.124,1.851-4.124,4.135v14.432H4.141   c-2.283,0-4.139,1.851-4.138,4.135c-0.001,1.141,0.46,2.187,1.207,2.934c0.748,0.749,1.78,1.222,2.92,1.222h14.453V41.27   c0,1.142,0.453,2.176,1.201,2.922c0.748,0.748,1.777,1.211,2.919,1.211c2.282,0,4.129-1.851,4.129-4.133V26.857h14.435   c2.283,0,4.134-1.867,4.133-4.15C45.399,20.425,43.548,18.557,41.267,18.557z\"/>\n"
"</g>\n"
"</svg><p>Add Item</p></body></html>"))
