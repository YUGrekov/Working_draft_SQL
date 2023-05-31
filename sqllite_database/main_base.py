from models import *
import openpyxl as wb
from datetime import datetime
import re
today = datetime.now()



# Additional general features
class general_functions():
    def __init__(self):
        self.cursor = db.cursor()
    def str_find(self, str1, arr):
        i = 0
        for el in arr:
            if str(str1).find(el) > -1:
                return True
    def translate(self, str):
            dict = {".":"_",
                    "/":"_",
                    "\\":"_",
                    ",":"_",
                    ":":"_",
                    ";":"_",
                    "А":"A",
                    "Б":"_B",
                    "В":"B",
                    "Г":"G",
                    "Д":"D",
                    "Е":"E",
                    "Ё":"_E",
                    "Ж":"J",
                    "З":"Z",
                    "И":"I",
                    "Й":"_I",
                    "К":"K",
                    "Л":"L",
                    "М":"M",
                    "Н":"H",
                    "О":"O",
                    "П":"_P",
                    "Р":"P",
                    "С":"C",
                    "Т":"T",
                    "У":"U",
                    "Ф":"F",
                    "Х":"X",
                    "Ц":"C",
                    "Ч":"CH",
                    "Ш":"SH",
                    "Щ":"SCH",
                    "Ь":"b",
                    "Ы":"_",
                    "Ъ":"_",
                    "Э":"E",
                    "Ю":"U",
                    "Я":"YA",
                    "а":"a",
                    "б":"_b",
                    "в":"b",
                    "г":"g",
                    "д":"d",
                    "е":"e",
                    "ё":"_e",
                    "ж":"j",
                    "з":"z",
                    "и":"i",
                    "й":"_i",
                    "к":"k",
                    "л":"l",
                    "м":"m",
                    "н":"h",
                    "о":"o",
                    "п":"_p",
                    "р":"p",
                    "с":"c",
                    "т":"t",
                    "у":"u",
                    "ф":"f",
                    "х":"x",
                    "ц":"c",
                    "ч":"ch",
                    "ш":"sh",
                    "щ":"sch",
                    "ь":"b",
                    "ы":"_",
                    "ъ":"_",
                    "э":"e",
                    "ю":"u",
                    "я":"ya"}

            intab = '.-пПаАфз/еЕсС'
            outtab = '__ppaafz_eEcC'
            trantab = str.maketrans(dict)
            outstr = str.translate(trantab)
            return outstr
    def column_check(self, table_used_model, table_used_base, list_column):
        # Logs
        msg = {}
        # Create tabl
        with db.atomic():
            db.create_tables([table_used_model])
        # Checking if a column exists
        column_tabl  = []
        new_column   = []
        
        for data_column in db.get_columns(table_used_base):
            if data_column[0] in list_column: column_tabl.append(data_column[0])
        
        for lst in list_column:
            if lst not in column_tabl: 
                msg[f'{today} - Отсутствует обязательный столбец таблицы {table_used_model}: {lst}'] = 2
                new_column.append(lst)
        
        for new_name in new_column:
            msg[f'{today} - Столбец: {new_name} добавлен в таблицу {table_used_model}'] = 3
            migrate(migrator.add_column(table_used_base, new_name, IntegerField(null=True)))
        return msg
    def empty_table(self, table_used):
        empty = self.cursor.execute(f'''SELECT COUNT(*) FROM {table_used}''')
        return True if int(empty.fetchall()[0][0]) == 0  else False
    # Clear tabl
    def clear_tabl(self, table_used, table_name, list_tabl):
        msg = {}
        if not table_used in list_tabl:
            msg[f'{today} - Таблица: {table_used} отсутствует!'] = 2
            return msg

        if self.empty_table(f'''{table_used}'''): 
            msg[f'{today} - Таблица: {table_name} пустая!'] = 2
            return msg
        
        self.cursor.execute(f'''DELETE FROM {table_used}''')
        msg[f'{today} - Таблица: {table_name} полностью очищена'] = 1
        return msg

# Work with filling in the table 'Signals'
class Import_in_SQL():
    def __init__(self, exel):
        self.exel    = exel
        self.connect = wb.load_workbook(self.exel, read_only=True, data_only=True)
    # Read tables from file
    def read_table(self):
        tables = []
        for sheet in self.connect.worksheets:
            tables.append(sheet.title)
        return tables
    # Looking for table hat
    def search_hat_table(self, uso, number_row):
        hat_tabl = []
        for sheet in self.connect.worksheets:
            if sheet.title == uso:
                column = sheet.max_column
                for i in range(int(number_row), int(number_row) + 1):
                    for j in range(1, column + 1):
                        cell = sheet.cell(row=i, column=j).value
                        if cell is None: continue
                        hat_tabl.append(cell)
        return hat_tabl
    # Reading table data
    def import_table(self, uso, number_row, name_column):
        hat_num  = {}
        for sheet in self.connect.worksheets:
            if sheet.title == uso:
                column = sheet.max_column
                for i in range(int(number_row), int(number_row) + 1):
                    for j in range(1, column + 1):
                        cell = sheet.cell(row=i, column=j).value
                        if cell is None: continue
                        for key, value in name_column.items():
                            if value == cell:
                                hat_num[key] = j - 1
                data = []
                for row in sheet.iter_rows(min_row=(int(number_row) + 1)):
                    keys   = []
                    values = []
                    for name, number in hat_num.items():
                        keys.append(name)
                        values.append(row[number].value)
                    values.append(uso)
                    array = {k: v for k, v in zip(keys, values)}
                    data.append(array)
        # Delete basket is None
        data_new = []
        for row in data:
            type_signal = row['type_signal']
            scheme      = row['schema']
            basket      = row['basket']

            list_type = ['CPU', 'PSU', 'CN', 'MN', 'AI','AO', 'DI', 'RS','DO']
            for value in list_type:
                if str(scheme).find(value) != -1: 
                    type_signal = value

            dict_column = {'type_signal' : type_signal,
                           'uso'         : uso,
                           'tag'         : row['tag'],
                           'description' : row['description'],
                           'schema'      : row['schema'],
                           'klk'         : row['klk'],
                           'contact'     : row['contact'],
                           'basket'      : basket,
                           'module'      : row['module'],
                           'channel'     : row['channel']}
            if basket is None: continue
            data_new.append(dict_column)
        return data_new
    # Importing into SQL
    def import_for_sql(self, data, uso):
        msg = {}
        # Checking for the existence of a database
        with db.atomic():
            Signals.insert_many(data).execute()

        msg[f'{today} - Добавлено новое УСО: {uso}'] = 1
        return(msg)
    # Update Database
    def update_for_sql(self, data, uso):
        msg = {}
        with db:
            # Filter by uso, basket, modul, channel
            for row_exel in data:
                exist_row = Signals.select().where(Signals.uso == uso,
                                                   Signals.basket  == str(row_exel['basket']),
                                                   Signals.module  == str(row_exel['module']),
                                                   Signals.channel == str(row_exel['channel']))
                if not bool(exist_row):
                    # new record
                    Signals.create(
                        type_signal=row_exel['type_signal'],
                        uso        =row_exel['uso'],
                        tag        =row_exel['tag'],
                        description=row_exel['description'],
                        scheme     =row_exel['scheme'],
                        klk        =row_exel['klk'],
                        contact    =row_exel['contact'],
                        basket     =row_exel['basket'],
                        module     =row_exel['module'],
                        channel    =row_exel['channel'],
                    )
                    msg[f'''{today} - Добавлен новый сигнал: Tag - {row_exel["tag"]}, description - {row_exel["description"]}, 
                                                             basket - {row_exel["basket"]}, module - {row_exel["module"]}, 
                                                             channel - {row_exel["channel"]}'''] = 0

                for row_sql in Signals.select().dicts():

                    if row_sql['uso']     == uso                     and \
                       row_sql['basket']  == str(row_exel['basket']) and \
                       row_sql['module']  == str(row_exel['module']) and \
                       row_sql['channel'] == str(row_exel['channel']):
                        
                        if str(row_sql['tag'])         == str(row_exel['tag'])         and \
                           str(row_sql['description']) == str(row_exel['description']) and \
                           str(row_sql['scheme'])      == str(row_exel['scheme'])      and \
                           str(row_sql['klk'])         == str(row_exel['klk'])         and \
                           str(row_sql['contact'])     == str(row_exel['contact']):
           
                            continue
                        else:
                            Signals.update(
                                type_signal=row_exel['type_signal'],
                                tag        =row_exel['tag'],
                                description=row_exel['description'],
                                scheme     =row_exel['scheme'],
                                klk        =row_exel['klk'],
                                contact    =row_exel['contact'],
                            ).where(Signals.id == row_sql['id']).execute()
                            msg[f'''{today} - Обновление сигнала id = {row_sql["id"]}: Было, 
                                                                                    uso - {row_sql['uso']}, 
                                                                                    type_signal - {row_sql['type_signal']}, 
                                                                                    tag - {row_sql['tag']},                      
                                                                                    description - {row_sql['description']}, 
                                                                                    scheme - {row_sql['scheme']}, 
                                                                                    klk - {row_sql['klk']},
                                                                                    contact - {row_sql['contact']} = 
                                                                                    Стало, 
                                                                                    uso - {row_exel['uso']}, 
                                                                                    type_signal - {row_exel['type_signal']}, 
                                                                                    tag - {row_exel['tag']}, 
                                                                                    description - {row_exel['description']}, 
                                                                                    scheme - {row_exel['scheme']}, 
                                                                                    klk - {row_exel['klk']},
                                                                                    contact - {row_exel['contact']}'''] = 3
                            continue
                    else:
                        continue
        return(msg)
    # Removing all rows
    def clear_tabl(self):
        msg = {}
        for row_sql in Signals.select().dicts():
            Signals.get(Signals.id == row_sql['id']).delete_instance()
        msg[f'{today} - Таблица: signals полностью очищена!'] = 1
        return(msg)
    # Column check
    def column_check(self):
        with db:
            list_default = ['id', 'type_signal', 'uso', 'tag', 'description', 'schema', 'klk', 'contact', 'basket', 'module', 'channel']

            self.dop_func = general_functions()
            msg = self.dop_func.column_check(Signals, 'signals', list_default)
        return msg

