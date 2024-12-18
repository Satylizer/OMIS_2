from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QStandardItem, QStandardItemModel
import sqlite3
from interface.client_card import Ui_Form
from handler.db_handler import update_client_info

class ClientCard(QtWidgets.QWidget):
    def __init__(self, client_id, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.client_id = client_id
        self.load_data()
        self.ui.pushButton.clicked.connect(self.go_back)
        self.ui.pushButton_2.clicked.connect(self.edit_info)

    def load_data(self):
        if self.client_id is None:
            return

        try:
            con = sqlite3.connect('handler/users.db')
            cur = con.cursor()
            
            cur.execute("SELECT client_FIO, client_tel, email, stage, info FROM client WHERE client_id = ?", (self.client_id,))
            client_data = cur.fetchone()

            if client_data:
                attributes = [
                    f'ФИО: {client_data[0]}',
                    f'Телефон: {client_data[1]}',
                    f'Email: {client_data[2]}',
                    f'Стадия: {client_data[3]}'
                ]

                self.ui.listWidget.clear()
                self.ui.listWidget.addItems(attributes)

                if client_data[4]:
                    self.populate_info(client_data[4])
                else:
                    self.ui.listView.setModel(QStandardItemModel(self.ui.listView))
            else:
                QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Клиент не найден.')
        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, 'Ошибка базы данных', str(e))
            return
        finally:
            cur.close()
            con.close()

    def populate_info(self, info):
        model = QStandardItemModel(self.ui.listView)
        for item_info in info.split(','):
            item = QStandardItem(item_info.strip())
            model.appendRow(item)
        self.ui.listView.setModel(model)

    def edit_info(self):
        current_info = self.get_current_info()
        
        edit_dialog = EditInfoDialog(current_info, self.client_id, self)
        if edit_dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_info = edit_dialog.new_info
            update_client_info(self.client_id, new_info)
            self.populate_info(new_info)

    def get_current_info(self):
        # Получаем текущее значение из QListView
        model = self.ui.listView.model()
        current_info = []
        for row in range(model.rowCount()):
            current_info.append(model.item(row).text())
        return ', '.join(current_info)

    def go_back(self):
        self.close()

class EditInfoDialog(QtWidgets.QDialog):
    def __init__(self, current_info, client_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать информацию")
        self.setGeometry(100, 100, 300, 100)

        self.client_id = client_id
        self.layout = QtWidgets.QVBoxLayout(self)

        self.lineEdit_info = QtWidgets.QLineEdit(self)
        self.lineEdit_info.setText(current_info)
        self.layout.addWidget(self.lineEdit_info)

        self.button_save = QtWidgets.QPushButton("Сохранить", self)
        self.button_save.clicked.connect(self.save_changes)
        self.layout.addWidget(self.button_save)

        self.new_info = None

    def save_changes(self):
        self.new_info = self.lineEdit_info.text()
        if self.new_info:
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Введите корректную информацию.')