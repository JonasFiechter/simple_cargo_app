import sys
from window import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from classes import RunOnDatabase, RunOnPrint
from widget_save import Ui_WidgetSave



class MainWindowMain(Ui_MainWindow, QMainWindow):
    def __init__(self):  
        super().__init__()
        super().setupUi(self)  # import with self as parameter from the mother class Ui_MainWindow
        self.btn_submit.clicked.connect(self.send_command_submit)
        self.btn_submit.clicked.connect(self.show_database)
        self.btn_print.clicked.connect(RunOnPrint.send_to_printer)
        self.btn_search.clicked.connect(lambda: widget_save.show())
        self.btn_delete.clicked.connect(self.delete_from_database_send_id)
        # self.btn_edit.clicked.connect(Ru.edit)
        self.tableWidget.setRowCount(50)
        self.show_database()

        #  Table widget config
        table_row_size = [(0, 40), (1, 160), (2, 100), (3, 200), (4, 110)]
        for item in table_row_size:
            row, size = item  # unpacks itens from the tuples
            self.tableWidget.setColumnWidth(row, size)

    # Main functions
    def send_command_submit(self):     
        self.show_submit_pop_up(self.input_id_container.text(), 
                                self.input_plate_code.text(), 
                                self.input_driver_name.text())
        if self.submit_pop_up_btn:
            submit_instance = RunOnDatabase(
                                            id_container=self.input_id_container.text(),
                                            plate_code=self.input_plate_code.text(),
                                            driver_name=self.input_driver_name.text())
            submit_instance.save_on_database()
    
    def show_database(self):
        data = RunOnDatabase()
        data_list = data.generate_table_iterator()

        for n, list_ in enumerate(data_list):
            for n_2, row in enumerate(list_):
                self.tableWidget.setItem(n, n_2, QtWidgets.QTableWidgetItem(str(row)))
        data.close_cursor_and_connection()

    def show_submit_pop_up(self, id_container, plate_code, driver_name):
        box = QMessageBox()
        box.setFixedWidth(400)
        box.setFixedHeight(600)
        box.setWindowTitle('Confirm submit')
        box.setText('Confirm data:')
        box.setIcon(QMessageBox.Question)
        box.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        box.setInformativeText(f'{id_container}\n{plate_code}\n{driver_name}')
        print(box.buttonClicked.connect(self.submit_pop_up_btn))
        box.exec_()
    
    def submit_pop_up_btn(self, i):
        print(i.text())
        if i.text == 'OK':
            return True
        return False

    def delete_from_database_send_id(self):
        instance_to_delete_from_id = RunOnDatabase()
        id_, ok = QInputDialog.getText(self, 'Delete register', 'enter ID:')
        if ok:
            print(f'sending {id_} to delete')
            instance_to_delete_from_id.delete_from_database(id_=id_)
            window.tableWidget.clear()
            self.show_database()

        instance_to_delete_from_id.close_cursor_and_connection()


class WidgetSave(Ui_WidgetSave, QWidget):
    def __init__(self) -> None:
        super().__init__()
        super().setupUi(self)
        self.btn_search.clicked.connect(self.search)
        self.input_id_container.setText('ID_CONTAINER')
        self.input_plate_code.setText('PLATE_CODE')
        self.input_driver_name.setText('DRIVER_NAME')
        self.input_date.setText('DATE')
    
    def search(self):
        search_instance = RunOnDatabase(data_path=r'c:/anything', # this data must come from the new btn 'select DB' at 'file' menu
                                        id_container=self.input_id_container.text(),
                                        plate_code=self.input_plate_code.text(),
                                        driver_name=self.input_driver_name.text(),
                                        date=self.input_date.text())
        data_search = search_instance.search_on_database()
        
        window.tableWidget.clear()
        
        for n, list_ in enumerate(data_search):
            for n_2, row in enumerate(list_):
                window.tableWidget.setItem(n, n_2, QtWidgets.QTableWidgetItem(str(row)))
        
        self.input_id_container.setText('ID_CONTAINER')
        self.input_plate_code.setText('PLATE_CODE')
        self.input_driver_name.setText('DRIVER_NAME')
        self.input_date.setText('DATE')
        
        search_instance.close_cursor_and_connection()


class PopUpSubmit:
    def __init__(self):
        pass
        

if __name__ == '__main__':
    qt = QApplication(sys.argv)
    window = MainWindowMain()
    window.show()
    pop_up_submit = PopUpSubmit()
    # the variable that keeps the widget class must be inside this loop
    widget_save = WidgetSave()  

    qt.exec_()