# Work with filling in the table 'HardWare'
class Filling_HardWare():
    def __init__(self):
        self.cursor = db.cursor()
        self.dop_function = general_functions()
    # Получаем данные с таблицы Signals по количеству корзин и модулю
    def getting_modul(self, kk_is_True):
        msg = {}
        list_type = {'CPU': 'MK-504-120', 
                     'PSU': 'MK-550-024', 
                     'CN' : 'MK-545-010', 
                     'MN' : 'MK-546-010', 
                     'AI' : 'MK-516-008A',
                     'AO' : 'MK-514-008', 
                     'DI' : 'MK-521-032', 
                     'RS' : 'MK-541-002', 
                     'DO' : 'MK-531-032'}
        with db:
            if self.dop_function.empty_table('signals'): 
                msg[f'{today} - Таблица: Signals пустая! Заполни таблицу!'] = 2
                return msg

            req_uso = self.cursor.execute(f'''SELECT DISTINCT uso 
                                              FROM signals''')
            list_uso = req_uso.fetchall()

            temp_flag    = False
            test_s       = []
            count_basket = 0
            count_AI     = 0
            count_AO     = 0
            count_DI     = 0
            count_DO     = 0
            count_RS     = 0
            for uso in list_uso:
                req_basket = self.cursor.execute(f'''SELECT DISTINCT basket 
                                                     FROM signals
                                                     WHERE uso="{uso[0]}"''')
                list_basket = req_basket.fetchall()

                # ЦК в количестве 2 - ONE!
                if temp_flag is False:
                    for i in range(2):
                        uso_kk = uso[0]
                        test_s.append(dict(uso = uso[0], tag = '',
                                           powerLink_ID ='',
                                           basket  = i + 1,
                                           type_0  = 'MK-550-024',  variable_0 = f'PSU', type_1 = f'MK-546-010', variable_1 = f'MN',
                                           type_2  = f'MK-504-120', variable_2 = f'CPU', type_3 = f'',           variable_3 = f'',
                                           type_4  = f'',           variable_4 = f'',    type_5 = f'',           variable_5 = f'',
                                           type_6  = f'',           variable_6 = f'',    type_7 = f'',           variable_7 = f'',
                                           type_8  = f'',           variable_8 = f'',    type_9 = f'',           variable_9 = f'',
                                           type_10 = f'',           variable_10= f'',    type_11= f'',           variable_11= f'',
                                           type_12 = f'',           variable_12= f'',    type_13= f'',           variable_13= f'',
                                           type_14 = f'',           variable_14= f'',    type_15= f'',           variable_15= f'',
                                           type_16 = f'',           variable_16= f'',    type_17= f'',           variable_17= f'',
                                           type_18 = f'',           variable_18= f'',    type_19= f'',           variable_19= f'',
                                           type_20 = f'',           variable_20= f'',    type_21= f'',           variable_21= f'',
                                           type_22 = f'',           variable_22= f'',    type_23= f'',           variable_23= f'',
                                           type_24 = f'',           variable_24= f'',    type_25= f'',           variable_25= f'',
                                           type_26 = f'',           variable_26= f'',    type_27= f'',           variable_27= f'',
                                           type_28 = f'',           variable_28= f'',    type_29= f'',           variable_29= f'',
                                           type_30 = f'',           variable_30= f'',    type_31= f'',           variable_31= f'',
                                           type_32 = f'',           variable_32= f''))
                    temp_flag = True
                for basket in list_basket:
                    count_basket     += 1
                    list_hw           = {}
                    list_hw['uso']    = uso[0]    
                    list_hw['basket'] = basket[0] 

                    # Если в проекте есть КК
                    if kk_is_True and count_basket == 3:
                        for i in range(4, 6, 1):
                            test_s.append(dict(uso        = uso_kk,
                                               tag        = '',
                                               basket     = i + 1,
                                               type_0     = 'MK-550-024',
                                               variable_0 = f'PSU',
                                               type_2     = f'MK-504-120',
                                               variable_2 = f'CPU'))

                    req_modul = self.cursor.execute(f'''SELECT DISTINCT module, type_signal 
                                                        FROM signals
                                                        WHERE uso="{uso[0]}" AND basket={basket[0]}
                                                        ORDER BY module''')
                    for i in req_modul.fetchall():
                        if i[1] is None or i[1] == '' or i[1] == ' ': 
                            type_kod = 'Неопределен!'
                            type_mod = 'Неопределен!'
                            msg[f'{today} - Таблица: Hardware. {uso[0]}.A{basket[0]}.{i[0]} тип не определен!'] = 2
                        else:
                            for key, value in list_type.items():
                                if str(i[1]).find(key) != -1: 
                                    if key == 'AI': 
                                        count_AI += 1
                                        type_mod = f'{key}[{count_AI}]'
                                    elif key == 'AO': 
                                        count_AO += 1
                                        type_mod = f'{key}[{count_AO}]'
                                    elif key == 'DI': 
                                        count_DI += 1
                                        type_mod = f'{key}[{count_DI}]'
                                    elif key == 'DO': 
                                        count_DO += 1
                                        type_mod = f'{key}[{count_DO}]'
                                    elif key == 'RS': 
                                        count_RS += 1
                                        type_mod = f'{key}[{count_RS}]'
                                    else:
                                        type_mod = key

                                    type_kod = value
                        list_hw[f'tag']             = ''
                        list_hw[f'powerLink_ID']    = count_basket
                        list_hw[f'type_0']          = 'MK-550-024'
                        list_hw[f'variable_0']      = 'PSU'
                        list_hw[f'type_1']          = 'MK-545-010'
                        list_hw[f'variable_1']      = 'CN'
                        list_hw[f'type_{i[0]}']     = type_kod
                        list_hw[f'variable_{i[0]}'] = type_mod
                    test_s.append(list_hw)

            # Checking for the existence of a database
            HardWare.insert_many(test_s).execute()
        msg[f'{today} - Таблица: hardware заполнена'] = 1
        return(msg)
    # Заполняем таблицу HardWare
    def column_check(self):
        list_default = ['tag', 'uso', 'basket', 'powerLink_ID', 
                        'type_0',  'variable_0',  'type_1',  'variable_1',  'type_2',  'variable_2', 
                        'type_3',  'variable_3',  'type_4',  'variable_4',  'type_5',  'variable_5', 
                        'type_6',  'variable_6',  'type_7',  'variable_7',  'type_8',  'variable_8',
                        'type_9',  'variable_9',  'type_10', 'variable_10', 'type_11', 'variable_11', 
                        'type_12', 'variable_12', 'type_13', 'variable_13', 'type_14', 'variable_14', 
                        'type_15', 'variable_15', 'type_16', 'variable_16', 'type_17', 'variable_17',
                        'type_18', 'variable_18', 'type_19', 'variable_19', 'type_20', 'variable_20', 
                        'type_21', 'variable_21', 'type_22', 'variable_22', 'type_23', 'variable_23', 
                        'type_24', 'variable_24', 'type_25', 'variable_25', 'type_26', 'variable_26',
                        'type_27', 'variable_27', 'type_28', 'variable_28', 'type_29', 'variable_29', 
                        'type_30', 'variable_30', 'type_31', 'variable_31', 'type_32', 'variable_32']
        
        self.dop_func = general_functions()
        msg = self.dop_func.column_check(HardWare, 'hardware', list_default)
        return msg

