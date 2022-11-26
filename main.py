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
        self.pushButton.clicked.connect(self.run)

    def run(self):
        aecoffee.show()


class AECoffee(QMainWindow):
    def __init__(self):
        super(AECoffee, self).__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.change = dict()
        self.titles = ['id', 'title', 'stepen', 'mol', 'des', 'price', 'volume']
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton.clicked.connect(self.findCoffee)
        self.pushButton_2.clicked.connect(self.save_results)

    def item_changed(self, item):
        self.change[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.change:
            with sqlite3.connect('coffee.sqlite') as db:
                cursor = db.cursor()
                que = "UPDATE data SET\n"
                que += ", ".join([f"{key}='{self.change.get(key)}'"
                                  for key in self.change.keys()])
                que += "WHERE id = ?"
                cursor.execute(que, (int(self.lineEdit.text()),))
                db.commit()
                self.change.clear()

    def findCoffee(self):
        try:
            if int(self.lineEdit.text()) != float(self.lineEdit.text()):
                raise Exception
            with sqlite3.connect('coffee.sqlite') as db:
                cursor = db.cursor()
                coffee_result = cursor.execute("""SELECT * FROM data WHERE id = ?""",
                                               (int(self.lineEdit.text()),)).fetchone()
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setHorizontalHeaderLabels(self.titles)
            self.tableWidget.setRowCount(1)
            for i, item in enumerate(coffee_result):
                self.tableWidget.setItem(0, i, QTableWidgetItem(str(item)))
            self.change.clear()
        except Exception:
            print("Error")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    coffee_win = Coffee()
    aecoffee = AECoffee()
    coffee_win.show()
    sys.exit(app.exec())
