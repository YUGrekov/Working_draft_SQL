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

        tab.addTab(tab_1, 'Соединение')
        tab.addTab(tab_2, 'Импорт КЗФКП')
        tab.addTab(tab_3, 'SQL разработки')
        tab.addTab(tab_4, 'SQL проекта')

        self.dop_function = General_functions()
        self.edit_SQL = Editing_table_SQL()
        self.list_tabl = self.edit_SQL.get_tabl()

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
        l_sql_base_path.setText(database_ust)
        l_sql_user_desc = QLabel('User: ',tab_1)
        l_sql_user_desc.move(200, 142)
        l_sql_user_path = QLabel(tab_1)
        l_sql_user_path.move(260, 142)
        l_sql_user_path.setText(user_ust)
        l_sql_pass_desc = QLabel('Password: ',tab_1)
        l_sql_pass_desc.move(200, 157)
        l_sql_pass_path = QLabel(tab_1)
        l_sql_pass_path.move(260, 157)
        l_sql_pass_path.setText(password_ust)
        l_sql_host_desc = QLabel('Host: ',tab_1)
        l_sql_host_desc.move(200, 172)
        l_sql_host_path = QLabel(tab_1)
        l_sql_host_path.move(260, 172)
        l_sql_host_path.setText(host_ust)
        l_sql_port_desc = QLabel('Port: ',tab_1)
        l_sql_port_desc.move(200, 187)
        l_sql_port_path = QLabel(tab_1)
        l_sql_port_path.move(260, 187)
        l_sql_port_path.setText(port_ust)

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
        # KTPR
        l_ktprp = QLabel('KTPR:', tab_3)
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
        l_msg_desc.move(100, 5)
        l_tabl_desc = QLabel('Таблицы', tab_4)
        l_tabl_desc.move(550, 5)
        
        l_diagn = QLabel('Диагностика: ', tab_4)
        l_diagn.move(10, 20)
        self.q_check_ai = QCheckBox('AI', tab_4)
        self.q_check_ai.move(10, 35) 
        self.q_check_ai.stateChanged.connect(self.check_ai)
        self.q_check_di = QCheckBox('DI', tab_4)
        self.q_check_di.move(10, 51) 
        self.q_check_di.stateChanged.connect(self.check_di)
        # self.q_check_do = QCheckBox('DO', tab_4)
        # self.q_check_do.move(10, 52) 
        # self.q_check_do.stateChanged.connect(self.check_do)
        # self.q_check_ao = QCheckBox('AO', tab_4)
        # self.q_check_ao.move(10, 68) 
        # self.q_check_ao.stateChanged.connect(self.check_ao)
        self.q_check_uso = QCheckBox('USO', tab_4)
        self.q_check_uso.setToolTip(''' ''')
        self.q_check_uso.move(10, 67) 
        self.q_check_uso.stateChanged.connect(self.check_uso)
        self.q_check_hw = QCheckBox('HardWare', tab_4)
        self.q_check_hw.setToolTip(''' ''')
        self.q_check_hw.move(10, 83) 
        self.q_check_hw.stateChanged.connect(self.check_hw)
        # Оборудование
        l_equip = QLabel('Оборудование: ', tab_4)
        l_equip.move(100, 20)
        self.q_check_umpna = QCheckBox('UMPNA', tab_4)
        self.q_check_umpna.setToolTip('''TblPumpsCMNA.xml\nTblPumpsUMPNA.xml\nTblPumpsKTPRAS.xml''')
        self.q_check_umpna.move(100, 35) 
        self.q_check_umpna.stateChanged.connect(self.check_umpna)
        self.q_check_zd = QCheckBox('ZD', tab_4)
        self.q_check_zd.move(100, 51) 
        self.q_check_zd.stateChanged.connect(self.check_zd)
        self.q_check_vs = QCheckBox('VS', tab_4)
        self.q_check_vs.move(100, 67) 
        self.q_check_vs.stateChanged.connect(self.check_vs)
        #self.q_check_vsgrp = QCheckBox('VSGRP', tab_4)
        #self.q_check_vsgrp.setToolTip(''' ''')
        #self.q_check_vsgrp.move(100, 83) 
        #self.q_check_vsgrp.stateChanged.connect(self.check_vsgrp)
        self.q_check_uts = QCheckBox('UTS', tab_4)
        self.q_check_uts.setToolTip('''Подбор шаблона по ключевым словам: звонок, табло, сирена, сирены, сигнализация\nTblSignalingDevices.xml\nTblSignalingDevicesFemale.xml\nTblSignalingDevicesMale.xml\nTblSignalingDevicesMany.xml''')
        self.q_check_uts.move(100, 83) 
        self.q_check_uts.stateChanged.connect(self.check_uts)
        self.q_check_upts = QCheckBox('UPTS', tab_4)
        self.q_check_upts.move(100, 99) 
        self.q_check_upts.stateChanged.connect(self.check_upts)
        self.q_check_upts.setToolTip('''Подбор шаблона по ключевым словам: звонок, табло, сирена, сирены, сигнализация\nTblSignalingDevices.xml\nTblSignalingDevicesFemale.xml\nTblSignalingDevicesMale.xml\nTblSignalingDevicesMany.xml''')
        self.q_check_vv = QCheckBox('VV', tab_4)
        self.q_check_vv.setToolTip('''TblHighVoltageSwitches.xml''')
        self.q_check_vv.move(100, 115) 
        self.q_check_vv.stateChanged.connect(self.check_vv)
        self.q_check_pi = QCheckBox('PI', tab_4)
        self.q_check_pi.setToolTip(''' ''')
        self.q_check_pi.move(100, 131) 
        self.q_check_pi.stateChanged.connect(self.check_pi)
        # Оборудование(уст)
        l_equip_ust = QLabel('Оборудование\n(уставки): ', tab_4)
        l_equip_ust.move(550, 20)
        self.q_check_umpna_ust = QCheckBox('UMPNA_tm', tab_4)
        self.q_check_umpna_ust.move(550, 50) 
        self.q_check_umpna_ust.stateChanged.connect(self.check_umpna_tm)
        self.q_check_zd_ust = QCheckBox('ZD_tm', tab_4)
        self.q_check_zd_ust.move(550, 66) 
        self.q_check_zd_ust.stateChanged.connect(self.check_zd_tm)
        self.q_check_vs_ust = QCheckBox('VS_tm', tab_4)
        self.q_check_vs_ust.move(550, 82) 
        self.q_check_vs_ust.stateChanged.connect(self.check_vs_tm)
        self.q_check_vsgrp_ust = QCheckBox('VSGRP_tm', tab_4)
        self.q_check_vsgrp_ust.move(550, 98) 
        self.q_check_vsgrp_ust.stateChanged.connect(self.check_vsgrp_tm)
        self.q_check_uts_ust = QCheckBox('UTS_tm', tab_4)
        self.q_check_uts_ust.move(550, 114) 
        self.q_check_uts_ust.stateChanged.connect(self.check_uts_tm)
        self.q_check_pz_ust = QCheckBox('PZ_tm', tab_4)
        self.q_check_pz_ust.move(550, 130) 
        self.q_check_pz_ust.stateChanged.connect(self.check_pz_tm)
        # Защиты, готовности
        l_protect = QLabel('Защиты,\nготовности: ', tab_4)
        l_protect.move(190, 20)
        self.q_check_ktpr = QCheckBox('KTPR', tab_4)
        self.q_check_ktpr.setToolTip('''TblStationDefences.xml''')
        self.q_check_ktpr.move(190, 50) 
        self.q_check_ktpr.stateChanged.connect(self.check_ktpr)
        self.q_check_ktprp = QCheckBox('KTPRP', tab_4)
        self.q_check_ktprp.setToolTip(''' ''')
        self.q_check_ktprp.move(190, 66) 
        self.q_check_ktprp.stateChanged.connect(self.check_ktprp)
        self.q_check_ktpra = QCheckBox('KTPRA', tab_4)
        self.q_check_ktpra.setToolTip('''TblPumpDefences.xml''')
        self.q_check_ktpra.move(190, 82) 
        self.q_check_ktpra.stateChanged.connect(self.check_ktpra)
        self.q_check_ktprs = QCheckBox('KTPRS', tab_4)
        self.q_check_ktprs.setToolTip('''TblLimitParameters.xml''')
        self.q_check_ktprs.move(190, 98) 
        self.q_check_ktprs.stateChanged.connect(self.check_ktprs)
        self.q_check_gmpna = QCheckBox('GMPNA', tab_4)
        self.q_check_gmpna.setToolTip('''TblPumpReadineses.xml''')
        self.q_check_gmpna.move(190, 114) 
        self.q_check_gmpna.stateChanged.connect(self.check_gmpna)
        # Установить все
        check_all = QCheckBox('Установить/Снять', tab_4)
        check_all.setToolTip('Установить или снять все флаги')
        check_all.move(10, 150) 
        check_all.stateChanged.connect(self.check_all)
        # Подтверждение
        b_export_list = QPushButton('Файл импорта', tab_4)
        b_export_list.setStyleSheet("border: 1px solid; border-radius: 3px;")
        b_export_list.setToolTip('''Генерировать файлы сообщений для базы данных PostgreSQL''')
        b_export_list.resize(120,23)
        b_export_list.move(10, 180) 
        b_export_list.clicked.connect(self.export_list)
        b_export_sql = QPushButton('Генерировать базу', tab_4)
        b_export_sql.setStyleSheet("border: 1px solid; border-radius: 3px;")
        b_export_sql.setToolTip('''Генерировать сообщения в базу данных PostgreSQL''')
        b_export_sql.resize(120,23)
        b_export_sql.move(150, 180) 
        b_export_sql.clicked.connect(self.write_in_sql)

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
        connect =self.gen_sql.check_database_connect(database_ust, user_ust, password_ust, host_ust, port_ust)
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
        msg = self.dop_function.clear_tabl('tmna_umpna', 'tmNA_UMPNA', self.list_tabl)
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
            #self.q_check_do.setChecked(True)
            #self.q_check_ao.setChecked(True)
            self.q_check_uso.setChecked(True)
            self.q_check_hw.setChecked(True)
            
            self.q_check_umpna.setChecked(True)
            self.q_check_zd.setChecked(True)
            self.q_check_vs.setChecked(True)
            #self.q_check_vsgrp.setChecked(True)
            self.q_check_uts.setChecked(True)
            self.q_check_upts.setChecked(True)
            self.q_check_vv.setChecked(True)
            self.q_check_pi.setChecked(True)
            
            self.q_check_umpna_ust.setChecked(True)
            self.q_check_zd_ust.setChecked(True)
            self.q_check_vs_ust.setChecked(True)
            self.q_check_vsgrp_ust.setChecked(True)
            self.q_check_uts_ust.setChecked(True)
            self.q_check_pz_ust.setChecked(True)
            
            self.q_check_ktpr.setChecked(True)
            self.q_check_ktprp.setChecked(True)
            self.q_check_ktpra.setChecked(True)
            self.q_check_ktprs.setChecked(True)
            self.q_check_gmpna.setChecked(True)
        else: 
            self.q_check_ai.setChecked(False)
            self.q_check_di.setChecked(False)
            #self.q_check_do.setChecked(False)
            #self.q_check_ao.setChecked(False)
            self.q_check_uso.setChecked(False)
            self.q_check_hw.setChecked(False)
            
            self.q_check_umpna.setChecked(False)
            self.q_check_zd.setChecked(False)
            self.q_check_vs.setChecked(False)
            #self.q_check_vsgrp.setChecked(False)
            self.q_check_uts.setChecked(False)
            self.q_check_upts.setChecked(False)
            self.q_check_vv.setChecked(False)
            self.q_check_pi.setChecked(False)
            
            self.q_check_umpna_ust.setChecked(False)
            self.q_check_zd_ust.setChecked(False)
            self.q_check_vs_ust.setChecked(False)
            self.q_check_vsgrp_ust.setChecked(False)
            self.q_check_uts_ust.setChecked(False)
            self.q_check_pz_ust.setChecked(False)
            
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
    def check_uso(self, checked):
        if checked: self.list_gen_msg.append('USO')
        else      : self.list_gen_msg.remove('USO')
    def check_hw(self, checked):
        if checked: self.list_gen_msg.append('HW')
        else      : self.list_gen_msg.remove('HW')
    def check_umpna(self, checked):
        if checked: self.list_gen_msg.append('UMPNA')
        else      : self.list_gen_msg.remove('UMPNA')
    def check_zd(self, checked):
        if checked: self.list_gen_msg.append('ZD')
        else      : self.list_gen_msg.remove('ZD')
    def check_vs(self, checked):
        if checked: self.list_gen_msg.append('VS')
        else      : self.list_gen_msg.remove('VS')
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
    # Button
    def export_list(self):
        msg = self.gen_sql.write_in_sql(self.list_gen_msg, False)
        self.logs_msg('default', 1, msg, True)
    def write_in_sql(self):
        msg = self.gen_sql.write_in_sql(self.list_gen_msg, True)
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











if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = Widget()
    myWin.show()
    sys.exit(app.exec())