from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from tkinter.filedialog import askopenfilenames
import sys
import smtplib
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from os.path import basename

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(400, 300)
        Dialog.setInputMethodHints(QtCore.Qt.ImhNone)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Dialog.setWindowIcon(QIcon('icon.ico'))
        self.title = QtWidgets.QTextEdit(Dialog)
        self.title.setGeometry(QtCore.QRect(10, 30, 381, 71))
        self.title.setStyleSheet("background-color: rgba(255, 255, 255,70);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:4px;")
        self.title.setObjectName("title")
        self.content = QtWidgets.QTextEdit(Dialog)
        self.content.setGeometry(QtCore.QRect(10, 130, 381, 71))
        self.content.setStyleSheet("background-color: rgba(255, 255, 255,70);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:4px;")
        self.content.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        self.content.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextEditable|QtCore.Qt.TextSelectableByMouse)
        self.content.setPlaceholderText("")
        self.content.setObjectName("content")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 0, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka Small")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: qlineargradient(spread:reflect, x1:0.153, y1:0.608, x2:1, y2:0, stop:0 rgba(81, 102, 255, 255), stop:1 rgba(255, 255, 255, 255));")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka Small")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: qlineargradient(spread:reflect, x1:0.153, y1:0.608, x2:1, y2:0, stop:0 rgba(81, 102, 255, 255), stop:1 rgba(255, 255, 255, 255));")
        self.label_2.setObjectName("label_2")
        self.sendButton = QtWidgets.QPushButton(Dialog)
        self.sendButton.setGeometry(QtCore.QRect(340, 220, 41, 41))
        self.sendButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sendButton.setAutoFillBackground(False)
        self.sendButton.setStyleSheet("QPushButton#sendButton{\n"
"border-radius:4px;\n"
"background-image: url(:/image/sendFile.png);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(145,140,233,1), stop:1 rgba(0,212,255,1));\n"
"border-radius:5px}\n"
"QPushButton#sendButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.45 rgba(208,205,255,1), stop:1  rgba(139,235,255,1));\n"
"}\n"
"QPushButton#sendButton:pressed{   \n"
"  padding-left:5px;\n"
"   padding-top:5px;\n"
"background-image: url(:/image/done.png);\n"
"}")
        self.sendButton.setText("")
        self.sendButton.setObjectName("sendButton")
        self.FROM = QtWidgets.QLabel(Dialog)
        self.FROM.setGeometry(QtCore.QRect(10, 220, 271, 16))
        self.FROM.setStyleSheet("color: rgb(170, 255, 255);\n"
"background-color: rgba(255, 255, 255, 70);\n"
"border-radius:4px;")
        self.FROM.setObjectName("FROM")
        self.TO = QtWidgets.QLabel(Dialog)
        self.TO.setGeometry(QtCore.QRect(10, 250, 271, 16))
        self.TO.setStyleSheet("color: rgb(170, 255, 255);\n"
"background-color: rgba(255, 255, 255, 70);\n"
"border-radius:4px;")
        self.TO.setObjectName("TO")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(0, 0, 401, 301))
        self.label_5.setStyleSheet("background-image: url(:/image/dark.jpg);")
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(":/image/dark.jpg"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.attachButton = QtWidgets.QPushButton(Dialog)
        self.attachButton.setGeometry(QtCore.QRect(290, 220, 41, 41))
        self.attachButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.attachButton.setAutoFillBackground(False)
        self.attachButton.setStyleSheet("QPushButton#attachButton{\n"
"background-image: url(:/image/attachFile.png);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(145,140,233,1), stop:1 rgba(0,212,255,1));\n"
"border-radius:4px;\n"
"}\n"
"QPushButton#attachButton:pressed{   \n"
"  padding-left:5px;\n"
"   padding-top:5px;\n"
" background-color:rgba(105, 118, 132, 200)}\n"
"QPushButton#attachButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.45 rgba(208,205,255,1), stop:1  rgba(139,235,255,1));\n"
"}")
        self.attachButton.setText("")
        self.attachButton.setObjectName("attachButton")
        self.numberOfAtt = QtWidgets.QLabel(Dialog)
        self.numberOfAtt.setGeometry(QtCore.QRect(290, 270, 41, 16))
        self.numberOfAtt.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color:rgb(0,0,0);\n"
"border-radius:4px")
        self.numberOfAtt.setText("")
        self.numberOfAtt.setObjectName("numberOfAtt")
        self.exitButton = QtWidgets.QPushButton(Dialog)
        self.exitButton.setGeometry(QtCore.QRect(380, 0, 21, 21))
        self.exitButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exitButton.setAutoFillBackground(False)
        self.exitButton.setStyleSheet("QPushButton#exitButton{  \n"
"   color:rgba(255, 255, 255, 210);\n"
"    border-radius:5px;\n"
"    \n"
"    \n"
"    font: 75 14pt \"Consolas\";\n"
"}\n"
"QButton#exitButton:hover{   \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226))\n"
"}\n"
"QPushButton#exitButton:hover{  \n"
"  background-color:rgba(105, 118, 132, 200)}")
        self.exitButton.setObjectName("exitButton")

        self.label_5.raise_()
        self.title.raise_()
        self.content.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.sendButton.raise_()
        self.FROM.raise_()
        self.TO.raise_()
        self.attachButton.raise_()
        self.numberOfAtt.raise_()
        self.exitButton.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "MAIN"))
        self.label.setText(_translate("Dialog", "Title:"))
        self.label_2.setText(_translate("Dialog", "Content:"))
        self.FROM.setText(_translate("Dialog", f"From: {sender_email}"))
        if len(receiver_email)==1:
                self.TO.setText(_translate("Dialog", f"To: {receiver_email[0]}"))
        else:
             self.TO.setText(_translate("Dialog", "To: <Many>"))
        self.numberOfAtt.setText(_translate("Dialog", f"{Nfiles} files"))
        self.exitButton.setText(_translate("Dialog", "x"))
