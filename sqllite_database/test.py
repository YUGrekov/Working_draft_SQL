from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from main_base import *



class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Меню разработки проекта')
        self.resize(1095, 400)

        tab = QTabWidget(self)
        tab.resize(1085, 275)
        tab.move(5, 5)

        tab_1 = QFrame()
        tab_2 = QFrame()
        tab_3 = QFrame()
        tab_4 = QFrame()  
        tab_5 = QFrame()   

        tab.addTab(tab_1, 'Соединение')
        tab.addTab(tab_2, 'Импорт КЗФКП')
        tab.addTab(tab_3, 'SQL разработки')
        tab.addTab(tab_4, 'SQL проекта')
        tab.addTab(tab_5, 'SQL редактор')

        self.dop_function = General_functions()
        self.edit_SQL = Editing_table_SQL()
        self.list_tabl = self.edit_SQL.get_tabl()

        # ------------------Окно редактирования------------------
        list_tabl = self.dop_function.all_tables()
        list_tabl.sort()
        l_table = QLabel('Выберите таблицу: ', tab_5)
        l_table.move(10, 5)

        self.combo = QComboBox(tab_5)
        self.combo.move(10, 20) 
        self.combo.resize(240,25)
        self.combo.setStyleSheet("border-radius: 3px; border: 1px solid")
        self.combo.setFont(QFont('Arial', 10))

        clickButton = QPushButton('Подключиться к таблице', tab_5)
        clickButton.setStyleSheet("border-radius: 3px; border: 1px solid")
        clickButton.resize(240,23)
        clickButton.move(10, 55) 
        clickButton.clicked.connect(self.choose_tabl)

        updateButton = QPushButton('Обновить', tab_5)
        updateButton.setStyleSheet("border-radius: 3px; border: 1px solid")
        updateButton.resize(120,23)
        updateButton.move(270, 20) 
        updateButton.clicked.connect(self.update_tabl)

        for tabl in list_tabl:
           self.combo.addItem(str(tabl))

        # ------------------Соединение------------------
        self.gen_sql = Generate_database_SQL()
        # Название проекта
        l_name_station_desc = QLabel('Название проекта: ', tab_1)
        l_name_station_desc.move(10, 5)
        l_name_station_path = QLabel(tab_1)
        l_name_station_path.move(135, 5)
        l_name_station_path.setText(name_project)
        # КЗФКП
        l_kzfkp_desc = QLabel('Путь до файла КД: ', tab_1)
        l_kzfkp_desc.move(10, 20)
        l_kzfkp_path = QLabel(tab_1)
        l_kzfkp_path.move(135, 20)
        l_kzfkp_path.setText(path_to_exel)
        # Шаблоны сообщений
        l_sample_desc = QLabel('Шаблоны сообщений: ', tab_1)
        l_sample_desc.move(10, 35)
        l_sample_path = QLabel(tab_1)
        l_sample_path.move(135, 35)
        l_sample_path.setText(path_sample)
        # Скрипты сообщений
        l_script_desc = QLabel('Скрипты сообщений: ', tab_1)
        l_script_desc.move(10, 50)
        l_script_path = QLabel(tab_1)
        l_script_path.move(135, 50)
        l_script_path.setText(path_location_file)
        # Файлы DevStudio
        l_devstudio_desc = QLabel('Файлы DevStudio: ', tab_1)
        l_devstudio_desc.move(10, 65)
        l_devstudio_path = QLabel(tab_1)
        l_devstudio_path.move(135, 65)
        l_devstudio_path.setText(path_to_devstudio)
        # SQL
        l_sql_desc = QLabel('Данные для подключения к базе SQL: ', tab_1)
        l_sql_desc.move(50, 100)
        l_sql_msg_desc = QLabel('SQL база разработки: ', tab_1)
        l_sql_msg_desc.setStyleSheet("background-color: #d8d99c")
        l_sql_msg_desc.move(10, 113)
        l_sql_ust_desc = QLabel('SQL база проекта: ', tab_1)
        l_sql_ust_desc.setStyleSheet("background-color: #d8d99c")
        l_sql_ust_desc.move(200, 113)
        # Проверка подключения
        #msg
        b_check_sql_msg = QPushButton('Проверить соединение', tab_1)
        b_check_sql_msg.setStyleSheet("border-radius: 4px; border: 1px solid")
        b_check_sql_msg.resize(130,23)
        b_check_sql_msg.move(10, 202) 
        b_check_sql_msg.clicked.connect(self.check_base_sql_msg)
        self.l_sql_msg_check = QLabel('Проверка не проводилась',tab_1)
        self.l_sql_msg_check.move(10, 227)
        #ust
        b_check_sql_ust = QPushButton('Проверить соединение', tab_1)
        b_check_sql_ust.setStyleSheet("border-radius: 4px; border: 1px solid")
        b_check_sql_ust.resize(130,23)
        b_check_sql_ust.move(200, 202) 
        b_check_sql_ust.clicked.connect(self.check_base_sql_ust)
        self.l_sql_ust_check = QLabel('Проверка не проводилась',tab_1)
        self.l_sql_ust_check.move(200, 227)
        # MSG
        l_sql_msg_base_desc = QLabel('Database: ',tab_1)
        l_sql_msg_base_desc.move(10, 127)
        l_sql_msg_base_path = QLabel(tab_1)
        l_sql_msg_base_path.move(70, 127)
        l_sql_msg_base_path.setText(database_msg)
        l_sql_msg_user_desc = QLabel('User: ',tab_1)
        l_sql_msg_user_desc.move(10, 142)
        l_sql_msg_user_path = QLabel(tab_1)
        l_sql_msg_user_path.move(70, 142)
        l_sql_msg_user_path.setText(user_msg)
        l_sql_msg_pass_desc = QLabel('Password: ',tab_1)
        l_sql_msg_pass_desc.move(10, 157)
        l_sql_msg_pass_path = QLabel(tab_1)
        l_sql_msg_pass_path.move(70, 157)
        l_sql_msg_pass_path.setText(password_msg)
        l_sql_msg_host_desc = QLabel('Host: ',tab_1)
        l_sql_msg_host_desc.move(10, 172)
        l_sql_msg_host_path = QLabel(tab_1)
        l_sql_msg_host_path.move(70, 172)
        l_sql_msg_host_path.setText(host_msg)
        l_sql_msg_port_desc = QLabel('Port: ',tab_1)
        l_sql_msg_port_desc.move(10, 187)
        l_sql_msg_port_path = QLabel(tab_1)
        l_sql_msg_port_path.move(70, 187)
        l_sql_msg_port_path.setText(port_msg)
        # asutp
        l_sql_base_desc = QLabel('Database: ',tab_1)
        l_sql_base_desc.move(200, 127)
        l_sql_base_path = QLabel(tab_1)
        l_sql_base_path.move(260, 127)
        l_sql_base_path.setText(database_prj)
        l_sql_user_desc = QLabel('User: ',tab_1)
        l_sql_user_desc.move(200, 142)
        l_sql_user_path = QLabel(tab_1)
        l_sql_user_path.move(260, 142)
        l_sql_user_path.setText(user_prj)
        l_sql_pass_desc = QLabel('Password: ',tab_1)
        l_sql_pass_desc.move(200, 157)
        l_sql_pass_path = QLabel(tab_1)
        l_sql_pass_path.move(260, 157)
        l_sql_pass_path.setText(password_prj)
        l_sql_host_desc = QLabel('Host: ',tab_1)
        l_sql_host_desc.move(200, 172)
        l_sql_host_path = QLabel(tab_1)
        l_sql_host_path.move(260, 172)
        l_sql_host_path.setText(host_prj)
        l_sql_port_desc = QLabel('Port: ',tab_1)
        l_sql_port_desc.move(200, 187)
        l_sql_port_path = QLabel(tab_1)
        l_sql_port_path.move(260, 187)
        l_sql_port_path.setText(port_prj)

        # ------------------Импорт КЗФКП------------------
        readtablbutt = QPushButton('Прочитать шапку таблицы', tab_2)
        readtablbutt.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        readtablbutt.resize(150,25)
        readtablbutt.move(350, 10) 
        readtablbutt.clicked.connect(self.read_hat_tabl)
        self.select_uso = QComboBox(tab_2)
        self.select_uso.addItem('Выбери таблицу')
        self.select_uso.setStyleSheet('border: 1px solid; border-radius: 3px;')
        self.select_uso.move(10, 10)
        self.select_uso.resize(150,25)
        self.select_uso.currentIndexChanged.connect(self.click_comboBox)
        self.select_row = QLineEdit(tab_2, placeholderText='Заполни строку заголовка', clearButtonEnabled=True)
        self.select_row.setStyleSheet('border: 1px solid #6f7370; border: 1px solid; border-radius: 3px;')
        self.select_row.move(180, 10)
        self.select_row.resize(150,25)
        self.select_row.returnPressed.connect(self.read_hat_tabl)

        self.q_type_sig = QComboBox(tab_2)
        self.q_type_sig.move(10, 55)
        self.q_type_sig.resize(150,25)
        self.q_type_sig.setStyleSheet('border: 1px solid; border-radius: 3px;')
        self.q_tag = QComboBox(tab_2)
        self.q_tag.move(170, 55)
        self.q_tag.resize(150,25)
        self.q_tag.setStyleSheet('border: 1px solid; border-radius: 3px;')
        self.q_dict = QComboBox(tab_2)
        self.q_dict.move(330, 55)
        self.q_dict.resize(150,25)
        self.q_dict.setStyleSheet('border: 1px solid; border-radius: 3px;')
        self.q_schema = QComboBox(tab_2)
        self.q_schema.move(10, 90)
        self.q_schema.resize(150,25)
        self.q_schema.setStyleSheet('border: 1px solid; border-radius: 3px;')
        self.q_klk = QComboBox(tab_2)
        self.q_klk.move(170, 90)
        self.q_klk.resize(150,25)
        self.q_klk.setStyleSheet('border: 1px solid; border-radius: 3px;')
        self.q_kont = QComboBox(tab_2)
        self.q_kont.move(330, 90)
        self.q_kont.resize(150,25)
        self.q_kont.setStyleSheet('border: 1px solid; border-radius: 3px;')
        self.q_basket = QComboBox(tab_2)
        self.q_basket.move(10, 125)
        self.q_basket.resize(150,25)
        self.q_basket.setStyleSheet('border: 1px solid; border-radius: 3px;')
        self.q_mod = QComboBox(tab_2)
        self.q_mod.move(170, 125)
        self.q_mod.resize(150,25)
        self.q_mod.setStyleSheet('border: 1px solid; border-radius: 3px;')
        self.q_channel = QComboBox(tab_2)
        self.q_channel.move(330, 125)
        self.q_channel.resize(150,25)
        self.q_channel.setStyleSheet('border: 1px solid; border-radius: 3px;')

        self.l_type_sig = QLabel('Тип сигнала', tab_2)
        self.l_type_sig.move(55, 43)
        self.l_tag = QLabel('Тэг', tab_2)
        self.l_tag.move(235, 43)
        self.l_dict = QLabel('Наименование', tab_2)
        self.l_dict.move(365, 43)
        self.l_schema = QLabel('Схема', tab_2)
        self.l_schema.move(65, 78)
        self.l_klk = QLabel('Клеммник', tab_2)
        self.l_klk.move(220, 78)
        self.l_kont = QLabel('Контакт', tab_2)
        self.l_kont.move(380, 78)
        self.l_basket = QLabel('Корзина', tab_2)
        self.l_basket.move(60, 113)
        self.l_mod = QLabel('Модуль', tab_2)
        self.l_mod.move(225, 113)
        self.l_channel = QLabel('Канал', tab_2)
        self.l_channel.move(385, 113)
        
        savebasebutt = QPushButton('Сохранить новое УСО', tab_2)
        savebasebutt.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        savebasebutt.setToolTip('''Добавляются новые сигналы в конец таблицы''')
        savebasebutt.resize(150,25)
        savebasebutt.move(330, 170) 
        savebasebutt.clicked.connect(self.start_fill_base)

        updatebasebutt = QPushButton('Обновить данные УСО', tab_2)
        updatebasebutt.setStyleSheet("background: #b2b4eb; border: 1px solid; border-radius: 3px;")
        updatebasebutt.setToolTip('''Сигнал проверяется по шкафу, модулю, корзине и каналу. Если такой отсутствует,\nто добавляется новый в конец таблицы, иначе данные которые различаются обновляются''')
        updatebasebutt.resize(150,25)
        updatebasebutt.move(330, 205) 
        updatebasebutt.clicked.connect(self.update_fill_base)

        cleartablbutt = QPushButton('Очистить таблицу signals', tab_2)
        cleartablbutt.setStyleSheet("background: #aeb37b; border: 1px solid; border-radius: 3px;")
        cleartablbutt.resize(170,25)
        cleartablbutt.move(10, 170) 
        cleartablbutt.clicked.connect(self.clear_table)
        # ------------------Заполнение таблиц------------------
        # Size default
        b_width_one = 8
        b_width_two = 92
        l_height    = 3
        b_height    = 20
        # HardWare
        self.kk_is_true = False
        l_hw = QLabel('HardWare:', tab_3)
        l_hw.move(b_width_one + 2, l_height)
        b_io_basket = QPushButton('Заполнить', tab_3)
        b_io_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px; ")
        b_io_basket.setToolTip('''Конфигурация корзин в проекте CodeSys. Обновления таблицы нет! При новом заполнении строки добавляются в конец таблицы''')
        b_io_basket.resize(80,23)
        b_io_basket.move(b_width_one, b_height) 
        b_io_basket.clicked.connect(self.filling_hardware)
        b_clear_tabl = QPushButton('Очистить', tab_3)
        b_clear_tabl.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_tabl.setToolTip("Очистить таблицу HardWare")
        b_clear_tabl.resize(80,23)
        b_clear_tabl.move(b_width_two, b_height) 
        b_clear_tabl.clicked.connect(self.clear_tabl)
        c_kk_is_true = QCheckBox('Есть KK?', tab_3)
        c_kk_is_true.setToolTip("Добавить в диагостику проекта коммуникационные контроллеры")
        c_kk_is_true.move(70, 2) 
        c_kk_is_true.stateChanged.connect(self.kk_check)
        # USO
        l_uso = QLabel('USO:', tab_3)
        l_uso.move(b_width_one + 182, l_height)
        b_uso_basket = QPushButton('Заполнить', tab_3)
        b_uso_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_uso_basket.setToolTip("Шкафная дигностика. Должны быть заполнены таблицы AI и DI")
        b_uso_basket.resize(80,23)
        b_uso_basket.move(b_width_one + 180, b_height) 
        b_uso_basket.clicked.connect(self.filling_uso)
        b_clear_uso = QPushButton('Очистить', tab_3)
        b_clear_uso.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_uso.setToolTip("Очистить таблицу USO")
        b_clear_uso.resize(80,23)
        b_clear_uso.move(b_width_two + 180, b_height) 
        b_clear_uso.clicked.connect(self.clear_uso_tabl)
        # AI
        l_ai = QLabel('AI:', tab_3)
        l_ai.move(b_width_one + 2, l_height + 45)
        b_ai_basket = QPushButton('Заполнить', tab_3)
        b_ai_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_ai_basket.setToolTip("Для корректного заполнения таблицы AI, необходимо указать тип сигнала в таблице signals")
        b_ai_basket.resize(80,23)
        b_ai_basket.move(b_width_one, b_height + 45) 
        b_ai_basket.clicked.connect(self.filling_ai)
        b_clear_ai = QPushButton('Очистить', tab_3)
        b_clear_ai.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_ai.setToolTip("Очистить таблицу AI")
        b_clear_ai.resize(80,23)
        b_clear_ai.move(b_width_two, b_height + 45) 
        b_clear_ai.clicked.connect(self.clear_ai_tabl)
        # AO
        l_ao = QLabel('AO:', tab_3)
        l_ao.move(b_width_one + 182, l_height + 45)
        b_ao_basket = QPushButton('Заполнить', tab_3)
        b_ao_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_ao_basket.setToolTip("Для корректного заполнения таблицы AO, необходимо указать тип сигнала в таблице signals")
        b_ao_basket.resize(80,23)
        b_ao_basket.move(b_width_one + 180, b_height + 45) 
        b_ao_basket.clicked.connect(self.filling_ao)
        b_clear_ao = QPushButton('Очистить', tab_3)
        b_clear_ao.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_ao.setToolTip("Очистить таблицу AO")
        b_clear_ao.resize(80,23)
        b_clear_ao.move(b_width_two + 180, b_height + 45) 
        b_clear_ao.clicked.connect(self.clear_ao_tabl)
        # DI
        l_di = QLabel('DI:', tab_3)
        l_di.move(b_width_one + 2, l_height + 90)
        b_di_basket = QPushButton('Заполнить', tab_3)
        b_di_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_di_basket.setToolTip('''Для корректного заполнения таблицы DI, необходимо указать тип сигнала в таблице signals, 
        а также заполнить таблицу hardware, и подписать идентификатор шкафа!''')
        b_di_basket.resize(80,23)
        b_di_basket.move(b_width_one, b_height + 90) 
        b_di_basket.clicked.connect(self.filling_di)
        b_clear_di = QPushButton('Очистить', tab_3)
        b_clear_di.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_di.setToolTip("Очистить таблицу DI")
        b_clear_di.resize(80,23)
        b_clear_di.move(b_width_two, b_height + 90) 
        b_clear_di.clicked.connect(self.clear_di_tabl)
        # DO
        l_do = QLabel('DO:', tab_3)
        l_do.move(b_width_one + 182, l_height + 90)
        b_do_basket = QPushButton('Заполнить', tab_3)
        b_do_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_do_basket.setToolTip('''Для корректного заполнения таблицы DO, необходимо указать тип сигнала в таблице signals, 
        а также заполнить таблицу hardware, и подписать идентификатор шкафа!''')
        b_do_basket.resize(80,23)
        b_do_basket.move(b_width_one + 180, b_height + 90) 
        b_do_basket.clicked.connect(self.filling_do)
        b_clear_do = QPushButton('Очистить', tab_3)
        b_clear_do.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_do.setToolTip("Очистить таблицу DO")
        b_clear_do.resize(80,23)
        b_clear_do.move(b_width_two + 180, b_height + 90) 
        b_clear_do.clicked.connect(self.clear_do_tabl)
        # UTS
        l_uts = QLabel('UTS:', tab_3)
        l_uts.move(b_width_one + 2, l_height + 135)
        b_uts_basket = QPushButton('Заполнить', tab_3)
        b_uts_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_uts_basket.setToolTip('''Происходит поиск по ключевым словам: 'сирен' и 'табл', и также по тегам 'ВВ'. 
        Существование сигнала определяется по шкафу,корзине, модулю и каналу. 
        - Если сигнал существует -> происходит проверка по названию, тегу и команде включения;
        - Если нет -> добавляется новый сигнал.''')
        b_uts_basket.resize(80,23)
        b_uts_basket.move(b_width_one, b_height + 135) 
        b_uts_basket.clicked.connect(self.filling_uts)
        b_clear_uts = QPushButton('Очистить', tab_3)
        b_clear_uts.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_uts.setToolTip("Очистить таблицу UTS")
        b_clear_uts.resize(80,23)
        b_clear_uts.move(b_width_two, b_height + 135) 
        b_clear_uts.clicked.connect(self.clear_uts_tabl)
        # UPTS
        l_upts = QLabel('UPTS:', tab_3)
        l_upts.move(b_width_one + 2, l_height + 180)
        b_upts_basket = QPushButton('Заполнить', tab_3)
        b_upts_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_upts_basket.setToolTip('''Происходит поиск по ключевым словам: 'сирен' и 'табл', и также по тегам 'ВВ'. 
        Существование сигнала определяется по шкафу,корзине, модулю и каналу. 
        - Если сигнал существует -> происходит проверка по названию, тегу и команде включения;
        - Если нет -> добавляется новый сигнал.''')
        b_upts_basket.resize(80,23)
        b_upts_basket.move(b_width_one, b_height + 180) 
        b_upts_basket.clicked.connect(self.filling_upts)
        b_clear_upts = QPushButton('Очистить', tab_3)
        b_clear_upts.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_upts.setToolTip("Очистить таблицу UPTS")
        b_clear_upts.resize(80,23)
        b_clear_upts.move(b_width_two, b_height + 180) 
        b_clear_upts.clicked.connect(self.clear_upts_tabl)
       
        # VV
        l_vv = QLabel('VV:', tab_3)
        l_vv.move(b_width_one + 910, l_height + 135)
        b_vv_basket = QPushButton('Заполнить', tab_3)
        b_vv_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_vv_basket.setToolTip('''Происходит поиск по ключевым словам: 'ввода','СВВ', 'ССВ' и также по тегам 'MBC'. 
        Для сигнала применяем замену и формируем короткое название, убираем дублирование и для каждого сигнала ищем DI. 
        Существование сигнала проходт по названию.
        - Если сигнал существует -> происходит проверка по включению и отключению;
        - Если нет -> добавляется новый сигнал.''')
        b_vv_basket.resize(80,23)
        b_vv_basket.move(b_width_one + 900, b_height + 135) 
        b_vv_basket.clicked.connect(self.filling_vv)
        b_clear_vv = QPushButton('Очистить', tab_3)
        b_clear_vv.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_vv.setToolTip("Очистить таблицу VV")
        b_clear_vv.resize(80,23)
        b_clear_vv.move(b_width_two + 900, b_height + 135) 
        b_clear_vv.clicked.connect(self.clear_vv_tabl)
         # tmUTS
        l_utstm = QLabel('tmUTS:', tab_3)
        l_utstm.move(b_width_one + 182, l_height + 135)
        b_utstm_basket = QPushButton('Заполнить', tab_3)
        b_utstm_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_utstm_basket.setToolTip('''Временные уставки UTS.
        Должна быть заполнена таблица UTS, откуда берется название и по умолчанию добавляются уставки.
        Проверки нет! Для нового заполнения необходимо очистить таблицу, иначе новые записи добавятся в конец таблицы!''')
        b_utstm_basket.resize(80,23)
        b_utstm_basket.move(b_width_one + 180, b_height + 135) 
        b_utstm_basket.clicked.connect(self.filling_uts_tm)
        b_clear_utstm = QPushButton('Очистить', tab_3)
        b_clear_utstm.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_utstm.setToolTip("Очистить таблицу Временные уставки UTS")
        b_clear_utstm.resize(80,23)
        b_clear_utstm.move(b_width_two + 180, b_height + 135) 
        b_clear_utstm.clicked.connect(self.clear_uts_tm_tabl)
        # KTPR
        l_ktpr = QLabel('KTPR:', tab_3)
        l_ktpr.move(b_width_one + 364, l_height)
        b_ktpr_basket = QPushButton('Подготовить', tab_3)
        b_ktpr_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_ktpr_basket.setToolTip('''Станционные защиты. Таблица не заполняется! 
        - Если отсутствует в базе, то добавиться новая со строками на 96 защит''')
        b_ktpr_basket.resize(80,23)
        b_ktpr_basket.move(b_width_one + 360, b_height) 
        b_ktpr_basket.clicked.connect(self.filling_ktpr)
        b_clear_ktpr = QPushButton('Очистить', tab_3)
        b_clear_ktpr.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_ktpr.setToolTip("Очистить таблицу KTPR")
        b_clear_ktpr.resize(80,23)
        b_clear_ktpr.move(b_width_two + 360, b_height) 
        b_clear_ktpr.clicked.connect(self.clear_ktpr_tabl)
        # KTPRA
        l_ktpra = QLabel('KTPRA:', tab_3)
        l_ktpra.move(b_width_one + 364, l_height + 45)
        b_ktpra_basket = QPushButton('Подготовить', tab_3)
        b_ktpra_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_ktpra_basket.setToolTip('''Агрегатные защиты. Таблица не заполняется! 
        - Если отсутствует в базе, то добавиться новая со строками на 4 агрегата и 96 защит''')
        b_ktpra_basket.resize(80,23)
        b_ktpra_basket.move(b_width_one + 360, b_height + 45) 
        b_ktpra_basket.clicked.connect(self.filling_ktpra)
        b_clear_ktpra = QPushButton('Очистить', tab_3)
        b_clear_ktpra.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_ktpra.setToolTip("Очистить таблицу KTPRA")
        b_clear_ktpra.resize(80,23)
        b_clear_ktpra.move(b_width_two + 360, b_height + 45) 
        b_clear_ktpra.clicked.connect(self.clear_ktpra_tabl)
        # KTPRS
        l_ktprs = QLabel('KTPRS:', tab_3)
        l_ktprs.move(b_width_one + 364, l_height + 90)
        b_ktprs_basket = QPushButton('Подготовить', tab_3)
        b_ktprs_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_ktprs_basket.setToolTip('''Предельные защиты. Таблица не заполняется! 
        - Если отсутствует в базе, то добавиться новая со строками на 20 защит''')
        b_ktprs_basket.resize(80,23)
        b_ktprs_basket.move(b_width_one + 360, b_height + 90) 
        b_ktprs_basket.clicked.connect(self.filling_ktprs)
        b_clear_ktprs = QPushButton('Очистить', tab_3)
        b_clear_ktprs.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_ktprs.setToolTip("Очистить таблицу KTPRS")
        b_clear_ktprs.resize(80,23)
        b_clear_ktprs.move(b_width_two + 360, b_height + 90) 
        b_clear_ktprs.clicked.connect(self.clear_ktprs_tabl)
        # GMPNA
        l_gmpna = QLabel('GMPNA:', tab_3)
        l_gmpna.move(b_width_one + 364, l_height + 135)
        b_gmpna_basket = QPushButton('Подготовить', tab_3)
        b_gmpna_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_gmpna_basket.setToolTip('''Агрегатные готовности. Таблица не заполняется! 
        - Если отсутствует в базе, то добавиться новая со строками на 4 агрегата и 64 готовности''')
        b_gmpna_basket.resize(80,23)
        b_gmpna_basket.move(b_width_one + 360, b_height + 135) 
        b_gmpna_basket.clicked.connect(self.filling_gmpna)
        b_clear_gmpna = QPushButton('Очистить', tab_3)
        b_clear_gmpna.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_gmpna.setToolTip("Очистить таблицу GMPNA")
        b_clear_gmpna.resize(80,23)
        b_clear_gmpna.move(b_width_two + 360, b_height + 135) 
        b_clear_gmpna.clicked.connect(self.clear_gmpna_tabl)
        # UMPNA
        l_umpna = QLabel('UMPNA:', tab_3)
        l_umpna.move(b_width_one + 546, l_height)
        self.l_count_NA = QLineEdit(tab_3, placeholderText='4', clearButtonEnabled=True)
        self.l_count_NA.setToolTip('Укажи количество НА (по умолчанию 4)')
        self.l_count_NA.setStyleSheet('border: 1px solid; border-radius: 3px;')
        self.l_count_NA.move(b_width_two + 540, l_height)
        self.l_count_NA.resize(80,15)
        b_umpna_basket = QPushButton('Заполнить', tab_3)
        b_umpna_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_umpna_basket.setToolTip('''Насосные агрегаты UMPNA:
        - Если таблица пустая -> добавятся и заполнятся новые ряды = количеству агрегатов;
        - Если количество рядов < количества агрегатов -> существующие обновятся или останутся без изменения, недостающие добавятся и заполнятся;
        - Если количество рядов = количеству агрегатов -> обновятся или останутся без изменения''')
        b_umpna_basket.resize(80,23)
        b_umpna_basket.move(b_width_one + 540, b_height) 
        b_umpna_basket.clicked.connect(self.filling_umpna)
        b_clear_umpna = QPushButton('Очистить', tab_3)
        b_clear_umpna.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_umpna.setToolTip("Очистить таблицу Насосные агрегаты UMPNA")
        b_clear_umpna.resize(80,23)
        b_clear_umpna.move(b_width_two + 540, b_height) 
        b_clear_umpna.clicked.connect(self.clear_umpna_tabl)
        # tmNA_UMPNA
        l_tm_umpna = QLabel('UMPNA_tm:', tab_3)
        l_tm_umpna.move(b_width_one + 728, l_height)
        b_tm_umpna_basket = QPushButton('Заполнить', tab_3)
        b_tm_umpna_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_tm_umpna_basket.setToolTip('''Временные уставки UMPNA.
        Должна быть заполнена таблица UMPNA, откуда берется название и по умолчанию добавляются уставки.
        Проверки нет! Для нового заполнения необходимо очистить таблицу, иначе новые записи добавятся в конец таблицы!''')
        b_tm_umpna_basket.resize(80,23)
        b_tm_umpna_basket.move(b_width_one + 720, b_height) 
        b_tm_umpna_basket.clicked.connect(self.filling_tmNA_umpna)
        b_clear_tm_umpna = QPushButton('Очистить', tab_3)
        b_clear_tm_umpna.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_tm_umpna.setToolTip("Очистить таблицу Временные уставки UMPNA")
        b_clear_tm_umpna.resize(80,23)
        b_clear_tm_umpna.move(b_width_two + 720, b_height) 
        b_clear_tm_umpna.clicked.connect(self.clear_tmNA_umpna_tabl)
        # tmNA_narab_UMPNA
        l_tm_umpna = QLabel('UMPNA_narab_tm:', tab_3)
        l_tm_umpna.move(b_width_one + 182, l_height + 180)
        b_tm_umpna_basket = QPushButton('Заполнить', tab_3)
        b_tm_umpna_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_tm_umpna_basket.setToolTip('''Временные уставки наработки UMPNA.
        Должна быть заполнена таблица UMPNA, откуда берется название и по умолчанию добавляются уставки.
        Проверки нет! Для нового заполнения необходимо очистить таблицу, иначе новые записи добавятся в конец таблицы!''')
        b_tm_umpna_basket.resize(80,23)
        b_tm_umpna_basket.move(b_width_one + 180, b_height + 180) 
        b_tm_umpna_basket.clicked.connect(self.filling_tmNA_umpna_narab)
        b_clear_tm_umpna = QPushButton('Очистить', tab_3)
        b_clear_tm_umpna.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_tm_umpna.setToolTip("Очистить таблицу Временные уставки UMPNA")
        b_clear_tm_umpna.resize(80,23)
        b_clear_tm_umpna.move(b_width_two + 180, b_height + 180) 
        b_clear_tm_umpna.clicked.connect(self.clear_tmNA_umpna_narab_tabl)
        # TM_TS
        l_tm_ts = QLabel('TM_TS:', tab_3)
        l_tm_ts.move(b_width_one + 364, l_height + 180)
        b_tm_ts_basket = QPushButton('Подготовить', tab_3)
        b_tm_ts_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_tm_ts_basket.setToolTip('''Подготавливается таблица на 2544 строки''')
        b_tm_ts_basket.resize(80,23)
        b_tm_ts_basket.move(b_width_one + 360, b_height + 180) 
        b_tm_ts_basket.clicked.connect(self.filling_tmts)
        b_clear_tm_ts = QPushButton('Очистить', tab_3)
        b_clear_tm_ts.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_tm_ts.setToolTip("Очистить таблицу Телемеханика - ТС")
        b_clear_tm_ts.resize(80,23)
        b_clear_tm_ts.move(b_width_two + 360, b_height + 180) 
        b_clear_tm_ts.clicked.connect(self.clear_tmts_tabl)
        # TM_TI4
        l_tm_ti4 = QLabel('TM_TI4:', tab_3)
        l_tm_ti4.move(b_width_one + 364, l_height + 220)
        b_tm_ti4_basket = QPushButton('Подготовить', tab_3)
        b_tm_ti4_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_tm_ti4_basket.setToolTip('''Подготавливается таблица на 108 строки''')
        b_tm_ti4_basket.resize(80,23)
        b_tm_ti4_basket.move(b_width_one + 360, b_height + 215) 
        b_tm_ti4_basket.clicked.connect(self.filling_tmti4)
        b_clear_tm_ti4 = QPushButton('Очистить', tab_3)
        b_clear_tm_ti4.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_tm_ti4.setToolTip("Очистить таблицу Телемеханика - ТИ4")
        b_clear_tm_ti4.resize(80,23)
        b_clear_tm_ti4.move(b_width_two + 360, b_height + 215) 
        b_clear_tm_ti4.clicked.connect(self.clear_tmti4_tabl)
        # TM_TI2
        l_tm_ti2 = QLabel('TM_TI2:', tab_3)
        l_tm_ti2.move(b_width_one + 546, l_height + 220)
        b_tm_ti2_basket = QPushButton('Подготовить', tab_3)
        b_tm_ti2_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_tm_ti2_basket.setToolTip('''Подготавливается таблица на 50 строк''')
        b_tm_ti2_basket.resize(80,23)
        b_tm_ti2_basket.move(b_width_one + 540, b_height + 215) 
        b_tm_ti2_basket.clicked.connect(self.filling_tmti2)
        b_clear_tm_ti2 = QPushButton('Очистить', tab_3)
        b_clear_tm_ti2.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_tm_ti2.setToolTip("Очистить таблицу Телемеханика - ТИ2")
        b_clear_tm_ti2.resize(80,23)
        b_clear_tm_ti2.move(b_width_two + 540, b_height + 215) 
        b_clear_tm_ti2.clicked.connect(self.clear_tmti2_tabl)
        # TM_TII
        l_tm_tii = QLabel('TM_TII:', tab_3)
        l_tm_tii.move(b_width_one + 546, l_height + 180)
        b_tm_tii_basket = QPushButton('Подготовить', tab_3)
        b_tm_tii_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_tm_tii_basket.setToolTip('''Подготавливается таблица на 54 строк''')
        b_tm_tii_basket.resize(80,23)
        b_tm_tii_basket.move(b_width_one + 540, b_height + 180) 
        b_tm_tii_basket.clicked.connect(self.filling_tmtii)
        b_clear_tm_tii = QPushButton('Очистить', tab_3)
        b_clear_tm_tii.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_tm_tii.setToolTip("Очистить таблицу Телемеханика - ТИИ")
        b_clear_tm_tii.resize(80,23)
        b_clear_tm_tii.move(b_width_two + 540, b_height + 180) 
        b_clear_tm_tii.clicked.connect(self.clear_tmtii_tabl)
        # TM_TU
        l_tm_tu = QLabel('TM_TU:', tab_3)
        l_tm_tu.move(b_width_one + 728, l_height + 180)
        b_tm_tu_basket = QPushButton('Подготовить', tab_3)
        b_tm_tu_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_tm_tu_basket.setToolTip('''Подготавливается таблица на 240 строк''')
        b_tm_tu_basket.resize(80,23)
        b_tm_tu_basket.move(b_width_one + 720, b_height + 180) 
        b_tm_tu_basket.clicked.connect(self.filling_tmtu)
        b_clear_tm_tu = QPushButton('Очистить', tab_3)
        b_clear_tm_tu.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_tm_tu.setToolTip("Очистить таблицу Телемеханика - ТУ")
        b_clear_tm_tu.resize(80,23)
        b_clear_tm_tu.move(b_width_two + 720, b_height + 180) 
        b_clear_tm_tu.clicked.connect(self.clear_tmtu_tabl)
        # TM_TR4
        l_tm_tr4 = QLabel('TM_TR4:', tab_3)
        l_tm_tr4.move(b_width_one + 728, l_height + 220)
        b_tm_tr4_basket = QPushButton('Подготовить', tab_3)
        b_tm_tr4_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_tm_tr4_basket.setToolTip('''Подготавливается таблица на 10 строк''')
        b_tm_tr4_basket.resize(80,23)
        b_tm_tr4_basket.move(b_width_one + 720, b_height + 215) 
        b_tm_tr4_basket.clicked.connect(self.filling_tmtr4)
        b_clear_tm_tr4 = QPushButton('Очистить', tab_3)
        b_clear_tm_tr4.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_tm_tr4.setToolTip("Очистить таблицу Телемеханика - ТP4")
        b_clear_tm_tr4.resize(80,23)
        b_clear_tm_tr4.move(b_width_two + 720, b_height + 215) 
        b_clear_tm_tr4.clicked.connect(self.clear_tmtr4_tabl)
        # TM_TR2
        l_tm_tr2 = QLabel('TM_TR2:', tab_3)
        l_tm_tr2.move(b_width_one + 910, l_height + 180)
        b_tm_tr2_basket = QPushButton('Подготовить', tab_3)
        b_tm_tr2_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_tm_tr2_basket.setToolTip('''Подготавливается таблица на 10 строк''')
        b_tm_tr2_basket.resize(80,23)
        b_tm_tr2_basket.move(b_width_one + 900, b_height + 180) 
        b_tm_tr2_basket.clicked.connect(self.filling_tmtr2)
        b_clear_tm_tr2 = QPushButton('Очистить', tab_3)
        b_clear_tm_tr2.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_tm_tr2.setToolTip("Очистить таблицу Телемеханика - ТP2")
        b_clear_tm_tr2.resize(80,23)
        b_clear_tm_tr2.move(b_width_two + 900, b_height + 180) 
        b_clear_tm_tr2.clicked.connect(self.clear_tmtr2_tabl)
        # ZD
        l_zd = QLabel('ZD:', tab_3)
        l_zd.move(b_width_one + 546, l_height + 45)
        b_zd_basket = QPushButton('Заполнить', tab_3)
        b_zd_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_zd_basket.setToolTip('''Заполнить или обновить данные таблицы Задвижки(ZD):
        Название задвижки определяется по тире(дефис) "-", если в строке 2 тире(дефиса) " - *** - " вероятнее всего название получится неккоректное -> данная задвижка не заполнится!
        Необходимо поправить сигналы названия задвижки в таблицах Signals, а затем в DI и DO, либо заполнить вручную!
        Могут заполниться столбцы: 
        ** КВО, КВЗ, МПО, МПЗ, Муфта, Авария_привода, Дист_ф, ВММО, ВММЗ, Закрыть_с_БРУ, Стоп_с_БРУ, Напряжение, Исправность_цепей_открытия, 
        ** Исправность_цепей_закрытия, Открыть, Закрыть, Остановить, Открытие_остановить, Закрытие_остановить;
        - Если таблица пустая -> добавятся и заполнятся новые ряды = найденным задвижкам(поиск происходит по тегам РД!);
        - Если появилась новая задвижка то добавится в конец таблицы;
        - Если есть изменения у задвижки в таблице DI или DO -> они будут найдены и заменены на новые;
        - Если задвижка больше не существует в проекте -> будет сообщение, что задвижки не существует!''')
        b_zd_basket.resize(80,23)
        b_zd_basket.move(b_width_one + 540, b_height + 45) 
        b_zd_basket.clicked.connect(self.filling_valves)
        b_clear_zd = QPushButton('Очистить', tab_3)
        b_clear_zd.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_zd.setToolTip("Очистить таблицу ZD")
        b_clear_zd.resize(80,23)
        b_clear_zd.move(b_width_two + 540, b_height + 45) 
        b_clear_zd.clicked.connect(self.clear_valves_tabl)
        # tmZD
        l_tmzd = QLabel('ZD_tm:', tab_3)
        l_tmzd.move(b_width_one + 728, l_height + 45)
        b_tm_zd_basket = QPushButton('Заполнить', tab_3)
        b_tm_zd_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_tm_zd_basket.setToolTip('''Временные уставки ZD.
        Должна быть заполнена таблица ZD, откуда берется название и по умолчанию добавляются уставки.
        Проверки нет! Для нового заполнения необходимо очистить таблицу, иначе новые записи добавятся в конец таблицы!''')
        b_tm_zd_basket.resize(80,23)
        b_tm_zd_basket.move(b_width_one + 720, b_height + 45) 
        b_tm_zd_basket.clicked.connect(self.filling_tmzd)
        b_clear_tm_zd = QPushButton('Очистить', tab_3)
        b_clear_tm_zd.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_tm_zd.setToolTip("Очистить таблицу Временные уставки ZD")
        b_clear_tm_zd.resize(80,23)
        b_clear_tm_zd.move(b_width_two + 720, b_height + 45) 
        b_clear_tm_zd.clicked.connect(self.clear_tmzd_tabl)
        # VS
        l_vs = QLabel('VS:', tab_3)
        l_vs.move(b_width_one + 546, l_height + 90)
        b_vs_basket = QPushButton('Заполнить', tab_3)
        b_vs_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_vs_basket.setToolTip('''Заполнить или обновить данные таблицы Вспомсистемы VS:
        Название вспомсистемы определяется по тире(дефис) "-", если в строке 2 тире(дефиса) " - *** - " вероятнее всего название получится неккоректное -> данная вспомсистема не заполнится!
        Необходимо поправить сигналы названия вспомсистемы в таблицах Signals, а затем в DI и DO, либо заполнить вручную!
        Могут заполниться столбцы: Группы впомсистем не заполняются!
        ** МП, Напряжение, Включить, Отключить, Внешняя авария, Исправность цепей открытия, Давление(может некорректно заполниться!);
        - Если таблица пустая -> добавятся и заполнятся новые ряды = найденным вспомсистемам(поиск происходит по тегам РД!);
        - Если появилась новая вспомсистема то добавится в конец таблицы;
        - Если есть изменения у вспомсистемы в таблице DI или DO -> они будут найдены и заменены на новые;
        - Если вспомсистемы больше не существует в проекте -> будет сообщение, что вспомсистемы не существует!''')
        b_vs_basket.resize(80,23)
        b_vs_basket.move(b_width_one + 540, b_height + 90) 
        b_vs_basket.clicked.connect(self.filling_vs)
        b_clear_vs = QPushButton('Очистить', tab_3)
        b_clear_vs.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_vs.setToolTip("Очистить таблицу VS")
        b_clear_vs.resize(80,23)
        b_clear_vs.move(b_width_two + 540, b_height + 90) 
        b_clear_vs.clicked.connect(self.clear_vs_tabl)
        # tmVS
        l_tmvs = QLabel('VS_tm:', tab_3)
        l_tmvs.move(b_width_one + 728, l_height + 90)
        b_tm_vs_basket = QPushButton('Заполнить', tab_3)
        b_tm_vs_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_tm_vs_basket.setToolTip('''Временные уставки VS.
        Должна быть заполнена таблица VS, откуда берется название и по умолчанию добавляются уставки.
        Проверки нет! Для нового заполнения необходимо очистить таблицу, иначе новые записи добавятся в конец таблицы!''')
        b_tm_vs_basket.resize(80,23)
        b_tm_vs_basket.move(b_width_one + 720, b_height + 90) 
        b_tm_vs_basket.clicked.connect(self.filling_tmvs)
        b_clear_tm_vs = QPushButton('Очистить', tab_3)
        b_clear_tm_vs.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_tm_vs.setToolTip("Очистить таблицу Временные уставки VS")
        b_clear_tm_vs.resize(80,23)
        b_clear_tm_vs.move(b_width_two + 720, b_height + 90) 
        b_clear_tm_vs.clicked.connect(self.clear_tmvs_tabl)
        # VSGRP
        l_vsgrp = QLabel('VSGRP:', tab_3)
        l_vsgrp.move(b_width_one + 546, l_height + 135)
        b_vsgrp_basket = QPushButton('Подготовить', tab_3)
        b_vsgrp_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_vsgrp_basket.setToolTip('''Группы вспомсистем VSGRP. Таблица не заполняется! 
        - Если отсутствует в базе, то добавиться новая таблица''')
        b_vsgrp_basket.resize(80,23)
        b_vsgrp_basket.move(b_width_one + 540, b_height + 135) 
        b_vsgrp_basket.clicked.connect(self.filling_vsgrp)
        b_clear_vsgrp = QPushButton('Очистить', tab_3)
        b_clear_vsgrp.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_vsgrp.setToolTip("Очистить таблицу VSGRP")
        b_clear_vsgrp.resize(80,23)
        b_clear_vsgrp.move(b_width_two + 540, b_height + 135) 
        b_clear_vsgrp.clicked.connect(self.clear_vsgrp_tabl)
        # tmVSGRP
        l_tmvsgrp = QLabel('VSGRP_tm:', tab_3)
        l_tmvsgrp.move(b_width_one + 728, l_height + 135)
        b_tm_vsgrp_basket = QPushButton('Заполнить', tab_3)
        b_tm_vsgrp_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_tm_vsgrp_basket.setToolTip('''Временные уставки VSGRP.
        Должна быть заполнена таблица VSGRP, откуда берется название и по умолчанию добавляются уставки.
        Проверки нет! Для нового заполнения необходимо очистить таблицу, иначе новые записи добавятся в конец таблицы!''')
        b_tm_vsgrp_basket.resize(80,23)
        b_tm_vsgrp_basket.move(b_width_one + 720, b_height + 135) 
        b_tm_vsgrp_basket.clicked.connect(self.filling_tmvsgrp)
        b_clear_tm_vsgrp = QPushButton('Очистить', tab_3)
        b_clear_tm_vsgrp.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_tm_vsgrp.setToolTip("Очистить таблицу Временные уставки VSGRP")
        b_clear_tm_vsgrp.resize(80,23)
        b_clear_tm_vsgrp.move(b_width_two + 720, b_height + 135) 
        b_clear_tm_vsgrp.clicked.connect(self.clear_tmvsgrp_tabl)
        # PI
        l_pi = QLabel('PI:', tab_3)
        l_pi.move(b_width_one + 910, l_height)
        b_pi_basket = QPushButton('Заполнить', tab_3)
        b_pi_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_pi_basket.setToolTip('''Заполнить или обновить данные таблицы Пожарные извещатели PI:
        Название определяется по ключевым словам в таблице AI !
        Могут заполниться столбцы:
        ** Идентификатор, Название, Тип ПИ, Пожар, Внимание, Загрязнение стекла, Неисправность/КЗ, Сброс ссылка;
        - Если таблица пустая -> добавятся и заполнятся новые ряды = найденным ПИ(поиск происходит по ключевым словам);
        - Если появился новаый ПИ то добавится в конец таблицы;
        - Если есть изменения у ПИ в таблице AI или DO -> они будут найдены и заменены на новые.''')
        b_pi_basket.resize(80,23)
        b_pi_basket.move(b_width_one + 900, b_height) 
        b_pi_basket.clicked.connect(self.filling_pi)
        b_clear_pi = QPushButton('Очистить', tab_3)
        b_clear_pi.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_pi.setToolTip("Очистить таблицу PI")
        b_clear_pi.resize(80,23)
        b_clear_pi.move(b_width_two + 900, b_height) 
        b_clear_pi.clicked.connect(self.clear_pi_tabl)
        # tmPZ
        l_tmpz = QLabel('PZ_tm:', tab_3)
        l_tmpz.move(b_width_one + 910, l_height + 45)
        b_tm_pz_basket = QPushButton('Заполнить', tab_3)
        b_tm_pz_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_tm_pz_basket.setToolTip('''Временные уставки PZ.
        Должна быть заполнена таблица PZ, откуда берется название и по умолчанию добавляются уставки.
        Проверки нет! Для нового заполнения необходимо очистить таблицу, иначе новые записи добавятся в конец таблицы!''')
        b_tm_pz_basket.resize(80,23)
        b_tm_pz_basket.move(b_width_one + 900, b_height + 45) 
        b_tm_pz_basket.clicked.connect(self.filling_tmpz)
        b_clear_tm_pz = QPushButton('Очистить', tab_3)
        b_clear_tm_pz.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_tm_pz.setToolTip("Очистить таблицу Временные уставки PZ")
        b_clear_tm_pz.resize(80,23)
        b_clear_tm_pz.move(b_width_two + 900, b_height + 45) 
        b_clear_tm_pz.clicked.connect(self.clear_tmpz_tabl)
        # KTPRP
        l_ktprp = QLabel('KTPRP:', tab_3)
        l_ktprp.move(b_width_one + 910, l_height + 90)
        b_ktprp_basket = QPushButton('Подготовить', tab_3)
        b_ktprp_basket.setStyleSheet("background: #bfd6bf; border: 1px solid; border-radius: 3px;")
        b_ktprp_basket.setToolTip('''Защиты по пожару. Таблица не заполняется! 
        - Если отсутствует в базе, то добавиться новая, со строками на 30 защит''')
        b_ktprp_basket.resize(80,23)
        b_ktprp_basket.move(b_width_one + 900, b_height + 90) 
        b_ktprp_basket.clicked.connect(self.filling_ktprp)
        b_clear_ktprp = QPushButton('Очистить', tab_3)
        b_clear_ktprp.setStyleSheet("background: #bbbabf; border: 1px solid; border-radius: 3px;")
        b_clear_ktprp.setToolTip("Очистить таблицу KTPRP")
        b_clear_ktprp.resize(80,23)
        b_clear_ktprp.move(b_width_two + 900, b_height + 90) 
        b_clear_ktprp.clicked.connect(self.clear_ktprp_tabl)

        # ------------------Сообщения------------------
        self.list_gen_msg = []
        self.gen_sql = Generate_database_SQL()
        # Диагностика
        l_msg_desc = QLabel('Сообщения', tab_4)
        l_msg_desc.move(150, 5)
        l_tabl_desc = QLabel('Таблицы', tab_4)
        l_tabl_desc.move(750, 5)
        
        l_diagn = QLabel('Диагностика: ', tab_4)
        l_diagn.move(10, 20)
        self.q_check_ai = QCheckBox('AI', tab_4)
        self.q_check_ai.setToolTip('''tag: AI''')
        self.q_check_ai.move(10, 35) 
        self.q_check_ai.stateChanged.connect(self.check_ai)
        self.q_check_di = QCheckBox('DI', tab_4)
        self.q_check_di.setToolTip('''tag: DI''')
        self.q_check_di.move(10, 51) 
        self.q_check_di.stateChanged.connect(self.check_di)
        self.q_check_do = QCheckBox('DO', tab_4)
        self.q_check_do.setToolTip('''tag: DOP''')
        self.q_check_do.move(10, 67) 
        self.q_check_do.stateChanged.connect(self.check_do)
        self.q_check_uso = QCheckBox('Диагностика', tab_4)
        self.q_check_uso.setToolTip('''tag: DiagMod, DiagCPUKC, DiagCPU, DiagMN, DiagCN, DiagRS, DiagEthEx''')
        self.q_check_uso.move(10, 83) 
        self.q_check_uso.stateChanged.connect(self.check_diag)
        self.q_check_ss = QCheckBox('Смежные\nсистемы', tab_4)
        self.q_check_ss.setToolTip('''tag: DiagSS\nTblD_RelatedSystems.xml''')
        self.q_check_ss.move(10, 99) 
        self.q_check_ss.stateChanged.connect(self.check_ss)
        # Оборудование
        l_equip = QLabel('Оборудование: ', tab_4)
        l_equip.move(140, 20)
        self.q_check_zd = QCheckBox('ZD', tab_4)
        self.q_check_zd.setToolTip('''tag: ZD''')
        self.q_check_zd.move(100, 35) 
        self.q_check_zd.stateChanged.connect(self.check_zd)
        self.q_check_vs = QCheckBox('VS', tab_4)
        self.q_check_vs.setToolTip('''tag: VS''')
        self.q_check_vs.move(100, 51) 
        self.q_check_vs.stateChanged.connect(self.check_vs)
        self.q_check_other = QCheckBox('Прочие', tab_4)
        self.q_check_other.setToolTip(''''Генерация без шаблона!\ntag: Others''')
        self.q_check_other.move(100, 67) 
        self.q_check_other.stateChanged.connect(self.check_others)
        self.q_check_global = QCheckBox('Общие', tab_4)
        self.q_check_global.setToolTip('''tag: Global''')
        self.q_check_global.move(100, 83) 
        self.q_check_global.stateChanged.connect(self.check_global)

        self.q_check_nps = QCheckBox('НПС', tab_4)
        self.q_check_nps.setToolTip(''''tag: KRMPN, NPS\ntabl:TblStationCommonKRMPN, TblNPS.xml''')
        self.q_check_nps.move(160, 35) 
        self.q_check_nps.stateChanged.connect(self.check_nps)
        self.q_check_umpna = QCheckBox('UMPNA', tab_4)
        self.q_check_umpna.setToolTip(''''tag: UMPNA, KTPRAS_1\nTblPumpsCMNA.xml\nTblPumpsUMPNA.xml\nTblPumpsKTPRAS.xml''')
        self.q_check_umpna.move(160, 51) 
        self.q_check_umpna.stateChanged.connect(self.check_umpna)
        self.q_check_uts = QCheckBox('UTS', tab_4)
        self.q_check_uts.setToolTip('''Подбор шаблона по ключевым словам: звонок, табло, сирена, сирены, сигнализация\nTblSignalingDevices.xml\nTblSignalingDevicesFemale.xml\nTblSignalingDevicesMale.xml\nTblSignalingDevicesMany.xml''')
        self.q_check_uts.move(160, 67) 
        self.q_check_uts.stateChanged.connect(self.check_uts) 
        self.q_check_vv = QCheckBox('VV', tab_4)
        self.q_check_vv.setToolTip('''TblHighVoltageSwitches.xml''')
        self.q_check_vv.move(160, 83) 
        self.q_check_vv.stateChanged.connect(self.check_vv)
        self.q_check_dps = QCheckBox('DPS', tab_4)
        self.q_check_dps.setToolTip('''TblPigSignallers.xml''')
        self.q_check_dps.move(160, 99) 
        self.q_check_dps.stateChanged.connect(self.check_dps)
        self.q_check_tmdp = QCheckBox('TM_DP', tab_4)
        self.q_check_tmdp.setToolTip('''TblD_TM_DP.xml''')
        self.q_check_tmdp.move(160, 115) 
        self.q_check_tmdp.stateChanged.connect(self.check_tmdp)
        
        self.q_check_pi = QCheckBox('PI', tab_4)
        self.q_check_pi.setToolTip(''' ''')
        self.q_check_pi.move(220, 35) 
        self.q_check_pi.stateChanged.connect(self.check_pi)
        self.q_check_pz = QCheckBox('PZ', tab_4)
        self.q_check_pz.setToolTip(''' ''')
        self.q_check_pz.move(220, 51) 
        self.q_check_pz.stateChanged.connect(self.check_pz)
        self.q_check_upts = QCheckBox('UPTS', tab_4)
        self.q_check_upts.setToolTip('''tag: UPTS\ntabl: TblFireSignalingDevices.xml''')
        self.q_check_upts.move(220, 67) 
        self.q_check_upts.stateChanged.connect(self.check_upts)
        self.q_check_upts.setToolTip('''Подбор шаблона по ключевым словам: звонок, табло, сирена, сирены, сигнализация\nTblSignalingDevices.xml\nTblSignalingDevicesFemale.xml\nTblSignalingDevicesMale.xml\nTblSignalingDevicesMany.xml''')
        self.q_check_bd = QCheckBox('BD', tab_4)
        self.q_check_bd.setToolTip('''tag:BD\ntabl:TblTankDispensers.xml''')
        self.q_check_bd.move(220, 83) 
        self.q_check_bd.stateChanged.connect(self.check_bd)
        self.q_check_bdgrp = QCheckBox('BDGRP', tab_4)
        self.q_check_bdgrp.setToolTip('''tag:BDGRP\ntabl:TblTankDispenserGroups''')
        self.q_check_bdgrp.move(220, 99) 
        self.q_check_bdgrp.stateChanged.connect(self.check_bdgrp)
        # Защиты, готовности
        l_protect = QLabel('Защиты,\nготовности: ', tab_4)
        l_protect.move(300, 20)
        self.q_check_ktpr = QCheckBox('KTPR', tab_4)
        self.q_check_ktpr.setToolTip('''TblStationDefences.xml''')
        self.q_check_ktpr.move(300, 50) 
        self.q_check_ktpr.stateChanged.connect(self.check_ktpr)
        self.q_check_ktprp = QCheckBox('KTPRP', tab_4)
        self.q_check_ktprp.setToolTip('''TblFireDefences.xml''')
        self.q_check_ktprp.move(300, 66) 
        self.q_check_ktprp.stateChanged.connect(self.check_ktprp)
        self.q_check_ktpra = QCheckBox('KTPRA', tab_4)
        self.q_check_ktpra.setToolTip('''TblPumpDefences.xml''')
        self.q_check_ktpra.move(300, 82) 
        self.q_check_ktpra.stateChanged.connect(self.check_ktpra)
        self.q_check_ktprs = QCheckBox('KTPRS', tab_4)
        self.q_check_ktprs.setToolTip('''TblLimitParameters.xml''')
        self.q_check_ktprs.move(300, 98) 
        self.q_check_ktprs.stateChanged.connect(self.check_ktprs)
        self.q_check_gmpna = QCheckBox('GMPNA', tab_4)
        self.q_check_gmpna.setToolTip('''TblPumpReadineses.xml''')
        self.q_check_gmpna.move(300, 114) 
        self.q_check_gmpna.stateChanged.connect(self.check_gmpna)

        # Таблицы
        self.list_gen_tabl = []
        self.q_check_ai_tabl = QCheckBox('TblAnalogs', tab_4)
        self.q_check_ai_tabl.setToolTip('''Название файла скрипта: TblAnalogs''')
        self.q_check_ai_tabl.move(530, 25) 
        self.q_check_ai_tabl.stateChanged.connect(self.check_ai_tabl)
        self.q_check_zd_tabl = QCheckBox('TblValveTimeSetpoints', tab_4)
        self.q_check_zd_tabl.setToolTip('''Название файла скрипта: TblValveTimeSetpoints''')
        self.q_check_zd_tabl.move(530, 41) 
        self.q_check_zd_tabl.stateChanged.connect(self.check_zd_tabl)
        self.q_check_vs_tabl = QCheckBox('TblAuxSysTimeSetpoints', tab_4)
        self.q_check_vs_tabl.setToolTip('''Название файла скрипта: TblAuxSysTimeSetpoints''')
        self.q_check_vs_tabl.move(530, 57) 
        self.q_check_vs_tabl.stateChanged.connect(self.check_vs_tabl)
        self.q_check_vsgrp_tabl = QCheckBox('TblAuxsysgrouptimeSetpoints', tab_4)
        self.q_check_vsgrp_tabl.setToolTip('''Название файла скрипта: TblAuxsysgrouptimeSetpoints''')
        self.q_check_vsgrp_tabl.move(530, 73) 
        self.q_check_vsgrp_tabl.stateChanged.connect(self.check_vsgrp_tabl)
        self.q_check_pupm_tabl = QCheckBox('TblPumpTimeSetpoints', tab_4)
        self.q_check_pupm_tabl.setToolTip('''Название файла скрипта: TblPumpTimeSetpoints''')
        self.q_check_pupm_tabl.move(710, 25) 
        self.q_check_pupm_tabl.stateChanged.connect(self.check_pump_tabl)
        self.q_check_pupm_time_tabl = QCheckBox('TblOpTimeSetpoints', tab_4)
        self.q_check_pupm_time_tabl.setToolTip('''Название файла скрипта: TblOpTimeSetpoints''')
        self.q_check_pupm_time_tabl.move(710, 41) 
        self.q_check_pupm_time_tabl.stateChanged.connect(self.check_pump_time_tabl)
        self.q_check_uts_tabl = QCheckBox('TblSignalingdevicetimeSetpoints', tab_4)
        self.q_check_uts_tabl.setToolTip('''Название файла скрипта: TblSignalingdevicetimeSetpoints''')
        self.q_check_uts_tabl.move(710, 57) 
        self.q_check_uts_tabl.stateChanged.connect(self.check_uts_tabl)
        self.q_check_prj_tabl = QCheckBox('TblProjecttimeSetpoints', tab_4)
        self.q_check_prj_tabl.setToolTip('''Название файла скрипта: TblProjecttimeSetpoints''')
        self.q_check_prj_tabl.move(710, 73) 
        self.q_check_prj_tabl.stateChanged.connect(self.check_prj_tabl)
        self.q_check_pz_tabl = QCheckBox('TblFirezonetimeSetpoints', tab_4)
        self.q_check_pz_tabl.setToolTip('''Название файла скрипта: TblFirezonetimeSetpoints''')
        self.q_check_pz_tabl.move(710, 89) 
        self.q_check_pz_tabl.stateChanged.connect(self.check_pz_tabl)

        self.q_check_ktpr_tabl = QCheckBox('TblStationDefencesSetpoints', tab_4)
        self.q_check_ktpr_tabl.setToolTip('''Название файла скрипта: TblStationDefencesSetpoints''')
        self.q_check_ktpr_tabl.move(900, 25) 
        self.q_check_ktpr_tabl.stateChanged.connect(self.check_ktpr_tabl)
        self.q_check_ktpra_tabl = QCheckBox('TblPumpDefencesSetpoints', tab_4)
        self.q_check_ktpra_tabl.setToolTip('''Название файла скрипта: TblPumpDefencesSetpoints''')
        self.q_check_ktpra_tabl.move(900, 41) 
        self.q_check_ktpra_tabl.stateChanged.connect(self.check_ktpra_tabl)
        self.q_check_gmpna_tabl = QCheckBox('TblPumpreadinesesSetpoints', tab_4)
        self.q_check_gmpna_tabl.setToolTip('''Название файла скрипта: TblPumpreadinesesSetpoints''')
        self.q_check_gmpna_tabl.move(900, 57) 
        self.q_check_gmpna_tabl.stateChanged.connect(self.check_gmpna_tabl)

        # Установить все
        check_all = QCheckBox('Установить/Снять', tab_4)
        check_all.setToolTip('Установить или снять все флаги')
        check_all.move(10, 140) 
        check_all.stateChanged.connect(self.check_all)
        # Подтверждение msg
        b_export_list = QPushButton('Файл импорта', tab_4)
        b_export_list.setStyleSheet("border: 1px solid; border-radius: 3px;")
        b_export_list.setToolTip('''Создается отдельный файл таблиц для ручной генерации базы данных PostgreSQL''')
        b_export_list.resize(120,23)
        b_export_list.move(10, 180) 
        b_export_list.clicked.connect(self.export_list)
        b_export_sql = QPushButton('Генерировать в базу', tab_4)
        b_export_sql.setStyleSheet("border: 1px solid; border-radius: 3px;")
        b_export_sql.setToolTip('''Схема: messages\nТаблица: opmessages\nТаблица должна существовать. Повторяющиеся строки удаляются, и добавляются новые''')
        b_export_sql.resize(120,23)
        b_export_sql.move(150, 180) 
        b_export_sql.clicked.connect(self.write_in_sql)
        # Подтверждение tabl
        b_export_list_tabl = QPushButton('Файл импорта', tab_4)
        b_export_list_tabl.setStyleSheet("border: 1px solid; border-radius: 3px;")
        b_export_list_tabl.setToolTip('''Создается отдельный файл таблиц для ручной генерации базы данных PostgreSQL''')
        b_export_list_tabl.resize(120,23)
        b_export_list_tabl.move(650, 115) 
        b_export_list_tabl.clicked.connect(self.export_list_tabl)
        b_export_sql_tabl = QPushButton('Генерировать в базу', tab_4)
        b_export_sql_tabl.setStyleSheet("border: 1px solid; border-radius: 3px;")
        b_export_sql_tabl.setToolTip('''Схема: objects\nСуществующая таблица чиститься, если нет, создается новая и заполняется''')
        b_export_sql_tabl.resize(120,23)
        b_export_sql_tabl.move(800, 115) 
        b_export_sql_tabl.clicked.connect(self.write_in_sql_tabl)

        # Logs
        self.logTextBox = QTextEdit(self)
        #self.logTextBox.setStyleSheet("border-radius: 4px; border: 1px solid")
        self.logTextBox.setGeometry(5,284,1083,110)
        self.logTextBox.setReadOnly(True)
        self.logs_msg(f'Запущено меню разработки проекта', 1)

        # Загружаем пути проекта
        self.path_file_prj()
    # ------------------Соединение------------------
    def check_base_sql_msg(self):
        connect = self.gen_sql.check_database_connect(database_msg, user_msg, password_msg, host_msg, port_msg)
        if connect is True:
            self.l_sql_msg_check.setText('Установлено')
            self.l_sql_msg_check.setStyleSheet("background-color: lightgreen")
        else:
            self.l_sql_msg_check.setText('Не установлено')
            self.l_sql_msg_check.setStyleSheet("background-color: red")
    def check_base_sql_ust(self):
        connect =self.gen_sql.check_database_connect(database_prj, user_prj, password_prj, host_prj, port_prj)
        if connect is True:
            self.l_sql_ust_check.setText('Установлено')
            self.l_sql_ust_check.setStyleSheet("background-color: lightgreen")
        else:
            self.l_sql_ust_check.setText('Не установлено')
            self.l_sql_ust_check.setStyleSheet("background-color: red")
    # ------------------Импорт КЗФКП------------------
    def update_fill_base(self):
        try:
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
        except:
            self.logs_msg(f'Ошибка импорта', 2)
            return
    def start_fill_base(self):
        try:
            if self.сolumn_title_loaded is False: 
                # Logs
                self.logs_msg(f'Не загружена шапка таблицы!', 2)
                return
        except:
            self.logs_msg(f'Ошибка импорта', 2)
            return

        dict_column = self.hat_list()
        data_uso = self.import_sql.import_table(self.select_uso.currentText(), self.select_row.text(), dict_column)
        msg = self.import_sql.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = self.import_sql.import_for_sql(data_uso, self.select_uso.currentText())
        self.logs_msg('default', 1, msg, True)
    def path_file_prj(self):
        try:
            self.import_sql = Import_in_SQL(path_to_exel)
            # Logs
            self.logs_msg(f'Соединение с файлом КЗФКП установленно', 1)
        except:
            # Logs
            self.logs_msg(f'Соединение с файлом КЗФКП не установленно', 2)
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
    # ------------------Импорт КЗФКП------------------
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
    # KTPRP
    def filling_ktprp(self):
        ktprp_table = Filling_KTPRP()
        msg = ktprp_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = ktprp_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_ktprp_tabl(self):
        msg = self.dop_function.clear_tabl('ktprp', 'KTPRP', self.list_tabl)
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
        msg = tmNA_umpna_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_tmNA_umpna_tabl(self):
        msg = self.dop_function.clear_tabl('umpna_tm', 'tmNA_UMPNA', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # tmNA_UMPNA_narab
    def filling_tmNA_umpna_narab(self):
        tmNA_umpna_narab_table = Filling_tmNA_UMPNA_narab()
        msg = tmNA_umpna_narab_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = tmNA_umpna_narab_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_tmNA_umpna_narab_tabl(self):
        msg = self.dop_function.clear_tabl('umpna_narab_tm', 'tmNA_UMPNA_narab', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # ZD
    def filling_valves(self):
        zd_table = Filling_ZD()
        msg = zd_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = zd_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_valves_tabl(self):
        msg = self.dop_function.clear_tabl('zd', 'ZD', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # tmZD
    def filling_tmzd(self):
        tmZD_table = Filling_ZD_tm()
        msg = tmZD_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = tmZD_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_tmzd_tabl(self):
        msg = self.dop_function.clear_tabl('zd_tm', 'ZD_tm', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # VS
    def filling_vs(self):
        vs_table = Filling_VS()
        msg = vs_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = vs_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_vs_tabl(self):
        msg = self.dop_function.clear_tabl('vs', 'VS', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # tmVS
    def filling_tmvs(self):
        tmvs_table = Filling_VS_tm()
        msg = tmvs_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = tmvs_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_tmvs_tabl(self):
        msg = self.dop_function.clear_tabl('vs_tm', 'VS_tm', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # VSGRP
    def filling_vsgrp(self):
        vsgrp_table = Filling_VSGRP()
        msg = vsgrp_table.column_check()
        self.logs_msg('default', 1, msg, True)
    def clear_vsgrp_tabl(self):
        msg = self.dop_function.clear_tabl('vsgrp', 'VSGRP', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # tmVSGRP
    def filling_tmvsgrp(self):
        tmvsgrp_table = Filling_VSGRP_tm()
        msg = tmvsgrp_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = tmvsgrp_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_tmvsgrp_tabl(self):
        msg = self.dop_function.clear_tabl('vsgrp_tm', 'VSGRP_tm', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # UTS
    def filling_uts(self):
        uts_table = Filling_UTS()
        msg = uts_table.column_check(False)
        self.logs_msg('default', 1, msg, True)
        msg = uts_table.getting_modul(False)
        self.logs_msg('default', 1, msg, True)
    def clear_uts_tabl(self):
        msg = self.dop_function.clear_tabl('uts', 'UTS', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # UPTS
    def filling_upts(self):
        upts_table = Filling_UTS()
        msg = upts_table.column_check(True)
        self.logs_msg('default', 1, msg, True)
        msg = upts_table.getting_modul(True)
        self.logs_msg('default', 1, msg, True)
    def clear_upts_tabl(self):
        msg = self.dop_function.clear_tabl('upts', 'UPTS', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # tmUTS
    def filling_uts_tm(self):
        vs_table = Filling_UTS_tm()
        msg = vs_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = vs_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_uts_tm_tabl(self):
        msg = self.dop_function.clear_tabl('uts_tm', 'UTS_tm', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # VV
    def filling_vv(self):
        vv_table = Filling_VV()
        msg = vv_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = vv_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_vv_tabl(self):
        msg = self.dop_function.clear_tabl('vv', 'VV', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # VV
    def filling_pi(self):
        pi_table = Filling_PI()
        msg = pi_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = pi_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_pi_tabl(self):
        msg = self.dop_function.clear_tabl('pi', 'PI', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # tmPZ
    def filling_tmpz(self):
        pz_table = Filling_PZ_tm()
        msg = pz_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = pz_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_tmpz_tabl(self):
        msg = self.dop_function.clear_tabl('pz_tm', 'PZ_tm', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # TM_TS
    def filling_tmts(self):
        tm_ts_table = Filling_TM_TS()
        msg = tm_ts_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = tm_ts_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_tmts_tabl(self):
        msg = self.dop_function.clear_tabl('tm_ts', 'TM_TS', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # TM_TI4
    def filling_tmti4(self):
        tm_ti4_table = Filling_TM_TI4()
        msg = tm_ti4_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = tm_ti4_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_tmti4_tabl(self):
        msg = self.dop_function.clear_tabl('tm_ti4', 'TM_TI4', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # TM_TI2
    def filling_tmti2(self):
        tm_ti2_table = Filling_TM_TI2()
        msg = tm_ti2_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = tm_ti2_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_tmti2_tabl(self):
        msg = self.dop_function.clear_tabl('tm_ti2', 'TM_TI2', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # TM_TII
    def filling_tmtii(self):
        tm_tii_table = Filling_TM_TII()
        msg = tm_tii_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = tm_tii_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_tmtii_tabl(self):
        msg = self.dop_function.clear_tabl('tm_tii', 'TM_TII', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # TM_TU
    def filling_tmtu(self):
        tm_tu_table = Filling_TM_TU()
        msg = tm_tu_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = tm_tu_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_tmtu_tabl(self):
        msg = self.dop_function.clear_tabl('tm_tu', 'TM_TU', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # TM_TR4
    def filling_tmtr4(self):
        tm_tr4_table = Filling_TM_TR4()
        msg = tm_tr4_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = tm_tr4_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_tmtr4_tabl(self):
        msg = self.dop_function.clear_tabl('tm_tr4', 'TM_TR4', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # TM_TR2
    def filling_tmtr2(self):
        tm_tr2_table = Filling_TM_TR2()
        msg = tm_tr2_table.column_check()
        self.logs_msg('default', 1, msg, True)
        msg = tm_tr2_table.getting_modul()
        self.logs_msg('default', 1, msg, True)
    def clear_tmtr2_tabl(self):
        msg = self.dop_function.clear_tabl('tm_tr2', 'TM_TR2', self.list_tabl)
        self.logs_msg('default', 1, msg, True)
    # ------------------Сообщения------------------
    # Check sql
    def check_sql(self):
        connect = self.gen_sql.check_database_connect(database_msg, user_msg, password_msg, host_msg, port_msg)
        if connect is True:
            self.l_check_sql.setText('Установлено')
            self.l_check_sql.setStyleSheet("background-color: lightgreen")
        else:
            self.l_check_sql.setText('Не установлено')
            self.l_check_sql.setStyleSheet("background-color: red")
    # CheckBox
    def check_all(self, checked):
        if checked: 
            self.q_check_ai.setChecked(True)
            self.q_check_di.setChecked(True)
            self.q_check_do.setChecked(True)
            self.q_check_uso.setChecked(True)
            self.q_check_ss.setChecked(True)
            
            self.q_check_umpna.setChecked(True)
            self.q_check_dps.setChecked(True)
            self.q_check_other.setChecked(True)
            self.q_check_zd.setChecked(True)
            self.q_check_nps.setChecked(True)
            self.q_check_vs.setChecked(True)
            self.q_check_bd.setChecked(True)
            self.q_check_tmdp.setChecked(True)
            self.q_check_bdgrp.setChecked(True)
            self.q_check_global.setChecked(True)
            self.q_check_uts.setChecked(True)
            self.q_check_upts.setChecked(True)
            self.q_check_vv.setChecked(True)
            self.q_check_pi.setChecked(True)
            self.q_check_pz.setChecked(True)
            
            # self.q_check_umpna_ust.setChecked(True)
            # self.q_check_zd_ust.setChecked(True)
            # self.q_check_vs_ust.setChecked(True)
            # self.q_check_vsgrp_ust.setChecked(True)
            # self.q_check_uts_ust.setChecked(True)
            # self.q_check_pz_ust.setChecked(True)
            
            self.q_check_ktpr.setChecked(True)
            self.q_check_ktprp.setChecked(True)
            self.q_check_ktpra.setChecked(True)
            self.q_check_ktprs.setChecked(True)
            self.q_check_gmpna.setChecked(True)
        else: 
            self.q_check_ai.setChecked(False)
            self.q_check_di.setChecked(False)
            self.q_check_do.setChecked(False)
            self.q_check_uso.setChecked(False)
            self.q_check_ss.setChecked(False)
            
            self.q_check_umpna.setChecked(False)
            self.q_check_dps.setChecked(False)
            self.q_check_other.setChecked(False)
            self.q_check_zd.setChecked(False)
            self.q_check_nps.setChecked(False)
            self.q_check_tmdp.setChecked(False)
            self.q_check_vs.setChecked(False)
            self.q_check_bd.setChecked(False)
            self.q_check_global.setChecked(False)
            self.q_check_bdgrp.setChecked(False)
            self.q_check_uts.setChecked(False)
            self.q_check_upts.setChecked(False)
            self.q_check_vv.setChecked(False)
            self.q_check_pi.setChecked(False)
            self.q_check_pz.setChecked(False)
            
            # self.q_check_umpna_ust.setChecked(False)
            # self.q_check_zd_ust.setChecked(False)
            # self.q_check_vs_ust.setChecked(False)
            # self.q_check_vsgrp_ust.setChecked(False)
            # self.q_check_uts_ust.setChecked(False)
            # self.q_check_pz_ust.setChecked(False)
            
            self.q_check_ktpr.setChecked(False)
            self.q_check_ktprp.setChecked(False)
            self.q_check_ktpra.setChecked(False)
            self.q_check_ktprs.setChecked(False)
            self.q_check_gmpna.setChecked(False)
    def check_ai(self, checked):
        if checked: self.list_gen_msg.append('AI')
        else      : self.list_gen_msg.remove('AI')
    def check_di(self, checked):
        if checked: self.list_gen_msg.append('DI')
        else      : self.list_gen_msg.remove('DI')
    def check_do(self, checked):
        if checked: self.list_gen_msg.append('DO')
        else      : self.list_gen_msg.remove('DO')
    def check_ao(self, checked):
        if checked: self.list_gen_msg.append('AO')
        else      : self.list_gen_msg.remove('AO')
    def check_diag(self, checked):
        if checked: self.list_gen_msg.append('Diag')
        else      : self.list_gen_msg.remove('Diag')
    def check_ss(self, checked):
        if checked: self.list_gen_msg.append('SS')
        else      : self.list_gen_msg.remove('SS')
    def check_umpna(self, checked):
        if checked: self.list_gen_msg.append('UMPNA')
        else      : self.list_gen_msg.remove('UMPNA')
    def check_others(self, checked):
        if checked: self.list_gen_msg.append('Others')
        else      : self.list_gen_msg.remove('Others')
    def check_global(self, checked):
        if checked: self.list_gen_msg.append('Global')
        else      : self.list_gen_msg.remove('Global')
    def check_zd(self, checked):
        if checked: self.list_gen_msg.append('ZD')
        else      : self.list_gen_msg.remove('ZD')
    def check_nps(self, checked):
        if checked: self.list_gen_msg.append('NPS')
        else      : self.list_gen_msg.remove('NPS')
    def check_tmdp(self, checked):
        if checked: self.list_gen_msg.append('TM_DP')
        else      : self.list_gen_msg.remove('TM_DP')
    def check_vs(self, checked):
        if checked: self.list_gen_msg.append('VS')
        else      : self.list_gen_msg.remove('VS')
    def check_dps(self, checked):
        if checked: self.list_gen_msg.append('DPS')
        else      : self.list_gen_msg.remove('DPS')
    def check_vsgrp(self, checked):
        if checked: self.list_gen_msg.append('VSGRP')
        else      : self.list_gen_msg.remove('VSGRP')
    def check_uts(self, checked):
        if checked: self.list_gen_msg.append('UTS')
        else      : self.list_gen_msg.remove('UTS')
    def check_upts(self, checked):
        if checked: self.list_gen_msg.append('UPTS')
        else      : self.list_gen_msg.remove('UPTS')
    def check_vv(self, checked):
        if checked: self.list_gen_msg.append('VV')
        else      : self.list_gen_msg.remove('VV')
    def check_pi(self, checked):
        if checked: self.list_gen_msg.append('PI')
        else      : self.list_gen_msg.remove('PI')
    def check_pz(self, checked):
        if checked: self.list_gen_msg.append('PZ')
        else      : self.list_gen_msg.remove('PZ')
    def check_bd(self, checked):
        if checked: self.list_gen_msg.append('BD')
        else      : self.list_gen_msg.remove('BD')
    def check_bdgrp(self, checked):
        if checked: self.list_gen_msg.append('BDGRP')
        else      : self.list_gen_msg.remove('BDGRP')
    def check_umpna_tm(self, checked):
        if checked: self.list_gen_msg.append('UMPNA_tm')
        else      : self.list_gen_msg.remove('UMPNA_tm')
    def check_zd_tm(self, checked):
        if checked: self.list_gen_msg.append('ZD_tm')
        else      : self.list_gen_msg.remove('ZD_tm')
    def check_vs_tm(self, checked):
        if checked: self.list_gen_msg.append('VS_tm')
        else      : self.list_gen_msg.remove('VS_tm')
    def check_vsgrp_tm(self, checked):
        if checked: self.list_gen_msg.append('VSGRP_tm')
        else      : self.list_gen_msg.remove('VSGRP_tm')
    def check_uts_tm(self, checked):
        if checked: self.list_gen_msg.append('UTS_tm')
        else      : self.list_gen_msg.remove('UTS_tm')
    def check_pz_tm(self, checked):
        if checked: self.list_gen_msg.append('PZ_tm')
        else      : self.list_gen_msg.remove('PZ_tm')
    def check_ktpr(self, checked):
        if checked: self.list_gen_msg.append('KTPR')
        else      : self.list_gen_msg.remove('KTPR')
    def check_ktprp(self, checked):
        if checked: self.list_gen_msg.append('KTPRP')
        else      : self.list_gen_msg.remove('KTPRP')
    def check_ktpra(self, checked):
        if checked: self.list_gen_msg.append('KTPRA')
        else      : self.list_gen_msg.remove('KTPRA')
    def check_ktprs(self, checked):
        if checked: self.list_gen_msg.append('KTPRS')
        else      : self.list_gen_msg.remove('KTPRS')
    def check_gmpna(self, checked):
        if checked: self.list_gen_msg.append('GMPNA')
        else      : self.list_gen_msg.remove('GMPNA')
    def check_ai_tabl(self, checked):
        if checked: self.list_gen_tabl.append('AI_tabl')
        else      : self.list_gen_tabl.remove('AI_tabl')
    def check_zd_tabl(self, checked):
        if checked: self.list_gen_tabl.append('ZD_tabl')
        else      : self.list_gen_tabl.remove('ZD_tabl')
    def check_vs_tabl(self, checked):
        if checked: self.list_gen_tabl.append('VS_tabl')
        else      : self.list_gen_tabl.remove('VS_tabl')
    def check_vsgrp_tabl(self, checked):
        if checked: self.list_gen_tabl.append('VSGRP_tabl')
        else      : self.list_gen_tabl.remove('VSGRP_tabl')
    def check_pump_tabl(self, checked):
        if checked: self.list_gen_tabl.append('Pump_tabl')
        else      : self.list_gen_tabl.remove('Pump_tabl')
    def check_pump_time_tabl(self, checked):
        if checked: self.list_gen_tabl.append('PumpTime_tabl')
        else      : self.list_gen_tabl.remove('PumpTime_tabl')
    def check_uts_tabl(self, checked):
        if checked: self.list_gen_tabl.append('UTS_tabl')
        else      : self.list_gen_tabl.remove('UTS_tabl')
    def check_prj_tabl(self, checked):
        if checked: self.list_gen_tabl.append('Prj_tabl')
        else      : self.list_gen_tabl.remove('Prj_tabl')
    def check_pz_tabl(self, checked):
        if checked: self.list_gen_tabl.append('PZ_tabl')
        else      : self.list_gen_tabl.remove('PZ_tabl')
    def check_ktpr_tabl(self, checked):
        if checked: self.list_gen_tabl.append('KTPR_tabl')
        else      : self.list_gen_tabl.remove('KTPR_tabl')
    def check_ktpra_tabl(self, checked):
        if checked: self.list_gen_tabl.append('KTPRA_tabl')
        else      : self.list_gen_tabl.remove('KTPRA_tabl')
    def check_gmpna_tabl(self, checked):
        if checked: self.list_gen_tabl.append('GMPNA_tabl')
        else      : self.list_gen_tabl.remove('GMPNA_tabl')
    # Button msg
    def export_list(self):
        msg = self.gen_sql.write_in_sql(self.list_gen_msg, False)
        self.logs_msg('default', 1, msg, True)
    def write_in_sql(self):
        msg = self.gen_sql.write_in_sql(self.list_gen_msg, True)
        self.logs_msg('default', 1, msg, True)
    # Button tabl
    def export_list_tabl(self):
        msg = self.gen_sql.write_in_sql_tabl(self.list_gen_tabl, False)
        self.logs_msg('default', 1, msg, True)
    def write_in_sql_tabl(self):
        msg = self.gen_sql.write_in_sql_tabl(self.list_gen_tabl, True)
        self.logs_msg('default', 1, msg, True)
    # ------------------Окно редактирования------------------
    # Choose table
    def choose_tabl(self):
        name_table = self.combo.currentText()
        self.ch_tabl = Window_update_sql(name_table)
        self.ch_tabl.show()
    # Update table
    def update_tabl(self):
        list_tabl = self.dop_function.all_tables()
        list_tabl.sort()
        self.combo.clear()
        for tabl in list_tabl:
           self.combo.addItem(str(tabl))
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


# Тип таблицы
class Window_type_tabl_sql(QWidget):
    def __init__(self, table_list):
        super(Window_type_tabl_sql, self).__init__()
        self.setWindowTitle('Тип столбцов таблицы')
        self.setStyleSheet("background-color: #e1e5e5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(500, 600)

        self.TableWidget = QTableWidget(self)
        self.TableWidget.move(500,600)
        self.TableWidget.verticalHeader().setVisible(False)
        self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        innerOutLayout = QVBoxLayout()
        innerOutLayout.addWidget(self.TableWidget)

        self.TableWidget.setColumnCount(3)
        self.TableWidget.setRowCount(len(table_list))
        tabl = ['Имя_eng', 'Имя_rus', 'Тип']
        self.TableWidget.setHorizontalHeaderLabels(tabl)
        # Color header
        style = "::section {""background-color: #bbbabf; }"
        self.TableWidget.horizontalHeader().setStyleSheet(style)

        for row_t in range(len(table_list)):
            for column_t in range(3):
                if column_t == 0: value = table_list[row_t][column_t]
                if column_t == 1: value = table_list[row_t][column_t]
                if column_t == 2: value = table_list[row_t][column_t]

                item = QTableWidgetItem(value)
                item.setFlags(Qt.ItemIsEnabled)
                self.TableWidget.setItem(row_t, column_t, item)

        self.setLayout(innerOutLayout)
# Дополнительное окно контекстного меню
class Window_contexmenu_sql(QWidget):
    def __init__(self, table_list):
        super(Window_contexmenu_sql, self).__init__()
        self.setWindowTitle('Дополнительное окно выбора сигнала')
        self.setStyleSheet("background-color: #e1e5e5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(500, 600)

        self.TableWidget = QTableWidget(self)
        self.TableWidget.move(500,600)
        self.TableWidget.verticalHeader().setVisible(False)
        self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        innerOutLayout = QVBoxLayout()
        innerOutLayout.addWidget(self.TableWidget)

        self.TableWidget.setColumnCount(3)
        self.TableWidget.setRowCount(len(table_list))
        tabl = ['№', 'Тэг', 'Название']
        self.TableWidget.setHorizontalHeaderLabels(tabl)
        # Color header
        style = "::section {""background-color: #bbbabf; }"
        self.TableWidget.horizontalHeader().setStyleSheet(style)

        for row_t in range(len(table_list)):
            for column_t in range(3):
                if column_t == 0: value = table_list[row_t][column_t]
                if column_t == 1: value = table_list[row_t][column_t]
                if column_t == 2: value = table_list[row_t][column_t]

                item = QTableWidgetItem(value)
                item.setFlags(Qt.ItemIsEnabled)
                self.TableWidget.setItem(row_t, column_t, item)

        self.setLayout(innerOutLayout)
# Основное окно просмотра и редактирования таблиц
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
        column, row, self.hat_name, value, msg = self.edit_SQL.editing_sql(self.table_used)
        self.logs_msg('default', 1, msg, True)

        self.gen_func = General_functions()
        
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

        clickButton_type = QPushButton('Тип данных', self)
        clickButton_type.setStyleSheet("background: #bfd6bf; border-radius: 4px; border: 1px solid")
        clickButton_type.resize(120,25)
        clickButton_type.move(1100, 40) 
        clickButton_type.clicked.connect(self.type_tabl)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.logTextBox)
        self.layout.addWidget(new_addrow_Button)
        self.layout.addWidget(new_addcol_Button)
        self.layout.addWidget(remoterow_Button)
        self.layout.addWidget(cleartab_Button)
        self.layout.addWidget(self.TableWidget)
        # Logs
        self.logs_msg(f'Запущен редактор базы данных. Таблица: {self.table_used}', 1)
    # Новое окно тип таблицы
    def type_tabl(self):
        type_list, msg = self.edit_SQL.type_column(self.table_used)
        self.type_tabl = Window_type_tabl_sql(type_list)
        self.type_tabl.show()
        self.logs_msg('default', 1, msg, True)
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
        find = General_functions()
        if find.str_find(str(request).lower(), {'select'}):
            column, row, hat_name, value, msg = self.edit_SQL.apply_request_select(request, self.table_used)
            self.logs_msg('default', 1, msg, True)
        else:
            msg = self.edit_SQL.other_requests(request, self.table_used)
            self.logs_msg('default', 1, msg, True)
            column, row, hat_name, value, msg = self.edit_SQL.editing_sql(self.table_used)
            self.logs_msg('default', 1, msg, True)
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

        column, row, self.hat_name, value, msg = self.edit_SQL.editing_sql(self.table_used)
        self.logs_msg('default', 1, msg, True)

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
        #if column_tooltip is not None:
        #    for col in range(self.TableWidget.columnCount()):
        #        self.TableWidget.horizontalHeaderItem(col).setToolTip(column_tooltip[col])

        self.TableWidget.verticalHeader().setVisible(False)

        # Разрешить щелчок правой кнопкой мыши для создания меню
        self.TableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.TableWidget.customContextMenuRequested.connect(self.generateMenu)

        # column size
        #for size_column in list_size:
        #   self.TableWidget.setColumnWidth(size_column[0], size_column[1])

        for row_t in range(row):
            for column_t in range(column):
                if value[row_t][column_t] is None:
                    item = QTableWidgetItem('')
                else:
                    item = QTableWidgetItem(str(value[row_t][column_t]))
                    # Подсказки к ячейкам
                    if self.gen_func.str_find(str(value[row_t][column_t]).lower(), {'di'}):
                        name_signal = self.edit_SQL.search_name("di", str(value[row_t][column_t]))
                        item.setToolTip(name_signal)
                    elif self.gen_func.str_find(str(value[row_t][column_t]).lower(), {'do'}):
                        name_signal = self.edit_SQL.search_name("do", str(value[row_t][column_t]))
                        item.setToolTip(name_signal)
                    elif self.gen_func.str_find(str(value[row_t][column_t]).lower(), {'ai'}):
                        name_signal = self.edit_SQL.search_name("ai", str(value[row_t][column_t]))
                        item.setToolTip(name_signal)
                    else: item.setToolTip('')
                    
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
        flag_NULL = True if len(text_cell) == 0 else False
        msg = self.edit_SQL.update_row_tabl(column, text_cell, text_cell_id, self.table_used, hat_name, flag_NULL)
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
    # ContexMenu
    def generateMenu(self, pos):
        # # Get index
        # for i in self.TableWidget.selectionModel().selection().indexes(): rowNum = i.row()
        # # If the selected row index is less than 1, the context menu will pop up
        # #if columnNum > 3:
        # menu = QMenu()
        # item1 = menu.addAction('AI')
        # item2 = menu.addAction('DI')
        # item3 = menu.addAction('DO')
        # # Make the menu display in the normal position
        # screenPos = self.TableWidget.mapToGlobal(pos)

        # # Click on a menu item to return, making it blocked
        # action = menu.exec(screenPos)
        # if action == item1:
        #     self.test()
        #     #print('Select Menu 1', self.TableWidget.item(rowNum, 0).text())
        # if action == item2:
        #     list_di = self.edit_SQL.dop_window_signal('di')
        #     di_tabl = Window_contexmenu_sql(list_di)
        #     di_tabl.show()
        #     #print('Select menu 2', self.TableWidget.item(rowNum, 0).text())
        # if action == item3:
        #     list_do = self.edit_SQL.dop_window_signal('do')
        #     do_tabl = Window_contexmenu_sql(list_do)
        #     do_tabl.show()
        #     #print('Select menu 3', self.TableWidget.item(rowNum, 0).text())
        # else: return
        menu = QMenu()
        menu.addAction("Foo Action TW")
        menu.exec_(self.TableWidget.mapToGlobal(pos))
        self.test()
    def test(self):
            list_ai = self.edit_SQL.dop_window_signal('ai')
            ai_tabl = Window_contexmenu_sql(list_ai)
            ai_tabl.show()


 











if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = Widget()
    myWin.show()
    sys.exit(app.exec())