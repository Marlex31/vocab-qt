import sys
from PyQt5.QtWidgets import QWidget, QListWidget, QGridLayout, QApplication

from utilities import set_font, lister, clicked, reader


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()

        
    def initUI(self):

        list_1 = QListWidget()
        lister(list_1, 'test1', 'test2', 'test3')
        list_1.itemSelectionChanged.connect(clicked)
        list_1.sortItems() # 1 for descending

        all_items =  [list_1.item(i).text() for i in range(list_1.count())]
        print(all_items)

        list_2 = QListWidget()
        lister(list_2, 'test1')
        list_2.itemSelectionChanged.connect(clicked)
        list_2.sortItems() 


        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(list_1, 1, 0)
        grid.addWidget(list_2, 1, 1)
     
        self.setLayout(grid)      
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Vocab')    
        self.show()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())