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

        if self.empty_table(table_used): 
            msg[f'{today} - Таблица: {table_name} пустая!'] = 2
            return msg
        
        self.cursor.execute(f'DELETE FROM {table_used}')
        msg[f'{today} - Таблица: {table_name} полностью очищена'] = 1
        return msg
    def search_signal(self, tabl_used_cl, tabl_used_str, tag):
        exists_tag = tabl_used_cl.select().where(tabl_used_cl.Идентификатор == tag)
        if bool(exists_tag):
            search_tag = self.cursor.execute(f'''SELECT id, Идентификатор
                                                FROM {tabl_used_str}
                                                WHERE Идентификатор="{tag}"''')
            for id_, tag in search_tag.fetchall():
                if tabl_used_str == 'di': return (f'DI[{id_}].Value')
                if tabl_used_str == 'do': return (f'ctrlDO[{id_}]')
                if tabl_used_str == 'ai': return (f'AI[{id_}].Norm')
        else:
            return ''
    def update_signal(self, tabl_used_cl, tabl_used_str, tag, number_NA, column_update_cl, column_update_str):
        msg = {}
        exist_value  = tabl_used_cl.select().where(tabl_used_cl.id == number_NA,
                                                    column_update_cl == tag)
        if not bool(exist_value):
            self.cursor.execute(f'''UPDATE {tabl_used_str}
                                    SET {column_update_str}='{tag}' 
                                    WHERE id="{number_NA}"''')
            msg[f'{today} - Таблица: UMPNA, NA[{number_NA}] обновлено {column_update_str} = {tag}'] = 3
            return msg
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

                ai_temp = self.cursor.execute(f'''SELECT Переменная, Название
                                                  FROM ai
                                                  WHERE Название LIKE "%{uso[0]}%"''')
                current_ai = ai_temp.fetchall()
                try:
                    if len(current_ai) == 0: raise
                    for ai in current_ai:
                        list_diag['temperature']  = f'{ai[0]}'
                        break
                except:
                    list_diag['temperature']  = ''
                    msg[f'{today} - Таблица: USO. Температура в шкафу {uso[0]} не найдена!'] = 2

                door_temp = self.cursor.execute(f'''SELECT Переменная, Название
                                                    FROM di
                                                    WHERE Название LIKE "%{uso[0]}%" AND 
                                                          (Название LIKE "%двер%" OR
                                                          Название LIKE "%Двер%")''')
                current_door = door_temp.fetchall()
                try:
                    if len(current_door) == 0: raise
                    for door in current_door:
                        list_diag['door']  = f'{door[0]}.Value'
                        break
                except:
                    list_diag['temperature']  = ''
                    msg[f'{today} - Таблица: USO. Сигнал открытой двери шкафа {uso[0]} не найден!'] = 2

                di_temp = self.cursor.execute(f'''SELECT Переменная, Название
                                                  FROM di
                                                  WHERE Название LIKE "%{uso[0]}%" AND 
                                                        (Название NOT LIKE "%двер%") AND (Название NOT LIKE "%Двер%") 
                                                  ORDER BY Название''')
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

                    coincidence = AI.select().where(AI.Шкаф    == uso_s,
                                                    AI.Корзина == basket_s,
                                                    AI.Модуль  == module_s,
                                                    AI.Канал   == channel_s)
                    if bool(coincidence):
                        exist_tag  = AI.select().where(AI.Идентификатор == tag)
                        exist_name = AI.select().where(AI.Название == description)

                        if not bool(exist_tag):
                            select_tag = self.cursor.execute(f'''SELECT id, Идентификатор 
                                                                 FROM ai
                                                                 WHERE Шкаф='{uso_s}' AND 
                                                                       Корзина={basket_s} AND 
                                                                       Модуль={module_s} AND 
                                                                       Канал={channel_s}''')
                            for id_, tag_ in select_tag.fetchall():
                                msg[f'{today} - Таблица: AI, у сигнала обновлен идентификатор: id = {id_}, ({tag_}) {tag}'] = 2
                            self.cursor.execute(f'''UPDATE ai
                                                    SET Идентификатор='{tag}' 
                                                    WHERE Шкаф='{uso_s}' AND 
                                                          Корзина={basket_s} AND 
                                                          Модуль={module_s} AND 
                                                          Канал={channel_s}''')
    
                        if not bool(exist_name):
                            select_name = self.cursor.execute(f'''SELECT id, Название 
                                                                  FROM ai
                                                                  WHERE Шкаф='{uso_s}' AND 
                                                                        Корзина={basket_s} AND 
                                                                        Модуль={module_s} AND 
                                                                        Канал={channel_s}''')
                            for id_, name_ in select_name.fetchall():
                                msg[f'{today} - Таблица: AI, у сигнала обновлено название: id = {id_}, ({name_}) {description}'] = 2
                            self.cursor.execute(f'''UPDATE ai
                                                    SET Название='{description}' 
                                                    WHERE Шкаф='{uso_s}' AND 
                                                          Корзина={basket_s} AND 
                                                          Модуль={module_s} AND 
                                                          Канал={channel_s}''')
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
                    
                    list_AI.append(dict(Переменная = f'AI[{count_AI}]',
                                        Идентификатор = tag,
                                        Название = description,
                                        pValue = f'mAI8[{isdigit_num[0]}, {module_s}]',
                                        pHealth = f'mAI8_HEALTH[{isdigit_num[0]}]',
                                        Группа_аналогов = group_analog,
                                        Группа_уставок_аналогов = group_ust_analog,
                                        Единица_измерения = unit,
                                        Подпись_для_ВУ = sign,
                                        Флаг_для_пересчета_в_кгс_см2 = flag_MPa_kgccm2,
                                        Номер_НА_или_вспом = '',
                                        Вибрация_насоса = '',
                                        Вибрация_ЭД = '',
                                        Ток_ЭД_НА = '',
                                        Давление_на_выходе_вспом = '',
                                        Номер_уставки_мин_авар = '',
                                        Номер_уставки_мин_пред = '',
                                        Номер_уставки_макс_авар = '',
                                        Номер_уставки_макс_пред = '',
                                        Полевой_мин = '4000',
                                        Полевой_макс = '20000',
                                        Инженерный_мин = eng_min,
                                        Инженерный_макс = eng_max,
                                        Достоверность_мин = '3900',
                                        Достоверность_макс = '20100',
                                        Гистерезис = '0',
                                        Фильтрация = '0',
                                        Уставка_мин_6 = '', Уставка_мин_5 = '', Уставка_мин_4 = '', Уставка_мин_3 = '', Уставка_мин_2 = '', Уставка_мин = '',
                                        Уставка_макс = '', Уставка_макс_2 = '', Уставка_макс_3 = '', Уставка_макс_4 = '', Уставка_макс_5 = '', Уставка_макс_6 = '',
                                        Точность_значения = value_precision,
                                        Pic = '', Группа_сброса_трендов = '', Гистерезис_ТИ = '0,1', АЦП = 'мкА', 
                                        Правило_для_карты_уставок = rule, Предохранитель = '', Шкаф = uso_s, Корзина = basket_s, Модуль = module_s, Канал = channel_s,
                                        AlphaHMI = '', AlphaHMI_PIC1 = '', AlphaHMI_PIC1_Number_kont = '', AlphaHMI_PIC2 = '', 
                                        AlphaHMI_PIC2_Number_kont = '', AlphaHMI_PIC3 = '', AlphaHMI_PIC3_Number_kont = '', 
                                        AlphaHMI_PIC4 = '', AlphaHMI_PIC4_Number_kont = ''))

            # Checking for the existence of a database
            AI.insert_many(list_AI).execute()

        msg[f'{today} - Таблица: AI заполнена'] = 1
        return(msg)
    # Заполняем таблицу AI
    def column_check(self):
        list_default = ['Переменная', 'Идентификатор', 'Название', 'pValue', 'pHealth', 'Группа_аналогов',
                        'Группа_уставок_аналогов',  'Единица_измерения',  'Подпись_для_ВУ',  'Флаг_для_пересчета_в_кгс_см2',  'Номер_НА_или_вспом',  
                        'Вибрация_насоса',  'Вибрация_ЭД',  'Ток_ЭД_НА',  'Давление_на_выходе_вспом', 
                        'Номер_уставки_мин_авар',  'Номер_уставки_мин_пред',  'Номер_уставки_макс_авар',  'Номер_уставки_макс_пред', 
                        'Полевой_мин',  'Полевой_макс',  'Инженерный_мин', 'Инженерный_макс', 'Достоверность_мин', 'Достоверность_макс', 
                        'Гистерезис', 'Фильтрация', 'Уставка_мин_6', 'Уставка_мин_5', 'Уставка_мин_4', 'Уставка_мин_3', 
                        'Уставка_мин_2', 'Уставка_мин', 'Уставка_макс', 'Уставка_макс_2', 'Уставка_макс_3', 'Уставка_макс_4',
                        'Уставка_макс_5', 'Уставка_макс_6', 'Точность_значения', 'Pic', 'Группа_сброса_трендов', 'Гистерезис_ТИ', 
                        'АЦП', 'Правило_для_карты_уставок', 'Предохранитель', 'Шкаф', 'Корзина', 'Модуль', 'Канал', 'AlphaHMI', 'AlphaHMI_PIC1', 
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

                    coincidence = AO.select().where(AO.Шкаф     == uso_s,
                                                    AO.Корзина  == basket_s,
                                                    AO.Модуль  == module_s,
                                                    AO.Канал == channel_s)
                    if bool(coincidence):
                        exist_tag  = AO.select().where(AO.Идентификатор == tag)
                        exist_name = AO.select().where(AO.Название == description)

                        if not bool(exist_tag):
                            select_tag = self.cursor.execute(f'''SELECT id, Идентификатор 
                                                                 FROM ao
                                                                 WHERE Шкаф='{uso_s}' AND 
                                                                       Корзина={basket_s} AND 
                                                                       Модуль={module_s} AND 
                                                                       Канал={channel_s}''')
                            for id_, tag_ in select_tag.fetchall():
                                msg[f'{today} - Таблица: AO, у сигнала обновлен идентификатор: id = {id_}, ({tag_}) {tag}'] = 2
                            self.cursor.execute(f'''UPDATE ao
                                                    SET Идентификатор='{tag}' 
                                                    WHERE Шкаф='{uso_s}' AND 
                                                          Корзина={basket_s} AND 
                                                          Модуль={module_s} AND 
                                                          Канал={channel_s}''')
    
                        if not bool(exist_name):
                            select_name = self.cursor.execute(f'''SELECT id, Название 
                                                                  FROM ao
                                                                  WHERE Шкаф='{uso_s}' AND 
                                                                        Корзина={basket_s} AND 
                                                                        Модуль={module_s} AND 
                                                                        Канал={channel_s}''')
                            for id_, name_ in select_name.fetchall():
                                msg[f'{today} - Таблица: AO, у сигнала обновлено название: id = {id_}, ({name_}) {description}'] = 2
                            self.cursor.execute(f'''UPDATE ao
                                                    SET Название='{description}' 
                                                    WHERE Шкаф='{uso_s}' AND 
                                                          Корзина={basket_s} AND 
                                                          Модуль={module_s} AND 
                                                          Канал={channel_s}''')
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
                
                    list_AO.append(dict(Переменная = f'AO[{count_AO}]',
                                        Идентификатор = tag,
                                        Название = description,
                                        pValue = f'{tag_h}_{prefix}_AO[{channel_s}]',
                                        pHealth = f'mAO_HEALTH[{isdigit_num[0]}]',
                                        Шкаф = uso_s, 
                                        Корзина = basket_s, 
                                        Модуль = module_s, 
                                        Канал = channel_s,
                                        ))

            # Checking for the existence of a database
            AO.insert_many(list_AO).execute()

        msg[f'{today} - Таблица: AO заполнена'] = 1
        return(msg)
    # Заполняем таблицу AO
    def column_check(self):
        list_default = ['Переменная', 'Идентификатор', 'Название', 'pValue', 'pHealth',  'Шкаф', 'Корзина', 'Модуль', 'Канал']
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

                    coincidence = DI.select().where(DI.Шкаф    == uso_s,
                                                    DI.Корзина == basket_s,
                                                    DI.Модуль  == module_s,
                                                    DI.Канал   == channel_s)
                    if bool(coincidence):
                        exist_tag  = DI.select().where(DI.Идентификатор == tag)
                        exist_name = DI.select().where(DI.Название == description)

                        if not bool(exist_tag):
                            select_tag = self.cursor.execute(f'''SELECT id, Идентификатор 
                                                                 FROM di
                                                                 WHERE Шкаф='{uso_s}' AND 
                                                                       Корзина={basket_s} AND 
                                                                       Модуль={module_s} AND 
                                                                       Канал={channel_s}''')
                            for id_, tag_ in select_tag.fetchall():
                                msg[f'{today} - Таблица: DI, у сигнала обновлен идентификатор: id = {id_}, ({tag_}) {tag}'] = 2
                            self.cursor.execute(f'''UPDATE di
                                                    SET Идентификатор='{tag}' 
                                                    WHERE Шкаф='{uso_s}' AND 
                                                          Корзина={basket_s} AND 
                                                          Модуль={module_s} AND 
                                                          Канал={channel_s}''')
    
                        if not bool(exist_name):
                            select_name = self.cursor.execute(f'''SELECT id, Название 
                                                                  FROM di
                                                                  WHERE Шкаф='{uso_s}' AND 
                                                                        Корзина={basket_s} AND 
                                                                        Модуль={module_s} AND 
                                                                        Канал={channel_s}''')
                            for id_, name_ in select_name.fetchall():
                                msg[f'{today} - Таблица: DI, у сигнала обновлено название: id = {id_}, ({name_}) {description}'] = 2
                            self.cursor.execute(f'''UPDATE di
                                                    SET Название='{description}' 
                                                    WHERE Шкаф='{uso_s}' AND 
                                                          Корзина={basket_s} AND 
                                                          Модуль={module_s} AND 
                                                          Канал={channel_s}''')
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
                    
                    list_DI.append(dict(Переменная = f'DI[{count_DI}]',
                                        Идентификатор = tag,
                                        Название = description,
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
                                        Таблица_сообщений = 'TblDiscretes',
                                        Группа_дискретов = group_diskrets,
                                        Приоритет_сообщения_при_0 = '',
                                        Приоритет_сообщения_при_1 = '',
                                        Короткое_название = description,
                                        Шкаф = uso_s, Корзина = basket_s, Модуль = module_s, Канал = channel_s,
                                        AlphaHMI = '', AlphaHMI_PIC1 = '', AlphaHMI_PIC1_Number_kont = '', AlphaHMI_PIC2 = '', 
                                        AlphaHMI_PIC2_Number_kont = '', AlphaHMI_PIC3 = '', AlphaHMI_PIC3_Number_kont = '', 
                                        AlphaHMI_PIC4 = '', AlphaHMI_PIC4_Number_kont = ''))

            # Checking for the existence of a database
            DI.insert_many(list_DI).execute()

        msg[f'{today} - Таблица: DI заполнена'] = 1
        return(msg)
    # Заполняем таблицу DI
    def column_check(self):
        list_default = ['Переменная', 'Идентификатор', 'Название', 'pValue', 'pHealth', 'Inv',
                        'ErrValue', 'priority_0', 'priority_1', 'Msg', 'isDI_NC',  
                        'isAI_Warn', 'isAI_Avar', 'pNC_AI',  'TS_ID', 
                        'isModuleNC',  'Pic',  'Таблица_сообщений',  'Группа_дискретов', 
                        'Приоритет_сообщения_при_0',  'Приоритет_сообщения_при_1', 'Короткое_название', 'Шкаф', 'Корзина', 'Модуль', 'Канал', 
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

                    coincidence = DO.select().where(DO.Шкаф    == uso_s,
                                                    DO.Корзина == basket_s,
                                                    DO.Модуль  == module_s,
                                                    DO.Канал   == channel_s)
                    if bool(coincidence):
                        exist_tag  = DO.select().where(DO.Идентификатор == tag)
                        exist_name = DO.select().where(DO.Название == description)

                        if not bool(exist_tag):
                            select_tag = self.cursor.execute(f'''SELECT id, Идентификатор 
                                                                 FROM do
                                                                 WHERE Шкаф='{uso_s}' AND 
                                                                       Корзина={basket_s} AND 
                                                                       Модуль={module_s} AND 
                                                                       Канал={channel_s}''')
                            for id_, tag_ in select_tag.fetchall():
                                msg[f'{today} - Таблица: DO, у сигнала обновлен идентификатор: id = {id_}, ({tag_}) {tag}'] = 2
                            self.cursor.execute(f'''UPDATE do
                                                    SET Идентификатор='{tag}' 
                                                    WHERE Шкаф='{uso_s}' AND 
                                                          Корзина={basket_s} AND 
                                                          Модуль={module_s} AND 
                                                          Канал={channel_s}''')
    
                        if not bool(exist_name):
                            select_name = self.cursor.execute(f'''SELECT id, Название 
                                                                  FROM do
                                                                  WHERE Шкаф='{uso_s}' AND 
                                                                        Корзина={basket_s} AND 
                                                                        Модуль={module_s} AND 
                                                                        Канал={channel_s}''')
                            for id_, name_ in select_name.fetchall():
                                msg[f'{today} - Таблица: DO, у сигнала обновлено название: id = {id_}, ({name_}) {description}'] = 2
                            self.cursor.execute(f'''UPDATE do
                                                    SET Название='{description}' 
                                                    WHERE Шкаф='{uso_s}' AND 
                                                          Корзина={basket_s} AND 
                                                          Модуль={module_s} AND 
                                                          Канал={channel_s}''')
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

                    list_DO.append(dict(Переменная = f'DO[{count_DO}]',
                                        Идентификатор = tag,
                                        Название = description,
                                        pValue = f'{tag_h}_{prefix}_DO[{channel_s}]',
                                        pHealth = f'mDO_HEALTH[{str(isdigit_num)}]',
                                        Короткое_название = description,
                                        Шкаф = uso_s, Корзина = basket_s, Модуль = module_s, Канал = channel_s,
                                        AlphaHMI = '', AlphaHMI_PIC1 = '', AlphaHMI_PIC1_Number_kont = '', AlphaHMI_PIC2 = '', 
                                        AlphaHMI_PIC2_Number_kont = '', AlphaHMI_PIC3 = '', AlphaHMI_PIC3_Number_kont = '', 
                                        AlphaHMI_PIC4 = '', AlphaHMI_PIC4_Number_kont = ''))

            # Checking for the existence of a database
            DO.insert_many(list_DO).execute()

        msg[f'{today} - Таблица: DO заполнена'] = 1
        return(msg)
    # Заполняем таблицу DO
    def column_check(self):
        list_default = ['Переменная', 'Идентификатор', 'Название', 'pValue', 'pHealth', 'Короткое_название', 'Шкаф', 'Корзина', 'Модуль', 'Канал', 
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
        list_KTPRS = []
        with db:
            for i in range(1, 21):
                list_KTPRS.append(dict(variable = f'KTPRS[{i}]',
                                       tag  = '',
                                       name = 'Резерв',
                                       drawdown = '',
                                       reference_to_value = '',
                                       priority_msg_0 = '',
                                       priority_msg_1 = '',
                                       prohibition_issuing_msg = '',
                                       PIC = ''))

            # Checking for the existence of a database
            KTPRS.insert_many(list_KTPRS).execute()

        msg[f'{today} - Таблица: KTPRS заполнена'] = 1
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
        list_GMPNA = []
        with db:
            for i in range(1, 5):
                for k in range(1, 65):
                    list_GMPNA.append(dict(variable = f'GMPNA[{i}][{k}]',
                                            tag  = '',
                                            name = 'Резерв',
                                            name_for_Chrp_in_local_mode = '',
                                            NA = '',
                                            time_setting = '',
                                            setting = '',
                                            group_ust = f'Tm - Агрегатные готовности МНА{i}',
                                            rule_map_ust = 'Временные уставки',
                                            number_list_VU = '',
                                            number_protect_VU = '',
                                            number_pump_VU = f'{i}'))

            # Checking for the existence of a database
            GMPNA.insert_many(list_GMPNA).execute()

        msg[f'{today} - Таблица: GMPNA заполнена'] = 1
        return(msg)
    # Заполняем таблицу GMPNA
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'name_for_Chrp_in_local_mode', 'NA', 'time_setting', 'setting', 'group_ust', 
                        'rule_map_ust', 'number_list_VU', 'number_protect_VU', 'number_pump_VU']
        msg = self.dop_function.column_check(GMPNA, 'gmpna', list_default)
        return msg 

# Work with filling in the table 'UMPNA'
class Filling_UMPNA():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = general_functions()
    # Получаем данные с таблицы AI и DI 
    def getting_modul(self, count_NA):
        msg = {}
        with db:
            try:
                if self.dop_function.empty_table('di') or self.dop_function.empty_table('ai'): 
                    msg[f'{today} - Таблицы: AI или DI пустые! Заполни таблицы!'] = 2
                    return msg
            except:
                msg[f'{today} - Таблицы: AI или DI отсутсвует!'] = 2
                return msg

            row_count_req = self.cursor.execute(f'''SELECT Count (*) FROM umpna''')
            row_count = row_count_req.fetchall()[0][0]

            for i in range(1, count_NA + 1):

                if row_count < i:
                    list_UMPNA = []
                    msg[f'{today} - Таблица: UMPNA, отсутствует NA[{i}] идет заполнение'] = 3

                    vv_included = self.dop_function.search_signal(DI, 'di', f'MBC{i}01-1')
                    vv_double_included = self.dop_function.search_signal(DI, 'di', f'MBC{i}01-2')
                    vv_disabled = self.dop_function.search_signal(DI, 'di', f'MBC{i}02-1')
                    vv_double_disabled = self.dop_function.search_signal(DI, 'di', f'MBC{i}02-2')
                    current_greater_than_noload_setting = self.dop_function.search_signal(AI, 'ai', f'CT{i}01')
                    serviceability_of_circuits_of_inclusion_of_VV = self.dop_function.search_signal(DI, 'di', f'ECB{i}01')
                    serviceability_of_circuits_of_shutdown_of_VV = self.dop_function.search_signal(DI, 'di', f'ECO{i}01-1')
                    serviceability_of_circuits_of_shutdown_of_VV_double = self.dop_function.search_signal(DI, 'di', f'ECO{i}01-2')
                    stop_1 = self.dop_function.search_signal(DI, 'di', f'KKC{i}01')
                    stop_2 = self.dop_function.search_signal(DI, 'di', f'KKC{i}02')
                    monitoring_the_presence_of_voltage_in_the_control_current_circuits = self.dop_function.search_signal(DI, 'di', f'EC{i}08')
                    vv_trolley_rolled_out = self.dop_function.search_signal(DI, 'di', f'EC{i}04')
                    command_to_turn_on_the_vv_only_for_UMPNA = self.dop_function.search_signal(DO, 'do', f'ABB{i}01')
                    command_to_turn_off_the_vv_output_1 = self.dop_function.search_signal(DO, 'do', f'ABO{i}01-1')
                    command_to_turn_off_the_vv_output_2 = self.dop_function.search_signal(DO, 'do', f'ABO{i}01-2')

                    list_UMPNA.append(dict(variable = f'NA[{i}]',
                        name ='',
                        vv_included = vv_included,
                        vv_double_included = vv_double_included,
                        vv_disabled = vv_disabled,
                        vv_double_disabled = vv_double_disabled,
                        current_greater_than_noload_setting = current_greater_than_noload_setting,
                        serviceability_of_circuits_of_inclusion_of_VV = serviceability_of_circuits_of_inclusion_of_VV,
                        serviceability_of_circuits_of_shutdown_of_VV = serviceability_of_circuits_of_shutdown_of_VV,
                        serviceability_of_circuits_of_shutdown_of_VV_double = serviceability_of_circuits_of_shutdown_of_VV_double,
                        stop_1 = f'NOT {stop_1}',
                        stop_2 = f'NOT {stop_2}',
                        stop_3 ='',
                        stop_4 ='',
                        monitoring_the_presence_of_voltage_in_the_control_current_circuits = monitoring_the_presence_of_voltage_in_the_control_current_circuits,
                        voltage_presence_flag_in_the_ZRU_motor_cell ='',
                        vv_trolley_rolled_out = vv_trolley_rolled_out,
                        remote_control_mode_of_the_RZiA_controller ='',
                        availability_of_communication_with_the_RZiA_controller ='',
                        the_state_of_the_causative_agent_of_ED ='',
                        engine_prepurge_end_flag ='',
                        flag_for_the_presence_of_safe_air_boost_pressure_in_the_engine_housing ='',
                        flag_for_the_presence_of_safe_air_boost_pressure_in_the_exciter_housing ='',
                        engine_purge_valve_closed_flag ='',
                        oil_system_oil_temperature_flag_is_above_10_at_the_cooler_outlet_for_an_individual_oil_system ='',
                        flag_for_the_minimum_oil_level_in_the_oil_tank_for_an_individual_oil_system ='',
                        flag_for_the_presence_of_the_minimum_level_of_the_barrier_liquid_in_the_tank_of_the_locking_system ='',
                        generalized_flag_for_the_presence_of_barrier_fluid_pressure_to_the_mechanical_seal ='',
                        command_to_turn_on_the_vv_only_for_UMPNA = command_to_turn_on_the_vv_only_for_UMPNA,
                        command_to_turn_off_the_vv_output_1 = command_to_turn_off_the_vv_output_1,
                        command_to_turn_off_the_vv_output_2 = command_to_turn_off_the_vv_output_2,
                        NA_Chrp ='',
                        type_NA_MNA ='',
                        pump_type_NM ='',
                        parametr_KTPRAS_1 ='',
                        number_of_delay_scans_of_the_analysis_of_the_health_of_the_control_circuits_NA_MNA ='',
                        unit_number_of_the_auxiliary_system_start_up_oil_pump_for_an_individual_oil_system ='',
                        NPS_number_1_or_2_which_the_AT_belongs ='',
                        achr_protection_number_in_the_array_of_station_protections ='',
                        saon_protection_number_in_the_array_of_station_protections ='',
                        gmpna_49 ='',
                        gmpna_50 ='',
                        gmpna_51 ='',
                        gmpna_52 ='',
                        gmpna_53 ='',
                        gmpna_54 ='',
                        gmpna_55 ='',
                        gmpna_56 ='',
                        gmpna_57 ='',
                        gmpna_58 ='',
                        gmpna_59 ='',
                        gmpna_60 ='',
                        gmpna_61 ='',
                        gmpna_62 ='',
                        gmpna_63 ='',
                        gmpna_64 ='',
                        PIC ='',
                        replacement_uso_signal_vv_1 ='',
                        replacement_uso_signal_vv_2 =''))
                        
                    # Checking for the existence of a database
                    UMPNA.insert_many(list_UMPNA).execute()
                    msg[f'{today} - Таблица: UMPNA, NA[{i}] заполнен'] = 1

                else:

                    msg[f'{today} - Таблица: UMPNA, NA[{i}] идет обновление'] = 3

                    msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                        self.dop_function.search_signal(DI, "di", f"MBC{i}01-1"), i, UMPNA.vv_included, 'vv_included'))
                    msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                        self.dop_function.search_signal(DI, "di", f"MBC{i}01-2"), i, UMPNA.vv_double_included, 'vv_double_included'))
                    msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                        self.dop_function.search_signal(DI, "di", f"MBC{i}02-1"), i, UMPNA.vv_disabled, 'vv_disabled'))
                    msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                        self.dop_function.search_signal(DI, "di", f"MBC{i}02-2"), i, UMPNA.vv_double_disabled, 'vv_double_disabled'))
                    msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                        self.dop_function.search_signal(AI, "ai", f"CT{i}01"), i, UMPNA.current_greater_than_noload_setting, 'current_greater_than_noload_setting'))
                    msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                        self.dop_function.search_signal(DI, "di", f"ECB{i}01"), i, UMPNA.serviceability_of_circuits_of_inclusion_of_VV, 'serviceability_of_circuits_of_inclusion_of_VV'))
                    msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                        self.dop_function.search_signal(DI, "di", f"ECO{i}01-1"), i, UMPNA.serviceability_of_circuits_of_shutdown_of_VV, 'serviceability_of_circuits_of_shutdown_of_VV'))
                    msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                        self.dop_function.search_signal(DI, "di", f"ECO{i}01-2"), i, UMPNA.serviceability_of_circuits_of_shutdown_of_VV_double, 'serviceability_of_circuits_of_shutdown_of_VV_double'))
                    msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                        f'NOT {self.dop_function.search_signal(DI, "di", f"KKC{i}01")}', i, UMPNA.stop_1, 'stop_1'))
                    msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                        f'NOT {self.dop_function.search_signal(DI, "di", f"KKC{i}02")}', i, UMPNA.stop_2, 'stop_2'))
                    msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                        self.dop_function.search_signal(DI, "di", f"EC{i}08"), i, UMPNA.monitoring_the_presence_of_voltage_in_the_control_current_circuits, 'monitoring_the_presence_of_voltage_in_the_control_current_circuits'))
                    msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                        self.dop_function.search_signal(DI, "di", f"EC{i}04"), i, UMPNA.vv_trolley_rolled_out, 'vv_trolley_rolled_out'))
                    msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                        self.dop_function.search_signal(DO, "do", f"ABB{i}01"), i, UMPNA.command_to_turn_on_the_vv_only_for_UMPNA, 'command_to_turn_on_the_vv_only_for_UMPNA'))
                    msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                        self.dop_function.search_signal(DO, "do", f"ABO{i}01-1"), i, UMPNA.command_to_turn_off_the_vv_output_1, 'command_to_turn_off_the_vv_output_1'))
                    msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                        self.dop_function.search_signal(DO, "do", f"ABO{i}01-2"), i, UMPNA.command_to_turn_off_the_vv_output_2, 'command_to_turn_off_the_vv_output_2'))
                    
                    msg[f'{today} - Таблица: UMPNA, сигналы NA[{i}] обновлены'] = 1
            
            exists_name = self.cursor.execute(f'''SELECT name FROM umpna''')
            for i in exists_name.fetchall():
                if i[0] is None or i[0] == '' or i[0] == ' ':
                    msg[f'{today} - Таблица: UMPNA, необходимо заполнить название НА!'] = 3
        return(msg)
    # Заполняем таблицу UMPNA
    def column_check(self):
        list_default = ['variable', 'name', 'vv_included', 'vv_double_included', 'vv_disabled', 
                        'vv_double_disabled', 'current_greater_than_noload_setting', 'serviceability_of_circuits_of_inclusion_of_VV',
                        'serviceability_of_circuits_of_shutdown_of_VV', 'serviceability_of_circuits_of_shutdown_of_VV_double',
                        'stop_1', 'stop_2', 'stop_3', 'stop_4',
                        'monitoring_the_presence_of_voltage_in_the_control_current_circuits', 'voltage_presence_flag_in_the_ZRU_motor_cell',
                        'vv_trolley_rolled_out', 'remote_control_mode_of_the_RZiA_controller', 
                        'availability_of_communication_with_the_RZiA_controller','the_state_of_the_causative_agent_of_ED',
                        'engine_prepurge_end_flag', 'flag_for_the_presence_of_safe_air_boost_pressure_in_the_engine_housing',
                        'flag_for_the_presence_of_safe_air_boost_pressure_in_the_exciter_housing', 'engine_purge_valve_closed_flag',
                        'oil_system_oil_temperature_flag_is_above_10_at_the_cooler_outlet_for_an_individual_oil_system', 
                        'flag_for_the_minimum_oil_level_in_the_oil_tank_for_an_individual_oil_system', 
                        'flag_for_the_presence_of_the_minimum_level_of_the_barrier_liquid_in_the_tank_of_the_locking_system',
                        'generalized_flag_for_the_presence_of_barrier_fluid_pressure_to_the_mechanical_seal', 'command_to_turn_on_the_vv_only_for_UMPNA',
                        'command_to_turn_off_the_vv_output_1', 'command_to_turn_off_the_vv_output_2', 'NA_Chrp', 'type_NA_MNA',
                        'pump_type_NM','parametr_KTPRAS_1', 'number_of_delay_scans_of_the_analysis_of_the_health_of_the_control_circuits_NA_MNA',
                        'unit_number_of_the_auxiliary_system_start_up_oil_pump_for_an_individual_oil_system', 'NPS_number_1_or_2_which_the_AT_belongs',
                        'achr_protection_number_in_the_array_of_station_protections','saon_protection_number_in_the_array_of_station_protections', 
                        'gmpna_49', 'gmpna_50', 'gmpna_51', 'gmpna_52','gmpna_53', 'gmpna_54', 'gmpna_55', 'gmpna_56',
                        'gmpna_57','gmpna_58', 'gmpna_59', 'gmpna_60', 'gmpna_61', 'gmpna_62','gmpna_63', 'gmpna_64', 'PIC', 
                        'replacement_uso_signal_vv_1', 'replacement_uso_signal_vv_2']
        msg = self.dop_function.column_check(UMPNA, 'umpna', list_default)
        return msg 
