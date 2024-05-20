import os
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, res
import requests
from tkinter import messagebox
from threading import Thread
import webbrowser

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(450, 550)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setWindowIcon(QtGui.QIcon('resources/icon.ico'))
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(30, 30, 370, 480))
        self.widget.setStyleSheet("QPushButton#pushButton{    \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));\n"
"    color:rgba(255, 255, 255, 210);\n"
"    border-radius:5px;\n"
"}\n"
"QPushButton#pushButton:hover{    \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));\n"
"}\n"
"QPushButton#pushButton:pressed{    \n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(105, 118, 132, 200);\n"
"}\n"
"\n"
"QPushButton#exitButton{    \n"
"    color:rgba(255, 255, 255, 210);\n"
"    border-radius:5px;\n"
"}\n"
"QButton#exitButton:hover{    \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));\n"
"}\n"
"QPushButton#exitButton:pressed{    \n"
"    background-color:rgba(105, 118, 132, 200);\n"
"}\n"
"\n"
"QPushButton#pushButton_2, #pushButton_3, #pushButton_4{    \n"
"    background-color: rgba(0, 0, 0, 0);\n"
"    color:rgba(85, 98, 112, 255);\n"
"}\n"
"QPushButton#pushButton_2:hover, #pushButton_3:hover, #pushButton_4:hover{    \n"
"    color:rgba(155, 168, 182, 220);\n"
"}\n"
"QPushButton#pushButton_2:pressed, #pushButton_3:pressed, #pushButton_4:pressed{    \n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    color:rgba(115, 128, 142, 255);\n"
"}")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(30, 30, 300, 420))
        self.label.setStyleSheet("border-image: url(:/images/background.png);\n"
"border-radius:20px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(30, 30, 300, 400))
        self.label_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:0.715909, stop:0 rgba(0, 0, 0, 9), stop:0.375 rgba(0, 0, 0, 50), stop:0.835227 rgba(0, 0, 0, 75));\n"
"border-radius:20px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(40, 60, 280, 390))
        self.label_3.setStyleSheet("background-color:rgba(0, 0, 0, 100);\n"
"border-radius:15px;")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(94, 95, 185, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:rgba(255, 255, 255, 210);")
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 165, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 230, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(80, 310, 200, 40))
        ############
        self.exitButton = QtWidgets.QPushButton(self.widget)
        self.exitButton.setGeometry(QtCore.QRect(300, 30, 30, 30))
        self.exitButton.setFont(font)
        self.exitButton.setObjectName("exitButton")
        ############
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(105, 399, 141, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Social Media Circled")
        font.setPointSize(15)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Social Media Circled")
        font.setPointSize(15)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_4.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Social Media Circled")
        font.setPointSize(15)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        font = QtGui.QFont()
        font.setFamily("Social Media Circled")
        font.setPointSize(15)

        self.label.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QtGui.QColor(234, 221, 186, 100)))
        self.label_3.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QtGui.QColor(105, 118, 132, 100)))
        self.pushButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3, color=QtGui.QColor(105, 118, 132, 100)))
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "Đăng nhập"))
        self.lineEdit.setPlaceholderText(_translate("Form", "  Tên Đăng Nhập"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "  Mật Khẩu"))
        self.pushButton.setText(_translate("Form", "Đăng Nhập"))

        self.exitButton.setText(_translate("Form", "X"))

        self.pushButton_2.setText(_translate("Form", "E"))
        self.pushButton_3.setText(_translate("Form", "D"))
        self.pushButton_4.setText(_translate("Form", "M"))
def login(userName,password):
    global Form
    APIurl = 'http://127.0.0.1:8000'
    result = requests.get(APIurl+'/userIn4',params={'getIn4By':'user_LOGIN',
                                                    'where':userName,
                                                    'wantToGet':'user_LOGINPASS'}).text.strip('''"''')
    if (result=='NotFound!') or (password!=result):
        messagebox.showerror(title='Thông báo',
                             message='Tên đăng nhập hoặc mật khẩu không chính xác\n\nVui lòng thử lại!')
    else:
        user_ID = requests.get(APIurl+'/userIn4',params={'getIn4By':'user_LOGIN',
                                                         'where':userName,
                                                         'wantToGet':'user_ID'}).text.strip('''"''')
        with open('run_GUI.ps1','w') as file:
            text = f'Scripts\python.exe .\GUI.py {user_ID}'
            print(text,file=file)
        Thread(target=lambda:os.system('run_GUI.ps1')).start()
    return
def facebook():
    webbrowser.open('https://www.facebook.com')
def call():
    global ui
    login(ui.lineEdit.text(),ui.lineEdit_2.text())
    ui.lineEdit.setText('')
    ui.lineEdit_2.setText('')
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    ui.exitButton.pressed.connect(lambda:sys.exit())
    ui.pushButton.pressed.connect(call)
    ui.pushButton_2.pressed.connect(facebook)
    sys.exit(app.exec_())