from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QFont #, QIcon
import csv


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


def lister(target, *items):

    for name in items:
        target.addItem(set_font(name)) # add a dict for loop or lambda?


def style(obj):
    obj.setStyleSheet("color: rgb(0, 0, 0);") # fixes a bug that causes the options to use the style sheet of the menubar, rendering them invisible


def reader(filename):

    with open(filename, 'r') as f:
        f_read = csv.reader(f) # DictReader or reader
        next(f_read)

        for line in f_read:
            yield line[0:2]

# for line in reader('french.csv'):
#     print(line)