# Work with filling in the table 'tmNA_UMPNA'
class Filling_tmNA_UMPNA():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = general_functions()
    # Получаем данные с таблицы Signals 
    def getting_modul(self):
        msg = {}
        count_NA = 0
        list_tmna_umpna = []
        time_ust = [('Время на проверку корректности состояния цепей контроля ВВ  (с отключенным контролем по току)' , 'T1noCT', '3'), 
                    ('Время на проверку корректности состояния цепей контроля ВВ (с включенным контролем по току)', 'T1CT', '6'),
                    ('Время удержания команды "Включить ВВ", после получения включенного состояния ВВ', 'T2', '1'),
                    ('Максимальное время удержания команды "Отключить ВВ"', 'T3', '1'),
                    ('Время до выдачи команды Включить ВВ, необходимое для отработки САР во время рамповой функции', 'T4', '3'),
                    ('Время на открытие выкидной задвижки перед выдачей команды на включение НА по программе П2', 'T5', '5'),
                    ('Контрольное время выполнения процесса отключения ВВ НА', 'T6', '4'),
                    ('Время на подъем силы тока ЭД после включения ВВ НА', 'T7', '3'),
                    ('Время полного хода выкидной задвижки (используется в алгоритмах программы пуска П2)', 'T8', '600'),
                    ('Время пускового режима работы ЭД при пуске', 'T9', '30'),
                    ('Время перед выдачей команды повторого отключения ВВ при невыполнении программы остановки', 'T10', '3'),
                    ('Контрольное время выполнения процесса включения ВВ НА', 'T11', '4'),
                    ('Время снижения силы тока ЭД после отключения ВВ НА', 'T12', '3'),
                    ('Время фильтрации сигналов цепей включения/отключения', 'T13', '3'),
                    ('Время пускового режима работы насоса при пуске', 'T14', '300'),
                    ('Длительность выдачи команды в САР для рамповой функции', 'T15', '5'),
                    ('Время на выполнение АВР при получении сигнала "Электрозащита" после получения состояния ВВ отключен', 'T16', '3'),
                    ('Время, через которое будет выдана команда "Стоп" при отсутствии электрозащиты', 'T17', '3'),
                    ('Резерв', 'T18', '0'), 
                    ('Размер колеса насосного агрегата', 'WheelSize', '1')] 
        with db:
            if self.dop_function.empty_table('umpna'): 
                msg[f'{today} - Таблицы: UMPNA пустая! Заполни таблицу!'] = 2
                return msg
            exists_name = self.cursor.execute(f'''SELECT name FROM umpna''')
            for i in exists_name.fetchall():
                count_NA += 1
                if i[0] is None or i[0] == '' or i[0] == ' ':
                    msg[f'{today} - Таблица: UMPNA, необходимо заполнить название НА!'] = 3
                else:
                    for ust in time_ust:
                        list_tmna_umpna.append(dict(variable = '',
                                                tag  = f'HNA{count_NA}_{ust[1]}',
                                                name = f'{i[0]}. {ust[0]}',
                                                unit = 'с',
                                                used = '1',
                                                value_ust = f'{ust[2]}',
                                                minimum = '0',
                                                maximum = '65535',
                                                group_ust = 'Временные уставки МНА',
                                                rule_map_ust = 'Временные уставки'))
                        
            # Checking for the existence of a database
            tmNA_UMPNA.insert_many(list_tmna_umpna).execute()
        msg[f'{today} - Таблица: tmNA_UMPNA заполнена'] = 1
        return(msg)
    # Заполняем таблицу tmNA_UMPNA
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 
                        'unit', 'used', 'value_ust', 'minimum', 'maximum', 'group_ust', 'rule_map_ust']
        msg = self.dop_function.column_check(tmNA_UMPNA, 'tmna_umpna', list_default)
        return msg 
    
