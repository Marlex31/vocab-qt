from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QFont, QColor #, QIcon

import csv
import json
import operator


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


def lister(target, index, mode=0):
	"""Adds items to specified column"""

	if mode == 0:
		for name in reader('french.csv', index=index): # get path through the dialog
			target.addItem(set_font(name)) 

	elif mode == 1:
		target.addItem(set_font(''))



def light_style(obj):
	"""Fixes a bug that causes the options to use the style sheet of the menubar, rendering them invisible"""

	obj.setStyleSheet("color: rgb(0, 0, 0);") 


def reader(filename, index): # add try and except for generating a template with 3 items
 
	with open(filename, 'r', encoding="utf8") as f:
		f_read = csv.reader(f) 
		next(f_read)

		for line in f_read:
			yield line[index]


def writer(data):

	fieldnames = ["word_1","word_2","notes","date_added"]
	with open('french.csv', 'w', encoding='utf8', newline='') as w:
		w_write = csv.DictWriter(w, delimiter=',', fieldnames=fieldnames)
		w_write.writeheader()
		
		for item in data:
			w_write.writerow(item)


def items_text(QList):

	all_items =  [QList.item(i).text() for i in range(QList.count())]
	return all_items

def total_items(QLists, dark_theme=False):

	for QList in QLists:
		items =  list(QList.item(i) for i in range(QList.count()))

		for item in items:
			if dark_theme == False:
				item.setForeground(QColor(0, 0, 0))
				QList.setStyleSheet("background-color: rgb(255, 255, 255);")

			else:
				item.setForeground(QColor(240, 240, 240))
				QList.setStyleSheet("background-color: rgb(0, 0, 0);")

############################################################################################################################################################################
 
def test_reader(): 

	with open('french.csv', 'r', encoding="utf8") as f:
		f_read = csv.reader(f)
		next(f_read)

		sortedList = sorted(f_read, key=operator.itemgetter(0), reverse=False) # alphabetical sorting by a specified key
		print(sortedList)

# test_reader()

def j_template(theme=False):

	try:
		with open('settings.json', 'r') as r:
			settings = json.load(r)

			if settings['first_launch'] == True:
				settings.update({'first_launch':False})

			settings.update({'dark_theme':theme})


	except: 
		settings = {'first_launch':True, 'dark_theme':theme, 'recent_files':[None, None, None]}


	with open('settings.json', 'w') as w:
		json.dump(settings, w)

# j_template()

def j_theme():

	try:
		with open('settings.json', 'r') as r:
			settings = json.load(r)	
			if settings['dark_theme'] == True:
				return True
			return False

	except:
		return False

