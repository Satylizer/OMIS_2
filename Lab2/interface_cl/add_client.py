from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from interface.client_add import Ui_Form
import sqlite3

class ClientAdd(QtWidgets.QWidget):
    client_added = pyqtSignal()

    def __init__(self, manager_id, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.manager_id = manager_id
        self.ui.pushButton.clicked.connect(self.add_client)
        self.ui.pushButton_2.clicked.connect(self.go_back)

    def add_client(self):
        client_fio = self.ui.lineEdit.text()
        client_tel = self.ui.lineEdit_2.text()
        email = self.ui.lineEdit_3.text()
        stage = self.ui.lineEdit_4.text()

        if not client_fio or not client_tel or not email or not stage:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Все поля обязательны!')
            return

        try:
            con = sqlite3.connect('handler/users.db')
            cur = con.cursor()
            cur.execute("INSERT INTO client (client_FIO, email, client_tel, stage, manager_id) VALUES (?, ?, ?, ?, ?)", 
                        (client_fio, email, client_tel, stage, self.manager_id))
            con.commit()
            QtWidgets.QMessageBox.information(self, 'Успех', 'Клиент успешно добавлен!')
            self.client_added.emit()
        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, 'Ошибка базы данных', str(e))
        finally:
            cur.close()
            con.close()

    def go_back(self):
        self.close()