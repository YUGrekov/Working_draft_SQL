from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from main_base import *



# Главное окно программы
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle('Меню разработки проекта')
        self.setFixedSize(250, 145)
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
        # Filling tables
        butt_fill_tabl = QPushButton('Заполнение таблиц', self)
        butt_fill_tabl.setStyleSheet(("background-color: #a4aba6;"))
        butt_fill_tabl.resize(220,25)
        butt_fill_tabl.move(15, 70)      
        butt_fill_tabl.clicked.connect(self.window_fill_tables)  
        # SQL button 
        butt_sql = QPushButton('Редактор базы данных', self)
        butt_sql.setStyleSheet(("background-color: #a4aba6;"))
        butt_sql.resize(220,25)
        butt_sql.move(15, 105)      
        butt_sql.clicked.connect(self.window_create_sql)  
    def create_menu_bars(self):
        menuBar = self.menuBar()
        menuBar.setStyleSheet('background-color: rgb(225, 225, 225);')

        settings = QMenu('&Настройки проекта', self)
        settings.setStyleSheet('background-color: rgb(225, 225, 225);')

        menuBar.addMenu(settings)

        path_prj = QAction('Файл конфигурации проекта', self)
        settings.addAction(path_prj)
        path_prj.triggered.connect(self.file_prj)
    def file_prj(self):
        return(QFileDialog.getOpenFileName(caption='Выберите файл конфигурации проекта')[0])
                        
    def window_import_exel(self):
        self.w_i_e = Window_import_exel()
        self.w_i_e.show()
    def window_fill_tables(self):
        self.w_f_t = Window_Filling_tables()
        self.w_f_t.show()
    def window_create_sql(self):
        self.edit_SQL = Editing_table_SQL()
        list_tabl = self.edit_SQL.get_tabl()

        self.w_t_c = Window_tabl_checkbox(list_tabl)
        self.w_t_c.show()

