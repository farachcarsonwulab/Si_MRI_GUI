# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_Window.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(912, 526)
        MainWindow.setFixedSize(512,526)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.options_txt = QtWidgets.QLabel(self.centralwidget)
        self.options_txt.setGeometry(QtCore.QRect(50, 320, 450, 23))
        self.options_txt.setObjectName("options_txt")
        self.instructions = QtWidgets.QLabel(self.centralwidget)
        self.instructions.setGeometry(QtCore.QRect(50, 50, 101, 21))
        self.instructions.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.instructions.setObjectName("instructions")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setGeometry(QtCore.QRect(80, 420, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.study_names_txt = QtWidgets.QLabel(self.centralwidget)
        self.study_names_txt.setGeometry(QtCore.QRect(50, 100, 181, 23))
        self.study_names_txt.setObjectName("study_names_txt")
        self.welcome = QtWidgets.QLabel(self.centralwidget)
        self.welcome.setGeometry(QtCore.QRect(100, 0, 361, 53))
        self.welcome.setObjectName("welcome")
        self.data_folder_txt = QtWidgets.QLabel(self.centralwidget)
        self.data_folder_txt.setGeometry(QtCore.QRect(50, 60, 171, 41))
        self.data_folder_txt.setObjectName("data_folder_txt")
        self.NormFactors = QtWidgets.QCheckBox(self.centralwidget)
        self.NormFactors.setGeometry(QtCore.QRect(50, 350, 131, 27))
        self.NormFactors.setObjectName("NormFactors")
        self.study_numbers_txt = QtWidgets.QLabel(self.centralwidget)
        self.study_numbers_txt.setGeometry(QtCore.QRect(50, 130, 191, 23))
        self.study_numbers_txt.setObjectName("study_numbers_txt")
        self.ok_txt = QtWidgets.QLabel(self.centralwidget)
        self.ok_txt.setGeometry(QtCore.QRect(50, 160, 111, 23))
        self.ok_txt.setObjectName("ok_txt")
        self.ChooseFolder = QtWidgets.QPushButton(self.centralwidget)
        self.ChooseFolder.setGeometry(QtCore.QRect(50, 190, 171, 39))
        self.ChooseFolder.setObjectName("ChooseFolder")

        self.ChooseFolder.clicked.connect(self.browse_folder)


        self.folder_label = QtWidgets.QLabel(self.centralwidget)
        self.folder_label.setGeometry(QtCore.QRect(230, 190, 351, 23))
        self.folder_label.setObjectName("folder_label")
        self.ChooseFile = QtWidgets.QPushButton(self.centralwidget)
        self.ChooseFile.setGeometry(QtCore.QRect(50, 250, 171, 39))
        self.ChooseFile.setObjectName("ChooseFile")


        self.ChooseFile.clicked.connect(self.browse_file)


        self.file_label = QtWidgets.QLabel(self.centralwidget)
        self.file_label.setGeometry(QtCore.QRect(230, 250, 351, 23))
        self.file_label.setObjectName("file_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 912, 35))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.buttonBox.accepted.connect(self.Process)
        self.buttonBox.rejected.connect(self.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MRI-SI Demo Suite"))
        self.options_txt.setText(_translate("MainWindow", "<b>Options:</b> Select if using additonal normalization coefficients."))
        self.instructions.setText(_translate("MainWindow", "<b>Instructions:</b>"))
        self.study_names_txt.setText(_translate("MainWindow", "2. Create Excel File"))
        self.welcome.setText(_translate("MainWindow", "For use in teaching and academic research only.\n Not for government, commercial, or other use."))
        self.data_folder_txt.setText(_translate("MainWindow", "1. Choose Data Folder"))
        self.NormFactors.setText(_translate("MainWindow", "Norm Factors"))
        self.study_numbers_txt.setText(_translate("MainWindow", "3. Choose Excel File"))
        self.ok_txt.setText(_translate("MainWindow", "4. Click \"OK\""))
        self.ChooseFolder.setText(_translate("MainWindow", "Choose Folder"))
        self.folder_label.setText(_translate("MainWindow", "No Folder Selected!"))
        self.ChooseFile.setText(_translate("MainWindow", "Choose Excel"))
        self.file_label.setText(_translate("MainWindow", "No File Selected!"))
