# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\李展旗\Desktop\python_demo\收作业平台\main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(204, 355)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(40, 180, 131, 61))
        self.pushButton_4.setStyleSheet("background-color: rgb(255, 210, 254);\n"
"border-radius:4px;\n"
"font: 14pt \"幼圆\";")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 260, 131, 61))
        self.pushButton.setStyleSheet("background-color: rgb(255, 210, 254);\n"
"border-radius:4px;\n"
"font: 14pt \"幼圆\";")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(39, 35, 131, 61))
        self.pushButton_3.setStyleSheet("background-color: rgb(255, 210, 254);\n"
"border-radius:4px;\n"
"font: 14pt \"幼圆\";")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 110, 131, 61))
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 210, 254);\n"
"border-radius:4px;\n"
"font: 14pt \"幼圆\";")
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "作业管理系统"))
        self.pushButton_4.setText(_translate("MainWindow", "提交系统"))
        self.pushButton.setText(_translate("MainWindow", "退出"))
        self.pushButton_3.setText(_translate("MainWindow", "爬秒应"))
        self.pushButton_2.setText(_translate("MainWindow", "图片合成"))
