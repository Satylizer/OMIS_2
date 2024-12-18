from PyQt5 import QtWidgets
from interface.client_add import Ui_Form as AddClientUi
from interface.admin_profile import Ui_Form as AdminProfileUi
from interface.manager_profile import Ui_Form as ManagerProfileUi
from interface.client_card import Ui_Form as ClientCardUi


class AddClientView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = AddClientUi()
        self.ui.setupUi(self)

    def get_client_info(self):
        return (
            self.ui.lineEdit.text(),
            self.ui.lineEdit_2.text(),
            self.ui.lineEdit_3.text(),
            self.ui.lineEdit_4.text(),
        )

    def show_error(self, message):
        QtWidgets.QMessageBox.warning(self, 'Ошибка', message)

    def show_success(self, message):
        QtWidgets.QMessageBox.information(self, 'Успех', message)


class AddManagerView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = ManagerProfileUi()
        self.ui.setupUi(self)

    def get_manager_info(self):
        return (
            self.ui.lineEdit.text(),
            self.ui.lineEdit_2.text(),
            self.ui.lineEdit_3.text(),
            self.ui.lineEdit_4.text(),
        )

    def show_error(self, message):
        QtWidgets.QMessageBox.warning(self, 'Ошибка', message)

    def show_success(self, message):
        QtWidgets.QMessageBox.information(self, 'Успех', message)


class AdminProfileView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = AdminProfileUi()
        self.ui.setupUi(self)

    def load_admin_data(self, data):
        self.ui.tableWidget.setRowCount(1)
        for column_index, item in enumerate(data):
            self.ui.tableWidget.setItem(0, column_index, QtWidgets.QTableWidgetItem(str(item)))

    def show_error(self, message):
        QtWidgets.QMessageBox.warning(self, 'Ошибка', message)


class ClientCardView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = ClientCardUi()
        self.ui.setupUi(self)

    def display_client_info(self, client_data):
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems([
            f"ФИО: {client_data['fio']}",
            f"Телефон: {client_data['tel']}",
            f"Email: {client_data['email']}",
            f"Стадия: {client_data['stage']}"
        ])