# Work with filling in the table 'USO'
class Filling_USO():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = general_functions()
    # Получаем данные с таблицы Signals 
    def getting_modul(self):
        msg = {}
        temp = False
        count_USO        = 0
        list_diag_signal = []
        with db:
            try:
                self.cursor.execute(f'''SELECT * FROM ai''')
                self.cursor.execute(f'''SELECT * FROM di''')
            except:
                msg[f'{today} - Таблицы: AI или DI не найдены!'] = 2
                return msg
            req_uso = self.cursor.execute(f'''SELECT DISTINCT uso 
                                              FROM signals''')
            list_uso = req_uso.fetchall()
            for uso in list_uso:
                count_DI  = 0
                count_USO += 1
                list_diag = {}

                list_diag['variable'] = f'USO[{count_USO}]'
                list_diag['name']     = f'{uso[0]}'

                ai_temp = self.cursor.execute(f'''SELECT variable, name
                                                  FROM ai
                                                  WHERE name LIKE "%{uso[0]}%"''')
                current_ai = ai_temp.fetchall()
                try:
                    if len(current_ai) == 0: raise
                    for ai in current_ai:
                        list_diag['temperature']  = f'{ai[0]}'
                        break
                except:
                    list_diag['temperature']  = ''
                    msg[f'{today} - Таблица: USO. Температура в шкафу {uso[0]} не найдена!'] = 2

                door_temp = self.cursor.execute(f'''SELECT variable, name
                                                    FROM di
                                                    WHERE name LIKE "%{uso[0]}%" AND 
                                                          (name LIKE "%двер%" OR
                                                          name LIKE "%Двер%")''')
                current_door = door_temp.fetchall()
                try:
                    if len(current_door) == 0: raise
                    for door in current_door:
                        list_diag['door']  = f'{door[0]}.Value'
                        break
                except:
                    list_diag['temperature']  = ''
                    msg[f'{today} - Таблица: USO. Сигнал открытой двери шкафа {uso[0]} не найден!'] = 2

                di_temp = self.cursor.execute(f'''SELECT variable, name
                                                  FROM di
                                                  WHERE name LIKE "%{uso[0]}%" AND 
                                                        (name NOT LIKE "%двер%") AND (name NOT LIKE "%Двер%") 
                                                  ORDER BY name''')
                current_di = di_temp.fetchall()
                try:
                    for di in current_di:
                        count_DI += 1
                        list_diag[f'signal_{count_DI}']  = f'{di[0]}.Value'
                except:
                    list_diag[f'signal_{count_DI}']  = ''

                # При первом заполнение необходимо использовать все колонки
                if temp is False:
                    for i in range(count_DI + 1, 33):
                        list_diag[f'signal_{i}']  = ''
                    temp = True

                list_diag_signal.append(list_diag)
            # Checking for the existence of a database
            USO.insert_many(list_diag_signal).execute()

        msg[f'{today} - Таблица: USO заполнена'] = 1
        return(msg)
    # Заполняем таблицу USO
    def column_check(self):
        list_default = ['variable', 'name', 'temperature', 'door',
                        'signal_1', 'signal_2', 'signal_3', 'signal_4', 'signal_5', 'signal_6', 'signal_7', 'signal_8', 
                        'signal_9', 'signal_10', 'signal_11', 'signal_12', 'signal_13', 'signal_14', 'signal_15', 'signal_16',
                        'signal_17', 'signal_18', 'signal_19', 'signal_20', 'signal_21', 'signal_22', 'signal_23', 'signal_24',
                        'signal_25', 'signal_26', 'signal_27', 'signal_28', 'signal_29', 'signal_30', 'signal_31', 'signal_32'
                        ]
        msg = self.dop_function.column_check(USO, 'uso', list_default)
        return msg 

# Work with filling in the table 'AI'
class Filling_AI():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = general_functions()
    # Получаем данные с таблицы Signals 
    def getting_modul(self):
        msg = {}
        list_AI = []
        count_AI = 0
        dop_analog = {'Аварийное отключение'  : ['', 'мА', 'Сигналы с контролем цепи', 'Сигнализаторы', 'Сигналы с контролем цепи', ['4', '20'], '1'],
                      'Аварийный максимальный': ['', 'мА', 'Сигналы с контролем цепи', 'Сигнализаторы', 'Сигналы с контролем цепи', ['4', '20'], '1'],
                      'Аварийный минимальный' : ['', 'мА', 'Сигналы с контролем цепи', 'Сигнализаторы', 'Сигналы с контролем цепи', ['4', '20'], '1'],
                      'объем'                 : ['V', 'м3', '', '', '', ['', ''], '1'], 
                      'объём'                 : ['V', 'м3', '', '', '', ['', ''], '1'],
                      'перепад'               : ['dP', 'МПа', 'Аналоги (макс1 = макс.уставка)', 'Перепад давления', '', ['0', '1'], '2'],
                      'давлени'               : ['P', 'МПа', 'Аналоги (макс1 = повышенная)', 'Давления', '', ['0', '6'], '2'],
                      'загазованность'        : ['Газ', '%', 'Загазованность', 'Загазованность', '', ['0', '100'], '1'],
                      'вертик'                : ['Xверт', 'мм/с', 'Вибрации', '', '', ['0', '30'], '1'],
                      'горизонт'              : ['Xгор', 'мм/с', 'Вибрации', '', '', ['0', '30'], '1'],
                      'осевая'                : ['Xос', 'мм/с', 'Вибрации', '', '', ['0', '30'], '1'],
                      'попереч'               : ['Xпоп', 'мм/с', 'Вибрации', '', '', ['0', '30'], '1'],
                      'осевое'                : ['Xoc', 'мм/с', 'Вибрации', 'Осевые смещения', '', ['0', '30'], '1'],
                      'сила'                  : ['I', 'A', 'Аналоги (макс1 = повышенная)', 'Общестанционные', '', ['0', '1000'], '1'],
                      'температура'           : ['T', '°C', 'Аналоги (макс1 = повышенная)', 'Температуры', '', ['-50', '100'], '1'],
                      'уровень'               : ['L', 'мм', 'Аналоги (макс1 = макс.уставка)', 'Уровни', '', ['200', '1000'], '1'],
                      'утечк'                 : ['L', 'мм', 'Сигналы с контролем цепи', 'Сигнализаторы', 'Сигналы с контролем цепи', ['4', '20'], '1'],
                      'расход'                : ['Q', 'м3/ч', 'Аналоги (макс1 = макс.уставка)', '', '', ['0', '1000'], '1'],
                      'положени'              : ['Q', '%', '', '', '', ['0', '100'], '1'],
                      'затоплен'              : ['L', 'мА', 'Сигналы с контролем цепи', 'Сигнализаторы', 'Сигналы с контролем цепи', ['4', '20'], '1'],
                      'частот'                : ['F', 'Гц', '', 'Уровни', '', ['0', '100'], '1'],
                      'процен'                : ['Q', '%', 'Аналоги (макс1 = макс.уставка)', '', '', ['0', '100'], '0'],
                      'заслон'                : ['Q', '%', 'Аналоги (макс1 = макс.уставка)', '', '', ['0', '100'], '0'],
                     }
        with db:
            if self.dop_function.empty_table('signals'): 
                msg[f'{today} - Таблица: Signals пустая! Заполни таблицу!'] = 2
                return msg
            
            for row_sql in Signals.select().dicts():
                id_s        = row_sql['id']    
                uso_s       = row_sql['uso']    
                tag         = row_sql['tag']
                description = str(row_sql['description']).replace('"', '').replace("'", '')
                type_signal = row_sql['type_signal']
                scheme      = row_sql['schema']
                basket_s    = row_sql['basket']
                module_s    = row_sql['module']
                channel_s   = row_sql['channel']

                if self.dop_function.str_find(type_signal, {'AI'}) or self.dop_function.str_find(scheme, {'AI'}):
                    count_AI += 1
                    # Выбор между полным заполнением или обновлением
                    empty = self.cursor.execute('SELECT COUNT(*) FROM ai')
                    if int(empty.fetchall()[0][0]) == 0:
                        msg[f'{today} - Таблица: AI пуста, идет заполнение'] = 1
                    else:
                        msg[f'{today} - Таблица: AI не пуста, идет обновление'] = 1

                    coincidence = AI.select().where(AI.uso     == uso_s,
                                                    AI.basket  == basket_s,
                                                    AI.module  == module_s,
                                                    AI.channel == channel_s)
                    if bool(coincidence):
                        exist_tag  = AI.select().where(AI.tag == tag)
                        exist_name = AI.select().where(AI.name == description)

                        if not bool(exist_tag):
                            select_tag = self.cursor.execute(f'''SELECT id, tag 
                                                                 FROM ai
                                                                 WHERE uso='{uso_s}' AND 
                                                                       basket={basket_s} AND 
                                                                       module={module_s} AND 
                                                                       channel={channel_s}''')
                            for id_, tag_ in select_tag.fetchall():
                                msg[f'{today} - Таблица: AI, у сигнала обновлен tag: id = {id_}, ({tag_}) {tag}'] = 2
                            self.cursor.execute(f'''UPDATE ai
                                                    SET tag='{tag}' 
                                                    WHERE uso='{uso_s}' AND 
                                                          basket={basket_s} AND 
                                                          module={module_s} AND 
                                                          channel={channel_s}''')
    
                        if not bool(exist_name):
                            select_name = self.cursor.execute(f'''SELECT id, name 
                                                                  FROM ai
                                                                  WHERE uso='{uso_s}' AND 
                                                                        basket={basket_s} AND 
                                                                        module={module_s} AND 
                                                                        channel={channel_s}''')
                            for id_, name_ in select_name.fetchall():
                                msg[f'{today} - Таблица: AI, у сигнала обновлен name: id = {id_}, ({name_}) {description}'] = 2
                            self.cursor.execute(f'''UPDATE ai
                                                    SET name='{description}' 
                                                    WHERE uso='{uso_s}' AND 
                                                          basket={basket_s} AND 
                                                          module={module_s} AND 
                                                          channel={channel_s}''')
                        continue

                    # Сквозной номер модуля
                    for through_module_number in HardWare.select().dicts():
                        uso_h    = through_module_number['uso']
                        basket_h = through_module_number['basket']

                        if uso_s == uso_h and basket_s == basket_h:
                            type_mod = through_module_number[f'variable_{module_s}']
                            isdigit_num  = re.findall('\d+', str(type_mod))
                            
                            try   : isdigit_num = isdigit_num[0]
                            except: 
                                isdigit_num = ''
                                msg[f'{today} - В таблице HardWare не найден модуль сигнала: {id_s}, {tag}, {description}, {uso_s}_A{basket_s}_{module_s}_{channel_s}, "pValue" не заполнен'] = 2
                            break

                    sign             = ''
                    unit             = ''
                    rule             = ''
                    group_analog     = ''
                    group_ust_analog = ''
                    eng_min          = ''
                    eng_max          = ''
                    value_precision  = ''

                    for key, short in dop_analog.items():
                        if self.dop_function.str_find(str(description).lower(), {key}):
                            sign = short[0]
                            unit = short[1]
                            rule = short[2]
                            group_analog = short[3]
                            group_ust_analog = short[4]
                            eng_min = short[5][0]
                            eng_max = short[5][1]
                            value_precision = short[6]
                            break

                    flag_MPa_kgccm2 = '1' if self.dop_function.str_find(str(description).lower(), {'давлен'}) else '0'
                    
                    list_AI.append(dict(variable = f'AI[{count_AI}]',
                                        tag = tag,
                                        name = description,
                                        pValue = f'mAI8[{isdigit_num[0]}, {module_s}]',
                                        pHealth = f'mAI8_HEALTH[{isdigit_num[0]}]',
                                        group_analog = group_analog,
                                        group_ust_analog = group_ust_analog,
                                        unit = unit,
                                        sign_VU = sign,
                                        flag_MPa_kgccm2 = flag_MPa_kgccm2,
                                        number_NA_or_aux = '',
                                        vibration_pump = '',
                                        vibration_motor = '',
                                        current_motor = '',
                                        aux_outlet_pressure = '',
                                        number_ust_min_avar = '',
                                        number_ust_min_pred = '',
                                        number_ust_max_pred = '',
                                        number_ust_max_avar = '',
                                        field_min = '4000',
                                        field_max = '20000',
                                        eng_min = eng_min,
                                        eng_max = eng_max,
                                        reliability_min = '3900',
                                        reliability_max = '20100',
                                        hysteresis = '0',
                                        filtration = '0',
                                        ust_min_6 = '', ust_min_5 = '', ust_min_4 = '', ust_min_3 = '', ust_min_2 = '', ust_min = '',
                                        ust_max = '', ust_max_2 = '', ust_max_3 = '', ust_max_4 = '', ust_max_5 = '', ust_max_6 = '',
                                        value_precision = value_precision,
                                        PIC = '', group_trend = '', hysteresis_TI = '0,1', unit_physical_ACP = 'мкА', 
                                        setpoint_map_rule = rule, fuse = '', uso = uso_s, basket = basket_s, module = module_s, channel = channel_s,
                                        AlphaHMI = '', AlphaHMI_PIC1 = '', AlphaHMI_PIC1_Number_kont = '', AlphaHMI_PIC2 = '', 
                                        AlphaHMI_PIC2_Number_kont = '', AlphaHMI_PIC3 = '', AlphaHMI_PIC3_Number_kont = '', 
                                        AlphaHMI_PIC4 = '', AlphaHMI_PIC4_Number_kont = ''))

            # Checking for the existence of a database
            AI.insert_many(list_AI).execute()

        msg[f'{today} - Таблица: AI заполнена'] = 1
        return(msg)
    # Заполняем таблицу AI
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'pValue', 'pHealth', 'group_analog',
                        'group_ust_analog',  'unit',  'sign_VU',  'flag_MPa_kgccm2',  'number_NA_or_aux',  
                        'vibration_pump',  'vibration_motor',  'current_motor',  'aux_outlet_pressure', 
                        'number_ust_min_avar',  'number_ust_min_pred',  'number_ust_max_pred',  'number_ust_max_avar', 
                        'field_min',  'field_max',  'eng_min', 'eng_max', 'reliability_min', 'reliability_max', 
                        'hysteresis', 'filtration', 'ust_min_6', 'ust_min_5', 'ust_min_4', 'ust_min_3', 
                        'ust_min_2', 'ust_min', 'ust_max', 'ust_max_2', 'ust_max_3', 'ust_max_4',
                        'ust_max_5', 'ust_max_6', 'value_precision', 'PIC', 'group_trend', 'hysteresis_TI', 
                        'unit_physical_ACP', 'setpoint_map_rule', 'fuse', 'uso', 'basket', 'module', 'channel', 'AlphaHMI', 'AlphaHMI_PIC1', 
                        'AlphaHMI_PIC1_Number_kont', 'AlphaHMI_PIC2', 'AlphaHMI_PIC2_Number_kont',
                        'AlphaHMI_PIC3', 'AlphaHMI_PIC3_Number_kont', 'AlphaHMI_PIC4', 'AlphaHMI_PIC4_Number_kont']
        msg = self.dop_function.column_check(AI, 'ai', list_default)
        return msg 

