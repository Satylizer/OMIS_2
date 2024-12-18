import sys
from controller import AddClientController, AddManagerController, AdminProfileController, ClientCardController, AuthController
from model import UserModel


if __name__ == "__main__":
    auth_controller = AuthController()
    sys.exit(auth_controller.app.exec())
