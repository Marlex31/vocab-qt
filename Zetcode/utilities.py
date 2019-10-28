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


def lister(target, index):

    for name in reader('french.csv', index=index): # get path through the dialog
        target.addItem(set_font(name)) 


def style(obj):
    obj.setStyleSheet("color: rgb(0, 0, 0);") # fixes a bug that causes the options to use the style sheet of the menubar, rendering them invisible


def reader(filename, index):

    with open(filename, 'r', encoding="utf8") as f:
        f_read = csv.reader(f) # DictReader or reader
        next(f_read)

        for line in f_read:
            yield line[index]

############################################################################################################################################################################

def writer(filename, *args):

    with open(filename, 'w', encoding='utf8') as w:
        w_write = csv.writer(w, delimiter=',')
        for arg in args:
            w_write.writerow(arg)

# writer("comma_file.csv", ['ici', 'here', '', 'non', 'no', '', 'oui', 'yes', 'はい'])t


def total_items(QList):

    all_items =  [QList.item(i).text() for i in range(QList.count())]
    return all_items



def test_reader():

    import operator
    with open('french.csv', 'r', encoding="utf8") as f:
        f_read = csv.reader(f)
        next(f_read)

        sortedList = sorted(f_read, key=operator.itemgetter(0), reverse=False)
        print(sortedList)

# test_reader()


# from collections import OrderedDict
# with open('french.csv', 'r', encoding="utf8") as f:
#     f_read = csv.DictReader(f) # DictReader or reader

#     for line in f_read:
#         # print(line)

#         dictionary = dict(line)
#         print(dictionary)


# fieldnames = ["word_1","word_2","kanji","date_added"]
# with open('comma_file.csv', 'w', encoding='utf8') as w:
#     w_write = csv.DictWriter(w, delimiter=',', fieldnames=fieldnames)
#     w_write.writeheader()
#     w_write.writerow(dictionary)