# Work with filling in the table 'AO'
class Filling_AO():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = general_functions()
    # Получаем данные с таблицы Signals 
    def getting_modul(self):
        msg = {}
        list_AO = []
        count_AO = 0
        
        with db:
            if self.dop_function.empty_table('signals'): 
                msg[f'{today} - Таблица: Signals пустая! Заполни таблицу!'] = 2
                return msg
            
            for row_sql in Signals.select().dicts():
                id_s        = row_sql['id']  
                uso_s       = row_sql['uso']    
                tag         = row_sql['tag']
                description = str(row_sql['description']).replace('"', '').replace("'", '')
                type_signal = row_sql['type_signal']
                scheme      = row_sql['schema']
                basket_s    = row_sql['basket']
                module_s    = row_sql['module']
                channel_s   = row_sql['channel']

                if self.dop_function.str_find(type_signal, {'AO'}) or self.dop_function.str_find(scheme, {'AO'}):
                    count_AO += 1
                    # Выбор между полным заполнением или обновлением
                    empty = self.cursor.execute('SELECT COUNT(*) FROM ao')
                    if int(empty.fetchall()[0][0]) == 0:
                        msg[f'{today} - Таблица: AO пуста, идет заполнение'] = 1
                    else:
                        msg[f'{today} - Таблица: AO не пуста, идет обновление'] = 1

                    coincidence = AO.select().where(AO.uso     == uso_s,
                                                    AO.basket  == basket_s,
                                                    AO.module  == module_s,
                                                    AO.channel == channel_s)
                    if bool(coincidence):
                        exist_tag  = AO.select().where(AO.tag == tag)
                        exist_name = AO.select().where(AO.name == description)

                        if not bool(exist_tag):
                            select_tag = self.cursor.execute(f'''SELECT id, tag 
                                                                 FROM ao
                                                                 WHERE uso='{uso_s}' AND 
                                                                       basket={basket_s} AND 
                                                                       module={module_s} AND 
                                                                       channel={channel_s}''')
                            for id_, tag_ in select_tag.fetchall():
                                msg[f'{today} - Таблица: AO, у сигнала обновлен tag: id = {id_}, ({tag_}) {tag}'] = 2
                            self.cursor.execute(f'''UPDATE ao
                                                    SET tag='{tag}' 
                                                    WHERE uso='{uso_s}' AND 
                                                          basket={basket_s} AND 
                                                          module={module_s} AND 
                                                          channel={channel_s}''')
    
                        if not bool(exist_name):
                            select_name = self.cursor.execute(f'''SELECT id, name 
                                                                  FROM ao
                                                                  WHERE uso='{uso_s}' AND 
                                                                        basket={basket_s} AND 
                                                                        module={module_s} AND 
                                                                        channel={channel_s}''')
                            for id_, name_ in select_name.fetchall():
                                msg[f'{today} - Таблица: AO, у сигнала обновлен name: id = {id_}, ({name_}) {description}'] = 2
                            self.cursor.execute(f'''UPDATE ao
                                                    SET name='{description}' 
                                                    WHERE uso='{uso_s}' AND 
                                                          basket={basket_s} AND 
                                                          module={module_s} AND 
                                                          channel={channel_s}''')
                        continue

                    # Сквозной номер модуля
                    for through_module_number in HardWare.select().dicts():
                        tag_h    = through_module_number['tag']
                        uso_h    = through_module_number['uso']
                        basket_h = through_module_number['basket']

                        if uso_s == uso_h and basket_s == basket_h:
                            type_mod = through_module_number[f'variable_{module_s}']
                            isdigit_num  = re.findall('\d+', str(type_mod))

                            try   : isdigit_num = isdigit_num[0]
                            except: 
                                isdigit_num = ''
                                msg[f'{today} - В таблице HardWare не найден модуль сигнала: {id_s}, {tag}, {description}, {uso_s}_A{basket_s}_{module_s}_{channel_s}, "pValue" не заполнен'] = 2
                            break

                    if module_s < 10: prefix = f'0{module_s}' 
                    else            : prefix = f'{module_s}'
                
                    list_AO.append(dict(variable = f'AO[{count_AO}]',
                                        tag = tag,
                                        name = description,
                                        pValue = f'{tag_h}_{prefix}_AO[{channel_s}]',
                                        pHealth = f'mAO_HEALTH[{isdigit_num[0]}]',
                                        uso = uso_s, 
                                        basket = basket_s, 
                                        module = module_s, 
                                        channel = channel_s,
                                        ))

            # Checking for the existence of a database
            AO.insert_many(list_AO).execute()

        msg[f'{today} - Таблица: AO заполнена'] = 1
        return(msg)
    # Заполняем таблицу AO
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'pValue', 'pHealth', 'uso', 'basket', 'module', 'channel']
        msg = self.dop_function.column_check(AO, 'ao', list_default)
        return msg 

