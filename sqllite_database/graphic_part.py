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
        self.setStyleSheet("background-color: #e1e5e5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        # Create menu bar
        self.create_menu_bars()
        # Сreating an import button exel
        butt_import_exel = QPushButton('Импорт данных КД из Exel', self)
        butt_import_exel.setStyleSheet(("background: #c6c3b5; border-radius: 4px; border: 1px solid"))
        butt_import_exel.setToolTip('Импорт сигналов из КЗФКП в базу SQL "signals"')
        butt_import_exel.resize(220,25)
        butt_import_exel.move(15, 35)      
        butt_import_exel.clicked.connect(self.window_import_exel)  
        # Filling tables
        butt_fill_tabl = QPushButton('Заполнение таблиц', self)
        butt_fill_tabl.setStyleSheet(("background: #c6c3b5; border-radius: 4px; border: 1px solid"))
        butt_fill_tabl.setToolTip('Заполнение или очистка таблиц базы данных')
        butt_fill_tabl.resize(220,25)
        butt_fill_tabl.move(15, 70)      
        butt_fill_tabl.clicked.connect(self.window_fill_tables)  
        # SQL button 
        butt_sql = QPushButton('Редактор базы данных', self)
        butt_sql.setStyleSheet(("background: #c6c3b5; border-radius: 4px; border: 1px solid"))
        butt_sql.setToolTip('Редактор таблиц базы данных')
        butt_sql.resize(220,25)
        butt_sql.move(15, 105)      
        butt_sql.clicked.connect(self.window_create_sql)  
    def create_menu_bars(self):
        menuBar = self.menuBar()
        menuBar.setStyleSheet('background-color: #c7c9c9;')

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
        self.setStyleSheet("background-color: #e1e5e5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(600, 380)

        self.l_path_base = QLabel('Расположение базы данных: ', self)
        self.l_path_base.move(10, 5)
        self.pathbasesql = QLabel('Каталог SQL базы', self)
        self.pathbasesql.move(10, 20)
        self.pathbasesql.resize(580,25)
        self.pathbasesql.setStyleSheet('border: 1px solid #6f7370; border-radius: 4px; border: 1px solid')

        self.l_path_kzfkp = QLabel('Расположение КЗФКП: ', self)
        self.l_path_kzfkp.move(10, 50)
        self.label1 = QLabel('Путь до файла КД', self)
        self.label1.move(10, 65)
        self.label1.resize(580,25)
        self.label1.setStyleSheet('border: 1px solid #6f7370; border-radius: 4px; border: 1px solid')

        readtablbutt = QPushButton('Прочитать шапку таблицы', self)
        readtablbutt.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        readtablbutt.resize(150,25)
        readtablbutt.move(440, 105) 
        readtablbutt.clicked.connect(self.read_hat_tabl)
        self.select_uso = QComboBox(self)
        self.select_uso.addItem('Выбери таблицу')
        self.select_uso.setStyleSheet('border-radius: 4px; border: 1px solid')
        self.select_uso.move(10, 105)
        self.select_uso.resize(150,25)
        self.select_uso.currentIndexChanged.connect(self.click_comboBox)
        self.select_row = QLineEdit(self, placeholderText='Заполни строку заголовка', clearButtonEnabled=True)
        self.select_row.setStyleSheet('border: 1px solid #6f7370; border-radius: 4px; border: 1px solid')
        self.select_row.move(180, 105)
        self.select_row.resize(150,25)
        self.select_row.returnPressed.connect(self.read_hat_tabl)

        self.q_type_sig = QComboBox(self)
        self.q_type_sig.move(10, 150)
        self.q_type_sig.resize(150,25)
        self.q_type_sig.setStyleSheet('border-radius: 4px; border: 1px solid')
        self.q_tag = QComboBox(self)
        self.q_tag.move(170, 150)
        self.q_tag.resize(150,25)
        self.q_tag.setStyleSheet('border-radius: 4px; border: 1px solid')
        self.q_dict = QComboBox(self)
        self.q_dict.move(330, 150)
        self.q_dict.resize(150,25)
        self.q_dict.setStyleSheet('border-radius: 4px; border: 1px solid')
        self.q_schema = QComboBox(self)
        self.q_schema.move(10, 185)
        self.q_schema.resize(150,25)
        self.q_schema.setStyleSheet('border-radius: 4px; border: 1px solid')
        self.q_klk = QComboBox(self)
        self.q_klk.move(170, 185)
        self.q_klk.resize(150,25)
        self.q_klk.setStyleSheet('border-radius: 4px; border: 1px solid')
        self.q_kont = QComboBox(self)
        self.q_kont.move(330, 185)
        self.q_kont.resize(150,25)
        self.q_kont.setStyleSheet('border-radius: 4px; border: 1px solid')
        self.q_basket = QComboBox(self)
        self.q_basket.move(10, 220)
        self.q_basket.resize(150,25)
        self.q_basket.setStyleSheet('border-radius: 4px; border: 1px solid')
        self.q_mod = QComboBox(self)
        self.q_mod.move(170, 220)
        self.q_mod.resize(150,25)
        self.q_mod.setStyleSheet('border-radius: 4px; border: 1px solid')
        self.q_channel = QComboBox(self)
        self.q_channel.move(330, 220)
        self.q_channel.resize(150,25)
        self.q_channel.setStyleSheet('border-radius: 4px; border: 1px solid')

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
        savebasebutt.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        savebasebutt.setToolTip('''Добавляются новые сигналы в конец таблицы''')
        savebasebutt.resize(150,25)
        savebasebutt.move(440, 252) 
        savebasebutt.clicked.connect(self.start_fill_base)

        updatebasebutt = QPushButton('Обновить данные УСО', self)
        updatebasebutt.setStyleSheet("background: #b2b4eb; border-radius: 4px; border: 1px solid")
        updatebasebutt.setToolTip('''Сигнал проверяется по шкафу, модулю, корзине и каналу. Если такой отсутствует,\nто добавляется новый в конец таблицы, иначе данные которые различаются обновляются''')
        updatebasebutt.resize(150,25)
        updatebasebutt.move(270, 252) 
        updatebasebutt.clicked.connect(self.update_fill_base)

        cleartablbutt = QPushButton('Очистить таблицу signals', self)
        cleartablbutt.setStyleSheet("background: #aeb37b; border-radius: 4px; border: 1px solid")
        cleartablbutt.resize(170,25)
        cleartablbutt.move(10, 252) 
        cleartablbutt.clicked.connect(self.clear_table)

        self.logTextBox = QTextEdit(self)
        self.logTextBox.setStyleSheet("border-radius: 4px; border: 1px solid")
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
        msg = self.import_sql.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = self.import_sql.update_for_sql(data_uso, self.select_uso.currentText())
        self.logs_msg('default', 1, msg, True)
    def start_fill_base(self):
        if self.сolumn_title_loaded is False: 
             # Logs
            self.logs_msg(f'Не загружена шапка таблицы!', 2)
            return

        dict_column = self.hat_list()
        data_uso = self.import_sql.import_table(self.select_uso.currentText(), self.select_row.text(), dict_column)
        msg = self.import_sql.column_check()
        self.logs_msg('default', 1, msg, True)
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
                       'schema'      : self.q_schema.currentText(),
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
        warningFormat = '<span style="color:#9ea108;">{}</span>'
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
        self.setStyleSheet("background-color: #e1e5e5;")
        self.resize(900, 295)
        self.dop_function = general_functions()

        self.edit_SQL = Editing_table_SQL()
        self.list_tabl = self.edit_SQL.get_tabl()
        # Size default
        b_width_one = 8
        b_width_two = 92
        l_height    = 3
        b_height    = 20

        # HardWare
        self.kk_is_true = False
        l_hw = QLabel('HardWare:', self)
        l_hw.move(b_width_one + 2, l_height)
        b_io_basket = QPushButton('Заполнить', self)
        b_io_basket.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        b_io_basket.setToolTip("Таблицу HardWare")
        b_io_basket.resize(80,23)
        b_io_basket.move(b_width_one, b_height) 
        b_io_basket.clicked.connect(self.filling_hardware)
        b_clear_tabl = QPushButton('Очистить', self)
        b_clear_tabl.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
        b_clear_tabl.setToolTip("Очистить таблицу HardWare")
        b_clear_tabl.resize(80,23)
        b_clear_tabl.move(b_width_two, b_height) 
        b_clear_tabl.clicked.connect(self.clear_tabl)
        c_kk_is_true = QCheckBox('Есть KK?', self)
        c_kk_is_true.setToolTip("Добавить в диагостику проекта коммуникационные контроллеры")
        c_kk_is_true.move(70, 2) 
        c_kk_is_true.stateChanged.connect(self.kk_check)
        # USO
        l_uso = QLabel('USO:', self)
        l_uso.move(b_width_one + 182, l_height)
        b_uso_basket = QPushButton('Заполнить', self)
        b_uso_basket.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        b_uso_basket.setToolTip("Должны быть заполнены таблицы AI и DI")
        b_uso_basket.resize(80,23)
        b_uso_basket.move(b_width_one + 180, b_height) 
        b_uso_basket.clicked.connect(self.filling_uso)
        b_clear_uso = QPushButton('Очистить', self)
        b_clear_uso.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
        b_clear_uso.setToolTip("Очистить таблицу USO")
        b_clear_uso.resize(80,23)
        b_clear_uso.move(b_width_two + 180, b_height) 
        b_clear_uso.clicked.connect(self.clear_uso_tabl)
        # AI
        l_ai = QLabel('AI:', self)
        l_ai.move(b_width_one + 2, l_height + 45)
        b_ai_basket = QPushButton('Заполнить', self)
        b_ai_basket.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        b_ai_basket.setToolTip("Таблицу AI")
        b_ai_basket.resize(80,23)
        b_ai_basket.move(b_width_one, b_height + 45) 
        b_ai_basket.clicked.connect(self.filling_ai)
        b_clear_ai = QPushButton('Очистить', self)
        b_clear_ai.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
        b_clear_ai.setToolTip("Очистить таблицу AI")
        b_clear_ai.resize(80,23)
        b_clear_ai.move(b_width_two, b_height + 45) 
        b_clear_ai.clicked.connect(self.clear_ai_tabl)
        # AO
        l_ao = QLabel('AO:', self)
        l_ao.move(b_width_one + 182, l_height + 45)
        b_ao_basket = QPushButton('Заполнить', self)
        b_ao_basket.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        b_ao_basket.setToolTip("Таблицу AO")
        b_ao_basket.resize(80,23)
        b_ao_basket.move(b_width_one + 180, b_height + 45) 
        b_ao_basket.clicked.connect(self.filling_ao)
        b_clear_ao = QPushButton('Очистить', self)
        b_clear_ao.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
        b_clear_ao.setToolTip("Очистить таблицу AO")
        b_clear_ao.resize(80,23)
        b_clear_ao.move(b_width_two + 180, b_height + 45) 
        b_clear_ao.clicked.connect(self.clear_ao_tabl)
        # DI
        l_di = QLabel('DI:', self)
        l_di.move(b_width_one + 2, l_height + 90)
        b_di_basket = QPushButton('Заполнить', self)
        b_di_basket.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        b_di_basket.setToolTip("Таблицу DI")
        b_di_basket.resize(80,23)
        b_di_basket.move(b_width_one, b_height + 90) 
        b_di_basket.clicked.connect(self.filling_di)
        b_clear_di = QPushButton('Очистить', self)
        b_clear_di.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
        b_clear_di.setToolTip("Очистить таблицу DI")
        b_clear_di.resize(80,23)
        b_clear_di.move(b_width_two, b_height + 90) 
        b_clear_di.clicked.connect(self.clear_di_tabl)
        # DO
        l_do = QLabel('DO:', self)
        l_do.move(b_width_one + 182, l_height + 90)
        b_do_basket = QPushButton('Заполнить', self)
        b_do_basket.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        b_do_basket.setToolTip("Таблицу DO")
        b_do_basket.resize(80,23)
        b_do_basket.move(b_width_one + 180, b_height + 90) 
        b_do_basket.clicked.connect(self.filling_do)
        b_clear_do = QPushButton('Очистить', self)
        b_clear_do.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
        b_clear_do.setToolTip("Очистить таблицу DO")
        b_clear_do.resize(80,23)
        b_clear_do.move(b_width_two + 180, b_height + 90) 
        b_clear_do.clicked.connect(self.clear_do_tabl)
        # KTPR
        l_ktpr = QLabel('KTPR:', self)
        l_ktpr.move(b_width_one + 364, l_height)
        b_ktpr_basket = QPushButton('Подготовить', self)
        b_ktpr_basket.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        b_ktpr_basket.setToolTip('Сформировать таблицу Станционные защиты')
        b_ktpr_basket.resize(80,23)
        b_ktpr_basket.move(b_width_one + 360, b_height) 
        b_ktpr_basket.clicked.connect(self.filling_ktpr)
        b_clear_ktpr = QPushButton('Очистить', self)
        b_clear_ktpr.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
        b_clear_ktpr.setToolTip("Очистить таблицу KTPR")
        b_clear_ktpr.resize(80,23)
        b_clear_ktpr.move(b_width_two + 360, b_height) 
        b_clear_ktpr.clicked.connect(self.clear_ktpr_tabl)
        # KTPRA
        l_ktpra = QLabel('KTPRA:', self)
        l_ktpra.move(b_width_one + 364, l_height + 45)
        b_ktpra_basket = QPushButton('Подготовить', self)
        b_ktpra_basket.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        b_ktpra_basket.setToolTip('Сформировать таблицу Агрегатные защиты')
        b_ktpra_basket.resize(80,23)
        b_ktpra_basket.move(b_width_one + 360, b_height + 45) 
        b_ktpra_basket.clicked.connect(self.filling_ktpra)
        b_clear_ktpra = QPushButton('Очистить', self)
        b_clear_ktpra.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
        b_clear_ktpra.setToolTip("Очистить таблицу KTPRA")
        b_clear_ktpra.resize(80,23)
        b_clear_ktpra.move(b_width_two + 360, b_height + 45) 
        b_clear_ktpra.clicked.connect(self.clear_ktpra_tabl)
        # KTPRS
        l_ktprs = QLabel('KTPRS:', self)
        l_ktprs.move(b_width_one + 364, l_height + 90)
        b_ktprs_basket = QPushButton('Подготовить', self)
        b_ktprs_basket.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        b_ktprs_basket.setToolTip('Сформировать таблицу Предельные параметры')
        b_ktprs_basket.resize(80,23)
        b_ktprs_basket.move(b_width_one + 360, b_height + 90) 
        b_ktprs_basket.clicked.connect(self.filling_ktprs)
        b_clear_ktprs = QPushButton('Очистить', self)
        b_clear_ktprs.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
        b_clear_ktprs.setToolTip("Очистить таблицу KTPRS")
        b_clear_ktprs.resize(80,23)
        b_clear_ktprs.move(b_width_two + 360, b_height + 90) 
        b_clear_ktprs.clicked.connect(self.clear_ktprs_tabl)
        # GMPNA
        l_gmpna = QLabel('GMPNA:', self)
        l_gmpna.move(b_width_one + 364, l_height + 135)
        b_gmpna_basket = QPushButton('Подготовить', self)
        b_gmpna_basket.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        b_gmpna_basket.setToolTip('Сформировать таблицу Агрегатные готовности')
        b_gmpna_basket.resize(80,23)
        b_gmpna_basket.move(b_width_one + 360, b_height + 135) 
        b_gmpna_basket.clicked.connect(self.filling_gmpna)
        b_clear_gmpna = QPushButton('Очистить', self)
        b_clear_gmpna.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
        b_clear_gmpna.setToolTip("Очистить таблицу GMPNA")
        b_clear_gmpna.resize(80,23)
        b_clear_gmpna.move(b_width_two + 360, b_height + 135) 
        b_clear_gmpna.clicked.connect(self.clear_gmpna_tabl)
        # UMPNA
        l_umpna = QLabel('UMPNA:', self)
        l_umpna.move(b_width_one + 546, l_height)
        self.l_count_NA = QLineEdit(self, placeholderText='4', clearButtonEnabled=True)
        self.l_count_NA.setToolTip('Укажи количество НА (по умолчанию 4)')
        self.l_count_NA.setStyleSheet('border: 1px solid #6f7370; border-radius: 4px; border: 1px solid')
        self.l_count_NA.move(b_width_two + 540, l_height)
        self.l_count_NA.resize(80,15)
        b_umpna_basket = QPushButton('Заполнить', self)
        b_umpna_basket.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        b_umpna_basket.setToolTip('''Заполнить или обновить данные таблицы Насосные агрегаты(UMPNA):
        - Если таблица пустая -> добавятся и заполнятся новые ряды = количеству агрегатов;
        - Если количество рядов < количества агрегатов -> существующие обновятся или останутся без изменения, недостающие добавятся и заполнятся;
        - Если количество рядов = количеству агрегатов -> обновятся или останутся без изменения''')
        b_umpna_basket.resize(80,23)
        b_umpna_basket.move(b_width_one + 540, b_height) 
        b_umpna_basket.clicked.connect(self.filling_umpna)
        b_clear_umpna = QPushButton('Очистить', self)
        b_clear_umpna.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
        b_clear_umpna.setToolTip("Очистить таблицу Насосные агрегаты(UMPNA)")
        b_clear_umpna.resize(80,23)
        b_clear_umpna.move(b_width_two + 540, b_height) 
        b_clear_umpna.clicked.connect(self.clear_umpna_tabl)
        # tmNA_UMPNA
        l_tm_umpna = QLabel('tmNA_UMPNA:', self)
        l_tm_umpna.move(b_width_one + 728, l_height)
        b_tm_umpna_basket = QPushButton('Заполнить', self)
        b_tm_umpna_basket.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        b_tm_umpna_basket.setToolTip('Заполнить таблицу Временные уставки НА')
        b_tm_umpna_basket.resize(80,23)
        b_tm_umpna_basket.move(b_width_one + 720, b_height) 
        b_tm_umpna_basket.clicked.connect(self.filling_tmNA_umpna)
        b_clear_tm_umpna = QPushButton('Очистить', self)
        b_clear_tm_umpna.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
        b_clear_tm_umpna.setToolTip("Очистить таблицу Временные уставки НА")
        b_clear_tm_umpna.resize(80,23)
        b_clear_tm_umpna.move(b_width_two + 720, b_height) 
        b_clear_tm_umpna.clicked.connect(self.clear_tmNA_umpna_tabl)
        # Logs
        self.logTextBox = QTextEdit(self)
        self.logTextBox.setStyleSheet("border-radius: 4px; border: 1px solid")
        self.logTextBox.setGeometry(10,200,880,85)
        self.logTextBox.setReadOnly(True)
        self.logs_msg(f'Запущена форма заполнения таблиц базы данных', 1)
    # HardWare
    def kk_check(self, checked):
        if checked:
            self.kk_is_true = True
            self.logs_msg(f'Добавить КК - флаг установлен', 3)
        else:
            self.kk_is_true = False
            self.logs_msg(f'Добавить КК - флаг cнят', 3)
    def clear_tabl(self):
        msg = self.dop_function.clear_tabl('hardware', 'HardWare', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    def filling_hardware(self):
        hw_table = Filling_HardWare()
        msg = hw_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = hw_table.getting_modul(self.kk_is_true)
        self.logs_msg('default', 1, msg, True)
    # USO
    def filling_uso(self):
        uso_table = Filling_USO()
        msg = uso_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = uso_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_uso_tabl(self):
        msg = self.dop_function.clear_tabl('uso', 'USO', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # AI
    def filling_ai(self):
        ai_table = Filling_AI()
        msg = ai_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = ai_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_ai_tabl(self):
        msg = self.dop_function.clear_tabl('ai', 'AI', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # AO
    def filling_ao(self):
        ao_table = Filling_AO()
        msg = ao_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = ao_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_ao_tabl(self):
        msg = self.dop_function.clear_tabl('ao', 'AO', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # DI
    def filling_di(self):
        di_table = Filling_DI()
        msg = di_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = di_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_di_tabl(self):
        msg = self.dop_function.clear_tabl('di', 'DI', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # DO
    def filling_do(self):
        do_table = Filling_DO()
        msg = do_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = do_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_do_tabl(self):
        msg = self.dop_function.clear_tabl('do', 'DO', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # KTPR
    def filling_ktpr(self):
        ktpr_table = Filling_KTPR()
        msg = ktpr_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = ktpr_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_ktpr_tabl(self):
        msg = self.dop_function.clear_tabl('ktpr', 'KTPR', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # KTPRA
    def filling_ktpra(self):
        ktpra_table = Filling_KTPRA()
        msg = ktpra_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = ktpra_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_ktpra_tabl(self):
        msg = self.dop_function.clear_tabl('ktpra', 'KTPRA', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # KTPRS
    def filling_ktprs(self):
        ktprs_table = Filling_KTPRS()
        msg = ktprs_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = ktprs_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_ktprs_tabl(self):
        msg = self.dop_function.clear_tabl('ktprs', 'KTPRS', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # GMPNA
    def filling_gmpna(self):
        gmpna_table = Filling_GMPNA()
        msg = gmpna_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = gmpna_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_gmpna_tabl(self):
        msg = self.dop_function.clear_tabl('gmpna', 'GMPNA', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # UMPNA
    def filling_umpna(self):
        umpna_table = Filling_UMPNA()
        msg = umpna_table.column_check()
        self.logs_msg('default', 1, msg, True)
        count = self.l_count_NA.text().strip() or '4'
        msg = umpna_table.getting_modul(int(count))
        self.logs_msg('default', 1, msg, True)
    def clear_umpna_tabl(self):
        msg = self.dop_function.clear_tabl('umpna', 'UMPNA', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # tmNA_UMPNA
    def filling_tmNA_umpna(self):
        tmNA_umpna_table = Filling_tmNA_UMPNA()
        msg = tmNA_umpna_table.column_check()
        self.logs_msg('default', 1, msg, True)
        count = self.l_count_NA.text().strip() or '4'
        msg = tmNA_umpna_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_tmNA_umpna_tabl(self):
        msg = self.dop_function.clear_tabl('tmna_umpna', 'tmNA_UMPNA', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # Logging messeges
    def logs_msg(self, logs=None, number_color=1, buffer_msg=None, msg=False):
        today = datetime.now()
        errorFormat   = '<span style="color:red;">{}</span>'
        warningFormat = '<span style="color:#9ea108;">{}</span>'
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
        self.setStyleSheet("background-color: #e1e5e5;")
        self.resize(260, 100)

        l_table = QLabel('Выберите таблицу: ', self)
        l_table.move(10, 5)

        self.combo = QComboBox(self)
        self.combo.move(10, 20) 
        self.combo.resize(240,25)
        self.combo.setStyleSheet("border-radius: 4px; border: 1px solid")
        self.combo.setFont(QFont('Arial', 10))

        clickButton = QPushButton('Подключиться к таблице', self)
        clickButton.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        clickButton.resize(240,35)
        clickButton.move(10, 55) 
        clickButton.clicked.connect(self.choose_tabl)

        for tabl in list_tabl:
           self.combo.addItem(str(tabl))
    # Choose table
    def choose_tabl(self):
        name_table = self.combo.currentText()
        self.ch_tabl = Window_update_sql(name_table)
        self.ch_tabl.show()
        self.close()
class Window_update_sql(QWidget):
    def __init__(self, table_used):
        super(Window_update_sql, self).__init__()
        self.setWindowTitle('Редактор базы данных')
        self.setStyleSheet("background-color: #e1e5e5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(1600, 890)

        self.TableWidget = QTableWidget(self)
        self.TableWidget.setGeometry(10,70,1580,710)

        self.logTextBox = QTextEdit(self)
        self.logTextBox.setGeometry(10,779,1580,100)
        self.logTextBox.setStyleSheet("border-radius: 4px; border: 1px solid")
        self.logTextBox.setFont(QFont('Arial', 10))
        self.logTextBox.setReadOnly(True)

        self.table_used = table_used
        self.edit_SQL = Editing_table_SQL()
        column, row, self.hat_name, value = self.edit_SQL.editing_sql(self.table_used)
        
        try   : self.tablew(column, row, self.hat_name, value, rus_list[self.table_used])
        except: self.tablew(column, row, self.hat_name, value)

        new_addrow_Button = QPushButton('Добавить строку', self)
        new_addrow_Button.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        new_addrow_Button.resize(120,25)
        new_addrow_Button.move(10, 8) 
        new_addrow_Button.clicked.connect(self.add_row)

        remoterow_Button = QPushButton('Удалить строку', self)
        remoterow_Button.setStyleSheet("background: #d65860; border-radius: 4px; border: 1px solid")
        remoterow_Button.resize(120,25)
        remoterow_Button.move(10, 40) 
        remoterow_Button.clicked.connect(self.delete_row)

        self.namecolumn = QLineEdit(self, placeholderText='Название нового столбца', clearButtonEnabled=True)
        self.namecolumn.setStyleSheet('border: 1px solid #6f7370; border-radius: 4px; border: 1px solid')
        self.namecolumn.move(160, 8)
        self.namecolumn.resize(260,25)
        new_addcol_Button = QPushButton('Добавить столбец', self)
        new_addcol_Button.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        new_addcol_Button.resize(120,25)
        new_addcol_Button.move(160, 40) 
        new_addcol_Button.clicked.connect(self.add_column)

        remotecolumn_Button = QPushButton('Удалить столбец', self)
        remotecolumn_Button.setStyleSheet("background: #d65860; border-radius: 4px; border: 1px solid")
        remotecolumn_Button.resize(120,25)
        remotecolumn_Button.move(300, 40) 
        remotecolumn_Button.clicked.connect(self.delete_column)

        cleartab_Button = QPushButton('Очистить таблицу', self)
        cleartab_Button.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
        cleartab_Button.resize(120,25)
        cleartab_Button.move(470, 8) 
        cleartab_Button.clicked.connect(self.clear_tabl)

        droptab_Button = QPushButton('Удалить таблицу', self)
        droptab_Button.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
        droptab_Button.resize(120,25)
        droptab_Button.move(470, 40) 
        droptab_Button.clicked.connect(self.drop_tabl)

        self.req_base = QLineEdit(self, placeholderText='Введите запрос к текущей таблице', clearButtonEnabled=True)
        self.req_base.setStyleSheet('border: 1px solid #6f7370; border-radius: 4px; border: 1px solid')
        self.req_base.setToolTip('Значения типа "string" обязательно брать в "ковычки"')
        self.req_base.move(750, 8)
        self.req_base.resize(820,25)
        apply_query_Button = QPushButton('Применить запрос', self)
        apply_query_Button.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        apply_query_Button.resize(120,25)
        apply_query_Button.move(750, 40) 
        apply_query_Button.clicked.connect(self.apply_database_query)
        reset_request_Button = QPushButton('Сбросить запрос', self)
        reset_request_Button.setStyleSheet("background: #bbbabf; border-radius: 4px; border: 1px solid")
        reset_request_Button.setToolTip("Если используется выборка из таблицы!")
        reset_request_Button.resize(120,25)
        reset_request_Button.move(900, 40) 
        reset_request_Button.clicked.connect(self.reset_database_query)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.logTextBox)
        self.layout.addWidget(new_addrow_Button)
        self.layout.addWidget(new_addcol_Button)
        self.layout.addWidget(remoterow_Button)
        self.layout.addWidget(cleartab_Button)
        self.layout.addWidget(self.TableWidget)
        # Logs
        self.logs_msg(f'Запущен редактор базы данных. Таблица: {self.table_used}', 1)
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
    # Drop the table
    def drop_tabl(self):
        self.close()
        self.edit_SQL.drop_tabl(self.table_used)


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
    
    # Changing a table while entering a query
    def apply_database_query(self):
        request = self.req_base.text()
        if request == '': 
            self.logs_msg(f'Пустой запрос!', 2)
            return
        # Под запрос 'select' отдельная функция
        find = general_functions()
        if find.str_find(str(request).lower(), {'select'}):
            column, row, hat_name, value, msg = self.edit_SQL.apply_request_select(request, self.table_used)
            self.logs_msg('default', 1, msg, True)
        else:
            msg = self.edit_SQL.other_requests(request, self.table_used)
            self.logs_msg('default', 1, msg, True)
            column, row, hat_name, value = self.edit_SQL.editing_sql(self.table_used)
        # Если запрос некорректный
        if column == 'error': return
        # Clear
        rowcount = self.TableWidget.rowCount()
        if rowcount != 0: 
            while rowcount >= 0:
                self.TableWidget.removeRow(rowcount)
                rowcount -= 1
        # Filling
        try   : self.tablew(column, row, hat_name, value, rus_list[self.table_used])
        except: self.tablew(column, row, hat_name, value)
        #SELECT * FROM ai WHERE uso='МНС-2.КЦ' AND basket=3 AND module=3 AND channel=1
    # Reset a table query
    def reset_database_query(self):
        rowcount = self.TableWidget.rowCount()
        if rowcount != 0: 
            while rowcount >= 0:
                self.TableWidget.removeRow(rowcount)
                rowcount -= 1

        column, row, self.hat_name, value = self.edit_SQL.editing_sql(self.table_used)

        try   : self.tablew(column, row, self.hat_name, value, rus_list[self.table_used])
        except: self.tablew(column, row, self.hat_name, value)

    # Building the selected table
    def tablew(self, column, row, hat_name, value, column_tooltip=None):
        # TableW
        self.TableWidget.setColumnCount(column)
        self.TableWidget.setRowCount(row)
        self.TableWidget.setHorizontalHeaderLabels(hat_name)
        # Color header
        style = "::section {""background-color: #bbbabf; }"
        self.TableWidget.horizontalHeader().setStyleSheet(style)
        # Подсказки к столбцам
        if column_tooltip is not None:
            for col in range(self.TableWidget.columnCount()):
                self.TableWidget.horizontalHeaderItem(col).setToolTip(column_tooltip[col])

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
                    item.setToolTip(str(value[row_t][column_t]))

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
        warningFormat = '<span style="color:#9ea108;">{}</span>'
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