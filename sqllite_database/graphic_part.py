from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import *
from main_base import *
from edit_window import *
from datetime import datetime
import sys



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
        # Save auto path
        self.settings = QSettings('project_development','AO_Nefteavtomatika',self)
        self.loadSetting()
    def saveSetting(self):
        self.settings.setValue('path_kzfkp', self.path_xml)
        self.settings.setValue('path_kzfkp', self.path_base)
    def loadSetting(self):
        pass

    def create_menu_bars(self):
        menuBar = self.menuBar()
        menuBar.setStyleSheet('background-color: rgb(225, 225, 225);')

        settings = QMenu('&Настройки проекта', self)
        settings.setStyleSheet('background-color: rgb(225, 225, 225);')

        menuBar.addMenu(settings)

        path_kzfkp = QAction('Путь до КЗФКП', self)
        path_base = QAction('Путь до базы данных', self)

        settings.addAction(path_kzfkp)
        settings.addAction(path_base)

        path_kzfkp.triggered.connect(self.settings_kzfkp)
        path_base.triggered.connect(self.settings_base)
    def settings_kzfkp(self):
        self.path_xml = QFileDialog.getOpenFileName(caption='Выберите файл КЗФКП')[0]
    def settings_base(self):
        self.path_base = QFileDialog.getOpenFileName(caption='Выберите файл базы данных')[0]
    def window_import_exel(self):
        self.w_i_e = Window_import_exel()
        self.w_i_e.show()
    def window_create_sql(self):
        self.edit_SQL = Editing_table_SQL()
        list_tabl = self.edit_SQL.get_tabl()

        self.w_u_c = Window_tabl_checkbox(list_tabl)
        self.w_u_c.show()

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
       

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = Window()
    myWin.show()
    sys.exit(app.exec())