from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QFont #, QIcon

import csv
import operator


def set_font(text):  

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

	if mode == 0:
		for name in reader('french.csv', index=index): # get path through the dialog
			target.addItem(set_font(name)) 

	elif mode == 1:
		target.addItem(set_font(''))



def style(obj):

	obj.setStyleSheet("color: rgb(0, 0, 0);") # fixes a bug that causes the options to use the style sheet of the menubar, rendering them invisible


def reader(filename, index):

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


def total_items(QList):

	all_items =  [QList.item(i).text() for i in range(QList.count())]
	return all_items

############################################################################################################################################################################
 
def test_reader(): 

	with open('french.csv', 'r', encoding="utf8") as f:
		f_read = csv.reader(f)
		next(f_read)

		sortedList = sorted(f_read, key=operator.itemgetter(0), reverse=False) # alphabetical sorting by a specified key
		print(sortedList)

# test_reader()



