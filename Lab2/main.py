import sys
from PyQt5 import QtWidgets
from interface import authorization as auth_ui
from interface.all_table import Ui_Form as AllTableUi
from handler.db_handler import login, get_clients
from interfaces_cl.client_card import ClientCard
from interfaces_cl.manager_pr import ManagerProfile
from interfaces_cl.admin_pr import AdminProfile
from interfaces_cl.add_client import ClientAdd

class AuthInterface(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = auth_ui.Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.auth)
        self.user_role = None
        self.user_id = None

    def auth(self):
        name = self.ui.lineEdit.text()
        passw = self.ui.lineEdit_2.text()
        
        role, user_id = login(name, passw)

        if role and user_id:
            self.user_role = role
            self.user_id = user_id
            self.open_all_table_interface()
        else:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Не удалось авторизоваться. Проверьте введенные данные.')

    def open_all_table_interface(self):
        self.all_table_interface = AllTableInterface(self.user_role, self.user_id)
        self.all_table_interface.show()
        self.close()

class AllTableInterface(QtWidgets.QWidget):
    def __init__(self, user_role, user_id):
        super().__init__()
        self.ui = AllTableUi()
        self.ui.setupUi(self)

        self.user_role = user_role
        self.user_id = user_id

        self.load_data()

        self.ui.pushButton.clicked.connect(self.open_profile)
        self.ui.pushButton_2.clicked.connect(self.add_client)
        self.ui.pushButton_3.clicked.connect(self.open_client_card)

    def load_data(self):
        clients_data = get_clients()

        self.ui.tableWidget.setRowCount(len(clients_data))
        self.ui.tableWidget.setColumnCount(5)

        for row_index, row_data in enumerate(clients_data):
            manager_id, manager_fio, client_id, client_fio, stage = row_data
            self.ui.tableWidget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(manager_id)))
            self.ui.tableWidget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(manager_fio))
            self.ui.tableWidget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(client_id)))
            self.ui.tableWidget.setItem(row_index, 3, QtWidgets.QTableWidgetItem(client_fio))
            self.ui.tableWidget.setItem(row_index, 4, QtWidgets.QTableWidgetItem(stage))

    def open_profile(self):
        if self.user_role == 'admin':
            self.admin_profile = AdminProfile(self.user_id)
            self.admin_profile.show()
        elif self.user_role == 'manager':
            self.manager_profile = ManagerProfile(parent=None, manager_id=self.user_id)
            self.manager_profile.show()
        else:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Неизвестная роль пользователя.')

    def add_client(self):
        self.client_add_window = ClientAdd(self.user_id)
        self.client_add_window.client_added.connect(self.load_data)
        self.client_add_window.show()

    def open_client_card(self):
        client_id, ok = QtWidgets.QInputDialog.getInt(self, 'Ввод ID клиента', 'Введите ID клиента:')
        if ok and client_id > 0:
            try:
                self.client_card = ClientCard(client_id)
                self.client_card.show()
            except TypeError as e:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', f'Неверный тип данных: {str(e)}')
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', str(e))
        else:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Необходимо ввести корректный ID клиента.')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mywin = AuthInterface()
    mywin.show()
    sys.exit(app.exec())