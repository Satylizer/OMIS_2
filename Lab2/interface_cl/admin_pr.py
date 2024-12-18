from PyQt5 import QtCore, QtWidgets
from interfaces_cl.add_manager import ManagerAdd
from interface.admin_profile import Ui_Form
import sqlite3

class DatabaseThread(QtCore.QThread):
    data_loaded = QtCore.pyqtSignal(list)
    error_occurred = QtCore.pyqtSignal(str)

    def __init__(self, admin_id):
        super().__init__()
        self.admin_id = admin_id

    def run(self):
        try:
            with sqlite3.connect('handler/users.db') as con:
                cur = con.cursor()
                cur.execute("SELECT role, FIO, Tel FROM users WHERE id = ?", (self.admin_id,))
                admin_data = cur.fetchone()
                if admin_data:
                    self.data_loaded.emit(list(admin_data))
                else:
                    self.error_occurred.emit('Данные администратора не найдены.')
        except sqlite3.Error as e:
            self.error_occurred.emit(str(e))

class AdminProfile(QtWidgets.QWidget):
    def __init__(self, admin_id, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.admin_id = admin_id

        self.load_data()

        self.ui.pushButton.clicked.connect(self.go_back)
        self.ui.pushButton_2.clicked.connect(self.get_report)
        self.ui.pushButton_3.clicked.connect(self.add_manager)

    def load_data(self):
        self.thread = DatabaseThread(self.admin_id)
        self.thread.data_loaded.connect(self.display_data)
        self.thread.error_occurred.connect(self.show_error)
        self.thread.start()

    def display_data(self, admin_data):
        self.ui.tableWidget.setRowCount(1)
        for column_index, data in enumerate(admin_data):
            self.ui.tableWidget.setItem(0, column_index, QtWidgets.QTableWidgetItem(str(data)))

    def show_error(self, message):
        QtWidgets.QMessageBox.warning(self, 'Ошибка', message)

    def go_back(self):
        self.close()

    def get_report(self):
        QtWidgets.QMessageBox.information(self, 'Отчет', 'Отчет успешно получен!')

    def add_manager(self):
        self.manager_add_window = ManagerAdd()
        self.manager_add_window.show()