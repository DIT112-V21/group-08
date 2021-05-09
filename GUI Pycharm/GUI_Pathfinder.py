"""

Made by Group Pathfinder (group 8 - DIT112)

"""

import sys
import os
import paho.mqtt.client as mqtt
from PyQt5 import QtCore, QtGui, QtWidgets
import speech_recognition as sr
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QThread
import design
import logging
import datetime
import time
import random
import shutil

#Logging
logging.basicConfig(filename="activeLog.log", level=logging.INFO, format="%(levelname)s : %(asctime)s : %(message)s")

with open('logBackup.txt','wb') as wfd:
    for f in ['logBackup.txt','activeLog.log']:
        with open(f,'rb') as fd:
            shutil.copyfileobj(fd, wfd)

with open("activeLog.log", "w"):
    pass

class Thread(QThread):
    log = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)
        self._items = []

    def setItems(self, items):
        if not self.isRunning():
            self._items[:] = items

    def run(self):
        for item in self._items:
            time.sleep(1)
            self.log.emit('processing: %s' % item)

class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui()
        self._worker = Thread()
        self._worker.log.connect(self.toLog)
        self._worker.started.connect(lambda: self.toLog('start'))
        self._worker.finished.connect(lambda: self.toLog('finished'))

    def process(self):
        items = ['Image%02d.png' % i for i in range(10)]
        self._worker.setItems(items)
        self._worker.start()

    def ui(self):
        self.LogOutputTxt = QtWidgets.QTextEdit()
        self.LogOutputTxt.setReadOnly(True)
        startBtn = QtWidgets.QPushButton('Start')
        startBtn.clicked.connect(self.start)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.LogOutputTxt)
        layout.addWidget(startBtn)
        self.setLayout(layout)
        self.resize(400, 300)
        self.show()

    def start(self):
        if not self._worker.isRunning():
            self.process()

    def toLog(self, txt):
        self.LogOutputTxt.append(txt)

# MQTT Stuff
broker_address = "localhost"
manualClient = mqtt.Client("Manual-Control")
manualClient.connect(broker_address)
manualClient.subscribe("/")


