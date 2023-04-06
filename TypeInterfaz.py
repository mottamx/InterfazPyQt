# importing required libraries
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys
import serial.tools.list_ports

#print(sys.version_info) #Check Python version

# Subclass QMainWindow
class MainWindow(QMainWindow):
    def __init__(self,*args, **kwargs):
        
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QtGui.QIcon('typewriter.png'))
        self.setWindowTitle("Auto-Typewriter")
        self.setFixedSize(850, 650)
        #QPlainTextEdit object
        self.editor = QPlainTextEdit()
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(9)
        self.editor.setFont(fixedfont)
        self.editor.setMinimumWidth(592)
        #Model and Port
        nameLabel = QLabel("Equipo:")
        self.wModelCombo = QComboBox()
        self.wModelCombo.addItems(["AX-325", "GX-6000"])
        nameLabel.setBuddy(self.wModelCombo)
        namePort = QLabel("Puerto:")
        self.wPortCombo = QComboBox()
        #perhaps this is not the best place, but works
        #Update ports in the combobox
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            #print("{}: {} [{}]".format(port, desc, hwid))
            self.wPortCombo.addItem(port)
        namePort.setBuddy(self.wPortCombo)
        wLinea=QLineEdit()
        #Buttons 
        wPortsB=QPushButton()
        wPortsB.setText("Actualizar puertos")
        wPortsB.pressed.connect( lambda n=2: self.updatePorts(n) )
        wTextB=QPushButton()
        wTextB.setText("Formato texto")
        wTextB.pressed.connect( lambda n=3: self.breakLines(n) )
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
        layout3.addWidget(self.wModelCombo, 0, 2)
        layout3.addWidget(wPortsB, 1, 1)
        layout3.addWidget(namePort, 2, 1)
        layout3.addWidget(self.wPortCombo, 2, 2)
        layout4.addWidget(wTextB)
        layout4.addWidget(wListo)
        layout5.addWidget(wLinea)
        layout5.addWidget(wLineB)
        layout5.addWidget(wAllB)
        layout5.addWidget(wAvance)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    #Update ports in the combobox
    def updatePorts(self,n):
        self.wPortCombo.clear()
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            #print("{}: {} [{}]".format(port, desc, hwid))
            self.wPortCombo.addItem(port)
    #Break text lines intro chucks that can be processed by hardware

    def breakLines(self,n):
        text = self.editor.toPlainText()
        lines = text.splitlines()
        print("Total de líneas: ", len(lines)) #If a single long string is entered, this method does not work, check to split despite no newlines
        print(type(lines))
        bufferCadena = ""
        # For each line split in 65 chars max and insert the exceding text to the new line
        for index, line in enumerate(lines):
            if len(line) > 65:
                indStr = line.rfind(' ', 0, 65) #search space to break the string
                if indStr == -1: #No space before 65, so break in 65
                    indStr = 65
                bufferCadena = line[indStr+1:]    
                formatedline = line[:indStr]
                print(formatedline)
                lines[index] = formatedline
                lines[index+1] = bufferCadena + ' ' + lines[index+1]
            else:
                print(line)
        #Here lines is already splitted, but will join to show text in windget        
        formattedText = "\n".join(lines)
        self.editor.clear()
        self.editor.setPlainText(formattedText)

# Main

app = QApplication(sys.argv)
app.setApplicationName("Auto-Typewriter")

window = MainWindow()
window.show()

# loop
app.exec_()
