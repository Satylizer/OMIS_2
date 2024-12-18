from PyQt5 import QtWidgets
from interface.manager_profile import Ui_Form
import sqlite3

class ManagerProfile(QtWidgets.QWidget):
    def __init__(self, parent=None, manager_id=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.manager_id = manager_id
        
        self.load_data()
        self.ui.pushButton.clicked.connect(self.go_back)

    def load_data(self):
        con = sqlite3.connect('handler/users.db')
        cur = con.cursor()
        
        cur.execute("SELECT role, FIO, Tel FROM users WHERE id = ?", (self.manager_id,))
        manager_data = cur.fetchone()
        
        if manager_data:
            self.ui.tableWidget.setRowCount(1)
            for column_index, data in enumerate(manager_data):
                self.ui.tableWidget.setItem(0, column_index, QtWidgets.QTableWidgetItem(str(data)))

        cur.close()
        con.close()

    def go_back(self):
        self.close()