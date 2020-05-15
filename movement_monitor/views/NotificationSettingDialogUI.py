# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NotificationSettingDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class NotificationSettingDialogUI(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.txt_phone_number = QtWidgets.QLineEdit(self.groupBox)
        self.txt_phone_number.setInputMethodHints(QtCore.Qt.ImhNone)
        self.txt_phone_number.setObjectName("txt_phone_number")
        self.gridLayout.addWidget(self.txt_phone_number, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.btn_add_subscriber = QtWidgets.QPushButton(self.groupBox)
        self.btn_add_subscriber.setObjectName("btn_add_subscriber")
        self.gridLayout.addWidget(self.btn_add_subscriber, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_remove_subscriber = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_remove_subscriber.setObjectName("btn_remove_subscriber")
        self.gridLayout_2.addWidget(self.btn_remove_subscriber, 0, 0, 1, 1)
        self.btn_clear_subscriber = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_clear_subscriber.setObjectName("btn_clear_subscriber")
        self.gridLayout_2.addWidget(self.btn_clear_subscriber, 0, 1, 1, 1)
        self.lsv_subscribers = QtWidgets.QListView(self.groupBox_2)
        self.lsv_subscribers.setObjectName("lsv_subscribers")
        self.gridLayout_2.addWidget(self.lsv_subscribers, 1, 0, 1, 2)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Notification Setting"))
        self.groupBox.setTitle(_translate("Dialog", "New Subscriber Setting"))
        self.txt_phone_number.setInputMask(_translate("Dialog", "+8600000000000"))
        self.label.setText(_translate("Dialog", "Mobile Phone Number:"))
        self.btn_add_subscriber.setText(_translate("Dialog", "Add"))
        self.groupBox_2.setTitle(_translate("Dialog", "Existing Subscribers"))
        self.btn_remove_subscriber.setText(_translate("Dialog", "Remove"))
        self.btn_clear_subscriber.setText(_translate("Dialog", "Clear"))

