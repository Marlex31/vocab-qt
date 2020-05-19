
from PyQt5.QtWidgets import (QWidget, QListWidget, QGridLayout, QApplication, QMenuBar, QAction, qApp, 
							QLineEdit, QAbstractItemView, QStyle, QFileDialog, QMenu, QStatusBar, QMessageBox)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPalette, QColor

import sys
from os import getcwd, remove

from utilities import *


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
		self.show_save = False # bool for showing unsaved changes dialog
		self.temp_file = ".temp.csv"
		self.refresh_file = False # failsafe 1 for itemChanged trigger

		self.list_1 = QListWidget()

		try:
			lister(file=self.curr_file, target=self.list_1, index=0, mode=0)

		except FileNotFoundError:
			print(getcwd())
			error_display()

		self.list_1.clicked.connect(self.neighbour_selection)
		self.list_1.installEventFilter(self)

		self.list_items = self.list_1.count() # failsafe 2 for itemChanged trigger
		self.list_1.itemChanged.connect(self.edit_next_item)
		self.list_1.verticalScrollBar().valueChanged.connect(self.sync_scroll)
		self.list_1.itemClicked.connect(self.edit_bind)

		self.list_2 = QListWidget()
		lister(file=self.curr_file, target=self.list_2, index=1, mode=0)
		self.list_2.clicked.connect(self.neighbour_selection)

		self.list_3 = QListWidget()
		lister(file=self.curr_file, target=self.list_3, index=2, mode=0)
		self.list_3.clicked.connect(self.neighbour_selection)

		self.all_lists = [self.list_1, self.list_2, self.list_3]


		self.menubar = QMenuBar()
		self.menubar.setNativeMenuBar(False)


		self.search_bar = QLineEdit()
		self.search_bar.setPlaceholderText('Search vocab')
		self.search_bar.setClearButtonEnabled(True)
		self.search_bar.setMaxLength(15)
		self.search_bar.returnPressed.connect(self.search_item)



		exit_event = QAction('Exit without saving', self)  
		exit_event.setShortcut('Ctrl+W')
		exit_event.triggered.connect(app.quit)

		showAct = QAction('Show extras', self, checkable=True)  
		showAct.setChecked(False)
		showAct.setShortcut('Ctrl+E')
		showAct.triggered.connect(self.hide_notes)

		addAct = QAction('Fields', self)  
		addAct.setShortcut('Ctrl+N')
		addAct.triggered.connect(self.add_item)

		fileOpen = QAction('Open file', self)
		fileOpen.triggered.connect(self.fileDialog)
		fileOpen.setShortcut('Ctrl+O')

		fileSave = QAction('Save file', self)
		fileSave.triggered.connect(self.save)
		fileSave.triggered.connect(self.refresh_recents)
		fileSave.setShortcut('Ctrl+S')

		self.fileRecents = QMenu('Recent file', self)
		self.refresh_recents()

		
		self.toggle_theme = QAction('Toggle theme', self, checkable=True)
		self.toggle_theme.setChecked(json_theme())
		self.toggle_theme.triggered.connect(self.theme)
		self.toggle_theme.setShortcut('Ctrl+T')

		self.search_act = QAction('Toggle theme', self)
		self.search_act.triggered.connect(self.search_bind)
		self.search_act.setShortcut('Ctrl+F')


		self.col_sort_index = QMenu('Sorting column index', self)
		self.col_sort_index.addAction(QAction(str(0), self))
		self.col_sort_index.addAction(QAction(str(1), self))
		self.col_sort_index.addAction(QAction(str(2), self))
		self.col_sort_index.triggered.connect(self.sort_col_choice)

		self.col_search_index = QMenu('Searching column index', self)
		self.col_search_index.addAction(QAction(str(0), self))
		self.col_search_index.addAction(QAction(str(1), self))
		self.col_search_index.addAction(QAction(str(2), self))
		self.col_search_index.triggered.connect(self.search_col_choice)

		self.sort = QAction('Sort entries', self, checkable=True)
		self.curr_col = 0
		self.search_col = 0
		self.sort.triggered.connect(self.refresh_list)
		self.sort.setShortcut('Ctrl+R')


		self.addFields = self.menubar.addMenu('Add')
		self.addFields.addAction(addAct)

		self.optionMenu = self.menubar.addMenu('Options')
		self.optionMenu.addAction(showAct)
		self.optionMenu.addAction(self.toggle_theme)
		self.optionMenu.addAction(self.search_act)
		self.optionMenu.addMenu(self.col_sort_index)
		self.optionMenu.addMenu(self.col_search_index)
		self.optionMenu.addAction(self.sort)

		self.fileMenu = self.menubar.addMenu('File')
		self.fileMenu.addAction(exit_event)
		self.fileMenu.addAction(fileOpen)
		self.fileMenu.addAction(fileSave)
		self.fileMenu.addMenu(self.fileRecents)


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
		self.setGeometry(*json_window_size())
		self.setWindowTitle(f'{split_name(self.curr_file)}')
		self.show()

		self.list_1.scrollToBottom()
		self.list_2.verticalScrollBar().setHidden(True)
		self.list_3.verticalScrollBar().setHidden(True)
		self.list_3.setHidden(True)


	def edit_bind(self, item):

		print(item.text())
		# self.list_1.editItem(item)
		# print(self.list_1.selectedItems())


	def search_bind(self):
		
		self.search_bar.setFocus()


	def sync_scroll(self):

		scroll_location = self.list_1.verticalScrollBar().value()

		self.list_2.verticalScrollBar().setValue(scroll_location)
		self.list_3.verticalScrollBar().setValue(scroll_location)


	def edit_next_item(self, event):
		"""When an item is added and edited on the first col, starts editing its counterpart on the next col"""

		if self.list_items == self.list_1.count()-2 or self.list_items != self.list_1.count() and self.refresh_file == False:

			item =  self.list_2.item(self.list_2.count()-1)
			self.list_2.editItem(item)

			self.list_items = self.list_1.count()


	def closeEvent(self, event):
		"""Triggered upon program exit, shows a dialog for unsaved changes using a bool"""

		if self.show_save == True:

			reply = QMessageBox.question(self, 'Message',
				"You may have unsaved changes, are you sure you want to quit?", QMessageBox.Yes | 
				QMessageBox.No, QMessageBox.No)

			if reply == QMessageBox.Yes:
				try:
					remove(self.temp_file)
				except:
					pass

				event.accept()
			else:
				event.ignore()       

		else:
			pass


	def sort_col_choice(self, action):
		self.curr_col = int(action.text())

	def search_col_choice(self, action):
		self.search_col = int(action.text())


	def refresh_list(self):
		"""Refreshes the contents of the lists, when sorting is used"""

		self.save(mode=1) # saves a temp copy, with changes, but irreversable sorting introduced

		clear_lists(self.all_lists)

		if self.sort.isChecked() == True:
			mode = 2
		else:
			mode = 0

		try:
			lister(file=self.temp_file, target=self.list_1, index=0, mode=mode, column=self.curr_col)
			lister(file=self.temp_file, target=self.list_2, index=1, mode=mode, column=self.curr_col)
			lister(file=self.temp_file, target=self.list_3, index=2, mode=mode, column=self.curr_col)
		
		except:
			lister(file=self.curr_file, target=self.list_1, index=0, mode=mode, column=self.curr_col)
			lister(file=self.curr_file, target=self.list_2, index=1, mode=mode, column=self.curr_col)
			lister(file=self.curr_file, target=self.list_3, index=2, mode=mode, column=self.curr_col)


	def refresh_recents(self):

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

		self.refresh_file = True

		file = self.sender().text()
		self.curr_file = file
		self.setWindowTitle(f'{split_name(self.curr_file)}')

		clear_lists(self.all_lists)

		lister(file=self.curr_file, target=self.list_1, index=0)
		lister(file=self.curr_file, target=self.list_2, index=1)
		lister(file=self.curr_file, target=self.list_3, index=2)

		status(self.status_bar, self.list_1)
		self.theme()

		self.list_1.scrollToBottom()
		self.list_3.setHidden(True)

		self.refresh_file = False


	def eventFilter(self, source, event):
		"""Item (row) deletion"""

		if (event.type() == QEvent.ContextMenu and source is self.list_1):
			menu = QMenu()
			menu.addAction("Delete row")
			if menu.exec_(event.globalPos()):
				item = source.itemAt(event.pos())
				try:
					model = self.list_1.indexFromItem(item) 
					row = model.row()

					self.show_save = True

					self.list_1.takeItem(row)
					self.list_2.takeItem(row)
					self.list_3.takeItem(row)

					status(self.status_bar, self.list_1, f'Deleted row number: {row+1}.')
					self.clearSelection()

				except:
					pass

			return True
		return super(Example, self).eventFilter(source, event)


	def hide_notes(self): 
		"""Toggles showing the note column and stretches the window for clearer reading of it"""

		self.list_3.setHidden(not self.list_3.isHidden())
	

	def theme(self):
		"""Sets the theme for the window and its widgets"""

		palette = QPalette()

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

			style_items(self.all_lists, dark_theme=True)
		
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

			style_items(self.all_lists, dark_theme=False)

		self.setPalette(palette)

		self.theme_bool = self.toggle_theme.isChecked() # used in the save func


	def search_item(self):
		"""Takes input from the search bar and matches with an item, 
		gets index and scrolls to it, more reusults being qued with the num class var
		""" 

		query = self.search_bar.text()
		search = self.all_lists[self.search_col].findItems(query, Qt.MatchContains)
		status(self.status_bar, self.list_1, f'Found {len(search)} results.')
		

		# testing search in all column

		# search_list =[]
		# for x in range(3):
		# 	search_list.append(self.all_lists[x].findItems(query, Qt.MatchContains))

		# parent_list = []
		# for x in range(3):
		# 	for y in range(len(search_list[x])):
		# 		parent_list.append(self.all_lists[x]) # replace with x

		# import itertools
		# merged = list(itertools.chain.from_iterable(search_list))

		# search_dict = dict(zip(parent_list, merged))
		# print(search_dict)
		# print()
		# print(len(merged))
		# print(len(parent_list))


		self.num+=1
		for i in search:

			try:
				model_index = self.all_lists[self.search_col].indexFromItem(search[self.num])

			except:
				self.num = 0
				model_index = self.all_lists[self.search_col].indexFromItem(search[self.num])

			item_index = model_index.row()

			for ls in self.all_lists:
				ls.item(item_index).setSelected(True)

			self.list_1.scrollToItem(self.list_1.item(item_index), QAbstractItemView.PositionAtCenter)


	def add_item(self):

		self.show_save = True

		for x in range(3):  
			if x == 0:
				lister(file=self.curr_file, target=self.list_1, index=x, mode=1)

			elif x == 1:
				lister(file=self.curr_file,target=self.list_2, index=x, mode=1)

			elif x == 2:
				lister(file=self.curr_file, target=self.list_3, index=x, mode=1)

		item =  self.list_1.item(self.list_1.count()-1)
		self.list_1.editItem(item)
		status(self.status_bar, self.list_1)
		
		self.list_1.scrollToBottom()
		self.list_2.scrollToBottom()
		self.list_3.scrollToBottom()


	def neighbour_selection(self, item):
		"""Selects items on the same row from different columns"""

		for ls in self.all_lists:
			ls.item(item.row()).setSelected(True)
		# print(dir(item))


	def fileDialog(self):

		fname = QFileDialog()
		path = fname.getOpenFileName(self, 'Open file', getcwd(), filter='csv (*.csv);;') 
		if path[0] == '': # failsafe for canceling the dialog
			return self.curr_file

		self.curr_file = path[0]
		self.setWindowTitle(f'{split_name(self.curr_file)}')

		clear_lists(self.all_lists)

		lister(file=self.curr_file ,target=self.list_1, index=0)
		lister(file=self.curr_file ,target=self.list_2, index=1)
		lister(file=self.curr_file ,target=self.list_3, index=2)

		status(self.status_bar, self.list_1)
		self.theme()


	def save(self, mode=0):

		self.show_save = False

		list1_items = items_text(self.list_1)
		list2_items = items_text(self.list_2)
		list3_items = items_text(self.list_3)

		total_dicts = []
		for (a, b, c) in zip(list1_items, list2_items, list3_items): # each letter is a column
			dictionary = {'word_1':a, 'word_2':b, 'notes':c}
			total_dicts.append(dictionary)
		
		if mode == 0:

			writer(file=self.curr_file, data=total_dicts)
			status(self.status_bar, self.list_1, ('Saved current changes.'))
			
			try:
				json_template(theme=self.theme_bool, files=[self.curr_file, None, None], window_size=self.geometry().getRect()) # current size values of the window 

			except:
				json_template() # bug cannot be avoided, even though used setChecked at the beggining


		elif mode == 1:

			self.show_save = True
			writer(file=self.temp_file, data=total_dicts)


		# avoids stacking and refreshes recent file actions
		actions = self.fileRecents.actions()
		for action in actions:
			self.fileRecents.removeAction(action)

if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
