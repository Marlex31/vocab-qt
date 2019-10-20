import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QMenu, QTextEdit
from PyQt5.QtGui import QIcon

# No toolbar was added, whereas the tutorial included it (zetcode)

class Example(QMainWindow):

	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):

		exitAct = QAction(QIcon('book.png'), '&Exit', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Exit app')
		exitAct.triggered.connect(qApp.quit)

		self.statusBar().showMessage('Ready')

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAct)

		impMenu = QMenu('Import', self)
		impAct = QAction('Import mail', self)
		impAct.setStatusTip('Import')
		impMenu.addAction(impAct)

		newAct = QAction('New', self)

		fileMenu.addAction(newAct)
		fileMenu.addMenu(impMenu)

		textEdit = QTextEdit()
		self.setCentralWidget(textEdit)

		self.setGeometry(300, 300, 300, 300)
		self.setWindowTitle('Staus Bar, Menu')
		self.show()

if __name__ == '__main__':

	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())