# Work with filling in the table 'ZD'
class Filling_ZD():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = general_functions()
    # Получаем данные с таблицы AI и DI 
    def getting_modul(self):
        msg = {}
        array_tag_zd = ('OKC', 'CKC', 'ODC', 'CDC', 'MC', 'OPC', 'DC', 'DCK', 'MCO', 'MCC', 'KKC', 'KKS')
        with db:
            try:
                if self.dop_function.empty_table('di'): 
                    msg[f'{today} - Таблица: DI пустая! Заполни таблицу!'] = 2
                    return msg
            except:
                msg[f'{today} - Таблицы: DI отсутсвует! Заполни таблицу!'] = 2
                return msg
            
            count_zd = self.cursor.execute(f'''SELECT Название 
                                               FROM di
                                               WHERE Название LIKE "%задвижк%" OR Название LIKE "%Задвижк%"''')
            list_zd = count_zd.fetchall()
            list_zd_name_split = []
            for i in list_zd: 
                list_zd_name_split.append(str(i[0]).split(' - ')[0])

            unique_name = set(list_zd_name_split)

            for name in unique_name:
                for tag in array_tag_zd:
                    count_zd = self.cursor.execute(f'''SELECT Идентификатор, Название 
                                                       FROM di
                                                       WHERE Название LIKE "%{name}%" AND Идентификатор LIKE "%{tag}%"''')


            #     if row_count < i:
            #         list_UMPNA = []
            #         msg[f'{today} - Таблица: UMPNA, отсутствует NA[{i}] идет заполнение'] = 3

            #         vv_included = self.dop_function.search_signal(DI, 'di', f'MBC{i}01-1')
            #         vv_double_included = self.dop_function.search_signal(DI, 'di', f'MBC{i}01-2')
            #         vv_disabled = self.dop_function.search_signal(DI, 'di', f'MBC{i}02-1')
            #         vv_double_disabled = self.dop_function.search_signal(DI, 'di', f'MBC{i}02-2')
            #         current_greater_than_noload_setting = self.dop_function.search_signal(AI, 'ai', f'CT{i}01')
            #         serviceability_of_circuits_of_inclusion_of_VV = self.dop_function.search_signal(DI, 'di', f'ECB{i}01')
            #         serviceability_of_circuits_of_shutdown_of_VV = self.dop_function.search_signal(DI, 'di', f'ECO{i}01-1')
            #         serviceability_of_circuits_of_shutdown_of_VV_double = self.dop_function.search_signal(DI, 'di', f'ECO{i}01-2')
            #         stop_1 = self.dop_function.search_signal(DI, 'di', f'KKC{i}01')
            #         stop_2 = self.dop_function.search_signal(DI, 'di', f'KKC{i}02')
            #         monitoring_the_presence_of_voltage_in_the_control_current_circuits = self.dop_function.search_signal(DI, 'di', f'EC{i}08')
            #         vv_trolley_rolled_out = self.dop_function.search_signal(DI, 'di', f'EC{i}04')
            #         command_to_turn_on_the_vv_only_for_UMPNA = self.dop_function.search_signal(DO, 'do', f'ABB{i}01')
            #         command_to_turn_off_the_vv_output_1 = self.dop_function.search_signal(DO, 'do', f'ABO{i}01-1')
            #         command_to_turn_off_the_vv_output_2 = self.dop_function.search_signal(DO, 'do', f'ABO{i}01-2')

            #         list_UMPNA.append(dict(variable = f'NA[{i}]',
            #             name ='',
            #             vv_included = vv_included,
            #             vv_double_included = vv_double_included,
            #             vv_disabled = vv_disabled,
            #             vv_double_disabled = vv_double_disabled,
            #             current_greater_than_noload_setting = current_greater_than_noload_setting,
            #             serviceability_of_circuits_of_inclusion_of_VV = serviceability_of_circuits_of_inclusion_of_VV,
            #             serviceability_of_circuits_of_shutdown_of_VV = serviceability_of_circuits_of_shutdown_of_VV,
            #             serviceability_of_circuits_of_shutdown_of_VV_double = serviceability_of_circuits_of_shutdown_of_VV_double,
            #             stop_1 = f'NOT {stop_1}',
            #             stop_2 = f'NOT {stop_2}',
            #             stop_3 ='',
            #             stop_4 ='',
            #             monitoring_the_presence_of_voltage_in_the_control_current_circuits = monitoring_the_presence_of_voltage_in_the_control_current_circuits,
            #             voltage_presence_flag_in_the_ZRU_motor_cell ='',
            #             vv_trolley_rolled_out = vv_trolley_rolled_out,
            #             remote_control_mode_of_the_RZiA_controller ='',
            #             availability_of_communication_with_the_RZiA_controller ='',
            #             the_state_of_the_causative_agent_of_ED ='',
            #             engine_prepurge_end_flag ='',
            #             flag_for_the_presence_of_safe_air_boost_pressure_in_the_engine_housing ='',
            #             flag_for_the_presence_of_safe_air_boost_pressure_in_the_exciter_housing ='',
            #             engine_purge_valve_closed_flag ='',
            #             oil_system_oil_temperature_flag_is_above_10_at_the_cooler_outlet_for_an_individual_oil_system ='',
            #             flag_for_the_minimum_oil_level_in_the_oil_tank_for_an_individual_oil_system ='',
            #             flag_for_the_presence_of_the_minimum_level_of_the_barrier_liquid_in_the_tank_of_the_locking_system ='',
            #             generalized_flag_for_the_presence_of_barrier_fluid_pressure_to_the_mechanical_seal ='',
            #             command_to_turn_on_the_vv_only_for_UMPNA = command_to_turn_on_the_vv_only_for_UMPNA,
            #             command_to_turn_off_the_vv_output_1 = command_to_turn_off_the_vv_output_1,
            #             command_to_turn_off_the_vv_output_2 = command_to_turn_off_the_vv_output_2,
            #             NA_Chrp ='',
            #             type_NA_MNA ='',
            #             pump_type_NM ='',
            #             parametr_KTPRAS_1 ='',
            #             number_of_delay_scans_of_the_analysis_of_the_health_of_the_control_circuits_NA_MNA ='',
            #             unit_number_of_the_auxiliary_system_start_up_oil_pump_for_an_individual_oil_system ='',
            #             NPS_number_1_or_2_which_the_AT_belongs ='',
            #             achr_protection_number_in_the_array_of_station_protections ='',
            #             saon_protection_number_in_the_array_of_station_protections ='',
            #             gmpna_49 ='',
            #             gmpna_50 ='',
            #             gmpna_51 ='',
            #             gmpna_52 ='',
            #             gmpna_53 ='',
            #             gmpna_54 ='',
            #             gmpna_55 ='',
            #             gmpna_56 ='',
            #             gmpna_57 ='',
            #             gmpna_58 ='',
            #             gmpna_59 ='',
            #             gmpna_60 ='',
            #             gmpna_61 ='',
            #             gmpna_62 ='',
            #             gmpna_63 ='',
            #             gmpna_64 ='',
            #             PIC ='',
            #             replacement_uso_signal_vv_1 ='',
            #             replacement_uso_signal_vv_2 =''))
                        
            #         # Checking for the existence of a database
            #         UMPNA.insert_many(list_UMPNA).execute()
            #         msg[f'{today} - Таблица: UMPNA, NA[{i}] заполнен'] = 1

            #     else:

            #         msg[f'{today} - Таблица: UMPNA, NA[{i}] идет обновление'] = 3

            #         msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
            #             self.dop_function.search_signal(DI, "di", f"MBC{i}01-1"), i, UMPNA.vv_included, 'vv_included'))
            #         msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
            #             self.dop_function.search_signal(DI, "di", f"MBC{i}01-2"), i, UMPNA.vv_double_included, 'vv_double_included'))
            #         msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
            #             self.dop_function.search_signal(DI, "di", f"MBC{i}02-1"), i, UMPNA.vv_disabled, 'vv_disabled'))
            #         msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
            #             self.dop_function.search_signal(DI, "di", f"MBC{i}02-2"), i, UMPNA.vv_double_disabled, 'vv_double_disabled'))
            #         msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
            #             self.dop_function.search_signal(AI, "ai", f"CT{i}01"), i, UMPNA.current_greater_than_noload_setting, 'current_greater_than_noload_setting'))
            #         msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
            #             self.dop_function.search_signal(DI, "di", f"ECB{i}01"), i, UMPNA.serviceability_of_circuits_of_inclusion_of_VV, 'serviceability_of_circuits_of_inclusion_of_VV'))
            #         msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
            #             self.dop_function.search_signal(DI, "di", f"ECO{i}01-1"), i, UMPNA.serviceability_of_circuits_of_shutdown_of_VV, 'serviceability_of_circuits_of_shutdown_of_VV'))
            #         msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
            #             self.dop_function.search_signal(DI, "di", f"ECO{i}01-2"), i, UMPNA.serviceability_of_circuits_of_shutdown_of_VV_double, 'serviceability_of_circuits_of_shutdown_of_VV_double'))
            #         msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
            #             f'NOT {self.dop_function.search_signal(DI, "di", f"KKC{i}01")}', i, UMPNA.stop_1, 'stop_1'))
            #         msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
            #             f'NOT {self.dop_function.search_signal(DI, "di", f"KKC{i}02")}', i, UMPNA.stop_2, 'stop_2'))
            #         msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
            #             self.dop_function.search_signal(DI, "di", f"EC{i}08"), i, UMPNA.monitoring_the_presence_of_voltage_in_the_control_current_circuits, 'monitoring_the_presence_of_voltage_in_the_control_current_circuits'))
            #         msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
            #             self.dop_function.search_signal(DI, "di", f"EC{i}04"), i, UMPNA.vv_trolley_rolled_out, 'vv_trolley_rolled_out'))
            #         msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
            #             self.dop_function.search_signal(DO, "do", f"ABB{i}01"), i, UMPNA.command_to_turn_on_the_vv_only_for_UMPNA, 'command_to_turn_on_the_vv_only_for_UMPNA'))
            #         msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
            #             self.dop_function.search_signal(DO, "do", f"ABO{i}01-1"), i, UMPNA.command_to_turn_off_the_vv_output_1, 'command_to_turn_off_the_vv_output_1'))
            #         msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
            #             self.dop_function.search_signal(DO, "do", f"ABO{i}01-2"), i, UMPNA.command_to_turn_off_the_vv_output_2, 'command_to_turn_off_the_vv_output_2'))
                    
            #         msg[f'{today} - Таблица: UMPNA, сигналы NA[{i}] обновлены'] = 1
            
            # exists_name = self.cursor.execute(f'''SELECT name FROM umpna''')
            # for i in exists_name.fetchall():
            #     if i[0] is None or i[0] == '' or i[0] == ' ':
            #         msg[f'{today} - Таблица: UMPNA, необходимо заполнить название НА!'] = 3
        return(msg)
    # Заполняем таблицу ZD
    def column_check(self):
        list_default = ['Переменная', 'Идентификатор', 'Название', 'Короткое_название', 'Наличие_ИНТЕРФЕЙСА', 'КВО', 'КВЗ', 'МПО', 'МПЗ', 'Дист_ф',
                        'Муфта', 'Авария_привода', 'Открыть', 'Закрыть', 'Остановить', 'Откртие_остановить', 'Закрытие_остановить', 'КВО_и', 'КВЗ_и',
                        'МПО_и', 'МПЗ_и', 'Дист_и', 'Муфта_и', 'Авария_привода_и', 'Открыть_и', 'Закрыть_и', 'Остановить_и', 'Открытие_остановить_и',
                        'Закрытие_остановить_и', 'Отсутствие_связи', 'Закрыть_с_БРУ', 'Стоп_с_БРУ', 'Напряжение', 'Напряжение_ЩСУ', 
                        'Напряжение_в_цепях_сигнализации', 'Исправность_цепей_открытия', 'Исправность_цепей_закрытия', 'ВММО', 'ВММЗ', 
                        'Замораживать_при_подозрительном_изм', 'Это_клапан', 'Процент_открытия', 'Pic', 'Тип_БУР_задвижки', 
                        'AlphaHMI', 'AlphaHMI_PIC1', 'AlphaHMI_PIC1_Number_kont', 'AlphaHMI_PIC2',
                        'AlphaHMI_PIC2_Number_kont','AlphaHMI_PIC3', 'AlphaHMI_PIC3_Number_kont', 
                        'AlphaHMI_PIC4', 'AlphaHMI_PIC4_Number_kont']
        msg = self.dop_function.column_check(ZD, 'zd', list_default)
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