# Work with filling in the table 'DI'
class Filling_DI():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = general_functions()
    # Получаем данные с таблицы Signals 
    def getting_modul(self):
        msg = {}
        list_DI = []
        count_DI = 0
        with db:
            if self.dop_function.empty_table('signals'): 
                msg[f'{today} - Таблица: Signals пустая! Заполни таблицу!'] = 2
                return msg
            
            for row_sql in Signals.select().dicts():
                id_s       = row_sql['id'] 
                uso_s       = row_sql['uso']    
                tag         = row_sql['tag']
                description = str(row_sql['description']).replace('"', '').replace("'", '')
                type_signal = row_sql['type_signal']
                scheme      = row_sql['schema']
                basket_s    = row_sql['basket']
                module_s    = row_sql['module']
                channel_s   = row_sql['channel']

                if self.dop_function.str_find(type_signal, {'DI'}) or self.dop_function.str_find(scheme, {'DI'}):
                    count_DI += 1
                    # Выбор между полным заполнением или обновлением
                    empty = self.cursor.execute('SELECT COUNT(*) FROM di')
                    if int(empty.fetchall()[0][0]) == 0:
                        msg[f'{today} - Таблица: DI пуста, идет заполнение'] = 1
                    else:
                        msg[f'{today} - Таблица: DI не пуста, идет обновление'] = 1

                    coincidence = DI.select().where(DI.uso     == uso_s,
                                                    DI.basket  == basket_s,
                                                    DI.module  == module_s,
                                                    DI.channel == channel_s)
                    if bool(coincidence):
                        exist_tag  = DI.select().where(DI.tag == tag)
                        exist_name = DI.select().where(DI.name == description)

                        if not bool(exist_tag):
                            select_tag = self.cursor.execute(f'''SELECT id, tag 
                                                                 FROM di
                                                                 WHERE uso='{uso_s}' AND 
                                                                       basket={basket_s} AND 
                                                                       module={module_s} AND 
                                                                       channel={channel_s}''')
                            for id_, tag_ in select_tag.fetchall():
                                msg[f'{today} - Таблица: DI, у сигнала обновлен tag: id = {id_}, ({tag_}) {tag}'] = 2
                            self.cursor.execute(f'''UPDATE di
                                                    SET tag='{tag}' 
                                                    WHERE uso='{uso_s}' AND 
                                                          basket={basket_s} AND 
                                                          module={module_s} AND 
                                                          channel={channel_s}''')
    
                        if not bool(exist_name):
                            select_name = self.cursor.execute(f'''SELECT id, name 
                                                                  FROM di
                                                                  WHERE uso='{uso_s}' AND 
                                                                        basket={basket_s} AND 
                                                                        module={module_s} AND 
                                                                        channel={channel_s}''')
                            for id_, name_ in select_name.fetchall():
                                msg[f'{today} - Таблица: DI, у сигнала обновлен name: id = {id_}, ({name_}) {description}'] = 2
                            self.cursor.execute(f'''UPDATE di
                                                    SET name='{description}' 
                                                    WHERE uso='{uso_s}' AND 
                                                          basket={basket_s} AND 
                                                          module={module_s} AND 
                                                          channel={channel_s}''')
                        continue

                    # Сквозной номер модуля
                    for through_module_number in HardWare.select().dicts():
                        tag_h    = through_module_number['tag']
                        uso_h    = through_module_number['uso']
                        basket_h = through_module_number['basket']

                        if uso_s == uso_h and basket_s == basket_h:
                            type_mod = through_module_number[f'variable_{module_s}']
                            isdigit_num  = re.findall('\d+', str(type_mod))

                            try   : isdigit_num = isdigit_num[0]
                            except: 
                                isdigit_num = ''
                                msg[f'{today} - В таблице HardWare не найден модуль сигнала: {id_s}, {tag}, {description}, {uso_s}_A{basket_s}_{module_s}_{channel_s}, "pValue" не заполнен'] = 2
                            break

                    if module_s < 10: prefix = f'0{module_s}' 
                    else            : prefix = f'{module_s}'

                    if self.dop_function.str_find(str(tag).lower(), {'csc'}) : group_diskrets = 'Диагностика'
                    elif self.dop_function.str_find(str(tag).lower(), {'ec'}): group_diskrets = 'Электроснабжение'
                    else: group_diskrets = 'Общие'
                    
                    list_DI.append(dict(variable = f'DI[{count_DI}]',
                                        tag = tag,
                                        name = description,
                                        pValue = f'{tag_h}_{prefix}_DI[{channel_s}]',
                                        pHealth = f'mDI_HEALTH[{str(isdigit_num)}]',
                                        Inv = '0',
                                        ErrValue = '0',
                                        priority_0 = '1',
                                        priority_1 = '1',
                                        Msg = '1',
                                        isDI_NC = '',
                                        isAI_Warn = '',
                                        isAI_Avar = '',
                                        pNC_AI = '',
                                        TS_ID = '',
                                        isModuleNC = '',
                                        Pic = '',
                                        tabl_msg = 'TblDiscretes',
                                        group_diskrets = group_diskrets,
                                        msg_priority_0 = '',
                                        msg_priority_1 = '',
                                        short_title = description,
                                        uso = uso_s, basket = basket_s, module = module_s, channel = channel_s,
                                        AlphaHMI = '', AlphaHMI_PIC1 = '', AlphaHMI_PIC1_Number_kont = '', AlphaHMI_PIC2 = '', 
                                        AlphaHMI_PIC2_Number_kont = '', AlphaHMI_PIC3 = '', AlphaHMI_PIC3_Number_kont = '', 
                                        AlphaHMI_PIC4 = '', AlphaHMI_PIC4_Number_kont = ''))

            # Checking for the existence of a database
            DI.insert_many(list_DI).execute()

        msg[f'{today} - Таблица: DI заполнена'] = 1
        return(msg)
    # Заполняем таблицу DI
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'pValue', 'pHealth', 'Inv',
                        'ErrValue', 'priority_0', 'priority_1', 'Msg', 'isDI_NC',  
                        'isAI_Warn', 'isAI_Avar', 'pNC_AI',  'TS_ID', 
                        'isModuleNC',  'Pic',  'tabl_msg',  'group_diskrets', 
                        'msg_priority_0',  'msg_priority_1', 'short_title', 'uso', 'basket', 'module', 'channel', 
                        'AlphaHMI', 'AlphaHMI_PIC1', 'AlphaHMI_PIC1_Number_kont', 'AlphaHMI_PIC2',
                        'AlphaHMI_PIC2_Number_kont','AlphaHMI_PIC3', 'AlphaHMI_PIC3_Number_kont', 
                        'AlphaHMI_PIC4', 'AlphaHMI_PIC4_Number_kont']
        msg = self.dop_function.column_check(DI, 'di', list_default)
        return msg 

# Work with filling in the table 'DO'
class Filling_DO():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = general_functions()
    # Получаем данные с таблицы Signals 
    def getting_modul(self):
        msg = {}
        list_DO = []
        count_DO = 0
        with db:
            if self.dop_function.empty_table('signals'): 
                msg[f'{today} - Таблица: Signals пустая! Заполни таблицу!'] = 2
                return msg
            
            for row_sql in Signals.select().dicts():
                id_s       = row_sql['id'] 
                uso_s       = row_sql['uso']    
                tag         = row_sql['tag']
                description = str(row_sql['description']).replace('"', '').replace("'", '')
                type_signal = row_sql['type_signal']
                scheme      = row_sql['schema']
                basket_s    = row_sql['basket']
                module_s    = row_sql['module']
                channel_s   = row_sql['channel']

                if self.dop_function.str_find(type_signal, {'DO'}) or self.dop_function.str_find(scheme, {'DO'}):
                    count_DO += 1
                    # Выбор между полным заполнением или обновлением
                    empty = self.cursor.execute('SELECT COUNT(*) FROM do')
                    if int(empty.fetchall()[0][0]) == 0:
                        msg[f'{today} - Таблица: DO пуста, идет заполнение'] = 1
                    else:
                        msg[f'{today} - Таблица: DO не пуста, идет обновление'] = 1

                    coincidence = DO.select().where(DO.uso     == uso_s,
                                                    DO.basket  == basket_s,
                                                    DO.module  == module_s,
                                                    DO.channel == channel_s)
                    if bool(coincidence):
                        exist_tag  = DO.select().where(DO.tag == tag)
                        exist_name = DO.select().where(DO.name == description)

                        if not bool(exist_tag):
                            select_tag = self.cursor.execute(f'''SELECT id, tag 
                                                                 FROM do
                                                                 WHERE uso='{uso_s}' AND 
                                                                       basket={basket_s} AND 
                                                                       module={module_s} AND 
                                                                       channel={channel_s}''')
                            for id_, tag_ in select_tag.fetchall():
                                msg[f'{today} - Таблица: DO, у сигнала обновлен tag: id = {id_}, ({tag_}) {tag}'] = 2
                            self.cursor.execute(f'''UPDATE do
                                                    SET tag='{tag}' 
                                                    WHERE uso='{uso_s}' AND 
                                                          basket={basket_s} AND 
                                                          module={module_s} AND 
                                                          channel={channel_s}''')
    
                        if not bool(exist_name):
                            select_name = self.cursor.execute(f'''SELECT id, name 
                                                                  FROM do
                                                                  WHERE uso='{uso_s}' AND 
                                                                        basket={basket_s} AND 
                                                                        module={module_s} AND 
                                                                        channel={channel_s}''')
                            for id_, name_ in select_name.fetchall():
                                msg[f'{today} - Таблица: DO, у сигнала обновлен name: id = {id_}, ({name_}) {description}'] = 2
                            self.cursor.execute(f'''UPDATE do
                                                    SET name='{description}' 
                                                    WHERE uso='{uso_s}' AND 
                                                          basket={basket_s} AND 
                                                          module={module_s} AND 
                                                          channel={channel_s}''')
                        continue

                    # Сквозной номер модуля
                    for through_module_number in HardWare.select().dicts():
                        tag_h    = through_module_number['tag']
                        uso_h    = through_module_number['uso']
                        basket_h = through_module_number['basket']

                        if uso_s == uso_h and basket_s == basket_h:
                            type_mod = through_module_number[f'variable_{module_s}']
                            isdigit_num  = re.findall('\d+', str(type_mod))

                            try   : isdigit_num = isdigit_num[0]
                            except: 
                                isdigit_num = ''
                                msg[f'{today} - В таблице HardWare не найден модуль сигнала: {id_s}, {tag}, {description}, {uso_s}_A{basket_s}_{module_s}_{channel_s}, "pValue" не заполнен'] = 2
                            break

                    if module_s < 10: prefix = f'0{module_s}' 
                    else            : prefix = f'{module_s}'

                    list_DO.append(dict(variable = f'DO[{count_DO}]',
                                        tag = tag,
                                        name = description,
                                        pValue = f'{tag_h}_{prefix}_DO[{channel_s}]',
                                        pHealth = f'mDO_HEALTH[{str(isdigit_num)}]',
                                        short_title = description,
                                        uso = uso_s, basket = basket_s, module = module_s, channel = channel_s,
                                        AlphaHMI = '', AlphaHMI_PIC1 = '', AlphaHMI_PIC1_Number_kont = '', AlphaHMI_PIC2 = '', 
                                        AlphaHMI_PIC2_Number_kont = '', AlphaHMI_PIC3 = '', AlphaHMI_PIC3_Number_kont = '', 
                                        AlphaHMI_PIC4 = '', AlphaHMI_PIC4_Number_kont = ''))

            # Checking for the existence of a database
            DO.insert_many(list_DO).execute()

        msg[f'{today} - Таблица: DO заполнена'] = 1
        return(msg)
    # Заполняем таблицу DO
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'pValue', 'pHealth', 'short_title', 'uso', 'basket', 'module', 'channel', 
                        'AlphaHMI', 'AlphaHMI_PIC1', 'AlphaHMI_PIC1_Number_kont', 'AlphaHMI_PIC2',
                        'AlphaHMI_PIC2_Number_kont','AlphaHMI_PIC3', 'AlphaHMI_PIC3_Number_kont', 
                        'AlphaHMI_PIC4', 'AlphaHMI_PIC4_Number_kont']
        msg = self.dop_function.column_check(DO, 'do', list_default)
        return msg 
    
