import sys
from PyQt5.QtWidgets import QWidget, QListWidget, QGridLayout, QApplication, QMenuBar, QAction, qApp, QLineEdit, QAbstractItemView, QStyle, QFileDialog, QMenu, QStatusBar
from PyQt5.QtCore import Qt, QEvent, QUrl
from PyQt5.QtGui import QPalette, QColor

from utilities import *
from os import getcwd


class Example(QWidget):
	
	def __init__(self):
		super().__init__() 

		self.filenames = json_files()

		if type(self.filenames) is list:
			self.curr_file = self.filenames[0]
		else:
			self.curr_file = self.filenames

		self.initUI()


	def initUI(self):

		self.num = -1 # index for search bar query

		self.list_1 = QListWidget()
		lister(file=self.curr_file ,target=self.list_1, index=0, mode=2)
		self.list_1.clicked.connect(self.clear) 
		self.list_1.installEventFilter(self)

		self.list_2 = QListWidget()
		lister(file=self.curr_file ,target=self.list_2, index=1, mode=2)
		self.list_2.clicked.connect(self.clear)

		self.list_3 = QListWidget()
		lister(file=self.curr_file ,target=self.list_3, index=2, mode=2)
		self.list_3.clicked.connect(self.clear)
		self.list_3.setHidden(True)


		self.menubar = QMenuBar()
		self.menubar.setNativeMenuBar(False)


		showAct = QAction('Show extras', self, checkable=True)  
		showAct.setChecked(False)
		showAct.setShortcut('Ctrl+E')
		showAct.triggered.connect(self.pressed)

		addAct = QAction('Fields', self)  
		addAct.setShortcut('Ctrl+N')
		addAct.triggered.connect(self.add_item)

		fileOpen = QAction('Open file', self)
		fileOpen.triggered.connect(self.fileDialog)
		fileOpen.setShortcut('Ctrl+O')

		fileSave = QAction('Save file', self)
		fileSave.triggered.connect(self.save)
		fileSave.triggered.connect(self.refreshRecents)
		fileSave.setShortcut('Ctrl+S')

		self.fileRecents = QMenu('Recent file', self)
		self.refreshRecents()
		
		self.toggle_theme = QAction('Toggle theme', self, checkable=True)
		self.toggle_theme.setChecked(json_theme())
		self.toggle_theme.triggered.connect(self.theme)
		self.toggle_theme.setShortcut('Ctrl+T')

		self.addFields = self.menubar.addMenu('Add')
		self.addFields.addAction(addAct)

		self.optionMenu = self.menubar.addMenu('Options')
		self.optionMenu.addAction(showAct)
		self.optionMenu.addAction(self.toggle_theme)

		self.fileMenu = self.menubar.addMenu('File')
		self.fileMenu.addAction(fileOpen)
		self.fileMenu.addAction(fileSave)
		self.fileMenu.addMenu(self.fileRecents)


		self.search_bar = QLineEdit()
		self.search_bar.setPlaceholderText('Search vocab')
		self.search_bar.setClearButtonEnabled(True)
		self.search_bar.setMaxLength(10)
		self.search_bar.returnPressed.connect(self.scroll_to)
		# self.search_bar.returnPressed.connect(lambda arg=0: self.scroll_to(arg))

		self.status_bar = QStatusBar()
		status(self.status_bar, self.list_1)

		grid = QGridLayout()
		grid.setSpacing(10)
		grid.addWidget(self.menubar, 0, 0)
		grid.addWidget(self.list_1, 1, 0)
		grid.addWidget(self.list_2, 1, 1)
		grid.addWidget(self.list_3, 1, 2)
		grid.addWidget(self.search_bar, 0, 1)
		grid.addWidget(self.status_bar)

		self.theme()
		self.setLayout(grid)      
		self.setGeometry(300, 300, 600, 300) 
		self.setWindowTitle(f'{split_name(self.curr_file)}')
		self.show()


	def refreshRecents(self):

		try:

		  file_1 = QAction(self.curr_file, self)
		  self.fileRecents.addAction(file_1)
		  file_1.triggered.connect(self.clickedFileAct)

		  if type(self.filenames) is list:

			  if self.filenames[1] != None:
				  file_2 = QAction(self.filenames[1], self)
				  self.fileRecents.addAction(file_2)
				  file_2.triggered.connect(self.clickedFileAct)

			  if self.filenames[2] != None:
				  file_3 = QAction(self.filenames[2], self)
				  self.fileRecents.addAction(file_3)
				  file_3.triggered.connect(self.clickedFileAct)
		
		except:
		  pass

	def clickedFileAct(self):

		file = self.sender().text()
		self.curr_file = file
		self.setWindowTitle(f'{split_name(self.curr_file)}')

		self.list_1.clear()
		self.list_2.clear()
		self.list_3.clear()

		lister(file=self.curr_file ,target=self.list_1, index=0)
		lister(file=self.curr_file ,target=self.list_2, index=1)
		lister(file=self.curr_file ,target=self.list_3, index=2)


	def eventFilter(self, source, event):

		if (event.type() == QEvent.ContextMenu and source is self.list_1):
			menu = QMenu()
			menu.addAction("Delete row")
			if menu.exec_(event.globalPos()):
				item = source.itemAt(event.pos())
				try:
					model = self.list_1.indexFromItem(item) 
					row = model.row()

					self.list_1.takeItem(row)
					self.list_2.takeItem(row)
					self.list_3.takeItem(row)

					status(self.status_bar, self.list_1, f'Deleted row number: {row}.')

				except:
					pass

			return True
		return super(Example, self).eventFilter(source, event)


	def pressed(self): 
		"""Toggles showing the note column and stretches the window for clearer reading of it"""

		self.list_3.setHidden(not self.list_3.isHidden())
	

	def theme(self):
		"""Sets the theme for the window and its widgets"""

		palette = QPalette()
		all_lists = [self.list_1, self.list_2, self.list_3]

		# dark theme
		if  self.toggle_theme.isChecked() == True:

			palette.setColor(QPalette.Window, QColor(0, 0, 0))
			dark = "background-color: rgb(0, 0, 0); color: rgb(255, 255, 255);"

			self.menubar.setStyleSheet(dark) 
			self.addFields.setStyleSheet(dark)
			self.optionMenu.setStyleSheet(dark)
			self.fileMenu.setStyleSheet(dark)
			self.search_bar.setStyleSheet("background-color: rgb(0, 0, 0); color: rgb(255, 255, 255)") # border: 0px; for transparency
			self.status_bar.setStyleSheet(dark)

			style_items(all_lists, dark_theme=True)
		
		# light theme
		elif  self.toggle_theme.isChecked() == False:

			palette.setColor(QPalette.Window, QColor(255, 255, 255))
			light = "background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)"

			self.menubar.setStyleSheet(light) 
			self.addFields.setStyleSheet(light)
			self.optionMenu.setStyleSheet(light)
			self.fileMenu.setStyleSheet(light)
			self.search_bar.setStyleSheet(light)
			self.status_bar.setStyleSheet(light)

			style_items(all_lists, dark_theme=False)

		self.setPalette(palette)

		self.theme_bool = self.toggle_theme.isChecked() # used in the save func


	def scroll_to(self):
		"""Takes input from the search bar and matches with an item, 
		gets index and scrolls to it, more reusults being qued with the num class var""" 

		query = self.search_bar.text()
		search = self.list_1.findItems(query, Qt.MatchContains) 
		status(self.status_bar, self.list_1, f'Found {len(search)} results.')

		self.num+=1
		for i in search:

			try:
				model_index = self.list_1.indexFromItem(search[self.num]) 

			except:
				self.num = 0
				model_index = self.list_1.indexFromItem(search[self.num]) 

			item_index = model_index.row()

			self.list_1.item(item_index).setSelected(True)
			self.list_1.scrollToItem(self.list_1.item(item_index), QAbstractItemView.PositionAtCenter)

			self.list_2.scrollToItem(self.list_2.item(item_index), QAbstractItemView.PositionAtCenter)
			self.list_3.scrollToItem(self.list_3.item(item_index), QAbstractItemView.PositionAtCenter)


	def add_item(self): # add auto-jumping to the next item when finished editing current

		for x in range(3):  
			if x == 0:
				lister(file=self.curr_file ,target=self.list_1, index=x, mode=1)

			elif x == 1:
				lister(file=self.curr_file ,target=self.list_2, index=x, mode=1)

			elif x == 2:
				lister(file=self.curr_file ,target=self.list_3, index=x, mode=1)

		item =  self.list_1.item(self.list_1.count()-1) # use itemChanged to jump to the next column and edit
		self.list_1.editItem(item)
		status(self.status_bar, self.list_1)

	def clear(self):
		"""Clears all item slections for aesthetical purposes, but only single clicks"""

		self.list_1.clearSelection()
		self.list_2.clearSelection()
		self.list_3.clearSelection()


	def fileDialog(self):

		fname = QFileDialog()
		path = fname.getOpenFileName(self, 'Open file', getcwd(), filter='csv (*.csv);') 
		if path[0] == '': # failsafe for canceling the dialog
			return self.curr_file

		self.curr_file = path[0]
		self.setWindowTitle(f'{split_name(self.curr_file)}')

		self.list_1.clear()
		self.list_2.clear()
		self.list_3.clear()

		lister(file=self.curr_file ,target=self.list_1, index=0)
		lister(file=self.curr_file ,target=self.list_2, index=1)
		lister(file=self.curr_file ,target=self.list_3, index=2)


	def save(self): # use itemSelectionChanged to trigger not saved dialog

		list1_items = items_text(self.list_1)
		list2_items = items_text(self.list_2)
		list3_items = items_text(self.list_3)

		total_dicts = []
		for (a, b, c) in zip(list1_items, list2_items, list3_items): # each letter is a column
			dictionary = {'word_1':a, 'word_2':b, 'notes':c}
			total_dicts.append(dictionary)
		
		writer(file=self.curr_file, data=total_dicts)
		status(self.status_bar, self.list_1, ('Saved current changes.'))
		
		try:
			json_template(theme=self.theme_bool, files=[self.curr_file, None, None])
		except:
			json_template() # bug cannot be avoided, even though used setChecked at the beggining

		# avoids stacking and refreshes recent file actions
		actions = self.fileRecents.actions()
		for action in actions:
			self.fileRecents.removeAction(action)

if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())