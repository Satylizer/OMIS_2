import sqlite3

class Database:
    @staticmethod
    def connect():
        return sqlite3.connect('handler/users.db')


class UserModel:
    @staticmethod
    def authenticate(username, password):
        try:
            with Database.connect() as con:
                cur = con.cursor()
                cur.execute('SELECT role, id, password FROM users WHERE name = ?', (username,))
                value = cur.fetchone()
                if value and value[2] == password:
                    return value[0], value[1]  # role, user_id
                return None, None
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    def add_manager(fio, tel, login, password):
        try:
            with Database.connect() as con:
                cur = con.cursor()
                cur.execute("""
                    INSERT INTO users (FIO, Tel, name, password, role) 
                    VALUES (?, ?, ?, ?, 'manager')
                """, (fio, tel, login, password))
                con.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")


class ClientModel:
    @staticmethod
    def get_clients():
        try:
            with Database.connect() as con:
                cur = con.cursor()
                cur.execute("""
                    SELECT u.id AS manager_id, u.FIO AS manager_FIO, 
                           c.client_id, c.client_FIO, c.stage 
                    FROM users u
                    LEFT JOIN client c ON u.id = c.manager_id
                    WHERE u.role = 'manager'
                """)
                return cur.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    def add_client(client_fio, email, client_tel, stage, manager_id):
        try:
            with Database.connect() as con:
                cur = con.cursor()
                cur.execute("""
                    INSERT INTO client (client_FIO, email, client_tel, stage, manager_id) 
                    VALUES (?, ?, ?, ?, ?)
                """, (client_fio, email, client_tel, stage, manager_id))
                con.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    def get_client_info(client_id):
        try:
            with Database.connect() as con:
                cur = con.cursor()
                cur.execute("SELECT client_FIO, client_tel, email, stage FROM client WHERE client_id = ?", (client_id,))
                value = cur.fetchone()
                if value:
                    return {
                        "fio": value[0],
                        "tel": value[1],
                        "email": value[2],
                        "stage": value[3],
                    }
                return None
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
