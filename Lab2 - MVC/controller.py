from model import UserModel, ClientModel
from view import AddClientView, AddManagerView, AdminProfileView, ClientCardView
from PyQt5 import QtWidgets
import sys

class AddClientController:
    def __init__(self, manager_id):
        self.view = AddClientView()
        self.manager_id = manager_id
        self.view.ui.pushButton.clicked.connect(self.add_client)

    def add_client(self):
        client_fio, client_tel, email, stage = self.view.get_client_info()
        if not all([client_fio, client_tel, email, stage]):
            self.view.show_error("Все поля обязательны!")
            return

        try:
            ClientModel.add_client(client_fio, email, client_tel, stage, self.manager_id)
            self.view.show_success("Клиент успешно добавлен!")
            self.view.close()
        except Exception as e:
            self.view.show_error(str(e))


class AddManagerController:
    def __init__(self):
        self.view = AddManagerView()
        self.view.ui.pushButton.clicked.connect(self.add_manager)

    def add_manager(self):
        fio, tel, login, password = self.view.get_manager_info()
        if not all([fio, tel, login, password]):
            self.view.show_error("Все поля обязательны!")
            return

        try:
            UserModel.add_manager(fio, tel, login, password)
            self.view.show_success("Менеджер успешно добавлен!")
            self.view.close()
        except Exception as e:
            self.view.show_error(str(e))


class AdminProfileController:
    def __init__(self, admin_id):
        self.view = AdminProfileView()
        self.admin_id = admin_id
        self.load_admin_data()

    def load_admin_data(self):
        try:
            data = UserModel.get_managers()
            self.view.load_admin_data(data)
        except Exception as e:
            self.view.show_error(str(e))


class ClientCardController:
    def __init__(self, client_id):
        self.view = ClientCardView()
        self.client_id = client_id
        self.load_client_data()

    def load_client_data(self):
        try:
            client_info = ClientModel.get_client_info(self.client_id)
            if client_info:
                self.view.display_client_info(client_info)
            else:
                self.view.show_error("Клиент не найден!")
        except Exception as e:
            self.view.show_error(str(e))

class AuthController:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle("Авторизация")
        self.setup_ui()
        self.window.show()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout()
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Имя пользователя")
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.login_button = QtWidgets.QPushButton("Войти")
        self.login_button.clicked.connect(self.authenticate)

        layout.addWidget(QtWidgets.QLabel("Введите ваши данные"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.window.setLayout(layout)

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            role, user_id = UserModel.authenticate(username, password)
            if role and user_id:
                self.open_role_interface(role, user_id)
            else:
                QtWidgets.QMessageBox.warning(self.window, "Ошибка", "Неверные имя пользователя или пароль.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.window, "Ошибка", str(e))

    def open_role_interface(self, role, user_id):
        self.window.close()
        if role == "admin":
            self.admin_interface(user_id)
        elif role == "manager":
            self.manager_interface(user_id)
        else:
            QtWidgets.QMessageBox.warning(None, "Ошибка", "Неизвестная роль пользователя.")

    def admin_interface(self, admin_id):
        admin_controller = AdminProfileController(admin_id)
        admin_controller.view.show()
        sys.exit(self.app.exec())

    def manager_interface(self, manager_id):
        client_controller = AddClientController(manager_id)
        client_controller.view.show()
        sys.exit(self.app.exec())