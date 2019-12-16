from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QFont, QColor #, QIcon

import csv
import json
import operator

from os import getcwd
from itertools import chain


def set_font(text):  
	"""Customizes the font of the list widget items"""

	item = QListWidgetItem()
	item.setText(text)

	font = QFont()
	font.setPointSize(12)
	font.setFamily('Helvatica')
	item.setFont(font)

	# item.setIcon(QIcon('book.png'))
	item.setFlags(item.flags() | 2)

	return item


def lister(file, target, index, mode=0, column=0):
	"""Adds items to specified column"""

	if mode == 0:
		for name in reader(file, index=index): # get path through the dialog
			target.addItem(set_font(name)) 

	elif mode == 1:
		target.addItem(set_font(''))

	elif mode == 2:
		for line in sorting(file, column)[index]:
			target.addItem(set_font(line))


def reader(filename, index): 
 
	with open(filename, 'r', encoding="utf8") as f:
		f_read = csv.reader(f) 
		next(f_read)

		for line in f_read:
			yield line[index]


def writer(file, data):
	"""Writes the contents of the lists inside csv files"""

	fieldnames = ["word_1","word_2","notes"]
	with open(file, 'w', encoding='utf8', newline='') as w:
		w_write = csv.DictWriter(w, delimiter=',', fieldnames=fieldnames)
		w_write.writeheader()
		
		for item in data:
			w_write.writerow(item)


def items_text(QList):

	all_items =  [QList.item(i).text() for i in range(QList.count())]
	return all_items


def style_items(QLists, dark_theme=False):
	"""Stylizes the QListWidget items for light and dark themes"""

	for QList in QLists:
		items =  list(QList.item(i) for i in range(QList.count()))

		for item in items:
			if dark_theme == False:
				item.setForeground(QColor(0, 0, 0))
				QList.setStyleSheet("background-color: rgb(255, 255, 255);")

			else:
				item.setForeground(QColor(240, 240, 240))
				QList.setStyleSheet("background-color: rgb(0, 0, 0);")


def status(bar, list_widget, message=''):
	"""Sets text displayed by status bar"""

	bar.showMessage(f"Total items: {list_widget.count()}. {message}")


def split_name(string):
       """Splits the filename from the path"""

       if '\\' in string:
       	return string.split('\\')[-1] # support for os.getcwd paths

       return string.split('/')[-1]


def json_template(theme=False, files=[f"{getcwd()}\\vocabulary.csv", None, None]):
	"""Creates a json config file"""

	try:
		with open('settings.json', 'r') as r:

			settings = json.load(r)

			for i in range(3): 
				if files[0] == settings['recent_files'][0]:
					files = settings['recent_files']
					break

				elif settings['recent_files'][i] not in files and i <= 1:
					files[i+1] = settings['recent_files'][i]

				elif i == 2:
					break

			settings.update({'dark_theme':theme})
			settings.update({'recent_files':files})

	except:
		settings = {'dark_theme':theme, 'recent_files':files}


	with open('settings.json', 'w') as w:
		json.dump(settings, w)

# json_template()


def json_files():
	"""Returns recently opened files and creates a default csv if none found"""
	try: 
		with open('settings.json', 'r', encoding='utf8') as f:
			settings = json.load(f)
			
			if settings['recent_files'][0] != None:
				return settings['recent_files']

	except:
		filename = f'{getcwd()}\\vocabulary.csv'
		with open(filename, 'w') as w:
			writer(file=filename, data=[{'word_1':'lorem', 'word_2':'ipsum', 'notes':'dolor'}])
			return filename

# print(json_files())


def json_theme():
	"""Returns the theme settings saved in the json config file, used on start-up of the program"""

	try:
		with open('settings.json', 'r') as r:
			settings = json.load(r)	
			if settings['dark_theme'] == True:
				return True
			return False

	except:
		return False


def sorting(file, column): 
	"""Sorts alphabetically the items in a column"""
	
	with open(file, 'r', encoding="utf8") as f: 
		f_read = csv.reader(f)

		next(f_read)

		new_list = sorted(f_read, key=operator.itemgetter(column), reverse=False) # alphabetical sorting by a specified column index
		unsorted_list=[]

		unsorted_list.extend(a for a,b,c in new_list)
		unsorted_list.extend(b for a,b,c in new_list)
		unsorted_list.extend(c for a,b,c in new_list)

		start = 0
		end = len(new_list)
		sorted_list = [[], [], []]

		for num in range(3):
			sorted_list[num] = [x for x in unsorted_list[start:end]]

			start = end
			end = end*2

		return sorted_list

# print(sorting('vocabulary.csv', 0))
