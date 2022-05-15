import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox


class RunOnDatabase:  # contains methods that works with the database
    def __init__(self, data_path=None, id_container=None, plate_code=None, driver_name=None, date=None):
        self.id_container = id_container
        self.plate_code = plate_code
        self.driver_name = driver_name
        self.date = date
        self.path = data_path
        self.connection = sqlite3.connect(r'D:\12 - MY DOCS\DEV\Dev\simple_cargo_register\database.db')
        self.cursor = self.connection.cursor()
    
    def check_for_table(self):  # check for table if it exist, if not creates one     
        self.cursor.execute('CREATE TABLE IF NOT EXISTS register ('
                        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                        'id_container TEXT,'
                        'plate_code TEXT,'
                        'driver_name TEXT,'
                        'date TEXT'
                        ')')
        self.connection.commit()

    def save_on_database(self):  # save received data from main.py and actual date on database
        self.check_for_table()
        date = datetime.now()
        date = date.strftime('%d/%m/%Y - %H:%M')

        self.cursor.execute('INSERT OR IGNORE INTO register (id_container, plate_code, driver_name, date)'
                        'VALUES (?, ?, ?, ?)', 
                        (self.id_container, self.plate_code, self.driver_name, date))
        
        self.connection.commit()
    
    def search_on_database(self):
        self.check_for_table()
        self.cursor.execute('SELECT * FROM register WHERE id_container LIKE ? OR '
                            'plate_code LIKE ? OR '
                            'driver_name LIKE ? OR '
                            'date LIKE ?',
                                        (
                                        f'%{str(self.id_container)}%',
                                        f'%{str(self.plate_code)}%',
                                        f'%{str(self.driver_name)}%',
                                        f'%{str(self.date)}%'
                                        )
                                    )
        search_data_list = []
        
        for row in self.cursor.fetchall():
            search_data_list.append(list(row))

        return search_data_list       

    def generate_table_iterator(self):  # generates a list to be used on main.show_database method
        self.check_for_table()
        data_list = []

        var_for_list = self.cursor.execute("SELECT * FROM register LIMIT 50")
        
        for row in var_for_list:
            data_list.append(list(row))

        return data_list
    
    def close_cursor_and_connection(self):
        self.cursor.close()
        self.connection.close()

    def delete_from_database(self, id_):
        self.check_for_table()
        self.cursor.execute('DELETE FROM register WHERE id LIKE ?', (id_,))
        self.connection.commit()

class RunOnPrint:
    def __init__(self) -> None:
        pass

    def send_to_printer(self):
        print('BTN PRINTER WORKING')


if __name__ == '__main__':
    print('testing...')
    # test_var = RunOnDatabase()
    # test_var.search_on_database(3, '', '', '')

    # print(test_var.generate_table_iterator())