# Окно импорта КЗФКП
class Window_import_exel(QWidget):
    def __init__(self):
        super(Window_import_exel, self).__init__()
        self.setWindowTitle('Заполнение и редактирование данных из КД')
        self.setStyleSheet("background-color: #a0b0a5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(600, 380)

        self.l_path_base = QLabel('Расположение базы данных: ', self)
        self.l_path_base.move(10, 5)
        self.pathbasesql = QLabel('Каталог SQL базы', self)
        self.pathbasesql.move(10, 20)
        self.pathbasesql.resize(580,25)
        self.pathbasesql.setStyleSheet('border: 1px solid #6f7370;')

        self.l_path_kzfkp = QLabel('Расположение КЗФКП: ', self)
        self.l_path_kzfkp.move(10, 50)
        self.label1 = QLabel('Путь до файла КД', self)
        self.label1.move(10, 65)
        self.label1.resize(580,25)
        self.label1.setStyleSheet('border: 1px solid #6f7370;')

        readtablbutt = QPushButton('Прочитать шапку таблицы', self)
        readtablbutt.setStyleSheet("background-color: #a087d4;")
        readtablbutt.resize(150,25)
        readtablbutt.move(440, 105) 
        readtablbutt.clicked.connect(self.read_hat_tabl)
        self.select_uso = QComboBox(self)
        self.select_uso.addItem('Выбери таблицу')
        self.select_uso.move(10, 105)
        self.select_uso.resize(150,25)
        self.select_uso.currentIndexChanged.connect(self.click_comboBox)
        self.select_row = QLineEdit(self, placeholderText='Заполни строку заголовка', clearButtonEnabled=True)
        self.select_row.setStyleSheet('border: 1px solid #6f7370;')
        self.select_row.move(180, 105)
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

        self.logTextBox = QTextEdit(self)
        self.logTextBox.setGeometry(10,285,580,85)
        self.logTextBox.setReadOnly(True)

        # Загружаем пути проекта
        self.path_file_prj()
    def update_fill_base(self):
        if self.сolumn_title_loaded is False: 
            # Logs
            self.logs_msg(f'Не загружена шапка таблицы!', 2)
            return

        dict_column = self.hat_list()
        data_uso = self.import_sql.import_table(self.select_uso.currentText(), self.select_row.text(), dict_column)
        msg = self.import_sql.update_for_sql(data_uso, self.select_uso.currentText())
        self.logs_msg('default', 1, msg, True)
    def start_fill_base(self):
        if self.сolumn_title_loaded is False: 
             # Logs
            self.logs_msg(f'Не загружена шапка таблицы!', 2)
            return

        dict_column = self.hat_list()
        data_uso = self.import_sql.import_table(self.select_uso.currentText(), self.select_row.text(), dict_column)
        msg = self.import_sql.import_for_sql(data_uso, self.select_uso.currentText())
        self.logs_msg('default', 1, msg, True)
    def path_file_prj(self):
        self.pathbasesql.setText(path_to_base)
        self.label1.setText(path_to_exel)

        try:
            self.import_sql = Import_in_SQL(path_to_exel)
            # Logs
            self.logs_msg(f'Соединение с файлом КД установленно', 1)
        except:
            # Logs
            self.logs_msg(f'Соединение с файлом КД не установленно! Выбирите другой файл', 2)
            return
        
        # Read tables exel
        tables = self.import_sql.read_table()
        self.select_uso.clear()    
        self.select_uso.addItems(tables)
    
    def read_hat_tabl(self):
        try   : int(self.select_row.text())
        except: 
            # Logs
            self.logs_msg(f'Строка заголовка должна быть заполнена цифрами!', 2)
            return

        try:
            num_row = self.select_row.text()
            text_uso = self.select_uso.currentText()
            # Search hat table
            hat_table = self.import_sql.search_hat_table(text_uso, num_row)
            # Logs
            self.logs_msg(f'Выбран шкаф и строка заголовка таблицы: {text_uso}, {num_row}', 1)
        except:
            # Logs
            self.logs_msg(f'Не выбран шкаф или не указана строка!', 2)
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
            # Logs
            self.logs_msg(f'Название столбцов должно имееть тип: string', 3)  
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
        msg = self.import_sql.clear_tabl()
        self.logs_msg('default', 1, msg, True)
    # Logging messeges
    def logs_msg(self, logs=None, number_color=1, buffer_msg=None, msg=False):
        today = datetime.now()
        errorFormat   = '<span style="color:red;">{}</span>'
        warningFormat = '<span style="color:yellow;">{}</span>'
        validFormat   = '<span style="color:black;">{}</span>'
        newFormat     = '<span style="color:green;">{}</span>'
        if msg:
            for string_msg, value in buffer_msg.items():
                if   value == 1: 
                    self.logTextBox.append(validFormat.format(string_msg))
                elif value == 2: 
                    self.logTextBox.append(errorFormat.format(string_msg))
                elif value == 3: 
                    self.logTextBox.append(warningFormat.format(string_msg))
                elif value == 0: 
                    self.logTextBox.append(newFormat.format(string_msg))
        else:
            if   number_color == 1: self.logTextBox.append(validFormat.format(f'{today} - {logs}'))
            elif number_color == 2: self.logTextBox.append(errorFormat.format(f'{today} - {logs}'))
            elif number_color == 3: self.logTextBox.append(warningFormat.format(f'{today} - {logs}'))
            elif number_color == 0: self.logTextBox.append(newFormat.format(f'{today} - {logs}'))

# Заполнение таблиц базы данных
class Window_Filling_tables(QWidget):
    def __init__(self):
        super(Window_Filling_tables, self).__init__()
        self.setWindowTitle('Заполнение таблиц базы данных')
        self.setStyleSheet("background-color: #a0b0a5;")
        self.resize(500, 200)

        b_io_basket = QPushButton('HardWare', self)
        b_io_basket.setStyleSheet("background-color: #a087d4;")
        b_io_basket.resize(130,23)
        b_io_basket.move(10, 10) 
        b_io_basket.clicked.connect(self.filling_hardware)
    # HardWare
    def filling_hardware(self):
        hw_table = Filling_HardWare()
        hw_table.import_for_sql()
    # Logging messeges
    def logs_msg(self, logs=None, number_color=1, buffer_msg=None, msg=False):
        today = datetime.now()
        errorFormat   = '<span style="color:red;">{}</span>'
        warningFormat = '<span style="color:yellow;">{}</span>'
        validFormat   = '<span style="color:black;">{}</span>'
        newFormat     = '<span style="color:green;">{}</span>'
        if msg:
            for string_msg, value in buffer_msg.items():
                if   value == 1: 
                    self.logTextBox.append(validFormat.format(string_msg))
                elif value == 2: 
                    self.logTextBox.append(errorFormat.format(string_msg))
                elif value == 3: 
                    self.logTextBox.append(warningFormat.format(string_msg))
                elif value == 0: 
                    self.logTextBox.append(newFormat.format(string_msg))
        else:
            if   number_color == 1: self.logTextBox.append(validFormat.format(f'{today} - {logs}'))
            elif number_color == 2: self.logTextBox.append(errorFormat.format(f'{today} - {logs}'))
            elif number_color == 3: self.logTextBox.append(warningFormat.format(f'{today} - {logs}'))
            elif number_color == 0: self.logTextBox.append(newFormat.format(f'{today} - {logs}'))

# Просмотр и редактирование таблиц
class Window_tabl_checkbox(QWidget):
    def __init__(self, list_tabl):
        super(Window_tabl_checkbox, self).__init__()
        self.setWindowTitle('Список таблиц')
        self.setStyleSheet("background-color: #a0b0a5;")
        self.resize(260, 80)
        #self.move(200,40)
        
        clickButton = QPushButton('Подключиться к таблице', self)
        clickButton.resize(80,40)
        clickButton.clicked.connect(self.choose_tabl)

        self.combo = QComboBox()
        self.combo.setFont(QFont('Arial', 10))

        for tabl in list_tabl:
            self.combo.addItem(str(tabl))

        layout = QVBoxLayout()
        layout.addWidget(self.combo)
        layout.addWidget(clickButton)

        self.setLayout(layout)
    # Choose table
    def choose_tabl(self):
        name_table = self.combo.currentText()
        self.ch_tabl = Window_update_sql(name_table)
        self.ch_tabl.show()
class Window_update_sql(QWidget):
    def __init__(self, table_used):
        super(Window_update_sql, self).__init__()
        self.setWindowTitle('Редактор базы данных')
        self.setStyleSheet("background-color: #a0b0a5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(1600, 870)

        self.TableWidget = QTableWidget(self)
        self.TableWidget.setGeometry(10,50,1580,710)

        self.logTextBox = QTextEdit(self)
        self.logTextBox.setGeometry(10,759,1580,100)
        self.logTextBox.setReadOnly(True)

        self.table_used = table_used
        self.edit_SQL = Editing_table_SQL()
        column, row, self.hat_name, value = self.edit_SQL.editing_sql(self.table_used)
        self.tablew(column, row, self.hat_name, value)

        new_addrow_Button = QPushButton('Добавить строку', self)
        new_addrow_Button.resize(120,25)
        new_addrow_Button.move(10, 10) 
        new_addrow_Button.clicked.connect(self.add_row)

        remoterow_Button = QPushButton('Удалить строку', self)
        remoterow_Button.resize(120,25)
        remoterow_Button.move(150, 10) 
        remoterow_Button.clicked.connect(self.delete_row)

        self.namecolumn = QLineEdit(self, placeholderText='Название нового столбца', clearButtonEnabled=True)
        self.namecolumn.setStyleSheet('border: 1px solid #6f7370;')
        self.namecolumn.move(300, 10)
        self.namecolumn.resize(150,25)
        new_addcol_Button = QPushButton('Добавить столбец', self)
        new_addcol_Button.resize(120,25)
        new_addcol_Button.move(455, 10) 
        new_addcol_Button.clicked.connect(self.add_column)

        remoterow_Button = QPushButton('Удалить столбец', self)
        remoterow_Button.resize(120,25)
        remoterow_Button.move(600, 10) 
        remoterow_Button.clicked.connect(self.delete_column)

        cleartab_Button = QPushButton('Очистить таблицу', self)
        cleartab_Button.resize(120,25)
        cleartab_Button.move(745, 10) 
        cleartab_Button.clicked.connect(self.clear_tabl)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.logTextBox)
        self.layout.addWidget(new_addrow_Button)
        self.layout.addWidget(new_addcol_Button)
        self.layout.addWidget(remoterow_Button)
        self.layout.addWidget(cleartab_Button)
        self.layout.addWidget(self.TableWidget)
    # Сompletely clear the table
    def clear_tabl(self):
        rowcount = self.TableWidget.rowCount()

        if rowcount == 0: 
            self.logs_msg(f'Таблица: {self.table_used} пустая', 3)
            return

        while rowcount >= 0:
            self.TableWidget.removeRow(rowcount)
            rowcount -= 1

        self.edit_SQL.clear_tabl(self.table_used)
         # Logs
        self.logs_msg(f'Таблица: {self.table_used} полностью очищена!', 3)
    # Adding new lines
    def add_row(self):  
        rowPos = self.TableWidget.rowCount()
        
        if rowPos == 0: 
            text_cell = 0
        else:
            text_cell = self.TableWidget.item(rowPos - 1, 0).text()

        self.TableWidget.insertRow(rowPos)
        self.TableWidget.setItem(rowPos, 0, QTableWidgetItem (f'{int(text_cell) + 1}'))

        self.edit_SQL.add_new_row(self.table_used)
        # Logs
        self.logs_msg('В конец таблицы добавлена новая строка', 1)
    # Removing rows
    def delete_row(self):
        row = self.TableWidget.currentRow()
        if row <= 0: 
            self.logs_msg('Невозможно удалить строки из пустой таблицы', 2)
            return
        
        text_cell_id = self.TableWidget.item(int(row), 0).text()
        if row > -1: 
            self.TableWidget.removeRow(row)
            self.TableWidget.selectionModel().clearCurrentIndex()

        self.edit_SQL.delete_row(text_cell_id, self.table_used)
        # Logs
        self.logs_msg(f'Из таблицы: {self.table_used} удалена строка id={text_cell_id}', 3)
    # Adding new column
    def add_column(self):
        def letters(name):
            if len(name) == 0: name = 'newcolumn'
            return ''.join(filter(str.isalnum, name))
        
        namecolumn = letters(self.namecolumn.text())
        hat_name = self.edit_SQL.column_names(self.table_used)
        if namecolumn in hat_name: 
            self.logs_msg('Дублирующие название столбца!', 2)
            return

        column_count = self.TableWidget.columnCount()
        self.TableWidget.insertColumn(column_count)

        self.edit_SQL.add_new_column(self.table_used, namecolumn)

        hat_name = self.edit_SQL.column_names(self.table_used)
        self.TableWidget.setHorizontalHeaderLabels(hat_name)
        # Logs
        self.logs_msg(f'В таблицу: {self.table_used} добавлен новый столбец: {namecolumn}', 1)
    # Removing column
    def delete_column(self):
        if self.table_used == 'signals': 
            self.logs_msg(f'Из таблицы: signals нельзя удалять столбцы!', 3)
            return
        column = self.TableWidget.currentColumn()
        self.TableWidget.removeColumn(column)

        hat_name = self.edit_SQL.column_names(self.table_used)
        self.edit_SQL.delete_column(column, hat_name, self.table_used)
        self.logs_msg(f'Из таблицы: {self.table_used} удален столбец', 3)
    # Building the selected table
    def tablew(self, column, row, hat_name, value):
        # Logs
        self.logs_msg(f'Запущен редактор базы данных. Таблица: {self.table_used}', 1)
        # TableW
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

                if column_t == 0: item.setFlags(Qt.ItemIsEnabled)
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

        if row == 0 and column == 0: return

        for currentQTableWidgetItem in self.TableWidget.selectedItems():
            text_cell = self.TableWidget.item(currentQTableWidgetItem.row(), column).text()
        # На случай, когда нет изменения в ячейке
        try:
            text_cell
        except:
            return
        
        check_cell = self.TableWidget.item(int(row), 0)
        if check_cell is None: return

        text_cell_id = self.TableWidget.item(int(row), 0).text()

        hat_name = self.edit_SQL.column_names(self.table_used)
        self.edit_SQL.update_row_tabl(column, text_cell, text_cell_id, self.table_used, hat_name)
    # Logging messeges
    def logs_msg(self, logs=None, number_color=1, buffer_msg=None, msg=False):
        today = datetime.now()
        errorFormat   = '<span style="color:red;">{}</span>'
        warningFormat = '<span style="color:yellow;">{}</span>'
        validFormat   = '<span style="color:black;">{}</span>'
        newFormat     = '<span style="color:green;">{}</span>'
        if msg:
            for string_msg, value in buffer_msg.items():
                if   value == 1: 
                    self.logTextBox.append(validFormat.format(string_msg))
                elif value == 2: 
                    self.logTextBox.append(errorFormat.format(string_msg))
                elif value == 3: 
                    self.logTextBox.append(warningFormat.format(string_msg))
                elif value == 0: 
                    self.logTextBox.append(newFormat.format(string_msg))
        else:
            if   number_color == 1: self.logTextBox.append(validFormat.format(f'{today} - {logs}'))
            elif number_color == 2: self.logTextBox.append(errorFormat.format(f'{today} - {logs}'))
            elif number_color == 3: self.logTextBox.append(warningFormat.format(f'{today} - {logs}'))
            elif number_color == 0: self.logTextBox.append(newFormat.format(f'{today} - {logs}'))
 










if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = Window()
    myWin.show()
    sys.exit(app.exec())