# PyQt5
class WindowMain(object):
    def setupUi(self, windowmain):

        logging.info("Opening main window")
        windowmain.setObjectName("windowMain")
        windowmain.resize(650, 450)

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(windowmain.sizePolicy().hasHeightForWidth())
        windowmain.setSizePolicy(size_policy)
        windowmain.setMinimumSize(QtCore.QSize(650, 450))
        windowmain.setMaximumSize(QtCore.QSize(650, 450))
        windowmain.setObjectName("main_window")
        windowmain.setStyleSheet(design.stylesheet)
        windowmain.setStyleSheet(design.stylesheet)
        app.aboutToQuit.connect(lambda: logging.info("--------------- Exiting Program ---------------"))


        self.buttonBrake = QtWidgets.QPushButton(windowmain)
        self.buttonBrake.setGeometry(QtCore.QRect(400, 330, 111, 81))
        self.buttonBrake.setAutoFillBackground(False)
        self.buttonBrake.setObjectName("buttonBrake")

        self.buttonForward = QtWidgets.QPushButton(windowmain)
        self.buttonForward.setGeometry(QtCore.QRect(160, 40, 111, 81))
        self.buttonForward.setStyleSheet("")
        self.buttonForward.setObjectName("buttonForward")

        self.buttonLeft = QtWidgets.QPushButton(windowmain)
        self.buttonLeft.setGeometry(QtCore.QRect(40, 130, 111, 81))
        self.buttonLeft.setStyleSheet("")
        self.buttonLeft.setObjectName("buttonLeft")

        self.buttonRight = QtWidgets.QPushButton(windowmain)
        self.buttonRight.setGeometry(QtCore.QRect(280, 130, 111, 81))
        self.buttonRight.setStyleSheet("")
        self.buttonRight.setObjectName("buttonRight")

        self.buttonBack = QtWidgets.QPushButton(windowmain)
        self.buttonBack.setGeometry(QtCore.QRect(160, 220, 111, 81))
        self.buttonBack.setStyleSheet("")
        self.buttonBack.setObjectName("buttonBack")

        self.buttonVoiceControl = QtWidgets.QPushButton(windowmain)
        self.buttonVoiceControl.setGeometry(QtCore.QRect(40, 330, 111, 81))
        self.buttonVoiceControl.setStyleSheet("")
        self.buttonVoiceControl.setObjectName("buttonVoiceControl")

        self.buttonHelp = QtWidgets.QPushButton(windowmain)
        self.buttonHelp.setGeometry(QtCore.QRect(160, 330, 111, 81))
        self.buttonHelp.setObjectName("buttonHelp")

        self.buttonLogging = QtWidgets.QPushButton(windowmain)
        self.buttonLogging.setGeometry(QtCore.QRect(280, 330, 111, 81))
        self.buttonLogging.setStyleSheet("background-color: gray")
        self.buttonLogging.setObjectName("buttonLogging")

        self.buttonExit = QtWidgets.QPushButton(windowmain)
        self.buttonExit.setGeometry(QtCore.QRect(550, 350, 80, 60))
        self.buttonExit.setAutoFillBackground(False)
        self.buttonExit.setStyleSheet("background-color: red")
        self.buttonExit.setObjectName("buttonExit")

        self.sliderSpeed = QtWidgets.QSlider(windowmain)
        self.sliderSpeed.setGeometry(QtCore.QRect(430, 40, 81, 261))
        self.sliderSpeed.setOrientation(QtCore.Qt.Vertical)
        self.sliderSpeed.setObjectName("sliderSpeed")
        self.sliderSpeed.setRange(0, 100)

        self.sliderSpeed.valueChanged[int].connect(self.changeValue)

        self.labelCurrentSpeed = QtWidgets.QLabel(windowmain)
        self.labelCurrentSpeed.setGeometry(QtCore.QRect(560, 340, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.labelCurrentSpeed.setFont(font)
        self.labelCurrentSpeed.setObjectName("labelCurrentSpeed")

        self.setUpButtons()
        self.retranslateUi(windowmain)
        QtCore.QMetaObject.connectSlotsByName(windowmain)

    def retranslateUi(self, windowMain):
        _translate = QtCore.QCoreApplication.translate
        windowMain.setWindowTitle(_translate("windowMain", "Path Finder"))
        self.buttonBrake.setText(_translate("windowMain", "Brake"))
        self.buttonForward.setText(_translate("windowMain", "Forward"))
        self.buttonLeft.setText(_translate("windowMain", "Left"))
        self.buttonRight.setText(_translate("windowMain", "Right"))
        self.buttonBack.setText(_translate("windowMain", "Back"))
        self.buttonVoiceControl.setText(_translate("windowMain", "Voice Control"))
        self.buttonVoiceControl.setIcon(QIcon('voice.png'))
        self.buttonVoiceControl.setStyleSheet("background-color:green")
        self.buttonHelp.setText(_translate("windowMain", "How to use"))
        self.buttonHelp.setIcon(QIcon('help.png'))
        self.buttonHelp.setStyleSheet("background-color: yellow")
        self.buttonLogging.setText(_translate("windowMain", "Logging"))
        self.buttonExit.setText(_translate("windowMain", "Exit"))
        self.buttonExit.setStyleSheet("background-color:brown")
        self.buttonLogging.setIcon(QIcon('history.png'))
        self.buttonBrake.setIcon(QIcon('brakes.png'))

        self.labelCurrentSpeed.setText(_translate("windowMain",
                                                  "<html><head/><body><p><span style=\" "
                                                  "color:white;\"></span></p></body></html>"))

    @staticmethod
    def changeValue(value):
        print(manualClient.publish("speed", value), " Slider value: ", value)

    @staticmethod
    def LoadSecondWindow():
        second_window = QtWidgets.QMainWindow()
        ui = UiSecondWindow()
        ui.setupUi(second_window)
        second_window.show()

    @staticmethod
    def LoadThirdWindow():
        third_window = QtWidgets.QMainWindow()
        ui = UiThirdWindow()
        ui.setupUi(third_window)
        third_window.show()

    def setUpButtons(self):
        self.buttonForward.clicked.connect(lambda: self.publish("/", "w"))
        self.buttonForward.clicked.connect(lambda: logging.info("Pressed forward button"))
        self.buttonLeft.clicked.connect(lambda: self.publish("/", "a"))
        self.buttonLeft.clicked.connect(lambda: logging.info("Pressed left button"))
        self.buttonRight.clicked.connect(lambda: self.publish("/", "d"))
        self.buttonRight.clicked.connect(lambda: logging.info("Pressed right button"))
        self.buttonBack.clicked.connect(lambda: self.publish("/", "s"))
        self.buttonBack.clicked.connect(lambda: logging.info("Pressed back button"))
        self.buttonBrake.clicked.connect(lambda: self.publish("/", "stop"))
        self.buttonBrake.clicked.connect(lambda: logging.info("Pressed brake button"))
        self.buttonExit.clicked.connect(lambda: self.exitProgram())
        self.buttonLogging.clicked.connect(lambda: os.startfile("activeLog.log"))

    @staticmethod
    def publish(topic, message):
        print(manualClient.publish(topic, message), " Action: ", message)

    @staticmethod
    def exitProgram():
        QtCore.QCoreApplication.instance().quit()

class UiSecondWindow(object):
    def setupUi(self, uisecondwindow):
        uisecondwindow.setObjectName("Voice Control")
        uisecondwindow.resize(400, 270)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(uisecondwindow.sizePolicy().hasHeightForWidth())
        uisecondwindow.setSizePolicy(size_policy)
        uisecondwindow.setMinimumSize(QtCore.QSize(400, 270))
        uisecondwindow.setMaximumSize(QtCore.QSize(400, 270))
        uisecondwindow.setObjectName("Ui_SecondWindow")
        uisecondwindow.setStyleSheet(design.stylesheet)

        self.centralWidget = QtWidgets.QWidget(uisecondwindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 130, 191, 23))
        self.pushButton.setObjectName("pushButton")
        self.labelVoiceExample = QtWidgets.QLabel(uisecondwindow)
        self.labelVoiceExample.setGeometry(QtCore.QRect(25, 180, 300, 50))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.labelVoiceExample.setFont(font)
        self.labelVoiceExample.setObjectName("labelVoiceExample")

        uisecondwindow.setCentralWidget(self.centralWidget)

        self.setUpButtons()
        self.retranslateUi(uisecondwindow)
        QtCore.QMetaObject.connectSlotsByName(uisecondwindow)

    def retranslateUi(self, uisecondwindow):
        _translate = QtCore.QCoreApplication.translate
        uisecondwindow.setWindowTitle(_translate("uisecondwindow", "Voice Window"))
        self.labelVoiceExample.setText(_translate("uisecondwindow",
                                                  '<html><head/><body><p><span>Example: "Drive '
                                                  'forward"</span></p></body></html>'))
        self.pushButton.setIcon(QIcon('record.png'))
        self.pushButton.setText(_translate("uisecondwindow", "Click, then say a command"))

    def setUpButtons(self):
        self.pushButton.clicked.connect(lambda: self.voiceRecognition())

    def voiceRecognition(self):
        self.pushButton.setText("Say command")
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                try:
                    logging.info("Recording voice")
                    audio = r.listen(source)
                    text = r.recognize_google(audio)
                    logging.info("You said: '{}'".format(text))
                    self.labelVoiceExample.setText("Last command: '{}'".format(text))
                    self.publish("/", text)
                except NotImplementedError:
                    logging.warning('Voice recognition error.')
        except NotImplementedError:
            logging.warning("Sound device error")
        self.pushButton.setText("Click, then say a command")

    @staticmethod
    def publish(topic, message):
        words = message.split()
        for w in words:
            if w == "forward":
                print(manualClient.publish(topic, "w"))
                logging.info("Telling car to drive forward.")
            elif w == "back":
                print(manualClient.publish(topic, "s"))
                logging.info("Telling car to drive back.")
            elif w == "left":
                print(manualClient.publish(topic, "a"))
                logging.info("Telling car to turn left.")
            elif w == "right":
                print(manualClient.publish(topic, "d"))
                logging.info("Telling car to turn right.")
            elif w == "stop":
                print(manualClient.publish(topic, "stop"))
                logging.info("Telling car to stop.")


class UiThirdWindow(object):
    def setupUi(self, uithirdwindow):
        uithirdwindow.setObjectName("How to use")
        uithirdwindow.resize(400, 300)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(uithirdwindow.sizePolicy().hasHeightForWidth())
        uithirdwindow.setSizePolicy(size_policy)
        uithirdwindow.setMinimumSize(QtCore.QSize(600, 350))
        uithirdwindow.setMaximumSize(QtCore.QSize(600, 350))
        uithirdwindow.setObjectName("Ui_ThirdWindow")
        uithirdwindow.setStyleSheet(design.stylesheet)

        self.labelInstructions = QtWidgets.QLabel(uithirdwindow)
        self.labelInstructions.setGeometry(QtCore.QRect(10, 5, 191, 23))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.labelInstructions.setFont(font)
        self.labelInstructions.setObjectName("labelInstructions")

        self.label1 = QtWidgets.QLabel(uithirdwindow)
        self.label1.setGeometry(QtCore.QRect(10, 30, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label1.setFont(font)
        self.label1.setObjectName("label1")

        self.label2 = QtWidgets.QLabel(uithirdwindow)
        self.label2.setGeometry(QtCore.QRect(10, 60, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label2.setFont(font)
        self.label2.setObjectName("label2")

        self.label3 = QtWidgets.QLabel(uithirdwindow)
        self.label3.setGeometry(QtCore.QRect(10, 90, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label3.setFont(font)
        self.label3.setObjectName("label3")

        self.label4 = QtWidgets.QLabel(uithirdwindow)
        self.label4.setGeometry(QtCore.QRect(10, 120, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label4.setFont(font)
        self.label4.setObjectName("label4")

        self.label5 = QtWidgets.QLabel(uithirdwindow)
        self.label5.setGeometry(QtCore.QRect(10, 150, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label5.setFont(font)
        self.label5.setObjectName("label5")

        self.label6 = QtWidgets.QLabel(uithirdwindow)
        self.label6.setGeometry(QtCore.QRect(10, 180, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label6.setFont(font)
        self.label6.setObjectName("label6")

        self.label7 = QtWidgets.QLabel(uithirdwindow)
        self.label7.setGeometry(QtCore.QRect(10, 210, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label7.setFont(font)
        self.label7.setObjectName("label7")

        self.label8 = QtWidgets.QLabel(uithirdwindow)
        self.label8.setGeometry(QtCore.QRect(10, 240, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label8.setFont(font)
        self.label8.setObjectName("label8")

        self.label9 = QtWidgets.QLabel(uithirdwindow)
        self.label9.setGeometry(QtCore.QRect(10, 270, 600, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label9.setFont(font)
        self.label9.setObjectName("label9")

        self.retranslateUi(uithirdwindow)
        QtCore.QMetaObject.connectSlotsByName(uithirdwindow)

    def retranslateUi(self, uithirdwindow):
        _translate = QtCore.QCoreApplication.translate
        uithirdwindow.setWindowTitle(_translate("uithirdwindow", "How to use"))
        self.labelInstructions.setText(_translate("uithirdwindow",
                                                  '<html><head/><b><body><p><span style=\" color:purple;\">'
                                                  'Instructions : '
                                                  '</span></p></body></html>'))
        self.label1.setText(_translate("uithirdwindow",
                                       '<html><head/><body><p><span style=\" color:black;\">'
                                       'Forward : When clicked the car will move forward'
                                       '</span></p></body></html>'))
        self.label2.setText(_translate("uithirdwindow",
                                       '<html><head/><body><p><span style=\" color:black;\">'
                                       'Backward : When clicked the car will move backward'
                                       '</span></p></body></html>'))
        self.label3.setText(_translate("uithirdwindow",
                                       '<html><head/><body><p><span style=\" color:black;\">'
                                       'Left : When clicked the car will steer into the left direction'
                                       '</span></p></body></html>'))
        self.label4.setText(_translate("uithirdwindow",
                                       '<html><head/><body><p><span style=\" color:black;\">'
                                       'Right  : When clicked the car will steer into the right direction'
                                       '</span></p></body></html>'))
        self.label5.setText(_translate("uithirdwindow",
                                       '<html><head/><body><p><span style=\" color:black;\">'
                                       'Voice Control : When clicked it will open a window for the Voice Command '
                                       'Control '
                                       '</span></p></body></html>'))
        self.label6.setText(_translate("uithirdwindow",
                                       '<html><head/><body><p><span style=\" color:black;\">'
                                       'Brake : When clicked it will stop the car instantly'
                                       '</span></p></body></html>'))
        self.label7.setText(_translate("uithirdwindow",
                                       '<html><head/><body><p><span style=\" color:black;\">'
                                       'Exit : When clicked it will terminate the whole app'
                                       '</span></p></body></html>'))
        self.label8.setText(_translate("uithirdwindow",
                                       '<html><head/><body><p><span style=\" color:black;\">'
                                       'Slider : To control car speed from 0 to 100'
                                       '</span></p></body></html>'))
        self.label9.setText(_translate("uithirdwindow",
                                       "<html><head/><body><p><span style=\" color:black;\">"
                                       "Logging : To show all the commands during the current session"
                                       "</span></p></body></html>"))


class Controller:
    def __init__(self):
        QtCore.QThread.currentThread().setObjectName('MainThread')

    def Show_FirstWindow(self):
        self.FirstWindow = QtWidgets.QMainWindow()
        self.ui = WindowMain()
        self.FirstWindow.setWindowIcon(QtGui.QIcon('Car icon.png'))
        self.ui.setupUi(self.FirstWindow)
        self.ui.buttonVoiceControl.clicked.connect(self.Show_SecondWindow)
        self.ui.buttonHelp.clicked.connect(self.Show_ThirdWindow)
        self.FirstWindow.show()

    def Show_SecondWindow(self):
        self.SecondWindow = QtWidgets.QMainWindow()
        self.ui = UiSecondWindow()
        self.SecondWindow.setWindowIcon(QtGui.QIcon('Car icon.png'))
        self.ui.setupUi(self.SecondWindow)
        self.SecondWindow.show()

    def Show_ThirdWindow(self):
        self.ThirdWindow = QtWidgets.QMainWindow()
        self.ui = UiThirdWindow()
        self.ThirdWindow.setWindowIcon(QtGui.QIcon('Car icon.png'))
        self.ui.setupUi(self.ThirdWindow)
        self.ThirdWindow.show()



if __name__ == "__main__":
    logging.info("------------- Launching Pathfinder -------------")
    app = QtWidgets.QApplication(sys.argv)
    Controller = Controller()
    Controller.Show_FirstWindow()
    sys.exit(app.exec_())
