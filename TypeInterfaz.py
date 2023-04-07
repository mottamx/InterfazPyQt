# importing required libraries
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys
import time #For delay sleep
import serial.tools.list_ports #For ComPort
import serial

#print(sys.version_info) #Check Python version

#For multithread
class WorkerSignals(QObject): #Signals for the worker thread
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    textFill = pyqtSignal(str)

class Worker(QRunnable):
    def __init__(self, allLines, portSer, dictionary):
        super(Worker, self).__init__()
        self.is_paused = False
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.allTextBlock = allLines
        self.port=portSer
        self.dictionary= dictionary
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self): #What will be done in the thread
        #print(self.port)
        #Serial
        ser = serial.Serial(port=self.port, baudrate=19200, timeout=1)
        time.sleep(1)
        #Print the first three elements to check if its OK
        #Gets text
        for index, line in enumerate(self.allTextBlock):
            self.mutex.lock()
            while self.is_paused:
                self.condition.wait(self.mutex)
            self.mutex.unlock()
            self.signals.textFill.emit(line)
            #print(line)
            #Here goes the serial part
            for letter in line:
                #Go to dictionary for data
                codeTw = self.dictionary[letter]
                print(codeTw)
                while True:
                    ser.write((codeTw + "*" + codeTw).encode())
                    time.sleep(0.15)
                    ack = ser.readline().decode().strip()
                    print(ack)
                    if ack == "OK":
                        #print("Data received OK")
                        break
                    else:
                        #print("There was an error in the transmission, retry")
                        time.sleep(0.15)
            progress_pc = int(100*index/len(self.allTextBlock)) # Progress
            self.signals.progress.emit(progress_pc)
            #time.sleep(1)
            ser.write('\n'.encode())
        #Everything went fine    
        self.signals.progress.emit(100)
        self.signals.finished.emit()
        ser.close()
            
    def pause(self):
        self.mutex.lock()
        self.is_paused = True
        self.mutex.unlock()

    def resume(self):
        self.mutex.lock()
        self.is_paused = False
        self.mutex.unlock()
        self.condition.wakeAll()


# Subclass QMainWindow
class MainWindow(QMainWindow):
    def __init__(self,*args, **kwargs):
        self.totalLines = 0
        self.modelDict = {}
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
        #Choose dictionary based on model
        self.wModelCombo.currentIndexChanged.connect(self.handleComboChange)
        namePort = QLabel("Puerto:")
        self.wPortCombo = QComboBox()
        #perhaps this is not the best place, but works
        #Update ports in the combobox
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            #print("{}: {} [{}]".format(port, desc, hwid))
            self.wPortCombo.addItem(port)
        last_index = self.wPortCombo.count() - 1
        self.wPortCombo.setCurrentIndex(last_index)
        namePort.setBuddy(self.wPortCombo)
        wlabelLineT = QLabel("Lineas totales:")
        #wlabelLineT.setFixedSize(200,25)
        self.wlineasTotales = QLineEdit("00")

        self.wLinea = QLineEdit(":Linea actual:")
        #Buttons 
        wPortsB=QPushButton()
        wPortsB.setText("Actualizar puertos")
        wPortsB.pressed.connect( lambda n=2: self.updatePorts(n) )
        wTextB=QPushButton()
        wTextB.setText("Formato texto")
        wTextB.pressed.connect( lambda n=3: self.breakLines(n) )
        self.wLineB=QPushButton()
        self.wLineB.setText("PAUSAR / DETENER")
        self.wLineB.setCheckable(True)
        self.wLineB.setEnabled(False)
        self.wLineB.clicked.connect(self.workerlock)
        self.wAllB=QPushButton()
        self.wAllB.setText("Iniciar envio")
        self.wAllB.pressed.connect( lambda n=4: self.sendToHW(n))
        self.wListo=QRadioButton("Texto listo para enviar")
        self.wListo.setChecked(False)
        self.wListo.setEnabled(False)
        #Progress bar
        self.wAvance=QProgressBar()
        self.wAvance.isTextVisible = True
        self.wAvance.setValue(0)
        
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
        layout5.addWidget(self.wAllB)
        layout5.addWidget(self.wLinea)
        layout5.addWidget(self.wAvance)
        layout5.addWidget(self.wLineB)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        #Threads
        self.threadpool = QThreadPool()
        self.worker = None
        #print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    #Update ports in the combobox
    def updatePorts(self,n):
        self.wPortCombo.clear()
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            #print("{}: {} [{}]".format(port, desc, hwid))
            self.wPortCombo.addItem(port)
        last_index = self.wPortCombo.count() - 1
        self.wPortCombo.setCurrentIndex(last_index)

    #Update model in combobox
    def handleComboChange(self, index):
        if self.wModelCombo.currentText() != '---':
            self.wLinea.setText(":Linea actual:")
            route=self.wModelCombo.currentText() + '.txt'
            with open(route, 'r') as fileA:
                content = fileA.read()
            self.modelDict = eval(content)
            '''
            #Print the first three elements to check if its OK
            i = 0
            for k, v in modelDict.items():
                if i == 3:
                    break
                print(k, v)
                i += 1
            '''
                        
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
            self.totalLines = len(splittedLine2Many)
            self.wlineasTotales.setText(str(self.totalLines))
            self.wLinea.setText(":Linea actual:")
            self.wListo.setChecked(True)
            #print("Fin")
    #Flag to see if new text was added and disable radio button
    def on_text_changed (self):
        #print("Texto updateado")
        self.wListo.setChecked(False)

    #All the magic happens here
    #Threads to update status
    def update_progress(self, progress):
        self.wAvance.setValue(progress) #Show progress in bar

    def display_output(self, textFill):
        self.wLinea.setText(textFill) #Show current line

    def thread_complete(self):
        print("THREAD COMPLETE!")
        self.wLinea.setText(":Linea actual:")
        self.wAllB.setEnabled(True)
        self.wLineB.setEnabled(False)
    def sendToHW(self,n):
        if len(self.modelDict) <= 0:
            route=self.wModelCombo.currentText() + '.txt'
            with open(route, 'r') as fileA:
                content = fileA.read()
            self.modelDict = eval(content)
        if self.wListo.isChecked() is False:
            self.wLinea.setText('Falta presionar "Formato Texto"')
            self.wAllB.setChecked(False) 
        elif self.wListo.isChecked():
            #View
            self.wLinea.setText("") 
            self.wAllB.setEnabled(False)
            self.wLineB.setEnabled(True)
            #Control
            text = self.editor.toPlainText() #Gets all text from QPlainTextEdit
            allLines = text.splitlines()
            self.worker = Worker(allLines, self.wPortCombo.currentText(), self.modelDict)
            self.worker.signals.progress.connect(self.update_progress) # Pass the function to execute
            self.worker.signals.textFill.connect(self.display_output)
            self.worker.signals.finished.connect(self.thread_complete)
            self.threadpool.start(self.worker)

    def workerlock(self, checked):
        if checked:
            self.worker.pause()
        else:
            self.worker.resume()

   

# Main

app = QApplication(sys.argv)
app.setApplicationName("Auto-Typewriter")

window = MainWindow()
window.show()

# loop
app.exec_()
