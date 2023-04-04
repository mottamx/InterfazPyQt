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
        
        layout = QVBoxLayout()
        widgets = [QCheckBox,
                   QComboBox,
                   QDateEdit,
                   QDateTimeEdit,
                   QDial,
                   QDoubleSpinBox,
                   QFontComboBox,
                   QLCDNumber,
                   QLabel,
                   QLineEdit,
                   QProgressBar,
                   QPushButton,
                   QRadioButton,
                   QSlider,
                   QSpinBox,
                   QTimeEdit]
        
        for w in widgets:
            layout.addWidget(w())

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget) #Be in the middle
       

#Only one of this per application. Pass sys argv
app=QApplication(sys.argv)

window=MainWindow()
window.show()

#Start loop
app.exec_()

#Pagina 31 (37 de 264)