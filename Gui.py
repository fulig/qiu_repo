# Form implementation generated from reading ui file 'designer_qiu_qiu.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Quip_test(object):
    def setupUi(self, Quip_test):
        Quip_test.setObjectName("Quip_test")
        Quip_test.resize(1131, 769)
        self.centralwidget = QtWidgets.QWidget(parent=Quip_test)
        self.centralwidget.setObjectName("centralwidget")
        self.connect = QtWidgets.QPushButton(parent=self.centralwidget)
        self.connect.setGeometry(QtCore.QRect(30, 40, 91, 25))
        self.connect.setObjectName("connect")
        self.app_version = QtWidgets.QPushButton(parent=self.centralwidget)
        self.app_version.setGeometry(QtCore.QRect(30, 80, 91, 25))
        self.app_version.setObjectName("app_version")
        self.api_version = QtWidgets.QPushButton(parent=self.centralwidget)
        self.api_version.setGeometry(QtCore.QRect(30, 120, 91, 25))
        self.api_version.setObjectName("api_version")
        self.main_operations = QtWidgets.QFrame(parent=self.centralwidget)
        self.main_operations.setGeometry(QtCore.QRect(10, 20, 281, 171))
        self.main_operations.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.main_operations.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.main_operations.setObjectName("main_operations")
        self.retrigger = QtWidgets.QCheckBox(parent=self.main_operations)
        self.retrigger.setEnabled(True)
        self.retrigger.setGeometry(QtCore.QRect(10, 140, 131, 23))
        self.retrigger.setObjectName("retrigger")
        self.retrigger_sec = QtWidgets.QSpinBox(parent=self.main_operations)
        self.retrigger_sec.setGeometry(QtCore.QRect(160, 140, 42, 26))
        self.retrigger_sec.setMaximum(20)
        self.retrigger_sec.setObjectName("retrigger_sec")
        self.label = QtWidgets.QLabel(parent=self.main_operations)
        self.label.setGeometry(QtCore.QRect(210, 140, 54, 21))
        self.label.setObjectName("label")
        self.app_version_text = QtWidgets.QLineEdit(parent=self.main_operations)
        self.app_version_text.setGeometry(QtCore.QRect(130, 60, 71, 25))
        self.app_version_text.setObjectName("app_version_text")
        self.api_version_text = QtWidgets.QLineEdit(parent=self.main_operations)
        self.api_version_text.setGeometry(QtCore.QRect(130, 100, 71, 25))
        self.api_version_text.setObjectName("api_version_text")
        self.qiup_name = QtWidgets.QLineEdit(parent=self.main_operations)
        self.qiup_name.setGeometry(QtCore.QRect(130, 20, 141, 25))
        self.qiup_name.setObjectName("qiup_name")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(340, 70, 88, 26))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(340, 110, 88, 26))
        self.pushButton_2.setObjectName("pushButton_2")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(340, 40, 156, 17))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.led1 = QtWidgets.QRadioButton(parent=self.widget)
        self.led1.setText("")
        self.led1.setAutoExclusive(False)
        self.led1.setObjectName("led1")
        self.horizontalLayout.addWidget(self.led1)
        self.led2 = QtWidgets.QRadioButton(parent=self.widget)
        self.led2.setText("")
        self.led2.setAutoExclusive(False)
        self.led2.setObjectName("led2")
        self.horizontalLayout.addWidget(self.led2)
        self.led3 = QtWidgets.QRadioButton(parent=self.widget)
        self.led3.setText("")
        self.led3.setAutoExclusive(False)
        self.led3.setObjectName("led3")
        self.horizontalLayout.addWidget(self.led3)
        self.led4 = QtWidgets.QRadioButton(parent=self.widget)
        self.led4.setText("")
        self.led4.setAutoExclusive(False)
        self.led4.setObjectName("led4")
        self.horizontalLayout.addWidget(self.led4)
        self.led5 = QtWidgets.QRadioButton(parent=self.widget)
        self.led5.setText("")
        self.led5.setAutoExclusive(False)
        self.led5.setObjectName("led5")
        self.horizontalLayout.addWidget(self.led5)
        self.led6 = QtWidgets.QRadioButton(parent=self.widget)
        self.led6.setText("")
        self.led6.setAutoExclusive(False)
        self.led6.setObjectName("led6")
        self.horizontalLayout.addWidget(self.led6)
        self.led7 = QtWidgets.QRadioButton(parent=self.widget)
        self.led7.setText("")
        self.led7.setAutoExclusive(False)
        self.led7.setObjectName("led7")
        self.horizontalLayout.addWidget(self.led7)
        self.led8 = QtWidgets.QRadioButton(parent=self.widget)
        self.led8.setText("")
        self.led8.setAutoExclusive(False)
        self.led8.setObjectName("led8")
        self.horizontalLayout.addWidget(self.led8)
        self.main_operations.raise_()
        self.connect.raise_()
        self.app_version.raise_()
        self.api_version.raise_()
        self.led1.raise_()
        self.led2.raise_()
        self.led3.raise_()
        self.led4.raise_()
        self.led5.raise_()
        self.led6.raise_()
        self.led8.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        Quip_test.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Quip_test)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1131, 23))
        self.menubar.setObjectName("menubar")
        self.menuQiuGui = QtWidgets.QMenu(parent=self.menubar)
        self.menuQiuGui.setObjectName("menuQiuGui")
        Quip_test.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Quip_test)
        self.statusbar.setObjectName("statusbar")
        Quip_test.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuQiuGui.menuAction())

        self.retranslateUi(Quip_test)
        QtCore.QMetaObject.connectSlotsByName(Quip_test)

    def retranslateUi(self, Quip_test):
        _translate = QtCore.QCoreApplication.translate
        Quip_test.setWindowTitle(_translate("Quip_test", "Qiu+ Hardware Test"))
        self.connect.setText(_translate("Quip_test", "Connect"))
        self.app_version.setText(_translate("Quip_test", "App Version"))
        self.api_version.setText(_translate("Quip_test", "API Version"))
        self.retrigger.setText(_translate("Quip_test", "Retrigger Mode"))
        self.label.setText(_translate("Quip_test", "Sec."))
        self.pushButton.setText(_translate("Quip_test", "All On"))
        self.pushButton_2.setText(_translate("Quip_test", "All Off"))
        self.menuQiuGui.setTitle(_translate("Quip_test", "QiuGui"))