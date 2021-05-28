import cv2
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print("connected OK Returned code=", rc)
        client.subscribe("/smartcar/camera")
    else:
        print("Bad connection Returned code=", rc)
    
class MainWindow(QMainWindow):
    def on_message(client, userdata, message):
        print(message.topic)
        global image
        image = QImage(message.payload, 600, 480, QImage.Format_RGB888)

    def window(self):
        super(MainWindow, self).__init__()
        self.title = "Video Viewer"
        self.setWindowTitle(self.title)

        label = QLabel(self)
        pixmap = QPixmap(image)
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())
        
def main():
    # Connections to mqtt
    broker_address = "localhost"
    client = mqtt.Client()
    client.connect(broker_address)
    client.subscribe('/smartcar/data/#')
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()

if __name__ == '__main__':
    main()
