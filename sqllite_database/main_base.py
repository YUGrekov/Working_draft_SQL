from models import *
import openpyxl as wb
from datetime import datetime
import re
today = datetime.now()



class general_functions():
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
        today = datetime.now()
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
# Work with filling in the table 'signals'
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
                        test_s.append(dict(uso = uso[0],
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
                            test_s.append(dict(uso         = uso_kk,
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
                            msg[f'{today} - Таблица: hardware. {uso[0]}.A{basket[0]}.{i[0]} тип не определен!'] = 2
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
        list_default = ['uso', 'basket', 'powerLink_ID', 
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
    # Clear tabl
    def clear_tabl(self):
        msg = {}
        self.cursor.execute(f'''DELETE FROM hardware''')
        msg[f'{today} - Таблица: hardware полностью очищена'] = 1
        return(msg)

# Work with filling in the table 'AI'
class Filling_AI():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_func = general_functions()
    # Получаем данные с таблицы Signals 
    def getting_modul(self):
        msg = {}
        list_AI = []
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
            for row_sql in Signals.select().dicts():
                uso_s       = row_sql['uso']    
                tag         = row_sql['tag']
                description = str(row_sql['description']).replace('"', '').replace("'", '')
                type_signal = row_sql['type_signal']
                scheme      = row_sql['schema']
                basket_s    = row_sql['basket']
                module_s    = row_sql['module']
                channel_s   = row_sql['channel']

                if self.dop_func.str_find(type_signal, {'AI'}) or self.dop_func.str_find(scheme, {'AI'}):

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
                            self.cursor.execute(f'''UPDATE ai
                                                    SET tag='{tag}' 
                                                    WHERE uso='{uso_s}' AND 
                                                          basket={basket_s} AND 
                                                          module={module_s} AND 
                                                          channel={channel_s}''')
    
                            print(select_tag.fetchall())
                            msg[f'{today} - Таблица: AI, у сигнала обновлен тэг: id = {select_tag.fetchall()[0][0]}, ({select_tag.fetchall()[1][0]}) {tag}'] = 1
                        if not bool(exist_name):
                            self.cursor.execute(f'''UPDATE ai
                                                    SET name='{description}' 
                                                    WHERE uso='{uso_s}' AND 
                                                          basket={basket_s} AND 
                                                          module={module_s} AND 
                                                          channel={channel_s}''')
                            print(f'обновлен {description}')
                        continue

                    # Сквозной номер модуля
                    for through_module_number in HardWare.select().dicts():
                        uso_h    = through_module_number['uso']
                        basket_h = through_module_number['basket']

                        if uso_s == uso_h and basket_s == basket_h:
                            type_mod = through_module_number[f'variable_{module_s}']
                            isdigit_num  = re.findall('\d+', str(type_mod))
                            break
                    
                    for key, short in dop_analog.items():
                        if self.dop_func.str_find(str(description).lower(), {key}):
                            sign = short[0]
                            unit = short[1]
                            rule = short[2]
                            group_analog = short[3]
                            group_ust_analog = short[4]
                            eng_min = short[5][0]
                            eng_max = short[5][1]
                            value_precision = short[6]
                            break

                    flag_MPa_kgccm2 = '1' if self.dop_func.str_find(str(description).lower(), {'давлен'}) else '0'
                    
                    list_AI.append(dict(tag = tag,
                                        name = description,
                                        channel_value = f'mAI8[{isdigit_num[0]}, {module_s}]',
                                        service_channel = f'mAI8_HEALTH[{isdigit_num[0]}]',
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
        list_default = ['tag', 'name', 'channel_value', 'service_channel', 'group_analog',
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
        msg = self.dop_func.column_check(AI, 'ai', list_default)
        return msg
        
    # Clear tabl
    def clear_tabl(self):
        msg = {}
        #self.cursor.execute(f'''DELETE FROM ai''')
        msg[f'{today} - Таблица: AI полностью очищена'] = 1
        return(msg)

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
    # Table selection window
    def get_tabl(self):
        return db.get_tables()


