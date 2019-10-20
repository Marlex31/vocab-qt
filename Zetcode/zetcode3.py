import sys
from PyQt5.QtWidgets import (QWidget, QListWidgetItem, QListWidget, QGridLayout, QApplication)
from PyQt5.QtGui import QFont



class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):

        def set_font(text):  
                item = QListWidgetItem()
                item.setText(text)
                font = QFont()
                font.setPointSize(17)
                font.setFamily('Helvatica')
                item.setFont(font)
                return item

        list_1 = QListWidget()
        list_1.addItem(set_font('lol'))

        list_2 = QListWidget()
        list_2.addItem(set_font('oof'))

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(list_1, 1, 0)
        grid.addWidget(list_2, 1, 1)
        
        self.setLayout(grid) 
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')    
        self.show()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())