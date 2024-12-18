from PyQt5 import QtWidgets
from interface.manager_add import Ui_Form
import sqlite3

class ManagerAdd(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.add_manager)
        self.ui.pushButton_2.clicked.connect(self.go_back)

    def add_manager(self):
        fio = self.ui.lineEdit.text()
        tel = self.ui.lineEdit_2.text()
        login = self.ui.lineEdit_3.text()
        password = self.ui.lineEdit_4.text()

        if not fio or not tel or not login or not password:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Все поля обязательны!')
            return

        try:
            with sqlite3.connect('handler/users.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (name, password, role, FIO, Tel) VALUES (?, ?, ?, ?, ?)", 
                            (login, password, 'manager', fio, tel))
                con.commit()
                QtWidgets.QMessageBox.information(self, 'Успех', 'Менеджер успешно добавлен!')
                self.close()
        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, 'Ошибка базы данных', str(e))

    def go_back(self):
        self.close()