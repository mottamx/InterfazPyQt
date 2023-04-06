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
        self.editor.textChanged.connect(self.on_text_changed)
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
        wlabelLineT = QLabel("Lineas totales:")
        #wlabelLineT.setFixedSize(200,25)
        self.wlineasTotales = QLineEdit("00")

        wLinea = QLineEdit(":Linea actual:")
        #Buttons 
        wPortsB=QPushButton()
        wPortsB.setText("Actualizar puertos")
        wPortsB.pressed.connect( lambda n=2: self.updatePorts(n) )
        wTextB=QPushButton()
        wTextB.setText("Formato texto")
        wTextB.pressed.connect( lambda n=3: self.breakLines(n) )
        wLineB=QPushButton()
        wLineB.setText("PAUSAR / DETENER")
        wAllB=QPushButton()
        wAllB.setText("Enviar todo")
        self.wListo=QRadioButton("Texto listo para enviar")
        self.wListo.setChecked(False)
        self.wListo.setEnabled(False)
        #Progress bar
        wAvance=QProgressBar()
        wAvance.isTextVisible = True
        wAvance.setValue(50)
        
        #Layout
        layout = QHBoxLayout() #All
        layout2 = QVBoxLayout() #All right side 
        layout3 = QGridLayout() #Top buttons
        layout3b = QGridLayout() #Top buttons
        layout4 = QVBoxLayout() #Middle buttons
        layout5 = QVBoxLayout() #Bottom buttons
        
        layout.addWidget(self.editor)
        layout.addLayout(layout2)
        layout2.addLayout(layout3)
        layout2.addLayout(layout4)
        layout2.addLayout(layout3b)
        layout2.addLayout(layout5)
        layout3.addWidget(nameLabel, 0, 1)
        layout3.addWidget(self.wModelCombo, 0, 2)
        layout3.addWidget(wPortsB, 1, 1)
        layout3.addWidget(namePort, 2, 1)
        layout3.addWidget(self.wPortCombo, 2, 2)
        layout3b.addWidget(wlabelLineT, 0, 1)
        layout3b.addWidget(self.wlineasTotales, 0, 2)
        layout4.addWidget(wTextB)
        layout4.addWidget(self.wListo)
        layout5.addWidget(wLinea)
        layout5.addWidget(wAllB)
        layout5.addWidget(wAvance)
        layout5.addWidget(wLineB)
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
        text = self.editor.toPlainText() #Gets all text from QPlainTextEdit
        allChars = len(text)
        if allChars > 0:
            #print(cantidad_caracteres)
            allLines = text.splitlines()
            #print("Total de líneas: ", len(allLines)) #If a single long string is entered, this method does not work, check to split despite no newlines
            splittedLine2Many = []
            #If there is a big text with no lines
            for index, line in enumerate(allLines):
                if len(line)>65:
                    #print("La linea supera longitud", index)
                    #As line is larger than 65 chars, we need to split accordingly (in a space)
                    indStr = 0 #To track current split char index start and end
                    indEnd = 0
                    newLen = 0 #Track if all chars are now in the list of strings
                    #print("La linea tiene caracteres", len(line))
                    while newLen <= len(line): #While we get all the chars in the new list
                        if(newLen + 65) <= len(line):
                            indEnd = line.rfind(' ', indStr, indStr+65) #Find first space to break
                            if indEnd == -1: #No space before 65, so break in 65
                                indEnd = 65
                            #print("El primer corte es en ", indEnd)
                            newLine=line[indStr:indEnd]
                            splittedLine2Many.append(newLine)
                            #print(newLine)
                            newLen += len(newLine)+1
                            #print("Del total, llevo asignados", newLen)
                            indStr = indEnd+1 #Update new start to previous end
                        else:
                            #print("Segundo caso, cadena mas corta de 65")
                            newLine=line[indStr:]
                            #print(newLine)
                            splittedLine2Many.append(newLine)
                            newLen += len(newLine)+1                     
                            #print("Del total, llevo asignados", newLen)
                else:
                    splittedLine2Many.append(line) 
            #Here lines is already splitted, but will join to show text in windget        
            formattedText = "\n".join(splittedLine2Many)
            self.editor.clear()
            self.editor.setPlainText(formattedText)
            self.wlineasTotales.setText(str(len(splittedLine2Many)))
            self.wListo.setChecked(True)
            #print("Fin")
    #
    def on_text_changed (self):
        #print("Texto updateado")
        self.wListo.setChecked(False)
# Main

app = QApplication(sys.argv)
app.setApplicationName("Auto-Typewriter")

window = MainWindow()
window.show()

# loop
app.exec_()
