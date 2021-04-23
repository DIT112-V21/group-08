import sys
import paho.mqtt.client as mqtt
from PyQt5 import QtCore, QtGui, QtWidgets
import speech_recognition as sr

# In order to get voice-recognition to work,
# paste the following commands into the termnial:
# pip install pipwin
# pipwin install PyAudio

#MQTT Stuff
broker_address = "localhost"
manualClient = mqtt.Client("Manual-Control")
manualClient.connect(broker_address)
manualClient.subscribe("/")

class windowMain(object):
    def setupUi(self, windowMain):
        windowMain.setObjectName("windowMain")
        windowMain.resize(700, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(windowMain.sizePolicy().hasHeightForWidth())
        windowMain.setSizePolicy(sizePolicy)
        windowMain.setMinimumSize(QtCore.QSize(700, 600))
        windowMain.setMaximumSize(QtCore.QSize(700, 600))
        windowMain.setStyleSheet("QWidget#windowMain{ background-image: url(star.png)}")
        self.labelWelcome = QtWidgets.QLabel(windowMain)
        self.labelWelcome.setGeometry(QtCore.QRect(340, 60, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.labelWelcome.setFont(font)
        self.labelWelcome.setObjectName("labelWelcome")
        self.buttonBrake = QtWidgets.QPushButton(windowMain)
        self.buttonBrake.setGeometry(QtCore.QRect(420, 320, 111, 81))
        self.buttonBrake.setAutoFillBackground(False)
        self.buttonBrake.setStyleSheet("background-color: red")
        self.buttonBrake.setObjectName("buttonBrake")
        self.buttonDeaccelerate = QtWidgets.QPushButton(windowMain)
        self.buttonDeaccelerate.setGeometry(QtCore.QRect(420, 230, 111, 81))
        self.buttonDeaccelerate.setStyleSheet("")
        self.buttonDeaccelerate.setObjectName("buttonDeaccelerate")
        self.buttonAccelerate = QtWidgets.QPushButton(windowMain)
        self.buttonAccelerate.setGeometry(QtCore.QRect(420, 140, 111, 81))
        self.buttonAccelerate.setStyleSheet("background-color: lightgreen")
        self.buttonAccelerate.setObjectName("buttonAccelerate")
        self.buttonForward = QtWidgets.QPushButton(windowMain)
        self.buttonForward.setGeometry(QtCore.QRect(160, 140, 111, 81))
        self.buttonForward.setStyleSheet("")
        self.buttonForward.setObjectName("buttonForward")
        self.buttonLeft = QtWidgets.QPushButton(windowMain)
        self.buttonLeft.setGeometry(QtCore.QRect(40, 230, 111, 81))
        self.buttonLeft.setStyleSheet("")
        self.buttonLeft.setObjectName("buttonLeft")
        self.buttonRight = QtWidgets.QPushButton(windowMain)
        self.buttonRight.setGeometry(QtCore.QRect(280, 230, 111, 81))
        self.buttonRight.setStyleSheet("")
        self.buttonRight.setObjectName("buttonRight")
        self.buttonBack = QtWidgets.QPushButton(windowMain)
        self.buttonBack.setGeometry(QtCore.QRect(160, 320, 111, 81))
        self.buttonBack.setStyleSheet("")
        self.buttonBack.setObjectName("buttonBack")
        self.buttonVoiceControl = QtWidgets.QPushButton(windowMain)
        self.buttonVoiceControl.setGeometry(QtCore.QRect(40, 430, 111, 81))
        self.buttonVoiceControl.setStyleSheet("")
        self.buttonVoiceControl.setObjectName("buttonVoiceControl")
        self.buttonMap = QtWidgets.QPushButton(windowMain)
        self.buttonMap.setGeometry(QtCore.QRect(160, 430, 111, 81))
        self.buttonMap.setStyleSheet("")
        self.buttonMap.setObjectName("buttonVoiceControl_2")
        self.buttonExit = QtWidgets.QPushButton(windowMain)
        self.buttonExit.setGeometry(QtCore.QRect(280, 430, 111, 81))
        self.buttonExit.setAutoFillBackground(False)
        self.buttonExit.setStyleSheet("background-color: red")
        self.buttonExit.setObjectName("buttonExit")
        self.sliderSpeed = QtWidgets.QSlider(windowMain)
        self.sliderSpeed.setGeometry(QtCore.QRect(560, 140, 81, 261))
        self.sliderSpeed.setOrientation(QtCore.Qt.Vertical)
        self.sliderSpeed.setObjectName("sliderSpeed")
        self.labelSpeedInteger = QtWidgets.QLabel(windowMain)
        self.labelSpeedInteger.setGeometry(QtCore.QRect(570, 440, 51, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.labelSpeedInteger.setFont(font)
        self.labelSpeedInteger.setObjectName("labelSpeedInteger")
        self.labelCurrentSpeed = QtWidgets.QLabel(windowMain)
        self.labelCurrentSpeed.setGeometry(QtCore.QRect(440, 440, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.labelCurrentSpeed.setFont(font)
        self.labelCurrentSpeed.setObjectName("labelCurrentSpeed")

        self.setUpButtons()
        self.retranslateUi(windowMain)
        QtCore.QMetaObject.connectSlotsByName(windowMain)

    def retranslateUi(self, windowMain):
        _translate = QtCore.QCoreApplication.translate
        windowMain.setWindowTitle(_translate("windowMain", "Dialog"))
        self.labelWelcome.setText(_translate("windowMain",
                                             "<html><head/><body><p><span style=\" color:#ffffff;\">Welcome to PathFinder</span></p><p><br/></p></body></html>"))
        self.buttonBrake.setText(_translate("windowMain", "Brake"))
        self.buttonDeaccelerate.setText(_translate("windowMain", "Deaccelerate"))
        self.buttonAccelerate.setText(_translate("windowMain", "Accelerate"))
        self.buttonForward.setText(_translate("windowMain", "Forward"))
        self.buttonLeft.setText(_translate("windowMain", "Left"))
        self.buttonRight.setText(_translate("windowMain", "Right"))
        self.buttonBack.setText(_translate("windowMain", "Back"))
        self.buttonVoiceControl.setText(_translate("windowMain", "Voice Control"))
        self.buttonMap.setText(_translate("windowMain", "Map"))
        self.buttonExit.setText(_translate("windowMain", "Exit"))
        self.labelSpeedInteger.setText(_translate("windowMain",
                                                  "<html><head/><body><p><span style=\" color:#ffffff;\">0</span></p></body></html>"))
        self.labelCurrentSpeed.setText(_translate("windowMain",
                                                  "<html><head/><body><p><span style=\" color:#ffffff;\">Current Speed:</span></p></body></html>"))

    def LoadSecondWindow(self):
        SecondWindow = QtWidgets.QMainWindow()
        ui = Ui_SecondWindow()
        ui.setupUi(SecondWindow)
        SecondWindow.show()

    def setUpButtons(self):
        self.buttonForward.clicked.connect(lambda: self.publish("w"))
        self.buttonLeft.clicked.connect(lambda: self.publish("a"))
        self.buttonRight.clicked.connect(lambda: self.publish("d"))
        self.buttonBack.clicked.connect(lambda: self.publish("s"))
        self.buttonAccelerate.clicked.connect(lambda: self.publish("e"))
        self.buttonDeaccelerate.clicked.connect(lambda: self.publish("q"))
        self.buttonBrake.clicked.connect(lambda: self.publish("stop"))
        self.buttonExit.clicked.connect(QtCore.QCoreApplication.instance().quit)

    def publish(self, message):
        print(manualClient.publish("/", message))

class Ui_SecondWindow(object):
    def setupUi(self, Ui_SecondWindow):
        Ui_SecondWindow.setObjectName("Voice Control")
        Ui_SecondWindow.resize(400, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Ui_SecondWindow.sizePolicy().hasHeightForWidth())
        Ui_SecondWindow.setSizePolicy(sizePolicy)
        Ui_SecondWindow.setMinimumSize(QtCore.QSize(400, 300))
        Ui_SecondWindow.setMaximumSize(QtCore.QSize(400, 300))
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
                print("ERROR")
            try:
                text = r.recognize_google(audio)
                self.publish(text)
                print("You said : {}".format(text))
            except:
                print('Sorry, could not recognize your voice')


    # Legal voice commands:
    # forward, back, left, right, stop, accelerate, accelerator, deaccelerate
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
            elif w == "accelerate":
                print(manualClient.publish("/", "e"))
            elif w == "accelerator":
                print(manualClient.publish("/", "e"))
            elif w == "deaccelerate":
                print(manualClient.publish("/", "q"))
            else:
                pass

class Controller:
    def __init__(self):
        pass

    def Show_FirstWindow(self):
        self.FirstWindow = QtWidgets.QMainWindow()
        self.ui = windowMain()
        self.ui.setupUi(self.FirstWindow)
        self.ui.buttonVoiceControl.clicked.connect(self.Show_SecondWindow)

        self.FirstWindow.show()

    def Show_SecondWindow(self):
        self.SecondWindow = QtWidgets.QMainWindow()
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self.SecondWindow)
        self.ui.pushButton.clicked.connect(self.Print)

        self.SecondWindow.show()

    def Print(self):
        print()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Controller = Controller()
    Controller.Show_FirstWindow()
    sys.exit(app.exec_())
