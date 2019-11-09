import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon

class Example(QWidget):

	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):

		self.setWindowIcon(QIcon('book.png'))
		self.setGeometry(300, 300, 300, 300)
		self.center()
		self.setWindowTitle('Icon')
		self.show()

	def center(self):

		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def closeEvent(self, event):

		reply = QMessageBox.question(self, 'Message', 'Are you sure you want to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

if __name__ == '__main__':

	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())