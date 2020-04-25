# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindowUI(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1426, 1088)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMaximumSize(QtCore.QSize(450, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lab_video_source = QtWidgets.QLabel(self.frame)
        self.lab_video_source.setObjectName("lab_video_source")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lab_video_source)
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.lab_move_status = QtWidgets.QLabel(self.frame)
        self.lab_move_status.setObjectName("lab_move_status")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lab_move_status)
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setObjectName("groupBox")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lab_monitor_range = QtWidgets.QLabel(self.groupBox)
        self.lab_monitor_range.setObjectName("lab_monitor_range")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lab_monitor_range)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.spb_sampling_interval = QtWidgets.QSpinBox(self.groupBox)
        self.spb_sampling_interval.setObjectName("spb_sampling_interval")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spb_sampling_interval)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.spb_sampling_quantity = QtWidgets.QSpinBox(self.groupBox)
        self.spb_sampling_quantity.setObjectName("spb_sampling_quantity")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.spb_sampling_quantity)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.groupBox)
        self.btn_run = QtWidgets.QPushButton(self.frame)
        self.btn_run.setObjectName("btn_run")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.btn_run)
        self.horizontalLayout.addWidget(self.frame)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1426, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuMonitor_Setting = QtWidgets.QMenu(self.menubar)
        self.menuMonitor_Setting.setObjectName("menuMonitor_Setting")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_open_video_file = QtWidgets.QAction(MainWindow)
        self.action_open_video_file.setObjectName("action_open_video_file")
        self.action_open_video_stream = QtWidgets.QAction(MainWindow)
        self.action_open_video_stream.setObjectName("action_open_video_stream")
        self.action_start_monitor = QtWidgets.QAction(MainWindow)
        self.action_start_monitor.setObjectName("action_start_monitor")
        self.action_quit = QtWidgets.QAction(MainWindow)
        self.action_quit.setObjectName("action_quit")
        self.action_set_monitor_range = QtWidgets.QAction(MainWindow)
        self.action_set_monitor_range.setObjectName("action_set_monitor_range")
        self.action_clear_monitor_range = QtWidgets.QAction(MainWindow)
        self.action_clear_monitor_range.setObjectName("action_clear_monitor_range")
        self.menuFile.addAction(self.action_open_video_file)
        self.menuFile.addAction(self.action_open_video_stream)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_start_monitor)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_quit)
        self.menuMonitor_Setting.addAction(self.action_set_monitor_range)
        self.menuMonitor_Setting.addAction(self.action_clear_monitor_range)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuMonitor_Setting.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Video Movement Monitor"))
        self.label.setText(_translate("MainWindow", "Video Source:"))
        self.lab_video_source.setText(_translate("MainWindow", "TextLabel"))
        self.label_8.setText(_translate("MainWindow", "Movement Status:"))
        self.lab_move_status.setText(_translate("MainWindow", "TextLabel"))
        self.groupBox.setTitle(_translate("MainWindow", "Monitor Setting"))
        self.label_3.setText(_translate("MainWindow", "Monitor Range:"))
        self.lab_monitor_range.setText(_translate("MainWindow", "(0,0) (0,0)"))
        self.label_7.setText(_translate("MainWindow", "Sampling Interval(s):"))
        self.label_6.setText(_translate("MainWindow", "Sampling Quantity"))
        self.btn_run.setText(_translate("MainWindow", "Start"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuMonitor_Setting.setTitle(_translate("MainWindow", "Monitor Setting"))
        self.action_open_video_file.setText(_translate("MainWindow", "Open video file"))
        self.action_open_video_file.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_open_video_stream.setText(_translate("MainWindow", "Open video stream"))
        self.action_open_video_stream.setShortcut(_translate("MainWindow", "Ctrl+Shift+O"))
        self.action_start_monitor.setText(_translate("MainWindow", "Start monitor"))
        self.action_start_monitor.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.action_quit.setText(_translate("MainWindow", "Quit"))
        self.action_quit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.action_set_monitor_range.setText(_translate("MainWindow", "Set monitor range"))
        self.action_set_monitor_range.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.action_clear_monitor_range.setText(_translate("MainWindow", "Clear monitor range"))
        self.action_clear_monitor_range.setShortcut(_translate("MainWindow", "Ctrl+D"))