# Work with filling in the table 'KTPR'
class Filling_KTPR():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = general_functions()
    def getting_modul(self):
        msg = {}
        list_KTPR = []
        with db:
            for i in range(1, 97):
                list_KTPR.append(dict(variable = f'KTPR[{i}]',
                                      tag = '',
                                      name = 'Резерв',
                                      avar_parameter = '',
                                      prohibition_masking = '',
                                      auto_unlock_protection = '',
                                      shutdown_PNS_a_time_delay_up_5s_after_turning_off_all_NA = '',
                                      bitmask_protection_group_membership = '',
                                      stop_type_NA = '',
                                      pump_station_stop_type = '',
                                      closing_gate_valves_at_the_inlet_NPS = '',
                                      closing_gate_valves_at_the_outlet_NPS = '',
                                      closing_gate_valves_between_PNS_and_MNS = '',
                                      closing_gate_valves_between_RP_and_PNS = '',
                                      closing_valves_inlet_and_outlet_MNS = '',
                                      closing_valves_inlet_and_outlet_PNS = '',
                                      closing_valves_inlet_and_outlet_MNA = '',
                                      closing_valves_inlet_and_outlet_PNA = '',
                                      closing_valves_inlet_RD = '',
                                      closing_valves_outlet_RD = '',
                                      closing_valves_inlet_SSVD = '',
                                      closing_valves_inlet_FGU = '',
                                      closing_secant_valve_connection_unit__oil_production_oil_refining_facility = '',
                                      closing_valves_inlet_RP = '',
                                      reserve_protect_14 = '',
                                      reserve_protect_15 = '',
                                      shutdown_oil_pumps_after_signal_stopped_NA = '',
                                      shutdown_circulating_water_pumps = '',
                                      shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_MNS = '',
                                      shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_PNS = '',
                                      shutdown_pumps_pumping_out_from_tanks_SSVD = '',
                                      switching_off_the_electric_room_fans = '',
                                      shutdown_of_booster_fans_ED = '',
                                      shutdown_of_retaining_fans_of_the_electrical_room = '',
                                      shutdown_of_ED_air_compressors = '',
                                      shutdown_pumps_providing_oil_oil_product_pumping_from_oil_production_oil_refining_facilities = '',
                                      disabling_pumps_for_pumping_oil_oil_products_through_BIC = '',
                                      shutdown_domestic_and_drinking_water_pumps = '',
                                      shutdown_of_art_well_pumps = '',
                                      AVO_shutdown = '',
                                      shutdown_of_water_cooling_fans_circulating_water_supply_system = '',
                                      shutdown_exhaust_fans_of_the_pumping_room_of_the_MNS = '',
                                      shutdown_of_exhaust_fans_of_the_pumping_room_PNS = '',
                                      shutdown_of_exhaust_fans_in_the_centralized_oil_system_room = '',
                                      shutdown_of_exhaust_fans_oil_pit_in_the_electrical_room = '',
                                      shutdown_of_exhaust_fans_in_the_RD_room = '',
                                      shutdown_of_exhaust_fans_in_the_SSVD_room = '',
                                      shutdown_of_the_roof_fans_of_the_MNS_pump_room = '',
                                      shutdown_of_the_roof_fans_of_the_PNS_pump_room = '',
                                      switching_off_the_supply_fans_pumping_room_of_the_MNS_and_closing_the_fire_dampers = '',
                                      switching_off_the_supply_fans_pumping_room_of_the_PNS_and_closing_the_fire_dampers = '',
                                      switch_off_the_supply_fans_in_the_centralized_oil_system_room_and_close_the_fire_dampers = '',
                                      switching_off_the_supply_fan_of_the_RD_room = '',
                                      switching_off_the_supply_fan_of_the_SSVD_room = '',
                                      switching_off_the_supply_fans_of_the_ED_air_compressor_room_and_closing_the_fire_dampers = '',
                                      switching_off_the_supply_fan_of_the_BIK_room = '',
                                      switching_off_the_supply_fan_of_the_SIKN_room = '',  
                                      closing_the_air_valves_louvered_grilles_of_the_pump_room = '',
                                      closing_of_air_valves_louvered_grilles_of_the_compressor_room_of_the_ED_air_overpressure = '',
                                      shutdown_of_electric_oil_heaters = '',
                                      shutdown_of_the_electric_heaters_of_the_leakage_collection_tank_MNS = '',
                                      shutdown_of_the_electric_heaters_of_the_leakage_collection_tank_PNS = '',
                                      shutdown_of_electric_heaters_of_the_SIKN_leak_collection_tank = '',
                                      shutdown_of_air_coolers_of_the_locking_system_of_mechanical_seals_of_all_MNA = '',
                                      shutdown_of_air_coolers_of_the_locking_system_of_mechanical_seals_disconnected_NA = '',
                                      shutdown_of_the_external_cooling_circuit_ChRP_MNA = '',
                                      shutdown_of_the_external_cooling_circuit_ChRP_PNA = '',
                                      shutdown_of_locking_system_pumps = '',
                                      shutdown_of_pumps_for_pumping_oil_oil_products_through_the_operational_BIK = '',
                                      shutdown_of_pumping_pumps_from_leakage_collection_tanks_of_all_SIKN = '',
                                      shutdown_of_anticondensation_electric_heaters_ED = '',
                                      fire_protection = '',
                                      reserve_aux_15 = '',
                                      time_ust = '',
                                      PIC = '',
                                      group_ust = 'Временные уставки общестанционных защит',
                                      rule_map_ust = 'Временные уставки',
                                      number_list_VU = '',
                                      number_protect_VU = ''))

            # Checking for the existence of a database
            KTPR.insert_many(list_KTPR).execute()

        msg[f'{today} - Таблица: KTPR сформирована'] = 1
        return(msg)
    # Заполняем таблицу KTPR
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 
                        'avar_parameter', 'prohibition_masking', 'auto_unlock_protection', 'shutdown_PNS_a_time_delay_up_5s_after_turning_off_all_NA',
                        'bitmask_protection_group_membership', 'stop_type_NA', 'pump_station_stop_type',
                        'closing_gate_valves_at_the_inlet_NPS', 'closing_gate_valves_at_the_outlet_NPS', 'closing_gate_valves_between_PNS_and_MNS',
                        'closing_gate_valves_between_RP_and_PNS', 'closing_valves_inlet_and_outlet_MNS', 'closing_valves_inlet_and_outlet_PNS',
                        'closing_valves_inlet_and_outlet_MNA', 'closing_valves_inlet_and_outlet_PNA', 'closing_valves_inlet_RD',
                        'closing_valves_outlet_RD', 'closing_valves_inlet_SSVD', 'closing_valves_inlet_FGU',
                        'closing_secant_valve_connection_unit__oil_production_oil_refining_facility', 'closing_valves_inlet_RP', 'reserve_protect_14', 'reserve_protect_15',
                        'shutdown_oil_pumps', 'shutdown_oil_pumps_after_signal_stopped_NA', 'shutdown_circulating_water_pumps',
                        'shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_MNS', 'shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_PNS',
                        'shutdown_pumps_pumping_out_from_tanks_SSVD', 'switching_off_the_electric_room_fans', 'shutdown_of_booster_fans_ED', 
                        'shutdown_of_retaining_fans_of_the_electrical_room', 'shutdown_of_ED_air_compressors', 
                        'shutdown_pumps_providing_oil_oil_product_pumping_from_oil_production_oil_refining_facilities', 
                        'disabling_pumps_for_pumping_oil_oil_products_through_BIC', 'shutdown_domestic_and_drinking_water_pumps', 'shutdown_of_art_well_pumps',
                        'AVO_shutdown', 'shutdown_of_water_cooling_fans_circulating_water_supply_system',
                        'shutdown_exhaust_fans_of_the_pumping_room_of_the_MNS', 'shutdown_of_exhaust_fans_of_the_pumping_room_PNS',
                        'shutdown_of_exhaust_fans_in_the_centralized_oil_system_room', 'shutdown_of_exhaust_fans_oil_pit_in_the_electrical_room', 
                        'shutdown_of_exhaust_fans_in_the_RD_room', 'shutdown_of_exhaust_fans_in_the_SSVD_room',
                        'shutdown_of_the_roof_fans_of_the_MNS_pump_room', 'shutdown_of_the_roof_fans_of_the_PNS_pump_room',
                        'switching_off_the_supply_fans_pumping_room_of_the_MNS_and_closing_the_fire_dampers', 'switching_off_the_supply_fans_pumping_room_of_the_PNS_and_closing_the_fire_dampers',
                        'switch_off_the_supply_fans_in_the_centralized_oil_system_room_and_close_the_fire_dampers', 'switching_off_the_supply_fan_of_the_RD_room',
                        'switching_off_the_supply_fan_of_the_SSVD_room', 'switching_off_the_supply_fans_of_the_ED_air_compressor_room_and_closing_the_fire_dampers',
                        'switching_off_the_supply_fan_of_the_BIK_room', 'switching_off_the_supply_fan_of_the_SIKN_room',
                        'closing_the_air_valves_louvered_grilles_of_the_pump_room', 'closing_of_air_valves_louvered_grilles_of_the_compressor_room_of_the_ED_air_overpressure',
                        'shutdown_of_electric_oil_heaters', 'shutdown_of_the_electric_heaters_of_the_leakage_collection_tank_MNS',
                        'shutdown_of_the_electric_heaters_of_the_leakage_collection_tank_PNS', 'shutdown_of_electric_heaters_of_the_SIKN_leak_collection_tank',
                        'shutdown_of_air_coolers_of_the_locking_system_of_mechanical_seals_of_all_MNA', 'shutdown_of_air_coolers_of_the_locking_system_of_mechanical_seals_disconnected_NA',
                        'shutdown_of_the_external_cooling_circuit_ChRP_MNA', 'shutdown_of_the_external_cooling_circuit_ChRP_PNA', 'shutdown_of_locking_system_pumps',
                        'shutdown_of_pumps_for_pumping_oil_oil_products_through_the_operational_BIK',
                        'shutdown_of_pumping_pumps_from_leakage_collection_tanks_of_all_SIKN', 'shutdown_of_anticondensation_electric_heaters_ED', 'fire_protection', 'reserve_aux_15', 
                        'time_ust', 'PIC', 'group_ust', 'rule_map_ust', 'number_list_VU', 'number_protect_VU']
        msg = self.dop_function.column_check(KTPR, 'ktpr', list_default)
        return msg 
