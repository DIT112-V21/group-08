# This is a sample Python script.

# Press Skift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/


import sys
import paho.mqtt.client as mqtt
from PyQt5 import QtCore, QtGui, QtWidgets
import speech_recognition as sr
import design

# MQTT Stuff

broker_address = "localhost"
manualClient = mqtt.Client("Manual-Control")
manualClient.connect(broker_address)
manualClient.subscribe("/")

# def on_message(client, userdata, message):
# windowMain.updateSpeedLabel(message)

# manualClient.on_message = on_message()

manualClient.subscribe("speed")


class windowMain(object):
    def setupUi(self, windowMain):
        windowMain.setObjectName("windowMain")
        windowMain.resize(700, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(windowMain.sizePolicy().hasHeightForWidth())
        windowMain.setSizePolicy(sizePolicy)
        windowMain.setMinimumSize(QtCore.QSize(650, 450))
        windowMain.setMaximumSize(QtCore.QSize(650, 450))
        windowMain.setObjectName("main_window")
        windowMain.setStyleSheet(design.stylesheet)

        self.buttonBrake = QtWidgets.QPushButton(windowMain)
        self.buttonBrake.setGeometry(QtCore.QRect(280, 330, 111, 81))
        self.buttonBrake.setAutoFillBackground(False)
        self.buttonBrake.setObjectName("buttonBrake")

        self.buttonForward = QtWidgets.QPushButton(windowMain)
        self.buttonForward.setGeometry(QtCore.QRect(160, 40, 111, 81))
        self.buttonForward.setStyleSheet("")
        self.buttonForward.setObjectName("buttonForward")
        self.buttonLeft = QtWidgets.QPushButton(windowMain)
        self.buttonLeft.setGeometry(QtCore.QRect(40, 130, 111, 81))
        self.buttonLeft.setStyleSheet("")
        self.buttonLeft.setObjectName("buttonLeft")
        self.buttonRight = QtWidgets.QPushButton(windowMain)
        self.buttonRight.setGeometry(QtCore.QRect(280, 130, 111, 81))
        self.buttonRight.setStyleSheet("")
        self.buttonRight.setObjectName("buttonRight")
        self.buttonBack = QtWidgets.QPushButton(windowMain)
        self.buttonBack.setGeometry(QtCore.QRect(160, 220, 111, 81))
        self.buttonBack.setStyleSheet("")
        self.buttonBack.setObjectName("buttonBack")
        self.buttonVoiceControl = QtWidgets.QPushButton(windowMain)
        self.buttonVoiceControl.setGeometry(QtCore.QRect(40, 330, 111, 81))
        self.buttonVoiceControl.setStyleSheet("")
        self.buttonVoiceControl.setObjectName("buttonVoiceControl")
        self.buttonHelp = QtWidgets.QPushButton(windowMain)
        self.buttonHelp.setGeometry(QtCore.QRect(160, 330, 111, 81))
        self.buttonHelp.setStyleSheet("")
        self.buttonHelp.setObjectName("buttonHelp")
        self.buttonExit = QtWidgets.QPushButton(windowMain)
        self.buttonExit.setGeometry(QtCore.QRect(430, 350, 80, 60))
        self.buttonExit.setAutoFillBackground(False)
        self.buttonExit.setStyleSheet("background-color: red")
        self.buttonExit.setObjectName("buttonExit")
        self.sliderSpeed = QtWidgets.QSlider(windowMain)
        self.sliderSpeed.setGeometry(QtCore.QRect(430, 40, 81, 261))
        self.sliderSpeed.setOrientation(QtCore.Qt.Vertical)
        self.sliderSpeed.setObjectName("sliderSpeed")
        self.sliderSpeed.setRange(0, 100)

        self.sliderSpeed.valueChanged[int].connect(self.changeValue)

        self.labelCurrentSpeed = QtWidgets.QLabel(windowMain)
        self.labelCurrentSpeed.setGeometry(QtCore.QRect(560, 340, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.labelCurrentSpeed.setFont(font)
        self.labelCurrentSpeed.setObjectName("labelCurrentSpeed")

        self.setUpButtons()
        self.retranslateUi(windowMain)
        # self.updateSpeedLabel(windowMain, 0)
        QtCore.QMetaObject.connectSlotsByName(windowMain)

    def retranslateUi(self, windowMain):
        _translate = QtCore.QCoreApplication.translate
        windowMain.setWindowTitle(_translate("windowMain", "Pathfinder"))

        self.buttonBrake.setText(_translate("windowMain", "Brake"))

        self.buttonForward.setText(_translate("windowMain", "Forward"))
        self.buttonLeft.setText(_translate("windowMain", "Left"))
        self.buttonRight.setText(_translate("windowMain", "Right"))
        self.buttonBack.setText(_translate("windowMain", "Back"))
        self.buttonVoiceControl.setText(_translate("windowMain", "Voice Control"))
        self.buttonHelp.setText(_translate("windowMain", "How to use"))
        self.buttonExit.setText(_translate("windowMain", "Exit"))

        self.labelCurrentSpeed.setText(_translate("windowMain", "0"))

    # def updateSpeedLabel(self, speed):
    # self.labelCurrentSpeed.setText("windowMain", speed)

    def changeValue(self, value):
        manualClient.publish("speed", value)

    def LoadSecondWindow(self):
        SecondWindow = QtWidgets.QMainWindow()
        ui = Ui_SecondWindow()
        ui.setupUi(SecondWindow)
        SecondWindow.show()

    def LoadThirdWindow(self):
        ThirdWindow = QtWidgets.QMainWindow()
        ui = Ui_ThirdWindow()
        ui.setupUi(ThirdWindow)
        ThirdWindow.show()

    def setUpButtons(self):
        self.buttonForward.clicked.connect(lambda: self.publish("/", "w"))
        self.buttonLeft.clicked.connect(lambda: self.publish("/", "a"))
        self.buttonRight.clicked.connect(lambda: self.publish("/", "d"))
        self.buttonBack.clicked.connect(lambda: self.publish("/", "s"))
        self.buttonBrake.clicked.connect(lambda: self.publish("/", "stop"))
        self.buttonExit.clicked.connect(QtCore.QCoreApplication.instance().quit)

    def publish(self, topic, message):
        print(manualClient.publish(topic, message))


class Ui_SecondWindow(object):
    def setupUi(self, Ui_SecondWindow):
        Ui_SecondWindow.setObjectName("Voice Control")
        Ui_SecondWindow.resize(400, 270)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Ui_SecondWindow.sizePolicy().hasHeightForWidth())
        Ui_SecondWindow.setSizePolicy(sizePolicy)
        Ui_SecondWindow.setMinimumSize(QtCore.QSize(400, 270))
        Ui_SecondWindow.setMaximumSize(QtCore.QSize(400, 270))
        Ui_SecondWindow.setObjectName("Ui_SecondWindow")
        Ui_SecondWindow.setStyleSheet(design.stylesheet)

        self.centralWidget = QtWidgets.QWidget(Ui_SecondWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 130, 191, 23))
        self.pushButton.setObjectName("pushButton")
        self.labelInstructions = QtWidgets.QLabel(Ui_SecondWindow)
        self.labelInstructions.setGeometry(QtCore.QRect(110, 180, 191, 23))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.labelInstructions.setFont(font)
        self.labelInstructions.setObjectName("labelInstructions")

        Ui_SecondWindow.setCentralWidget(self.centralWidget)

        self.setUpButtons()
        self.retranslateUi(Ui_SecondWindow)
        QtCore.QMetaObject.connectSlotsByName(Ui_SecondWindow)

    def retranslateUi(self, Ui_SecondWindow):
        _translate = QtCore.QCoreApplication.translate
        Ui_SecondWindow.setWindowTitle(_translate("Ui_SecondWindow", "Voice Window"))
        self.labelInstructions.setText(_translate("Ui_SecondWindow",
                                                  '<html><head/><body><p><span style=\" color:black;\">Example: "Drive forward"</span></p></body></html>'))
        self.pushButton.setText(_translate("Ui_SecondWindow", "Click, then say a command"))

    def setUpButtons(self):
        self.pushButton.clicked.connect(lambda: self.voiceRecognition())

    def voiceRecognition(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Say Anything : ')
            try:
                audio = r.listen(source)
            except:
                print("EROR")
            try:
                text = r.recognize_google(audio)
                self.publish(text)
                print("You said : {}".format(text))
            except:
                print('Sorry, could not recognize your voice')

    def publish(self, message):
        words = message.split()
        for w in words:
            if w == "forward":
                print(manualClient.publish("/", "w"))
            elif w == "back":
                print(manualClient.publish("/", "s"))
            elif w == "left":
                print(manualClient.publish("/", "a"))
            elif w == "right":
                print(manualClient.publish("/", "d"))
            elif w == "stop":
                print(manualClient.publish("/", "stop"))


class Ui_ThirdWindow(object):
    def setupUi(self, Ui_ThirdWindow):
        Ui_ThirdWindow.setObjectName("How to use")
        Ui_ThirdWindow.resize(600, 250)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Ui_ThirdWindow.sizePolicy().hasHeightForWidth())
        Ui_ThirdWindow.setSizePolicy(sizePolicy)
        Ui_ThirdWindow.setMinimumSize(QtCore.QSize(600, 250))
        Ui_ThirdWindow.setMaximumSize(QtCore.QSize(600, 250))
        Ui_ThirdWindow.setStyleSheet(design.stylesheet)

        self.labelInstructions = QtWidgets.QLabel(Ui_ThirdWindow)
        self.labelInstructions.setGeometry(QtCore.QRect(10, 5, 191, 23))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.labelInstructions.setFont(font)
        self.labelInstructions.setObjectName("labelInstructions")

        self.label1 = QtWidgets.QLabel(Ui_ThirdWindow)
        self.label1.setGeometry(QtCore.QRect(10, 30, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label1.setFont(font)
        self.label1.setObjectName("label1")

        self.label2 = QtWidgets.QLabel(Ui_ThirdWindow)
        self.label2.setGeometry(QtCore.QRect(10, 50, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label2.setFont(font)
        self.label2.setObjectName("label2")

        self.label3 = QtWidgets.QLabel(Ui_ThirdWindow)
        self.label3.setGeometry(QtCore.QRect(10, 70, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label3.setFont(font)
        self.label3.setObjectName("label3")

        self.label4 = QtWidgets.QLabel(Ui_ThirdWindow)
        self.label4.setGeometry(QtCore.QRect(10, 90, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label4.setFont(font)
        self.label4.setObjectName("label4")

        self.label5 = QtWidgets.QLabel(Ui_ThirdWindow)
        self.label5.setGeometry(QtCore.QRect(10, 110, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label5.setFont(font)
        self.label5.setObjectName("label5")

        self.label6 = QtWidgets.QLabel(Ui_ThirdWindow)
        self.label6.setGeometry(QtCore.QRect(10, 130, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label6.setFont(font)
        self.label6.setObjectName("label6")

        self.label7 = QtWidgets.QLabel(Ui_ThirdWindow)
        self.label7.setGeometry(QtCore.QRect(10, 150, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label7.setFont(font)
        self.label7.setObjectName("label7")

        self.label8 = QtWidgets.QLabel(Ui_ThirdWindow)
        self.label8.setGeometry(QtCore.QRect(10, 170, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label8.setFont(font)
        self.label8.setObjectName("label8")

        self.label9 = QtWidgets.QLabel(Ui_ThirdWindow)
        self.label9.setGeometry(QtCore.QRect(10, 190, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label9.setFont(font)
        self.label9.setObjectName("label9")

        self.retranslateUi(Ui_ThirdWindow)
        QtCore.QMetaObject.connectSlotsByName(Ui_ThirdWindow)

    def retranslateUi(self, Ui_ThirdWindow):
        _translate = QtCore.QCoreApplication.translate
        Ui_ThirdWindow.setWindowTitle(_translate("Ui_ThirdWindow", "How to use"))
        self.labelInstructions.setText(_translate("Ui_ThirdWindow",
                                                  '<html><head/><body><p><span style=\" color:black;\">'
                                                  'Instructions: '
                                                  '</span></p></body></html>'))
        self.label1.setText(_translate("Ui_ThirdWindow",
                                       '<html><head/><body><p><span style=\" color:black;\">'
                                       'Forward : When clicked the car will move forward'
                                       '</span></p></body></html>'))
        self.label2.setText(_translate("Ui_ThirdWindow",
                                       '<html><head/><body><p><span style=\" color:black;\">'
                                       'Backward : When clicked the car will move backward'
                                       '</span></p></body></html>'))
        self.label3.setText(_translate("Ui_ThirdWindow",
                                       '<html><head/><body><p><span style=\" color:black;\">'
                                       'Left : When clicked the car will steer into the left direction'
                                       '</span></p></body></html>'))
        self.label4.setText(_translate("Ui_ThirdWindow",
                                       '<html><head/><body><p><span style=\" color:black;\">'
                                       'Right  : When clicked the car will steer into the right direction'
                                       '</span></p></body></html>'))
        self.label5.setText(_translate("Ui_ThirdWindow",
                                       '<html><head/><body><p><span style=\" color:black;\">'
                                       'Voice Control : When clicked it will open a window for the Voice Command Control'
                                       '</span></p></body></html>'))
        self.label6.setText(_translate("Ui_ThirdWindow",
                                       '<html><head/><body><p><span style=\" color:black;\">'
                                       'Exit : When clicked it will terminate the whole app'
                                       '</span></p></body></html>'))

        self.label9.setText(_translate("Ui_ThirdWindow",
                                       '<html><head/><body><p><span style=\" color:black;\">'
                                       'Brake : When clicked it will stop the car instantly'
                                       '</span></p></body></html>'))


class Controller():
    def __init__(self):
        pass

    def Show_FirstWindow(self):
        self.FirstWindow = QtWidgets.QMainWindow()
        self.ui = windowMain()
        self.ui.setupUi(self.FirstWindow)
        self.ui.buttonVoiceControl.clicked.connect(self.Show_SecondWindow)
        self.ui.buttonHelp.clicked.connect(self.Show_ThirdWindow)
        self.FirstWindow.show()

    def Show_SecondWindow(self):
        self.SecondWindow = QtWidgets.QMainWindow()
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self.SecondWindow)
        self.ui.pushButton.clicked.connect(self.Print)

        self.SecondWindow.show()

    def Show_ThirdWindow(self):
        self.ThirdWindow = QtWidgets.QMainWindow()
        self.ui = Ui_ThirdWindow()
        self.ui.setupUi(self.ThirdWindow)

        self.ThirdWindow.show()

    def Print(self):
        print()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Controller = Controller()
    Controller.Show_FirstWindow()
    manualClient.loop()
    sys.exit(app.exec_())
