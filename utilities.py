from PyQt5.QtWidgets import QListWidgetItem, QMessageBox
from PyQt5.QtGui import QFont, QColor #, QIcon
from PyQt5.QtCore import QRect

import csv
import operator
from os import getcwd
from itertools import chain


def clear_selections(QLists):
	for ls in QLists: ls.clearSelection()

def option_checking(QMenu, custom_var):

	for action in QMenu.actions():

		if action.text() != str(custom_var):
			action.setChecked(False) 	

	# print(self.font_act.actions()[0].isChecked())


def set_font(text, size):  
	"""Customizes the font of the list widget items"""

	item = QListWidgetItem()
	item.setText(text)

	font = QFont()
	font.setPointSize(size)
	font.setFamily('Helvatica')
	item.setFont(font)

	# item.setIcon(QIcon('Images/book.png'))
	item.setFlags(item.flags() | 2)

	return item


def lister(file, target, index=0, mode=0, column=0, size=15, multiple_writing=False):
	"""Adds items to specified column"""

	if mode == 0 and multiple_writing == True:
		for i in target:
			for name in reader(file, index=index): # get path through the dialog
				i.addItem(set_font(name, size))
			index+=1

	elif mode == 0:
		for name in reader(file, index=index):
			target.addItem(set_font(name, size))

	elif mode == 1:
		target.addItem(set_font('', size))

	elif mode == 2:
		for line in sorting(file, column)[index]:
			target.addItem(set_font(line, size))


def reader(filename, index): 
 
	with open(filename, 'r', encoding="utf8") as f:
		f_read = csv.reader(f) 
		next(f_read)

		for line in f_read:
			yield line[index]


def writer(file, data):
	"""Writes the contents of the lists inside csv files"""

	fieldnames = ["col_1","col_2","col_3", "col_4"]
	with open(file, 'w', encoding='utf8', newline='') as w:
		w_write = csv.DictWriter(w, delimiter=',', fieldnames=fieldnames)
		w_write.writeheader()
		for item in data:
			w_write.writerow(item)


def style_items(QLists, dark_theme=False):
	"""Stylizes the QListWidget items for light and dark themes"""

	for ls in QLists:
		items =  [ls.item(i) for i in range(ls.count())]

		for item in items:
			if dark_theme == False:
				item.setForeground(QColor(0, 0, 0))

			else:
				item.setForeground(QColor(240, 240, 240))


def items_text(QLists, multiple_lists=True):
	"""Storing list text"""
	
	if multiple_lists == True:
		text=[]
		for ls in QLists:
			text.append([ls.item(i).text() for i in range(ls.count())])
	else:
		text = [QLists.item(i).text() for i in range(QLists.count())]

	return text
	
def clear_lists(QListWidgets):
	"""Clears QListWidgets of items"""

	for i in QListWidgets: i.clear()


def status(bar, list_widget, message=''):
	"""Sets text displayed by status bar"""

	bar.showMessage(f"Total items: {list_widget.count()}. {message}")


def split_name(string):
       """Splits the filename from the path"""

       if '\\' in string:
       	return string.split('\\')[-1] # support for os.getcwd paths

       return string.split('/')[-1]


def sorting(file, column): 
	"""Sorts alphabetically the items in a column"""
	
	with open(file, 'r', encoding="utf8") as f: 
		f_read = csv.reader(f)

		next(f_read)

		new_list = sorted(f_read, key=operator.itemgetter(column), reverse=False) # alphabetical sorting by a specified column index
		unsorted_list=[]

		unsorted_list.extend(a for a,b,c,d in new_list)
		unsorted_list.extend(b for a,b,c,d in new_list)
		unsorted_list.extend(c for a,b,c,d in new_list)

		start = 0
		end = len(new_list)
		sorted_list = [[], [], []]

		for num in range(3):
			sorted_list[num] = [x for x in unsorted_list[start:end]]

			start = end
			end = end*2

		return sorted_list

# print(sorting('vocabulary.csv', 0))

def error_display():
	
	error_dialog = QMessageBox()
	# print(dir(error_dialog))
	error_dialog.setIcon(QMessageBox.Critical)
	error_dialog.setText('File not found!')
	error_dialog.setInformativeText('A new file will be created.')
	error_dialog.setWindowTitle("Error")
	error_dialog.setStyleSheet("QLabel{min-width: 135px;}")
	error_dialog.exec_()