# Work with filling in the table 'KTPRA'
class Filling_KTPRA():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = general_functions()
    # Получаем данные с таблицы Signals 
    def getting_modul(self):
        msg = {}
        list_ktpra = []
        with db:
            for i in range(1, 5):
                for k in range(1, 97):
                    list_ktpra.append(dict(variable = f'KTPRA[{i}][{k}]',
                                            tag  = '',
                                            name = 'Резерв',
                                            NA = '',
                                            avar_parameter = '',
                                            stop_type = '',
                                            AVR = '',
                                            close_valves = '',
                                            prohibition_of_masking = '',
                                            time_setting = '',
                                            PIC = '',
                                            group_ust = f'Tm - Агрегатные защиты МНА{i}',
                                            rule_map_ust = 'Временные уставки',
                                            number_list_VU = '',
                                            number_protect_VU = '',
                                            number_pump_VU = f'{i}'))
            # Checking for the existence of a database
            KTPRA.insert_many(list_ktpra).execute()
        msg[f'{today} - Таблица: KTPRA заполнена'] = 1
        return(msg)
    # Заполняем таблицу KTPRA
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 
                        'NA', 'avar_parameter', 'stop_type', 'AVR', 'close_valves',
                        'prohibition_of_masking', 'time_setting', 'PIC', 
                        'group_ust', 'rule_map_ust', 'number_list_VU', 'number_protect_VU', 'number_pump_VU']
        msg = self.dop_function.column_check(KTPRA, 'ktpra', list_default)
        return msg 
# Work with filling in the table 'KTPRS'
class Filling_KTPRS():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = general_functions()
    # Получаем данные с таблицы Signals 
    def getting_modul(self):
        msg = {}
        list_DO = []
        count_DO = 0
        with db:
            if self.dop_function.empty_table('signals'): 
                msg[f'{today} - Таблица: Signals пустая! Заполни таблицу!'] = 2
                return msg
            
            for row_sql in Signals.select().dicts():
                id_s       = row_sql['id'] 
                uso_s       = row_sql['uso']    
                tag         = row_sql['tag']
                description = str(row_sql['description']).replace('"', '').replace("'", '')
                type_signal = row_sql['type_signal']
                scheme      = row_sql['schema']
                basket_s    = row_sql['basket']
                module_s    = row_sql['module']
                channel_s   = row_sql['channel']

                if self.dop_function.str_find(type_signal, {'DO'}) or self.dop_function.str_find(scheme, {'DO'}):
                    count_DO += 1
                    # Выбор между полным заполнением или обновлением
                    empty = self.cursor.execute('SELECT COUNT(*) FROM do')
                    if int(empty.fetchall()[0][0]) == 0:
                        msg[f'{today} - Таблица: DO пуста, идет заполнение'] = 1
                    else:
                        msg[f'{today} - Таблица: DO не пуста, идет обновление'] = 1

                    coincidence = DO.select().where(DO.uso     == uso_s,
                                                    DO.basket  == basket_s,
                                                    DO.module  == module_s,
                                                    DO.channel == channel_s)
                    if bool(coincidence):
                        exist_tag  = DO.select().where(DO.tag == tag)
                        exist_name = DO.select().where(DO.name == description)

                        if not bool(exist_tag):
                            select_tag = self.cursor.execute(f'''SELECT id, tag 
                                                                 FROM do
                                                                 WHERE uso='{uso_s}' AND 
                                                                       basket={basket_s} AND 
                                                                       module={module_s} AND 
                                                                       channel={channel_s}''')
                            for id_, tag_ in select_tag.fetchall():
                                msg[f'{today} - Таблица: DO, у сигнала обновлен tag: id = {id_}, ({tag_}) {tag}'] = 2
                            self.cursor.execute(f'''UPDATE do
                                                    SET tag='{tag}' 
                                                    WHERE uso='{uso_s}' AND 
                                                          basket={basket_s} AND 
                                                          module={module_s} AND 
                                                          channel={channel_s}''')
    
                        if not bool(exist_name):
                            select_name = self.cursor.execute(f'''SELECT id, name 
                                                                  FROM do
                                                                  WHERE uso='{uso_s}' AND 
                                                                        basket={basket_s} AND 
                                                                        module={module_s} AND 
                                                                        channel={channel_s}''')
                            for id_, name_ in select_name.fetchall():
                                msg[f'{today} - Таблица: DO, у сигнала обновлен name: id = {id_}, ({name_}) {description}'] = 2
                            self.cursor.execute(f'''UPDATE do
                                                    SET name='{description}' 
                                                    WHERE uso='{uso_s}' AND 
                                                          basket={basket_s} AND 
                                                          module={module_s} AND 
                                                          channel={channel_s}''')
                        continue

                    # Сквозной номер модуля
                    for through_module_number in HardWare.select().dicts():
                        tag_h    = through_module_number['tag']
                        uso_h    = through_module_number['uso']
                        basket_h = through_module_number['basket']

                        if uso_s == uso_h and basket_s == basket_h:
                            type_mod = through_module_number[f'variable_{module_s}']
                            isdigit_num  = re.findall('\d+', str(type_mod))

                            try   : isdigit_num = isdigit_num[0]
                            except: 
                                isdigit_num = ''
                                msg[f'{today} - В таблице HardWare не найден модуль сигнала: {id_s}, {tag}, {description}, {uso_s}_A{basket_s}_{module_s}_{channel_s}, "pValue" не заполнен'] = 2
                            break

                    if module_s < 10: prefix = f'0{module_s}' 
                    else            : prefix = f'{module_s}'

                    list_DO.append(dict(variable = f'DO[{count_DO}]',
                                        tag = tag,
                                        name = description,
                                        pValue = f'{tag_h}_{prefix}_DO[{channel_s}]',
                                        pHealth = f'mDO_HEALTH[{str(isdigit_num)}]',
                                        short_title = description,
                                        uso = uso_s, basket = basket_s, module = module_s, channel = channel_s,
                                        AlphaHMI = '', AlphaHMI_PIC1 = '', AlphaHMI_PIC1_Number_kont = '', AlphaHMI_PIC2 = '', 
                                        AlphaHMI_PIC2_Number_kont = '', AlphaHMI_PIC3 = '', AlphaHMI_PIC3_Number_kont = '', 
                                        AlphaHMI_PIC4 = '', AlphaHMI_PIC4_Number_kont = ''))

            # Checking for the existence of a database
            DO.insert_many(list_DO).execute()

        msg[f'{today} - Таблица: DO заполнена'] = 1
        return(msg)
    # Заполняем таблицу KTPRS
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'drawdown', 'reference_to_value', 'priority_msg_0', 
                        'priority_msg_1', 'prohibition_issuing_msg', 'PIC']
        msg = self.dop_function.column_check(KTPRS, 'ktprs', list_default)
        return msg 
    
    # Work with filling in the table 'KTPR'
