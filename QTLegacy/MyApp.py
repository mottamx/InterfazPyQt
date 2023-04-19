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

        toolbar=QToolBar("Main toolbar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)

        button_action=QAction(QIcon("bug.png"), "Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        button_action.setShortcut(QKeySequence("Ctrl+p"))
        toolbar.addAction(button_action)

        toolbar.addSeparator()
        button_action2=QAction(QIcon("bug.png"), "Your button2", self)
        button_action2.setStatusTip("This is your button 2")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)        

        toolbar.addWidget(QLabel("Hello"))
        toolbar.addWidget(QCheckBox())

        self.setStatusBar(QStatusBar(self))

        menu=self.menuBar()
        file_menu=menu.addMenu("&File") #Ampersand is letter for Alt menu
        file_menu.addAction(button_action)
        file_menu.addSeparator()

        file_submenu = file_menu.addMenu("Submenu")
        file_submenu.addAction(button_action2)

    def contextMenuEvent(self, event):
        print("Context event")

    def onMyToolBarButtonClick(self,s):
        print("click",s)

#Only one of this per application. Pass sys argv
app=QApplication(sys.argv)

window=MainWindow()
window.show()

#Start loop
app.exec_()
