import sqlite3
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5 import uic


class Coffee(QMainWindow):
    def __init__(self):
        super(Coffee, self).__init__()
        uic.loadUi('main.ui', self)
        with sqlite3.connect('coffee.sqlite') as db:
            cursor = db.cursor()
            coffee_result = cursor.execute("""SELECT * FROM data""").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'title', 'stepen', 'mol', 'des', 'price', 'volume'])
        self.tableWidget.setRowCount(len(coffee_result))
        for i, row in enumerate(coffee_result):
            for j, item in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    coffee_win = Coffee()
    coffee_win.show()
    sys.exit(app.exec())