# Work with filling in the table 'GMPNA'
class Filling_GMPNA():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = general_functions()
    # Получаем данные с таблицы Signals 
    def getting_modul(self):
        msg = {}
        list_DO = []
        count_DO = 0
        with db:
            if self.dop_function.empty_table('signals'): 
                msg[f'{today} - Таблица: Signals пустая! Заполни таблицу!'] = 2
                return msg
            
            for row_sql in Signals.select().dicts():
                id_s       = row_sql['id'] 
                uso_s       = row_sql['uso']    
                tag         = row_sql['tag']
                description = str(row_sql['description']).replace('"', '').replace("'", '')
                type_signal = row_sql['type_signal']
                scheme      = row_sql['schema']
                basket_s    = row_sql['basket']
                module_s    = row_sql['module']
                channel_s   = row_sql['channel']

                if self.dop_function.str_find(type_signal, {'DO'}) or self.dop_function.str_find(scheme, {'DO'}):
                    count_DO += 1
                    # Выбор между полным заполнением или обновлением
                    empty = self.cursor.execute('SELECT COUNT(*) FROM do')
                    if int(empty.fetchall()[0][0]) == 0:
                        msg[f'{today} - Таблица: DO пуста, идет заполнение'] = 1
                    else:
                        msg[f'{today} - Таблица: DO не пуста, идет обновление'] = 1

                    coincidence = DO.select().where(DO.uso     == uso_s,
                                                    DO.basket  == basket_s,
                                                    DO.module  == module_s,
                                                    DO.channel == channel_s)
                    if bool(coincidence):
                        exist_tag  = DO.select().where(DO.tag == tag)
                        exist_name = DO.select().where(DO.name == description)

                        if not bool(exist_tag):
                            select_tag = self.cursor.execute(f'''SELECT id, tag 
                                                                 FROM do
                                                                 WHERE uso='{uso_s}' AND 
                                                                       basket={basket_s} AND 
                                                                       module={module_s} AND 
                                                                       channel={channel_s}''')
                            for id_, tag_ in select_tag.fetchall():
                                msg[f'{today} - Таблица: DO, у сигнала обновлен tag: id = {id_}, ({tag_}) {tag}'] = 2
                            self.cursor.execute(f'''UPDATE do
                                                    SET tag='{tag}' 
                                                    WHERE uso='{uso_s}' AND 
                                                          basket={basket_s} AND 
                                                          module={module_s} AND 
                                                          channel={channel_s}''')
    
                        if not bool(exist_name):
                            select_name = self.cursor.execute(f'''SELECT id, name 
                                                                  FROM do
                                                                  WHERE uso='{uso_s}' AND 
                                                                        basket={basket_s} AND 
                                                                        module={module_s} AND 
                                                                        channel={channel_s}''')
                            for id_, name_ in select_name.fetchall():
                                msg[f'{today} - Таблица: DO, у сигнала обновлен name: id = {id_}, ({name_}) {description}'] = 2
                            self.cursor.execute(f'''UPDATE do
                                                    SET name='{description}' 
                                                    WHERE uso='{uso_s}' AND 
                                                          basket={basket_s} AND 
                                                          module={module_s} AND 
                                                          channel={channel_s}''')
                        continue

                    # Сквозной номер модуля
                    for through_module_number in HardWare.select().dicts():
                        tag_h    = through_module_number['tag']
                        uso_h    = through_module_number['uso']
                        basket_h = through_module_number['basket']

                        if uso_s == uso_h and basket_s == basket_h:
                            type_mod = through_module_number[f'variable_{module_s}']
                            isdigit_num  = re.findall('\d+', str(type_mod))

                            try   : isdigit_num = isdigit_num[0]
                            except: 
                                isdigit_num = ''
                                msg[f'{today} - В таблице HardWare не найден модуль сигнала: {id_s}, {tag}, {description}, {uso_s}_A{basket_s}_{module_s}_{channel_s}, "pValue" не заполнен'] = 2
                            break

                    if module_s < 10: prefix = f'0{module_s}' 
                    else            : prefix = f'{module_s}'

                    list_DO.append(dict(variable = f'DO[{count_DO}]',
                                        tag = tag,
                                        name = description,
                                        pValue = f'{tag_h}_{prefix}_DO[{channel_s}]',
                                        pHealth = f'mDO_HEALTH[{str(isdigit_num)}]',
                                        short_title = description,
                                        uso = uso_s, basket = basket_s, module = module_s, channel = channel_s,
                                        AlphaHMI = '', AlphaHMI_PIC1 = '', AlphaHMI_PIC1_Number_kont = '', AlphaHMI_PIC2 = '', 
                                        AlphaHMI_PIC2_Number_kont = '', AlphaHMI_PIC3 = '', AlphaHMI_PIC3_Number_kont = '', 
                                        AlphaHMI_PIC4 = '', AlphaHMI_PIC4_Number_kont = ''))

            # Checking for the existence of a database
            DO.insert_many(list_DO).execute()

        msg[f'{today} - Таблица: DO заполнена'] = 1
        return(msg)
    # Заполняем таблицу GMPNA
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'time_setting', 'setting', 'PIC', 'group_ust', 
                        'rule_map_ust', 'number_list_VU', 'number_protect_VU', 'number_pump_VU']
        msg = self.dop_function.column_check(GMPNA, 'gmpna', list_default)
        return msg 


# Changing tables SQL
class Editing_table_SQL():
    def __init__(self):
        self.cursor = db.cursor()
    def editing_sql(self,table_sql):
        #all_signal  = []
        #hat_tabl    = {}
        #unpacking   = []
        unpacking_  = []

        self.cursor.execute(f'SELECT * FROM {table_sql}')
        name_column = next(zip(*self.cursor.description))

        records = self.cursor.fetchall()
        unpacking_.append(records)

        count_column = len(name_column)
        count_row    = len(records)
        return count_column, count_row, name_column, records

        # with db:
        #     for row_sql in table_sql.select().dicts():
        #         all_signal.append(row_sql)
        #         hat_tabl = row_sql
        # for key in all_signal:
        #     for i, a in key.items():
        #         unpacking.append(str(a))
        # name_column  = hat_tabl.keys()
        # count_column = len(hat_tabl.keys())
        # count_row    = len(all_signal)
        # unpacking = list(self.func_chunks_generators(unpacking, count_column))
        #for i in unpacking: unpacking_.append(i)
        #db.close()
        #return count_column, count_row, name_column, unpacking_
    def func_chunks_generators(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    # Column names
    def column_names(self, table_used):
        self.cursor.execute(f'SELECT * FROM {table_used}')
        return next(zip(*self.cursor.description))
    # Apply request 
    def apply_request_select(self, request, table_used):
        msg = {}
        unpacking = []
        try:
            self.cursor.execute(f'''{request}''')
            name_column = next(zip(*self.cursor.description))

            records = self.cursor.fetchall()
            unpacking.append(records)

            count_column = len(name_column)
            count_row    = len(records)
            return count_column, count_row, name_column, records, msg
        except:
            msg[f'{today} - Таблица: {table_used} некорректный запрос!'] = 2
            return 'error', 'error', 'error', 'error', msg
    def other_requests(self, request, table_used):
        msg = {}
        try:
            self.cursor.execute(f'''{request}''')
            msg[f'{today} - Таблица: {table_used} запрос применен!'] = 1
            return msg
        except:
            msg[f'{today} - Таблица: {table_used} некорректный запрос!'] = 2
            return msg

    # Updating cell values
    def update_row_tabl(self, column, text_cell, text_cell_id, table_used, hat_name):
        active_column = list(hat_name)[column]
        self.cursor.execute(f'''UPDATE {table_used} 
                                SET {active_column}='{text_cell}' 
                                WHERE id == {text_cell_id}''')
        #table_used.update(**{active_column: text_cell}).where(table_used.id == text_cell_id).execute()
    # Adding new lines
    def add_new_row(self, table_used):
        self.cursor.execute(f'''INSERT INTO {table_used} DEFAULT VALUES''')

        #table_used.insert(**{active_column: ''}).execute()
    # Removing rows
    def delete_row(self, text_cell_id, table_used):
        self.cursor.execute(f'''DELETE FROM {table_used}
                                WHERE id={text_cell_id}''')
        #table_used.get(table_used.id == text_cell_id).delete_instance()
    # Adding new column
    def add_new_column(self, table_used, new_column):
        self.cursor.execute(f'''ALTER TABLE {table_used} 
                                ADD '{new_column}' VARCHAR(255)''')
    # Removing column
    def delete_column(self, column, hat_name, table_used):
        active_column = list(hat_name)[column]
        self.cursor.execute(f'''ALTER TABLE {table_used} 
                                DROP COLUMN {active_column}''')
    # Removing all rows
    def clear_tabl(self, table_used):
        self.cursor.execute(f'''DELETE FROM {table_used}''')
    # Drop table
    def drop_tabl(self, table_used):
        self.cursor.execute(f'''DROP TABLE {table_used}''')
    # Table selection window
    def get_tabl(self):
        return db.get_tables()


