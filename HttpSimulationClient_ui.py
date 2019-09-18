# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HttpSimulationClient_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(465, 402)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 110, 61, 21))
        self.label.setObjectName("label")
        self.GetBtn = QtWidgets.QPushButton(self.centralwidget)
        self.GetBtn.setGeometry(QtCore.QRect(360, 10, 75, 23))
        self.GetBtn.setObjectName("GetBtn")
        self.PostBtn = QtWidgets.QPushButton(self.centralwidget)
        self.PostBtn.setGeometry(QtCore.QRect(360, 110, 75, 23))
        self.PostBtn.setObjectName("PostBtn")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 160, 61, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 61, 21))
        self.label_3.setObjectName("label_3")
        self.PostDataText = QtWidgets.QTextEdit(self.centralwidget)
        self.PostDataText.setGeometry(QtCore.QRect(80, 160, 271, 181))
        self.PostDataText.setObjectName("PostDataText")
        self.PostUrlText = QtWidgets.QTextEdit(self.centralwidget)
        self.PostUrlText.setGeometry(QtCore.QRect(80, 110, 271, 31))
        self.PostUrlText.setObjectName("PostUrlText")
        self.GetUrlText = QtWidgets.QTextEdit(self.centralwidget)
        self.GetUrlText.setGeometry(QtCore.QRect(80, 10, 271, 31))
        self.GetUrlText.setObjectName("GetUrlText")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 465, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "PostUrl"))
        self.GetBtn.setText(_translate("MainWindow", "Get"))
        self.PostBtn.setText(_translate("MainWindow", "Post"))
        self.label_2.setText(_translate("MainWindow", "PostData"))
        self.label_3.setText(_translate("MainWindow", "PostUrl"))