def AskOpenFileNames():
    global Nfiles,files
    files = askopenfilenames()
    Nfiles = len(files)
    ui.numberOfAtt.setText(QtCore.QCoreApplication.translate("Dialog", f"{Nfiles} files"))
    return files
def sendEmailBackend(sender_address = 'hoangkimmanhha2@gmail.com',
                     sender_pass = 'ctnghphvyvpmihzu',
                     receiver_address = 'hoanghunghalinh@gmail.com',
                     mail_title = '',
                     mail_content = '',
                     attach_file_list = []):
    
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = mail_title

    message.attach(MIMEText(mail_content, 'plain'))
    for attach_file_name in attach_file_list:
        attach_file = open(attach_file_name, 'rb') 
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)
        filename = basename(attach_file_name)
        payload.add_header('Content-Disposition', f'attachment; filename="{filename}"')

        message.attach(payload)

    session = smtplib.SMTP('smtp.gmail.com', 587) 
    session.starttls() 
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

import image
def main(s_email:str = 'hoangkimmanhha2@gmail.com',
         r_email:list = ['hoanghunghalinh@gmail.com'],
         sender_passw:str = 'ctnghphvyvpmihzu'):
    global sender_email,receiver_email,Nfiles,ui
    receiver_email = r_email.split(',')
    print(receiver_email)
    sender_email = s_email
    Nfiles = 0
    
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)

    def sendEmail():
        for recv in receiver_email:
            sendEmailBackend(sender_address=sender_email,
                             sender_pass=sender_passw,
                             receiver_address=recv,
                             mail_title=ui.title.toPlainText(),
                             mail_content=ui.content.toPlainText(),
                             attach_file_list=files)
        
    ui.exitButton.pressed.connect(sys.exit)
    ui.attachButton.pressed.connect(AskOpenFileNames)
    ui.sendButton.pressed.connect(lambda:Thread(target=sendEmail).start())
    Dialog.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()