import sys

from PyQt5 import QtWidgets, uic
from MainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets


data = {'coup de foudre':'fulger'}

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.retranslateUi(self)      
        self.setWindowTitle('Vocabulary')
        
        self.read_dict(self)

    def read_dict(self, Ui_MainWindow):
    	_translate = QtCore.QCoreApplication.translate
    	MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
    	__sortingEnabled = self.listWidget.isSortingEnabled()
    	self.listWidget.setSortingEnabled(False)
    	item = self.listWidget.item(0)
    	item.setText(_translate("MainWindow", "test"))


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()