import sys
from PyQt5.QtWidgets import QWidget, QListWidget, QGridLayout, QApplication, QMenuBar, QAction, qApp, QFileDialog
from PyQt5.QtCore import Qt

from utilities import *


class Example(QWidget):
	
	def __init__(self):
		super().__init__() 

		self.initUI()


	def initUI(self):

		global list_1
		list_1 = QListWidget()
		lister(list_1, 0)
		list_1.clicked.connect(self.clear) 
		# list_1.sortItems() # 1 for descending

		global list_2
		list_2 = QListWidget()
		lister(list_2, 1)
		list_2.clicked.connect(self.clear)

		global list_3
		list_3 = QListWidget()
		lister(list_3, 2)
		list_3.clicked.connect(self.clear)
		list_3.setHidden(True)


		menubar = QMenuBar()
		menubar.setNativeMenuBar(False)
		menubar.setStyleSheet("background-color: rgb(240, 240, 240);") # blending the toolbar with the app bg

		showAct = QAction('Show kanji', self, checkable=True)  
		showAct.setChecked(False)
		showAct.setShortcut('Ctrl+E')
		showAct.triggered.connect(self.pressed)

		optionMenu = menubar.addMenu('Options')
		style(optionMenu)
		optionMenu.addAction(showAct)

		fileMenu = menubar.addMenu('File')
		fileOpen = QAction('Open file', self)
		fileOpen.triggered.connect(self.fileDialog)
		fileOpen.setShortcut('Ctrl+O')

		fileSave = QAction('Save file', self)
		fileSave.triggered.connect(self.save)
		fileSave.setShortcut('Ctrl+S')

		style(fileMenu)
		fileMenu.addAction(fileOpen)
		fileMenu.addAction(fileSave)


		grid = QGridLayout()
		grid.setSpacing(10)
		grid.addWidget(menubar, 0, 0)
		grid.addWidget(list_1, 1, 0)
		grid.addWidget(list_2, 1, 1)
		grid.addWidget(list_3, 1, 2)

		self.setLayout(grid)      
		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle('Vocabulary')    
		self.show()


	def pressed(self): #, e
		
		# if e.key() == Qt.Key_E: # ctrl+e
		list_3.setHidden(not list_3.isHidden())
		self.add_item()


	def add_item(self): # under testing

		for x in range(3):	
			if x == 0:
				lister(list_1, x, 1)

			elif x == 1:
				lister(list_2, x, 1)

			elif x == 2:
				lister(list_3, x, 1)

		item =  list_1.item(list_1.count()-1) # use itemChanged to jump to the next column and edit
		list_1.editItem(item)

	def clear(self):
		"""Clears all item slections for aesthetical purposes"""

		list_1.clearSelection()
		list_2.clearSelection()
		list_3.clearSelection()


	def fileDialog(self):

		fname = QFileDialog()
		path = fname.getOpenFileName(self, 'Open file', '/french.csv', filter='txt (*.txt);;All files (*.*)') # could use this for recents, also change the second parameter to the last opened file
		print(path[0])


	def save(self): # use itemSelectionChanged to trigger this

		list1_items = total_items(list_1)
		list2_items = total_items(list_2)
		list3_items = total_items(list_3)

		total_dicts = []
		for (a, b, c) in zip(list1_items, list2_items, list3_items): # each letter is a column
			dictionary = {'word_1':a, 'word_2':b, 'notes':c}
			total_dicts.append(dictionary)
			s
		writer(total_dicts)

if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())