# importing required libraries
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys

#print(sys.version_info) #Check Python version

# Subclass QMainWindow
class MainWindow(QMainWindow):
    def __init__(self,*args, **kwargs):
        
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QtGui.QIcon('typewriter.png'))
        self.setWindowTitle("Auto-Typewriter")
        self.setFixedSize(650, 650)
        #QPlainTextEdit object
        self.editor = QPlainTextEdit()
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)
        self.editor.setMinimumWidth(450)
        #Model and Port
        nameLabel = QLabel("Equipo:")
        wModelCombo = QComboBox()
        wModelCombo.addItems(["Brother", "Gris"])
        nameLabel.setBuddy(wModelCombo)
        namePort = QLabel("Puerto:")
        wPortCombo = QComboBox()
        wPortCombo.addItems(["COM1", "COM8"])
        namePort.setBuddy(wPortCombo)
        wLinea=QLineEdit()
        #Buttons 
        wPortsB=QPushButton()
        wPortsB.setText("Actualizar puertos")
        wTextB=QPushButton()
        wTextB.setText("Formato texto")
        wLineB=QPushButton()
        wLineB.setText("Enviar linea")
        wAllB=QPushButton()
        wAllB.setText("Enviar todo")
        wListo=QRadioButton("Texto listo para enviar")
        wListo.setChecked(False)
        wListo.setEnabled(False)
        #Progress bar
        wAvance=QProgressBar()
        wAvance.isTextVisible = True
        wAvance.setValue(50)
        
        #Layout
        layout = QHBoxLayout() #All
        layout2 = QVBoxLayout() #All right side 
        layout3 = QGridLayout() #Top buttons
        layout4 = QVBoxLayout() #Middle buttons
        layout5 = QVBoxLayout() #Bottom buttons
        layout.addWidget(self.editor)
        layout.addLayout(layout2)
        layout2.addLayout(layout3)
        layout2.addLayout(layout4)
        layout2.addLayout(layout5)
        layout3.addWidget(nameLabel, 0, 1)
        layout3.addWidget(wModelCombo, 0, 2)
        layout3.addWidget(wPortsB, 1, 1)
        layout3.addWidget(namePort, 2, 1)
        layout3.addWidget(wPortCombo, 2, 2)
        layout4.addWidget(wTextB)
        layout4.addWidget(wListo)
        layout5.addWidget(wLinea)
        layout5.addWidget(wLineB)
        layout5.addWidget(wAllB)
        layout5.addWidget(wAvance)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
 

toPlainText

# Main
app = QApplication(sys.argv)
app.setApplicationName("Auto-Typewriter")
window = MainWindow()
window.show()
# loop
app.exec_()