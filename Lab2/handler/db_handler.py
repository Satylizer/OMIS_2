import sqlite3
from PyQt5 import QtWidgets

def login(name, passw):
    con = sqlite3.connect('handler/users.db')
    cur = con.cursor()

    try:
        cur.execute('SELECT role, id, password FROM users WHERE name = ?', (name,))
        value = cur.fetchone()

        if value:
            role, user_id, password_value = value

            if password_value == passw:
                return role, user_id
            else:
                return None, None
        else:
            return None, None
    except sqlite3.Error as e:
        QtWidgets.QMessageBox.warning(None, 'Ошибка базы данных', str(e))
        return None, None
    finally:
        cur.close()
        con.close()

def get_clients():
    con = sqlite3.connect('handler/users.db')
    cur = con.cursor()

    try:
        cur.execute("""
            SELECT u.id AS manager_id, u.FIO AS manager_FIO, 
                   c.client_id, c.client_FIO, c.stage 
            FROM users u
            LEFT JOIN client c ON u.id = c.manager_id
            WHERE u.role = 'manager'
        """)
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {str(e)}")
        return []
    finally:
        cur.close()
        con.close()
        
def get_client_info(client_id):
    con = sqlite3.connect('handler/users.db')
    cur = con.cursor()

    try:
        cur.execute("SELECT info FROM client WHERE client_id = ?", (client_id,))
        value = cur.fetchone()
        if value:
            return value[0]
        else:
            return None
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {str(e)}")
        return None
    finally:
        cur.close()
        con.close()
        
def update_client_info(client_id, new_info):
    try:
        with sqlite3.connect('handler/users.db') as con:
            cur = con.cursor()
            cur.execute("UPDATE client SET info = ? WHERE client_id = ?", (new_info, client_id))
            con.commit()
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {str(e)}")