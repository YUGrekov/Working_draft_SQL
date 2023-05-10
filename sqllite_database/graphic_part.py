from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from main_base import *
from datetime import datetime


today = datetime.now()
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle('Меню разработки проекта')
        self.setFixedSize(250, 110)
        self.setStyleSheet("background-color: #a0b0a5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        # Create menu bar
        self.create_menu_bars()
        # Сreating an import button exel
        butt_import_exel = QPushButton('Импорт данных КД из Exel', self)
        butt_import_exel.setStyleSheet(("background-color: #a4aba6;"))
        butt_import_exel.resize(220,25)
        butt_import_exel.move(15, 35)      
        butt_import_exel.clicked.connect(self.window_import_exel)  
        # SQL button 
        butt_sql = QPushButton('Редактор базы данных', self)
        butt_sql.setStyleSheet(("background-color: #a4aba6;"))
        butt_sql.resize(220,25)
        butt_sql.move(15, 70)      
        butt_sql.clicked.connect(self.window_create_sql)  
    def create_menu_bars(self):
        menuBar = self.menuBar()
        menuBar.setStyleSheet('background-color: rgb(225, 225, 225);')
        infoMenu  = QMenu('&О программе', self)
        menuBar.addMenu(infoMenu)
    def window_import_exel(self):
        self.w_i_e = Window_import_exel()
        self.w_i_e.show()
    def window_create_sql(self):
        self.w_u_s = Window_update_sql()
        self.w_u_s.show()

class Window_import_exel(QWidget):
    def __init__(self):
        super(Window_import_exel, self).__init__()
        self.setWindowTitle('Заполнение и редактирование данных из КД')
        self.setStyleSheet("background-color: #a0b0a5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(600, 284)

        pathbaseButton = QPushButton('Выбери папку с базой', self)
        pathbaseButton.resize(120,25)
        pathbaseButton.move(10, 10) 
        pathbaseButton.clicked.connect(self.pathfilesql)
        self.pathbasesql = QLabel('Каталог SQL базы', self)
        self.pathbasesql.move(140, 10)
        self.pathbasesql.resize(455,25)
        self.pathbasesql.setStyleSheet('border: 1px solid #6f7370;')

        self.namesql = QLineEdit(self, placeholderText='Заполни название базы SQL', clearButtonEnabled=True)
        self.namesql.setStyleSheet('border: 1px solid #6f7370;')
        self.namesql.move(10, 40)
        self.namesql.resize(230,25)
        self.l_check = QLabel('По умолчанию будет иметь название: default_base', self)
        self.l_check.move(250, 46)

        openDirButton = QPushButton('Выбрать файл КД', self)
        openDirButton.resize(110,25)
        openDirButton.move(10, 80) 
        openDirButton.clicked.connect(self.getFileName)
        self.label1 = QLabel('Путь до файла КД', self)
        self.label1.move(125, 80)
        self.label1.resize(470,25)
        self.label1.setStyleSheet('border: 1px solid #6f7370;')

        readtablbutt = QPushButton('Прочитать шапку таблицы', self)
        readtablbutt.setStyleSheet("background-color: #a087d4;")
        readtablbutt.resize(150,25)
        readtablbutt.move(440, 110) 
        readtablbutt.clicked.connect(self.read_hat_tabl)
        self.select_uso = QComboBox(self)
        self.select_uso.addItem('Выбери таблицу')
        self.select_uso.move(10, 110)
        self.select_uso.resize(150,25)
        self.select_uso.currentIndexChanged.connect(self.click_comboBox)
        self.select_row = QLineEdit(self, placeholderText='Заполни строку заголовка', clearButtonEnabled=True)
        self.select_row.setStyleSheet('border: 1px solid #6f7370;')
        self.select_row.move(180, 110)
        self.select_row.resize(150,25)
        self.select_row.returnPressed.connect(self.read_hat_tabl)

        self.q_type_sig = QComboBox(self)
        self.q_type_sig.move(10, 150)
        self.q_type_sig.resize(150,25)
        self.q_tag = QComboBox(self)
        self.q_tag.move(170, 150)
        self.q_tag.resize(150,25)
        self.q_dict = QComboBox(self)
        self.q_dict.move(330, 150)
        self.q_dict.resize(150,25)
        self.q_schema = QComboBox(self)
        self.q_schema.move(10, 185)
        self.q_schema.resize(150,25)
        self.q_klk = QComboBox(self)
        self.q_klk.move(170, 185)
        self.q_klk.resize(150,25)
        self.q_kont = QComboBox(self)
        self.q_kont.move(330, 185)
        self.q_kont.resize(150,25)
        self.q_basket = QComboBox(self)
        self.q_basket.move(10, 220)
        self.q_basket.resize(150,25)
        self.q_mod = QComboBox(self)
        self.q_mod.move(170, 220)
        self.q_mod.resize(150,25)
        self.q_channel = QComboBox(self)
        self.q_channel.move(330, 220)
        self.q_channel.resize(150,25)

        self.l_type_sig = QLabel('Тип сигнала', self)
        self.l_type_sig.move(55, 144)
        self.l_tag = QLabel('Тэг', self)
        self.l_tag.move(235, 144)
        self.l_dict = QLabel('Наименование', self)
        self.l_dict.move(365, 144)
        self.l_schema = QLabel('Схема', self)
        self.l_schema.move(65, 178)
        self.l_klk = QLabel('Клеммник', self)
        self.l_klk.move(220, 178)
        self.l_kont = QLabel('Контакт', self)
        self.l_kont.move(380, 178)
        self.l_basket = QLabel('Корзина', self)
        self.l_basket.move(60, 213)
        self.l_mod = QLabel('Модуль', self)
        self.l_mod.move(225, 213)
        self.l_channel = QLabel('Канал', self)
        self.l_channel.move(385, 213)
        
        savebasebutt = QPushButton('Сохранить новое УСО', self)
        savebasebutt.setStyleSheet("background-color: #a087d4;")
        savebasebutt.resize(150,25)
        savebasebutt.move(440, 252) 
        savebasebutt.clicked.connect(self.start_fill_base)

        updatebasebutt = QPushButton('Обновить данные УСО', self)
        updatebasebutt.setStyleSheet("background-color: #a087d4;")
        updatebasebutt.resize(150,25)
        updatebasebutt.move(270, 252) 
        updatebasebutt.clicked.connect(self.update_fill_base)

        cleartablbutt = QPushButton('Очистить таблицу', self)
        cleartablbutt.setStyleSheet("background-color: #a087d4;")
        cleartablbutt.resize(150,25)
        cleartablbutt.move(10, 252) 
        cleartablbutt.clicked.connect(self.clear_table)
    def update_fill_base(self):
        if self.сolumn_title_loaded is False: 
            print('Не загружена шапка таблицы!')
            return

        self.name_sql = self.namesql.text().replace(' ', '') 
        if len(self.name_sql) == 0: self.name_sql = 'default_base'

        dict_column = self.hat_list()
        data_uso = self.import_sql.import_table(self.select_uso.currentText(), self.select_row.text(), dict_column)
        self.import_sql.update_for_sql(self.namesql.text(), self.path_sql, data_uso, self.select_uso.currentText())
    def start_fill_base(self):
        if self.сolumn_title_loaded is False: 
            print('Не загружена шапка таблицы!')
            return
        
        self.name_sql = self.namesql.text().replace(' ', '') 
        if len(self.name_sql) == 0: self.name_sql = 'default_base'

        dict_column = self.hat_list()
        data_uso = self.import_sql.import_table(self.select_uso.currentText(), self.select_row.text(), dict_column)
        self.import_sql.import_for_sql(self.name_sql, self.path_sql, data_uso)
    def pathfilesql(self):
        self.path_sql = QFileDialog.getExistingDirectory(caption='Выбери каталог')
        try   : self.pathbasesql.setText(self.path_sql)
        except: print('Каталог SQL базы не выбран')
    def getFileName(self):
        file_exel = QFileDialog.getOpenFileName(caption='Выберите файл')
        self.label1.setText(file_exel[0])
        try:
            self.import_sql = Import_in_SQL(file_exel[0])
            print('Файл КД корректный. Связь установлена')
        except:
            print('Файл КД некорректный. Выбирите другой файл')
            return
        # Read tables exel
        tables = self.import_sql.read_table()
        self.select_uso.clear()    
        self.select_uso.addItems(tables)
    def read_hat_tabl(self):
        try   : int(self.select_row.text())
        except: 
            print('Строка заголовка должна быть заполнена цифрами!')
            return

        try:
            num_row = self.select_row.text()
            text_uso = self.select_uso.currentText()
            # Search hat table
            hat_table = self.import_sql.search_hat_table(text_uso, num_row)
            print(f'Выбран шкаф и строка заголовка таблицы: {text_uso}, {num_row}')
        except:
            print('ОШИБКА. Не выбран шкаф или не указана строка')
            return
        
        try:
            self.q_type_sig.addItems(hat_table)
            self.q_tag.addItems(hat_table)
            self.q_dict.addItems(hat_table)
            self.q_schema.addItems(hat_table)
            self.q_klk.addItems(hat_table)
            self.q_kont.addItems(hat_table)
            self.q_basket.addItems(hat_table)
            self.q_mod.addItems(hat_table)
            self.q_channel.addItems(hat_table)
        except:
            print('Название столбцов должно имееть тип: string')
            return

        # Column title loaded
        self.сolumn_title_loaded = True
    def hat_list(self):
        dict_column = {'type_signal' : self.q_type_sig.currentText(),
                       'uso'         : '',
                       'tag'         : self.q_tag.currentText(),
                       'description' : self.q_dict.currentText(),
                       'scheme'      : self.q_schema.currentText(),
                       'klk'         : self.q_klk.currentText(),
                       'contact'     : self.q_kont.currentText(),
                       'basket'      : self.q_basket.currentText(),
                       'module'      : self.q_mod.currentText(),
                       'channel'     : self.q_channel.currentText()}
        return dict_column  
    def click_comboBox(self):
        self.сolumn_title_loaded = False
    def clear_table(self):
        self.import_sql.clear_tabl()

class Window_update_sql(QWidget):
    def __init__(self):
        super(Window_update_sql, self).__init__()
        self.edit_SQL = Editing_table_SQL()
        self.setWindowTitle('Редактор базы данных')
        self.setStyleSheet("background-color: #a0b0a5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(1600, 900)

        self.TableWidget = QTableWidget(self)
        self.TableWidget.setGeometry(10,180,1580,710)

        pathbaseButton = QPushButton('Signals', self)
        pathbaseButton.resize(120,25)
        pathbaseButton.move(10, 10) 
        pathbaseButton.clicked.connect(self.tabl_signals)

        self.logTextBox = QTextEdit(self)
        self.logTextBox.setGeometry(890,65,700,110)
        self.logTextBox.setReadOnly(True)

        new_addrow_Button = QPushButton('Добавить строку', self)
        new_addrow_Button.resize(120,25)
        new_addrow_Button.move(10, 150) 
        new_addrow_Button.clicked.connect(self.add_row)

        remoterow_Button = QPushButton('Удалить строку', self)
        remoterow_Button.resize(120,25)
        remoterow_Button.move(150, 150) 
        remoterow_Button.clicked.connect(self.delete_row)

        self.namecolumn = QLineEdit(self, placeholderText='Название нового столбца', clearButtonEnabled=True)
        self.namecolumn.setStyleSheet('border: 1px solid #6f7370;')
        self.namecolumn.move(300, 150)
        self.namecolumn.resize(150,25)
        new_addcol_Button = QPushButton('Добавить столбец', self)
        new_addcol_Button.resize(120,25)
        new_addcol_Button.move(455, 150) 
        new_addcol_Button.clicked.connect(self.add_column)

        remoterow_Button = QPushButton('Удалить столбец', self)
        remoterow_Button.resize(120,25)
        remoterow_Button.move(600, 150) 
        remoterow_Button.clicked.connect(self.delete_column)

        cleartab_Button = QPushButton('Очистить таблицу', self)
        cleartab_Button.resize(120,25)
        cleartab_Button.move(745, 150) 
        cleartab_Button.clicked.connect(self.clear_tabl)

        self.layout = QVBoxLayout()
        self.layout.addWidget(pathbaseButton)
        self.layout.addWidget(self.logTextBox)
        self.layout.addWidget(new_addrow_Button)
        self.layout.addWidget(new_addcol_Button)
        self.layout.addWidget(remoterow_Button)
        self.layout.addWidget(cleartab_Button)
        self.layout.addWidget(self.TableWidget)
    # Сompletely clear the table
    def clear_tabl(self):
        rowcount = self.TableWidget.rowCount()

        while rowcount >= 0:
            self.TableWidget.removeRow(rowcount)
            rowcount -= 1

        self.edit_SQL.clear_tabl(self.table_used)
    # Adding new lines
    def add_row(self):  
        column = self.TableWidget.currentColumn()
        rowPos = self.TableWidget.rowCount()
        
        if rowPos == 0: 
            print('Невозможно добавить строки в пустую таблицу')
            return

        self.TableWidget.insertRow(rowPos)

        text_cell = self.TableWidget.item(rowPos - 1, 0).text()
        self.TableWidget.setItem(rowPos, 0, QTableWidgetItem (f'{int(text_cell) + 1}'))

        self.edit_SQL.add_new_row(column, self.table_used, self.hat_name)
        # Logs
        self.logTextBox.insertPlainText(f'{today} - Добавлена новая строка\n')
    # Removing rows
    def delete_row(self):
        row = self.TableWidget.currentRow()
        print(row)

        if row <= 0: 
            print('Невозможно удалить строки из пустой таблицы')
            return
        
        text_cell_id = self.TableWidget.item(int(row), 0).text()
        if row > -1: 
            self.TableWidget.removeRow(row)
            self.TableWidget.selectionModel().clearCurrentIndex()

        self.edit_SQL.delete_row(text_cell_id, self.models_used)
    # Adding new column
    def add_column(self):
        def letters(name):
            if len(name) == 0: name = 'newcolumn'
            return ''.join(filter(str.isalnum, name))
        
        namecolumn = letters(self.namecolumn.text())
        hat_name = self.edit_SQL.column_names(self.table_used)
        if namecolumn in hat_name: 
            print('Дублирующие название колонки!')
            return

        column_count = self.TableWidget.columnCount()
        self.TableWidget.insertColumn(column_count)

        self.edit_SQL.add_new_column(self.table_used, namecolumn)

        hat_name = self.edit_SQL.column_names(self.table_used)
        self.TableWidget.setHorizontalHeaderLabels(hat_name)
    
    
        # Removing rows
    # Removing column
    def delete_column(self):
        column = self.TableWidget.currentColumn()
        self.TableWidget.removeColumn(column)

        hat_name = self.edit_SQL.column_names(self.table_used)
        self.edit_SQL.delete_column(column, hat_name, self.table_used)
    # tabl: Signals
    def tabl_signals(self):
        self.table_used = 'signals'
        self.models_used = Signals
        column, row, self.hat_name, value = self.edit_SQL.editing_sql(self.table_used)
        self.tablew(column, row, self.hat_name, value)
    # Building the selected table
    def tablew(self, column, row, hat_name, value):
        self.TableWidget.setColumnCount(column)
        self.TableWidget.setRowCount(row)
        self.TableWidget.setHorizontalHeaderLabels(hat_name)
        # Разрешить щелчок правой кнопкой мыши для создания меню
        #self.TableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.TableWidget.verticalHeader().setVisible(False)
        # column size
        #for size_column in list_size:
        #   self.TableWidget.setColumnWidth(size_column[0], size_column[1])

        for row_t in range(row):
            for column_t in range(column):
                if value[row_t][column_t] is None:
                    item = QTableWidgetItem('')
                else:
                    item = QTableWidgetItem(str(value[row_t][column_t]))
                # center text
                #item.setTextAlignment(Qt.AlignHCenter)
                # Выравнивание все столбцов по общей ширине
                #self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.TableWidget.setItem(row_t, column_t, item)
        # Выравнивание по столбцов и строк по наибольшей длине
        self.TableWidget.resizeColumnsToContents()
        self.TableWidget.resizeRowsToContents()
        # Events
        self.TableWidget.itemChanged.connect(self.click_position)
    # Cell change on click
    def click_position(self):
        row    = self.TableWidget.currentRow()
        column = self.TableWidget.currentColumn()

        for currentQTableWidgetItem in self.TableWidget.selectedItems():
            text_cell = self.TableWidget.item(currentQTableWidgetItem.row(), column).text()
        
        check_cell = self.TableWidget.item(int(row), 0)
        if check_cell is None: return

        text_cell_id = self.TableWidget.item(int(row), 0).text()

        hat_name = self.edit_SQL.column_names(self.table_used)
        self.edit_SQL.update_row_tabl(column, text_cell, text_cell_id, self.table_used, hat_name)
    # Logging fault
    def logs_msg(self):
        pass



        













# https://www.pythonguis.com/tutorials/pyqt-layouts/
# https://www.programmersought.com/article/50577692774/
# https://linuxhint.com/use-pyqt-qtablewidget/
# https://www.pythontutorial.net/pyqt/pyqt-qtablewidget/
# https://russianblogs.com/article/594578971/




       

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = Window()
    myWin.show()
    sys.exit(app.exec())



# class Window1(QWidget):
#     def __init__(self):
#         super(Window1, self).__init__()
#         self.setWindowTitle('Window1')
#         self.setMinimumWidth(200)
#         self.setMinimumHeight(50)
#         self.button = QPushButton(self)
#         self.button.setText('Ok')
#         self.button.show()


# class Window2(QWidget):
#     def __init__(self):
#         super(Window2, self).__init__()
#         self.setWindowTitle('Window2')


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.setWindowTitle('MainWindow')

#     def show_window_1(self):
#         self.w1 = Window1()
#         self.w1.button.clicked.connect(self.show_window_2)
#         self.w1.button.clicked.connect(self.w1.close)
#         self.w1.show()

#     def show_window_2(self):
#         self.w2 = Window2()
#         self.w2.show()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = MainWindow()
#     w.show()
#     w.show_window_1()
#     sys.exit(app.exec_())