# Form implementation generated from reading ui file 'designer_qiu_qiu.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from Qiup import *
from Gui import *  

class MainWindow(QtWidgets.QMainWindow, Ui_Quip_test):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.connect_state = 0
        self.default_values()
        self.gui = Ui_Quip_test()
        self.qiup = Qiup()
        self.default_values()
        self.connect_gui()
        self.setup_led_buttons()

    def default_values(self):
        self.retrigger.setChecked(True)
        self.retrigger_sec.setValue(10)
        self.leds = [self.led1,self.led2,self.led3,self.led4,self.led5,self.led6,self.led8,self.led7]
        
    def connect_gui(self):
        self.connect.clicked.connect(self.register)    

    def retranslateUi(self, Quip_test):
        _translate = QtCore.QCoreApplication.translate
        Quip_test.setWindowTitle(_translate("Quip_test", "Qiu+ Hardware Test"))
        self.connect.setText(_translate("Quip_test", "Connect"))
        self.app_version.setText(_translate("Quip_test", "App Version"))
        self.api_version.setText(_translate("Quip_test", "API Version"))
        self.retrigger.setText(_translate("Quip_test", "Retrigger Mode"))
        self.label.setText(_translate("Quip_test", "Sec."))
        self.menuQiuGui.setTitle(_translate("Quip_test", "QiuGui"))

    def register(self):
        button_text = self.connect.text()
        if button_text == "Connect":
            self.qiup.setup_serial()
            retrigger  = int(self.retrigger.isChecked())
            self.connect_state = self.qiup.register(retrigger)
            if self.connect_state == None:
                self.qiup.close_serial()
                self.connect.setText("Connect")
                return
            else:
                self.get_api_version()
                self.get_app_version()
                self.connect.setText( "Release")
                self.qiup_name.setText(self.qiup.name)
        if button_text == "Release":
            self.connect_state = self.qiup.release()
            self.qiup.close_serial()
            self.connect.setText("Connect")
            self.api_version_text.setText("")
            self.app_version_text.setText("")
            self.qiup_name.setText("")
    
    def setup_led_buttons(self):
        for led in self.leds:
            led.clicked.connect(self.set_ledbar)
        return
    
    def set_ledbar(self):
        if self.connect_state == 1:
            led_bar = []
            for led in self.leds:
                led_bar.append(int(led.isChecked()))
            print(led_bar)
            self.qiup.ledbar_control(led_bar)
        if self.connect_state == 0:
            print("Not Connected, Please register first.")
        return

    def get_api_version(self):
        api_version = self.qiup.get_api_version()
        self.api_version_text.setText(api_version)
        return
    
    def get_app_version(self):
        app_version = self.qiup.get_appl_version()
        self.app_version_text.setText(app_version)
        return
    


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()