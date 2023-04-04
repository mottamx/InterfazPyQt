from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


import sys
#print(sys.version_info) #Check if same as terminal

#Subclass QMainWindow customize window
class MainWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Interfaz de Sistema")
        label=QLabel("Primera version")
        #Verificar en http://doc.qt.io/qt-5/qt.html
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label) #Be in the middle


#Only one of this per application. Pass sys argv
app=QApplication(sys.argv)

window=MainWindow()
window.show()

#Start loop
app.exec_()

