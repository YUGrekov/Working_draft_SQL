from models import *
import openpyxl as wb
from lxml import etree
from datetime import datetime
import re, traceback, os, codecs
import psycopg2
today = datetime.now()



# Additional general features
class General_functions():
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
                    "Ё":"E",
                    "Ж":"J",
                    "З":"Z",
                    "И":"I",
                    "Й":"I",
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
                    "ё":"e",
                    "ж":"j",
                    "з":"z",
                    "и":"i",
                    "й":"i",
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
        # try:
        #     cursor = db.cursor()
        #     cursor.execute(f'''SELECT * FROM {table_used_base}''')
        #     msg[f'{today} - Таблица: {table_used_base} существует'] = 1
        # except:
        with db.atomic():
            db.create_tables([table_used_model])
            #msg[f'{today} - Таблица: {table_used_base} добавлена в базу данных'] = 3
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
        cursor = db.cursor()
        cursor.execute(f'''SELECT COUNT (*) FROM "{table_used}"''')
        empty = cursor.fetchall()
        return True if int(empty[0][0]) == 0  else False

    # Clear tabl
    def clear_tabl(self, table_used, table_name, list_tabl):
        msg = {}
        cursor = db.cursor()
        if not table_used in list_tabl:
            msg[f'{today} - Таблица: {table_used} отсутствует!'] = 2
            return msg

        if self.empty_table(table_used): 
            msg[f'{today} - Таблица: {table_used} пустая!'] = 2
            return msg
        
        cursor.execute(f'DELETE FROM "{table_used}"')
        msg[f'{today} - Таблица: {table_used} полностью очищена'] = 1
        return msg
    def search_signal(self, tabl_used_cl, tabl_used_str, tag):
        exists_tag = tabl_used_cl.select().where(tabl_used_cl.tag == tag)
        if bool(exists_tag):
            cursor = db.cursor()
            cursor.execute(f"""SELECT id, tag
                               FROM "{tabl_used_str}"
                               WHERE tag='{tag}'""")
            for id_, tag in cursor.fetchall():
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
            cursor = db.cursor()
            cursor.execute(f"""UPDATE {tabl_used_str}
                               SET "{column_update_str}"='{tag}' 
                               WHERE "id"='{number_NA}'""")
            msg[f'{today} - Таблица: umpna, NA[{number_NA}] обновлено {column_update_str} = {tag}'] = 3
            return msg
        return msg
    
    def update_signal_dop(self, tabl_used_cl, tabl_used_str, name, column_update_cl, column_update_str, value):
        msg = {}
        exist_value  = tabl_used_cl.select().where(tabl_used_cl.name == name,
                                                    column_update_cl == value)
        if not bool(exist_value):
            cursor = db.cursor()
            cursor.execute(f"""UPDATE {tabl_used_str}
                               SET "{column_update_str}"='{value}' 
                               WHERE "name"='{name}'""")
            msg[f'{today} - Таблица: {tabl_used_str}, обновлен: {name},  {column_update_str} = {value}'] = 3
            return msg
        return msg
    def parser_sample(self, path, kod_msg, name, flag_write_db, table, *args):
        cursor = db.cursor()
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(path, parser)
        root = tree.getroot()

        list_msg = []

        for lvl_one in root.iter('Row'):
            category  = lvl_one.attrib['Category']
            isAck     = lvl_one.attrib['IsAck']
            isCycle   = lvl_one.attrib['IsCycle']
            isSound   = lvl_one.attrib['IsSound']
            isHide    = lvl_one.attrib['IsHide']
            priority  = lvl_one.attrib['Priority']
            isAlert   = lvl_one.attrib['IsAlert']
            mess      = lvl_one.attrib['Message']
            soundFile = lvl_one.attrib['SoundFile']
            nextLink  = lvl_one.attrib['NextLink']
            base      = lvl_one.attrib['Base']

            if table == 'KTPRAS_1' or table == 'UMPNA':
                if self.str_find(mess, {'%1'}): 
                    mess = str(mess).replace('%1', args[0])
                if self.str_find(mess, {'%2'}): 
                    mess = str(mess).replace('%2', args[1])

            del_row_tabl = f"""DELETE FROM messages.opmessages WHERE Category ={kod_msg + int(category)};\n"""
            ins_row_tabl = f"INSERT INTO messages.opmessages (Category, Message, IsAck, SoundFile, IsCycle, IsSound, IsHide, Priority, IsAlert) VALUES({kod_msg + int(category)}, '{name}. {mess}', {isAck}, '{soundFile}', {isCycle}, {isSound}, {isHide}, {priority}, {isAlert});\n"
            
            if flag_write_db:
                cursor.execute(del_row_tabl)
                cursor.execute(ins_row_tabl)
            else:
                list_msg.append(dict(delete = del_row_tabl,
                                     insert = ins_row_tabl))
        return list_msg

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
            module      = row['module']
            channel     = row['channel']

            if basket is None or module is None or channel is None: continue

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
            try:
                Signals.insert_many(data).execute()
                msg[f'{today} - Добавлено новое УСО: {uso}'] = 1
            except Exception:
                msg[f'{today} - Таблица: signals, ошибка при заполнении: {traceback.format_exc()}'] = 2
        return(msg)
    # Update Database
    def update_for_sql(self, data, uso):
        msg = {}
        with db:
            try:
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
                            schema     =row_exel['schema'],
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
                                    schema     =row_exel['scheme'],
                                    klk        =row_exel['klk'],
                                    contact    =row_exel['contact'],
                                ).where(Signals.id == row_sql['id']).execute()
                                msg[f'''{today} - Обновление сигнала id = {row_sql["id"]}: Было, 
                                                                                        uso - {row_sql['uso']}, 
                                                                                        type_signal - {row_sql['type_signal']}, 
                                                                                        tag - {row_sql['tag']},                      
                                                                                        description - {row_sql['description']}, 
                                                                                        schema - {row_sql['scheme']}, 
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
            except Exception:
                msg[f'{today} - Таблица: signals, ошибка при обновлении: {traceback.format_exc()}'] = 2
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

            self.dop_func = General_functions()
            msg = self.dop_func.column_check(Signals, 'signals', list_default)
        return msg

# Work with filling in the table 'HardWare'
class Filling_HardWare():
    def __init__(self):
        self.cursor = db.cursor()
        self.dop_function = General_functions()
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
            try:
                if self.dop_function.empty_table('signals'): 
                    msg[f'{today} - Таблица: signals пустая! Заполни таблицу!'] = 2
                    return msg

                self.cursor.execute(f'''SELECT DISTINCT uso 
                                        FROM signals
                                        ORDER BY uso''')
                list_uso = self.cursor.fetchall()

                temp_flag    = False
                test_s       = []
                count_basket = 0
                count_AI, count_AO = 0, 0
                count_DI, count_DO, count_RS = 0, 0, 0 
                for uso in list_uso:
                    self.cursor.execute(f"""SELECT DISTINCT basket 
                                            FROM signals
                                            WHERE uso='{uso[0]}'
                                            ORDER BY basket""")
                    list_basket = self.cursor.fetchall()

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

                        self.cursor.execute(f"""SELECT DISTINCT module, type_signal 
                                                FROM signals
                                                WHERE uso='{uso[0]}' AND basket={basket[0]}
                                                ORDER BY module""")
                        req_modul = self.cursor.fetchall()
                        for i in req_modul:
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
            except Exception:
                msg[f'{today} - Таблица: hardware, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: hardware, выполнение кода завершено!'] = 1
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
        
        self.dop_func = General_functions()
        msg = self.dop_func.column_check(HardWare, 'hardware', list_default)
        return msg

# Work with filling in the table 'USO'
class Filling_USO():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    # Получаем данные с таблицы Signals 
    def getting_modul(self):
        msg = {}
        temp = False
        count_USO        = 0
        list_diag_signal = []
        with db:
            try:
                if self.dop_function.empty_table('ai') or self.dop_function.empty_table('di'): 
                    msg[f'{today} - Таблицы: ai или di пустые! Заполни таблицу!'] = 2
                    return msg
                try:
                    self.cursor.execute(f'''SELECT * FROM ai''')
                    self.cursor.execute(f'''SELECT * FROM di''')
                except:
                    msg[f'{today} - Таблицы: ai или di не найдены!'] = 2
                    return msg
                self.cursor.execute(f'''SELECT DISTINCT uso 
                                        FROM signals''')
                list_uso = self.cursor.fetchall()
                for uso in list_uso:
                    count_DI  = 0
                    count_USO += 1
                    list_diag = {}

                    list_diag['variable'] = f'USO[{count_USO}]'
                    list_diag['name']     = f'{uso[0]}'

                    self.cursor.execute(f"""SELECT variable, name
                                            FROM ai
                                            WHERE name LIKE '%{uso[0]}%'""")
                    current_ai = self.cursor.fetchall()
                    try:
                        if len(current_ai) == 0: raise
                        for ai in current_ai:
                            list_diag['temperature']  = f'{ai[0]}'
                            break
                    except:
                        list_diag['temperature']  = ''
                        msg[f'{today} - Таблица: uso. Температура в шкафу {uso[0]} не найдена!'] = 2

                    self.cursor.execute(f"""SELECT variable, name
                                            FROM di
                                            WHERE name LIKE '%{uso[0]}%' AND 
                                                 (name LIKE '%двер%' OR name LIKE '%Двер%')""")
                    current_door = self.cursor.fetchall()
                    try:
                        if len(current_door) == 0: raise
                        for door in current_door:
                            list_diag['door']  = f'{door[0]}.Value'
                            break
                    except:
                        list_diag['temperature']  = ''
                        msg[f'{today} - Таблица: uso. Сигнал открытой двери шкафа {uso[0]} не найден!'] = 2

                    self.cursor.execute(f"""SELECT variable, name
                                            FROM di
                                            WHERE name LIKE '%{uso[0]}%' AND 
                                                 (name NOT LIKE '%двер%') AND (name NOT LIKE '%Двер%') 
                                            ORDER BY name""")
                    current_di = self.cursor.fetchall()
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
                msg[f'{today} - Таблица: uso заполнена'] = 1
            except Exception:
                msg[f'{today} - Таблица: uso, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: uso, выполнение кода завершено!'] = 1
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
        self.dop_function = General_functions()
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
            try:
                if self.dop_function.empty_table('signals') or self.dop_function.empty_table('hardware'): 
                    msg[f'{today} - Таблицы: signals или hardware пустые! Заполни таблицу!'] = 2
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

                    tag_translate = self.dop_function.translate(str(tag))
                    if tag_translate == 'None': tag_translate = ''

                    if self.dop_function.str_find(type_signal, {'AI'}) or self.dop_function.str_find(scheme, {'AI'}):
                        count_AI += 1
                        # Выбор между полным заполнением или обновлением
                        if self.dop_function.empty_table('ai'):
                            msg[f'{today} - Таблица: ai пуста, идет заполнение'] = 1
                        else:
                            msg[f'{today} - Таблица: ai не пуста, идет обновление'] = 1

                        coincidence = AI.select().where(AI.uso     == uso_s,
                                                        AI.basket  == basket_s,
                                                        AI.module  == module_s,
                                                        AI.channel == channel_s)
                        if bool(coincidence):
                            exist_tag  = AI.select().where(AI.tag  == tag_translate)
                            exist_name = AI.select().where(AI.name == description)

                            if not bool(exist_tag):
                                self.cursor.execute(f"""SELECT id, tag 
                                                        FROM ai
                                                        WHERE uso='{uso_s}' AND 
                                                              basket={basket_s} AND 
                                                              module={module_s} AND 
                                                              channel={channel_s}""")
                                for id_, tag_ in self.cursor.fetchall():
                                    msg[f'{today} - Таблица: ai, у сигнала обновлен tag: id = {id_}, ({tag_}) {tag_translate}'] = 2
                                self.cursor.execute(f'''UPDATE ai
                                                        SET tag='{tag_translate}' 
                                                        WHERE uso='{uso_s}' AND 
                                                            basket={basket_s} AND 
                                                            module={module_s} AND 
                                                            channel={channel_s}''')
        
                            if not bool(exist_name):
                                self.cursor.execute(f'''SELECT id, name 
                                                        FROM ai
                                                        WHERE uso='{uso_s}' AND 
                                                        basket={basket_s} AND 
                                                        module={module_s} AND 
                                                        channel={channel_s}''')
                                for id_, name_ in self.cursor.fetchall():
                                    msg[f'{today} - Таблица: ai, у сигнала обновлено name: id = {id_}, ({name_}) {description}'] = 2
                                self.cursor.execute(f'''UPDATE ai
                                                        SET name='{description}' 
                                                        WHERE uso='{uso_s}' AND 
                                                              basket={basket_s} AND 
                                                              module={module_s} AND 
                                                              channel={channel_s}''')
                            continue

                        # Сквозной номер модуля
                        try:
                            for through_module_number in HardWare.select().dicts():
                                uso_h    = through_module_number['uso']
                                basket_h = through_module_number['basket']

                                isdigit_num = ''
                                if uso_s == uso_h and basket_s == basket_h:
                                    type_mod = through_module_number[f'variable_{module_s}']
                                    isdigit_num  = re.findall('\d+', str(type_mod))
                                    
                                    try   : isdigit_num = isdigit_num[0]
                                    except: 
                                        msg[f'{today} - В таблице hardware не найден модуль сигнала: {id_s}, {tag}, {description}, {uso_s}_A{basket_s}_{module_s}_{channel_s}, "pValue" не заполнен'] = 2
                                    break
                        except Exception:
                            msg[f'{today} - Таблица: ai, ошибка при заполнении. Заполнение продолжится: {traceback.format_exc()}'] = 2
                            msg[f'{today} - Таблица: signals, ошибка в этой строке. Строка пропускается: {row_sql}'] = 2
                            continue

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

                        if isdigit_num == '':
                            msg[f'{today} - В таблице hardware не найден модуль сигнала: {id_s}, {tag}, {description}, {uso_s}_A{basket_s}_{module_s}_{channel_s}, "pValue" не заполнен'] = 2

                        msg[f'{today} - Таблица: ai, добавлен новый сигнал: {row_sql}'] = 1
                        list_AI.append(dict(variable = f'AI[{count_AI}]',
                                            tag = tag_translate,
                                            name = description,
                                            pValue = f'mAI8[{isdigit_num}, {module_s}]',
                                            pHealth = f'mAI8_HEALTH[{isdigit_num}]',
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
                                            Pic = '', group_trend = '', hysteresis_TI = '0,1', unit_physical_ACP = 'мкА', 
                                            setpoint_map_rule = rule, fuse = '', uso = uso_s, basket = basket_s, module = module_s, channel = channel_s,
                                            AlphaHMI = '', AlphaHMI_PIC1 = '', AlphaHMI_PIC1_Number_kont = '', AlphaHMI_PIC2 = '', 
                                            AlphaHMI_PIC2_Number_kont = '', AlphaHMI_PIC3 = '', AlphaHMI_PIC3_Number_kont = '', 
                                            AlphaHMI_PIC4 = '', AlphaHMI_PIC4_Number_kont = ''))

                # Checking for the existence of a database
                AI.insert_many(list_AI).execute()
            except Exception:
                msg[f'{today} - Таблица: ai, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: ai, выполнение кода завершено!'] = 1
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
                        'ust_max_5', 'ust_max_6', 'value_precision', 'Pic', 'group_trend', 'hysteresis_TI', 
                        'unit_physical_ACP', 'setpoint_map_rule', 'fuse', 'uso', 'basket', 'module', 'channel', 'AlphaHMI', 'AlphaHMI_PIC1', 
                        'AlphaHMI_PIC1_Number_kont', 'AlphaHMI_PIC2', 'AlphaHMI_PIC2_Number_kont',
                        'AlphaHMI_PIC3', 'AlphaHMI_PIC3_Number_kont', 'AlphaHMI_PIC4', 'AlphaHMI_PIC4_Number_kont']
        msg = self.dop_function.column_check(AI, 'ai', list_default)
        return msg 

# Work with filling in the table 'AO'
class Filling_AO():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    # Получаем данные с таблицы Signals 
    def getting_modul(self):
        msg = {}
        list_AO = []
        count_AO = 0
        
        with db:
            try:
                if self.dop_function.empty_table('signals') or self.dop_function.empty_table('hardware'): 
                    msg[f'{today} - Таблицы: signals или hardware пустые! Заполни таблицу!'] = 2
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
                        if self.dop_function.empty_table('ao'):
                            msg[f'{today} - Таблица: ao пуста, идет заполнение'] = 1
                        else:
                            msg[f'{today} - Таблица: ao не пуста, идет обновление'] = 1

                        coincidence = AO.select().where(AO.uso     == uso_s,
                                                        AO.basket  == basket_s,
                                                        AO.module  == module_s,
                                                        AO.channel == channel_s)
                        if bool(coincidence):
                            exist_tag  = AO.select().where(AO.tag == tag)
                            exist_name = AO.select().where(AO.name == description)

                            if not bool(exist_tag):
                                self.cursor.execute(f'''SELECT id, tag 
                                                        FROM ao
                                                        WHERE uso='{uso_s}' AND 
                                                              basket={basket_s} AND 
                                                              module={module_s} AND 
                                                              channel={channel_s}''')
                                for id_, tag_ in self.cursor.fetchall():
                                    msg[f'{today} - Таблица: ao, у сигнала обновлен tag: id = {id_}, ({tag_}) {tag}'] = 2
                                self.cursor.execute(f'''UPDATE ao
                                                        SET tag='{tag}' 
                                                        WHERE uso='{uso_s}' AND 
                                                              basket={basket_s} AND 
                                                              module={module_s} AND 
                                                              channel={channel_s}''')
        
                            if not bool(exist_name):
                                self.cursor.execute(f'''SELECT id, name 
                                                        FROM ao
                                                        WHERE uso='{uso_s}' AND 
                                                              basket={basket_s} AND 
                                                              module={module_s} AND 
                                                              channel={channel_s}''')
                                for id_, name_ in self.cursor.fetchall():
                                    msg[f'{today} - Таблица: ao, у сигнала обновлено name: id = {id_}, ({name_}) {description}'] = 2
                                self.cursor.execute(f'''UPDATE ao
                                                        SET name='{description}' 
                                                        WHERE uso='{uso_s}' AND 
                                                              basket={basket_s} AND 
                                                              module={module_s} AND 
                                                              channel={channel_s}''')
                            continue

                        # Сквозной номер модуля
                        try:
                            for through_module_number in HardWare.select().dicts():
                                tag_h    = through_module_number['tag']
                                uso_h    = through_module_number['uso']
                                basket_h = through_module_number['basket']

                                isdigit_num = ''
                                if uso_s == uso_h and basket_s == basket_h:
                                    type_mod = through_module_number[f'variable_{module_s}']
                                    isdigit_num  = re.findall('\d+', str(type_mod))

                                    try   : isdigit_num = isdigit_num[0]
                                    except: 
                                        msg[f'{today} - В таблице hardware не найден модуль сигнала: {id_s}, {tag}, {description}, {uso_s}_A{basket_s}_{module_s}_{channel_s}, "pValue" не заполнен'] = 2
                                    break

                            if module_s < 10: prefix = f'0{module_s}' 
                            else            : prefix = f'{module_s}'
                        except Exception:
                            msg[f'{today} - Таблица: ao, ошибка при заполнении. Заполнение продолжится: {traceback.format_exc()}'] = 2
                            msg[f'{today} - Таблица: signals, ошибка в этой строке. Строка пропусается: {row_sql}'] = 2
                            continue
                        
                        if isdigit_num == '':
                            msg[f'{today} - В таблице hardware не найден модуль сигнала: {id_s}, {tag}, {description}, {uso_s}_A{basket_s}_{module_s}_{channel_s}, "pValue" не заполнен'] = 2
                        
                        msg[f'{today} - Таблица: ao, добавлен новый сигнал: {row_sql}'] = 1
                        list_AO.append(dict(variable = f'AO[{count_AO}]',
                                        tag = tag,
                                        name = description,
                                        pValue = f'{tag_h}_{prefix}_AO[{channel_s}]',
                                        pHealth = f'mAO_HEALTH[{isdigit_num}]',
                                        uso = uso_s, 
                                        basket = basket_s, 
                                        module = module_s, 
                                        channel = channel_s,
                                        ))

                # Checking for the existence of a database
                AO.insert_many(list_AO).execute()
            except Exception:
                msg[f'{today} - Таблица: ao, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: ao, выполнение кода завершено!'] = 1
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
        self.dop_function = General_functions()
    # Получаем данные с таблицы Signals 
    def getting_modul(self):
        msg = {}
        list_DI = []
        count_DI = 0
        with db:
            try:
                if self.dop_function.empty_table('signals') or self.dop_function.empty_table('hardware'): 
                    msg[f'{today} - Таблицы: signals или hardware пустые! Заполни таблицу!'] = 2
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

                    tag_translate = self.dop_function.translate(str(tag))
                    if tag_translate == 'None': tag_translate = ''

                    if self.dop_function.str_find(type_signal, {'DI'}) or self.dop_function.str_find(scheme, {'DI'}):
                        count_DI += 1
                        # Выбор между полным заполнением или обновлением
                        if self.dop_function.empty_table('di'):
                            msg[f'{today} - Таблица: di пуста, идет заполнение'] = 1
                        else:
                            msg[f'{today} - Таблица: di не пуста, идет обновление'] = 1

                        coincidence = DI.select().where(DI.uso     == uso_s,
                                                        DI.basket  == basket_s,
                                                        DI.module  == module_s,
                                                        DI.channel == channel_s)
                        if bool(coincidence):
                            exist_tag  = DI.select().where(DI.tag  == tag_translate)
                            exist_name = DI.select().where(DI.name == description)

                            if not bool(exist_tag):
                                self.cursor.execute(f'''SELECT id, tag 
                                                        FROM di
                                                        WHERE uso='{uso_s}' AND 
                                                              basket={basket_s} AND 
                                                              module={module_s} AND 
                                                              channel={channel_s}''')
                                for id_, tag_ in self.cursor.fetchall():
                                    msg[f'{today} - Таблица: di, у сигнала обновлен tag: id = {id_}, ({tag_}) {tag_translate}'] = 2
                                self.cursor.execute(f'''UPDATE di
                                                        SET tag='{tag_translate}' 
                                                        WHERE uso='{uso_s}' AND 
                                                              basket={basket_s} AND 
                                                              module={module_s} AND 
                                                              channel={channel_s}''')
        
                            if not bool(exist_name):
                                self.cursor.execute(f'''SELECT id, name 
                                                        FROM di
                                                        WHERE uso='{uso_s}' AND 
                                                              basket={basket_s} AND 
                                                              module={module_s} AND 
                                                              channel={channel_s}''')
                                for id_, name_ in self.cursor.fetchall():
                                    msg[f'{today} - Таблица: di, у сигнала обновлено name: id = {id_}, ({name_}) {description}'] = 2
                                self.cursor.execute(f'''UPDATE di
                                                        SET name='{description}' 
                                                        WHERE uso='{uso_s}' AND 
                                                              basket={basket_s} AND 
                                                              module={module_s} AND 
                                                              channel={channel_s}''')
                            continue

                        # Сквозной номер модуля
                        try:
                            for through_module_number in HardWare.select().dicts():
                                tag_h    = through_module_number['tag']
                                uso_h    = through_module_number['uso']
                                basket_h = through_module_number['basket']

                                isdigit_num = ''
                                if uso_s == uso_h and basket_s == basket_h:
                                    type_mod = through_module_number[f'variable_{module_s}']
                                    isdigit_num  = re.findall('\d+', str(type_mod))

                                    try   : isdigit_num = isdigit_num[0]
                                    except: 
                                        msg[f'{today} - В таблице hardware не найден модуль сигнала: {id_s}, {tag}, {description}, {uso_s}_A{basket_s}_{module_s}_{channel_s}, "pValue" не заполнен'] = 2
                                    break

                            if module_s < 10: prefix = f'0{module_s}' 
                            else            : prefix = f'{module_s}'
                        except Exception:
                            msg[f'{today} - Таблица: di, ошибка при заполнении. Заполнение продолжится: {traceback.format_exc()}'] = 2
                            msg[f'{today} - Таблица: signals, ошибка в этой строке. Строка пропусается: {row_sql}'] = 2
                            continue

                        if self.dop_function.str_find(str(tag).lower(), {'csc'}) : group_diskrets = 'Диагностика'
                        elif self.dop_function.str_find(str(tag).lower(), {'ec'}): group_diskrets = 'Электроснабжение'
                        else: group_diskrets = 'Общие'

                        if isdigit_num == '':
                            msg[f'{today} - В таблице hardware не найден модуль сигнала: {id_s}, {tag}, {description}, {uso_s}_A{basket_s}_{module_s}_{channel_s}, "pValue" не заполнен'] = 2
                        
                        msg[f'{today} - Таблица: di, добавлен новый сигнал: {row_sql}'] = 1

                        list_DI.append(dict(variable = f'DI[{count_DI}]',
                                            tag = tag_translate,
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
            except Exception:
                msg[f'{today} - Таблица: di, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: di, выполнение кода завершено!'] = 1
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
        self.dop_function = General_functions()
    # Получаем данные с таблицы Signals 
    def getting_modul(self):
        msg = {}
        list_DO = []
        count_DO = 0
        with db:
            try:
                if self.dop_function.empty_table('signals') or self.dop_function.empty_table('hardware'): 
                    msg[f'{today} - Таблицы: signals или hardware пустые! Заполни таблицу!'] = 2
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

                    tag_translate = self.dop_function.translate(str(tag))
                    if tag_translate == 'None': tag_translate = ''

                    if self.dop_function.str_find(type_signal, {'DO'}) or self.dop_function.str_find(scheme, {'DO'}):
                        count_DO += 1
                        # Выбор между полным заполнением или обновлением
                        if self.dop_function.empty_table("do"):
                            msg[f'{today} - Таблица: do пуста, идет заполнение'] = 1
                        else:
                            msg[f'{today} - Таблица: do не пуста, идет обновление'] = 1

                        coincidence = DO.select().where(DO.uso    == uso_s,
                                                        DO.basket == basket_s,
                                                        DO.module == module_s,
                                                        DO.channel== channel_s)
                        if bool(coincidence):
                            exist_tag  = DO.select().where(DO.tag == tag_translate)
                            exist_name = DO.select().where(DO.name == description)

                            if not bool(exist_tag):
                                self.cursor.execute(f'''SELECT id, tag 
                                                        FROM "do"
                                                        WHERE uso='{uso_s}' AND 
                                                              basket={basket_s} AND 
                                                              module={module_s} AND 
                                                              channel={channel_s}''')
                                for id_, tag_ in self.cursor.fetchall():
                                    msg[f'{today} - Таблица: do, у сигнала обновлен tag: id = {id_}, ({tag_}) {tag_translate}'] = 2
                                self.cursor.execute(f'''UPDATE "do"
                                                        SET tag='{tag_translate}' 
                                                        WHERE uso='{uso_s}' AND 
                                                              basket={basket_s} AND 
                                                              module={module_s} AND 
                                                              channel={channel_s}''')
        
                            if not bool(exist_name):
                                self.cursor.execute(f'''SELECT id, name 
                                                        FROM "do"
                                                        WHERE uso='{uso_s}' AND 
                                                              basket={basket_s} AND 
                                                              module={module_s} AND 
                                                              channel={channel_s}''')
                                for id_, name_ in self.cursor.fetchall():
                                    msg[f'{today} - Таблица: do, у сигнала обновлено name: id = {id_}, ({name_}) {description}'] = 2
                                self.cursor.execute(f'''UPDATE "do"
                                                        SET name='{description}' 
                                                        WHERE uso='{uso_s}' AND 
                                                              basket={basket_s} AND 
                                                              module={module_s} AND 
                                                              channel={channel_s}''')
                            continue

                        # Сквозной номер модуля
                        try:
                            for through_module_number in HardWare.select().dicts():
                                tag_h    = through_module_number['tag']
                                uso_h    = through_module_number['uso']
                                basket_h = through_module_number['basket']

                                isdigit_num = ''
                                if uso_s == uso_h and basket_s == basket_h:
                                    type_mod = through_module_number[f'variable_{module_s}']
                                    isdigit_num  = re.findall('\d+', str(type_mod))

                                    try   : isdigit_num = isdigit_num[0]
                                    except: 
                                        msg[f'{today} - В таблице hardware не найден модуль сигнала: {id_s}, {tag}, {description}, {uso_s}_A{basket_s}_{module_s}_{channel_s}, "pValue" не заполнен'] = 2
                                    break

                            if module_s < 10: prefix = f'0{module_s}' 
                            else            : prefix = f'{module_s}'
                        except Exception:
                            msg[f'{today} - Таблица: do, ошибка при заполнении. Заполнение продолжится: {traceback.format_exc()}'] = 2
                            msg[f'{today} - Таблица: signals, ошибка в этой строке. Строка пропусается: {row_sql}'] = 2
                            continue

                        if isdigit_num == '':
                            msg[f'{today} - В таблице hardware не найден модуль сигнала: {id_s}, {tag}, {description}, {uso_s}_A{basket_s}_{module_s}_{channel_s}, "pValue" не заполнен'] = 2
                        
                        msg[f'{today} - Таблица: do, добавлен новый сигнал: {row_sql}'] = 1

                        list_DO.append(dict(variable = f'DO[{count_DO}]',
                                        tag = tag_translate,
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
            except Exception:
                msg[f'{today} - Таблица: do, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: do, выполнение кода завершено!'] = 1
        return(msg)
    # Заполняем таблицу DO
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'pValue', 'pHealth', 'short_title', 'uso', 'basket', 'module', 'channel', 
                        'AlphaHMI', 'AlphaHMI_PIC1', 'AlphaHMI_PIC1_Number_kont', 'AlphaHMI_PIC2',
                        'AlphaHMI_PIC2_Number_kont','AlphaHMI_PIC3', 'AlphaHMI_PIC3_Number_kont', 
                        'AlphaHMI_PIC4', 'AlphaHMI_PIC4_Number_kont']
        msg = self.dop_function.column_check(DO, 'do', list_default)
        return msg 
    
# Work with filling in the table 'KTPRP'
class Filling_KTPRP():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    def getting_modul(self):
        msg = {}
        list_KTPRP = []
        with db:
            for i in range(1, 31):
                list_KTPRP.append(dict(variable = f'KTPRP[{i}]',
                                       tag = '',
                                       name = 'Резерв',
                                       Number_PZ = '',
                                       Type = '',
                                       Pic = ''))

            # Checking for the existence of a database
            KTPRP.insert_many(list_KTPRP).execute()

        msg[f'{today} - Таблица: ktprp подготовлена'] = 1
        return(msg)
    # Заполняем таблицу KTPRP
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'Number_PZ', 'Type', 'Pic', 
                         'number_list_VU', 'number_protect_VU']
        msg = self.dop_function.column_check(KTPRP, 'ktprp', list_default)
        return msg 
# Work with filling in the table 'KTPR'
class Filling_KTPR():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    def getting_modul(self):
        msg = {}
        list_KTPR = []
        with db:
            for i in range(1, 97):
                list_KTPR.append(dict(variable = f'KTPR[{i}]',
                                      tag = '',
                                      name = 'Резерв',
                                      avar_parameter = '',
                                    #   prohibition_masking = '',
                                    #   auto_unlock_protection = '',
                                    #   shutdown_PNS_a_time_delay_up_5s_after_turning = '',
                                    #   bitmask_protection_group_membership = '',
                                    #   stop_type_NA = '',
                                    #   pump_station_stop_type = '',
                                    #   closing_gate_valves_at_the_inlet_NPS = '',
                                    #   closing_gate_valves_at_the_outlet_NPS = '',
                                    #   closing_gate_valves_between_PNS_and_MNS = '',
                                    #   closing_gate_valves_between_RP_and_PNS = '',
                                    #   closing_valves_inlet_and_outlet_MNS = '',
                                    #   closing_valves_inlet_and_outlet_PNS = '',
                                    #   closing_valves_inlet_and_outlet_MNA = '',
                                    #   closing_valves_inlet_and_outlet_PNA = '',
                                    #   closing_valves_inlet_RD = '',
                                    #   closing_valves_outlet_RD = '',
                                    #   closing_valves_inlet_SSVD = '',
                                    #   closing_valves_inlet_FGU = '',
                                    #   closing_secant_valve_connection_unit__oil_production_oil = '',
                                    #   closing_valves_inlet_RP = '',
                                    #   reserve_protect_14 = '',
                                    #   reserve_protect_15 = '',
                                    #   shutdown_oil_pumps_after_signal_stopped_NA = '',
                                    #   shutdown_circulating_water_pumps = '',
                                    #   shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_MNS = '',
                                    #   shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_PNS = '',
                                    #   shutdown_pumps_pumping_out_from_tanks_SSVD = '',
                                    #   switching_off_the_electric_room_fans = '',
                                    #   shutdown_of_booster_fans_ED = '',
                                    #   shutdown_of_retaining_fans_of_the_electrical_room = '',
                                    #   shutdown_of_ED_air_compressors = '',
                                    #   shutdown_pumps_providing_oil = '',
                                    #   disabling_pumps_for_pumping_oil_oil_products_through_BIC = '',
                                    #   shutdown_domestic_and_drinking_water_pumps = '',
                                    #   shutdown_of_art_well_pumps = '',
                                    #   AVO_shutdown = '',
                                    #   shutdown_of_water_cooling_fans_circulating_water_supply_system = '',
                                    #   shutdown_exhaust_fans_of_the_pumping_room_of_the_MNS = '',
                                    #   shutdown_of_exhaust_fans_of_the_pumping_room_PNS = '',
                                    #   shutdown_of_exhaust_fans_in_the_centralized_oil_system_room = '',
                                    #   shutdown_of_exhaust_fans_oil_pit_in_the_electrical_room = '',
                                    #   shutdown_of_exhaust_fans_in_the_RD_room = '',
                                    #   shutdown_of_exhaust_fans_in_the_SSVD_room = '',
                                    #   shutdown_of_the_roof_fans_of_the_MNS_pump_room = '',
                                    #   shutdown_of_the_roof_fans_of_the_PNS_pump_room = '',
                                    #   switching_off_the_supply_fans_pumping_room_of_the_MNS = '',
                                    #   switching_off_the_supply_fans_pumping_room_of_the_PNS = '',
                                    #   switch_off_the_supply_fans_in_the_centralized_oil = '',
                                    #   switching_off_the_supply_fan_of_the_RD_room = '',
                                    #   switching_off_the_supply_fan_of_the_SSVD_room = '',
                                    #   switching_off_the_supply_fans_of_the_ED_air_compressor = '',
                                    #   switching_off_the_supply_fan_of_the_BIK_room = '',
                                    #   switching_off_the_supply_fan_of_the_SIKN_room = '',  
                                    #   closing_the_air_valves_louvered_grilles_of_the_pump_room = '',
                                    #   closing_of_air_valves_louvered_grilles_of_the_compressor_room = '',
                                    #   shutdown_of_electric_oil_heaters = '',
                                    #   shutdown_of_the_electric_heaters_of_the_leakage_collection_MNS = '',
                                    #   shutdown_of_the_electric_heaters_of_the_leakage_collection_PNS = '',
                                    #   shutdown_of_electric_heaters_of_the_SIKN_leak_collection_tank = '',
                                    #   shutdown_of_air_coolers_of_the_locking_system_MNA = '',
                                    #   shutdown_of_air_coolers_of_the_locking_system_disc_NA = '',
                                    #   shutdown_of_the_external_cooling_circuit_ChRP_MNA = '',
                                    #   shutdown_of_the_external_cooling_circuit_ChRP_PNA = '',
                                    #   shutdown_of_locking_system_pumps = '',
                                    #   shutdown_of_pumps_for_pumping_oil_oil_products_through = '',
                                    #   shutdown_of_pumping_pumps_from_leakage_collection_tanks = '',
                                    #   shutdown_of_anticondensation_electric_heaters_ED = '',
                                    #   fire_protection = '',
                                    #   reserve_aux_15 = '',
                                    #   time_ust = '',
                                    #   Pic = '',
                                      group_ust = 'Временные уставки общестанционных защит',
                                      rule_map_ust = 'Временные уставки',
                                    #   number_list_VU = '',
                                    #   number_protect_VU = ''
                                    ))

            # Checking for the existence of a database
            KTPR.insert_many(list_KTPR).execute()

        msg[f'{today} - Таблица: ktpr подготовлена'] = 1
        return(msg)
    # Заполняем таблицу KTPR
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 
                        'avar_parameter', 'prohibition_masking', 'auto_unlock_protection', 'shutdown_PNS_a_time_delay_up_5s_after_turning',
                        'bitmask_protection_group_membership', 'stop_type_NA', 'pump_station_stop_type',
                        'closing_gate_valves_at_the_inlet_NPS', 'closing_gate_valves_at_the_outlet_NPS', 'closing_gate_valves_between_PNS_and_MNS',
                        'closing_gate_valves_between_RP_and_PNS', 'closing_valves_inlet_and_outlet_MNS', 'closing_valves_inlet_and_outlet_PNS',
                        'closing_valves_inlet_and_outlet_MNA', 'closing_valves_inlet_and_outlet_PNA', 'closing_valves_inlet_RD',
                        'closing_valves_outlet_RD', 'closing_valves_inlet_SSVD', 'closing_valves_inlet_FGU',
                        'closing_secant_valve_connection_unit__oil_production_oil', 'closing_valves_inlet_RP', 'reserve_protect_14', 'reserve_protect_15',
                        'shutdown_oil_pumps', 'shutdown_oil_pumps_after_signal_stopped_NA', 'shutdown_circulating_water_pumps',
                        'shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_MNS', 'shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_PNS',
                        'shutdown_pumps_pumping_out_from_tanks_SSVD', 'switching_off_the_electric_room_fans', 'shutdown_of_booster_fans_ED', 
                        'shutdown_of_retaining_fans_of_the_electrical_room', 'shutdown_of_ED_air_compressors', 
                        'shutdown_pumps_providing_oil', 
                        'disabling_pumps_for_pumping_oil_oil_products_through_BIC', 'shutdown_domestic_and_drinking_water_pumps', 'shutdown_of_art_well_pumps',
                        'AVO_shutdown', 'shutdown_of_water_cooling_fans_circulating_water_supply_system',
                        'shutdown_exhaust_fans_of_the_pumping_room_of_the_MNS', 'shutdown_of_exhaust_fans_of_the_pumping_room_PNS',
                        'shutdown_of_exhaust_fans_in_the_centralized_oil_system_room', 'shutdown_of_exhaust_fans_oil_pit_in_the_electrical_room', 
                        'shutdown_of_exhaust_fans_in_the_RD_room', 'shutdown_of_exhaust_fans_in_the_SSVD_room',
                        'shutdown_of_the_roof_fans_of_the_MNS_pump_room', 'shutdown_of_the_roof_fans_of_the_PNS_pump_room',
                        'switching_off_the_supply_fans_pumping_room_of_the_MNS', 'switching_off_the_supply_fans_pumping_room_of_the_PNS',
                        'switch_off_the_supply_fans_in_the_centralized_oil', 'switching_off_the_supply_fan_of_the_RD_room',
                        'switching_off_the_supply_fan_of_the_SSVD_room', 'switching_off_the_supply_fans_of_the_ED_air_compressor',
                        'switching_off_the_supply_fan_of_the_BIK_room', 'switching_off_the_supply_fan_of_the_SIKN_room',
                        'closing_the_air_valves_louvered_grilles_of_the_pump_room', 'closing_of_air_valves_louvered_grilles_of_the_compressor_room',
                        'shutdown_of_electric_oil_heaters', 'shutdown_of_the_electric_heaters_of_the_leakage_collection_MNS',
                        'shutdown_of_the_electric_heaters_of_the_leakage_collection_PNS', 'shutdown_of_electric_heaters_of_the_SIKN_leak_collection_tank',
                        'shutdown_of_air_coolers_of_the_locking_system_MNA', 'shutdown_of_air_coolers_of_the_locking_system_disc_NA',
                        'shutdown_of_the_external_cooling_circuit_ChRP_MNA', 'shutdown_of_the_external_cooling_circuit_ChRP_PNA', 'shutdown_of_locking_system_pumps',
                        'shutdown_of_pumps_for_pumping_oil_oil_products_through',
                        'shutdown_of_pumping_pumps_from_leakage_collection_tanks', 'shutdown_of_anticondensation_electric_heaters_ED', 'fire_protection', 'reserve_aux_15', 
                        'time_ust', 'Pic', 'group_ust', 'rule_map_ust', 'number_list_VU', 'number_protect_VU']
        msg = self.dop_function.column_check(KTPR, 'ktpr', list_default)
        return msg 
# Work with filling in the table 'KTPRA'
class Filling_KTPRA():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    def getting_modul(self):
        msg = {}
        list_ktpra = []
        with db:
            for i in range(1, 5):
                for k in range(1, 97):
                    list_ktpra.append(dict(variable = f'KTPRA[{i}][{k}]',
                                            tag  = '',
                                            name = f'Резерв',
                                            NA = '',
                                            avar_parameter = '',
                                            stop_type = '',
                                            AVR = '',
                                            close_valves = '',
                                            prohibition_of_masking = '',
                                            time_setting = '',
                                            Pic = '',
                                            group_ust = f'Tm - Агрегатные защиты МНА{i}',
                                            rule_map_ust = 'Временные уставки',
                                            # number_list_VU = ,
                                            # number_protect_VU = '',
                                            number_pump_VU = i
                                            ))
            # Checking for the existence of a database
            KTPRA.insert_many(list_ktpra).execute()
        msg[f'{today} - Таблица: ktpra подготовлена'] = 1
        return(msg)
    # Заполняем таблицу KTPRA
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 
                        'NA', 'avar_parameter', 'stop_type', 'AVR', 'close_valves',
                        'prohibition_of_masking', 'time_setting', 'Pic', 
                        'group_ust', 'rule_map_ust', 'number_list_VU', 'number_protect_VU', 'number_pump_VU']
        msg = self.dop_function.column_check(KTPRA, 'ktpra', list_default)
        return msg 
# Work with filling in the table 'KTPRS'
class Filling_KTPRS():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
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
                                       Pic = ''))

            # Checking for the existence of a database
            KTPRS.insert_many(list_KTPRS).execute()

        msg[f'{today} - Таблица: ktprs подготовлена'] = 1
        return(msg)
    # Заполняем таблицу KTPRS
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'drawdown', 'reference_to_value', 'priority_msg_0', 
                        'priority_msg_1', 'prohibition_issuing_msg', 'Pic']
        msg = self.dop_function.column_check(KTPRS, 'ktprs', list_default)
        return msg 
    
    # Work with filling in the table 'KTPR'
# Work with filling in the table 'GMPNA'
class Filling_GMPNA():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
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
                                            # number_list_VU = '',
                                            # number_protect_VU = '',
                                            number_pump_VU = i))

            # Checking for the existence of a database
            GMPNA.insert_many(list_GMPNA).execute()

        msg[f'{today} - Таблица: gmpna подготовлена'] = 1
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
        self.dop_function = General_functions()
    # Получаем данные с таблицы AI и DI 
    def getting_modul(self, count_NA):
        msg = {}
        with db:
            try:
                try:
                    if self.dop_function.empty_table('di') or self.dop_function.empty_table('ai'): 
                        msg[f'{today} - Таблицы: ai или di пустые! Заполни таблицы!'] = 2
                        return msg
                except:
                    msg[f'{today} - Таблицы: ai или di отсутсвует!'] = 2
                    return msg

                self.cursor.execute(f'''SELECT Count (*) FROM "umpna"''')
                row_count = self.cursor.fetchall()[0][0]

                for i in range(1, count_NA + 1):

                    if row_count < i:
                        list_UMPNA = []
                        msg[f'{today} - Таблица: umpna, отсутствует NA[{i}] идет заполнение'] = 3

                        vv_included = self.dop_function.search_signal(DI, "di", f"MBC{i}01-1")
                        vv_double_included = self.dop_function.search_signal(DI, "di", f'MBC{i}01-2')
                        vv_disabled = self.dop_function.search_signal(DI, "di", f'MBC{i}02-1')
                        vv_double_disabled = self.dop_function.search_signal(DI, "di", f'MBC{i}02-2')
                        current_greater_than_noload_setting = self.dop_function.search_signal(AI, 'ai', f'CT{i}01')
                        serviceability_of_circuits_of_inclusion_of_VV = self.dop_function.search_signal(DI, "di", f'ECB{i}01')
                        serviceability_of_circuits_of_shutdown_of_VV = self.dop_function.search_signal(DI, "di", f'ECO{i}01-1')
                        serviceability_of_circuits_of_shutdown_of_VV_double = self.dop_function.search_signal(DI, "di", f'ECO{i}01-2')
                        stop_1 = self.dop_function.search_signal(DI, "di", f'KKC{i}01')
                        stop_2 = self.dop_function.search_signal(DI, "di", f'KKC{i}02')
                        monitoring_the_presence_of_voltage_in_the_control_current_circuits = self.dop_function.search_signal(DI, "di", f'EC{i}08')
                        vv_trolley_rolled_out = self.dop_function.search_signal(DI, "di", f'EC{i}04')
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
                            monitoring_the_presence_of_voltage_in_the_control_current = monitoring_the_presence_of_voltage_in_the_control_current_circuits,
                            voltage_presence_flag_in_the_ZRU_motor_cell ='',
                            vv_trolley_rolled_out = vv_trolley_rolled_out,
                            remote_control_mode_of_the_RZiA_controller ='',
                            availability_of_communication_with_the_RZiA_controller ='',
                            the_state_of_the_causative_agent_of_ED ='',
                            engine_prepurge_end_flag ='',
                            flag_for_the_presence_of_safe_air_boost_pressure_in_the_en ='',
                            flag_for_the_presence_of_safe_air_boost_pressure_in_the_ex ='',
                            engine_purge_valve_closed_flag ='',
                            oil_system_oil_temperature_flag_is_above_10_at_the_cooler_ou ='',
                            flag_for_the_minimum_oil_level_in_the_oil_tank_for_an_indiv ='',
                            flag_for_the_presence_of_the_minimum_level_of_the_barrier ='',
                            generalized_flag_for_the_presence_of_barrier_fluid_pressure ='',
                            command_to_turn_on_the_vv_only_for_UMPNA = command_to_turn_on_the_vv_only_for_UMPNA,
                            command_to_turn_off_the_vv_output_1 = command_to_turn_off_the_vv_output_1,
                            command_to_turn_off_the_vv_output_2 = command_to_turn_off_the_vv_output_2,
                            NA_Chrp ='',
                            type_NA_MNA ='',
                            pump_type_NM ='',
                            parametr_KTPRAS_1 ='',
                            number_of_delay_scans_of_the_analysis_of_the_health_of_the ='',
                            unit_number_of_the_auxiliary_system_start_up_oil_pump ='',
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
                            Pic ='',
                            tabl_msg = 'TblPumpsUMPNA',
                            replacement_uso_signal_vv_1 ='',
                            replacement_uso_signal_vv_2 =''))
                            
                        # Checking for the existence of a database
                        UMPNA.insert_many(list_UMPNA).execute()
                        msg[f'{today} - Таблица: umpna, NA[{i}] заполнен'] = 1

                    else:

                        msg[f'{today} - Таблица: umpna, NA[{i}] идет обновление'] = 3

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
                            self.dop_function.search_signal(DI, "di", f"EC{i}08"), i, UMPNA.monitoring_the_presence_of_voltage_in_the_control_current, 'monitoring_the_presence_of_voltage_in_the_control_current'))
                        msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                            self.dop_function.search_signal(DI, "di", f"EC{i}04"), i, UMPNA.vv_trolley_rolled_out, 'vv_trolley_rolled_out'))
                        msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                            self.dop_function.search_signal(DO, 'do', f"ABB{i}01"), i, UMPNA.command_to_turn_on_the_vv_only_for_UMPNA, 'command_to_turn_on_the_vv_only_for_UMPNA'))
                        msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                            self.dop_function.search_signal(DO, 'do', f"ABO{i}01-1"), i, UMPNA.command_to_turn_off_the_vv_output_1, 'command_to_turn_off_the_vv_output_1'))
                        msg.update(self.dop_function.update_signal(UMPNA, 'umpna', 
                            self.dop_function.search_signal(DO, 'do', f"ABO{i}01-2"), i, UMPNA.command_to_turn_off_the_vv_output_2, 'command_to_turn_off_the_vv_output_2'))
                        
                        msg[f'{today} - Таблица: umpna, сигналы NA[{i}] обновлены'] = 1
                
                self.cursor.execute(f'''SELECT name FROM "umpna"''')
                for i in self.cursor.fetchall():
                    if i[0] is None or i[0] == '' or i[0] == ' ':
                        msg[f'{today} - Таблица: umpna, необходимо заполнить название НА!'] = 3
            except Exception:
                msg[f'{today} - Таблица: umpna, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: umpna, выполнение кода завершено!'] = 1
        return(msg)
    # Заполняем таблицу UMPNA
    def column_check(self):
        list_default = ['variable', 'name', 'vv_included', 'vv_double_included', 'vv_disabled', 
                        'vv_double_disabled', 'current_greater_than_noload_setting', 'serviceability_of_circuits_of_inclusion_of_VV',
                        'serviceability_of_circuits_of_shutdown_of_VV', 'serviceability_of_circuits_of_shutdown_of_VV_double',
                        'stop_1', 'stop_2', 'stop_3', 'stop_4',
                        'monitoring_the_presence_of_voltage_in_the_control_current', 'voltage_presence_flag_in_the_ZRU_motor_cell',
                        'vv_trolley_rolled_out', 'remote_control_mode_of_the_RZiA_controller', 
                        'availability_of_communication_with_the_RZiA_controller','the_state_of_the_causative_agent_of_ED',
                        'engine_prepurge_end_flag', 'flag_for_the_presence_of_safe_air_boost_pressure_in_the_en',
                        'flag_for_the_presence_of_safe_air_boost_pressure_in_the_ex', 'engine_purge_valve_closed_flag',
                        'oil_system_oil_temperature_flag_is_above_10_at_the_cooler_ou', 
                        'flag_for_the_minimum_oil_level_in_the_oil_tank_for_an_indiv', 
                        'flag_for_the_presence_of_the_minimum_level_of_the_barrier',
                        'generalized_flag_for_the_presence_of_barrier_fluid_pressure', 'command_to_turn_on_the_vv_only_for_UMPNA',
                        'command_to_turn_off_the_vv_output_1', 'command_to_turn_off_the_vv_output_2', 'NA_Chrp', 'type_NA_MNA',
                        'pump_type_NM','parametr_KTPRAS_1', 'number_of_delay_scans_of_the_analysis_of_the_health_of_the',
                        'unit_number_of_the_auxiliary_system_start_up_oil_pump', 'NPS_number_1_or_2_which_the_AT_belongs',
                        'achr_protection_number_in_the_array_of_station_protections','saon_protection_number_in_the_array_of_station_protections', 
                        'gmpna_49', 'gmpna_50', 'gmpna_51', 'gmpna_52','gmpna_53', 'gmpna_54', 'gmpna_55', 'gmpna_56',
                        'gmpna_57','gmpna_58', 'gmpna_59', 'gmpna_60', 'gmpna_61', 'gmpna_62','gmpna_63', 'gmpna_64', 'Pic', 'tabl_msg',
                        'replacement_uso_signal_vv_1', 'replacement_uso_signal_vv_2']
        msg = self.dop_function.column_check(UMPNA, 'umpna', list_default)
        return msg 
# Work with filling in the table 'tmNA_UMPNA'
class Filling_tmNA_UMPNA():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
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
            try:
                if self.dop_function.empty_table('umpna'): 
                    msg[f'{today} - Таблицы: umpna пустая! Заполни таблицу!'] = 2
                    return msg
                self.cursor.execute(f'''SELECT name FROM umpna''')
                for i in self.cursor.fetchall():
                    count_NA += 1
                    if i[0] is None or i[0] == '' or i[0] == ' ':
                        msg[f'{today} - Таблица: umpna, необходимо заполнить название НА!'] = 3
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
                        msg[f'{today} - Таблица: umpna_tm, заполнен НА_{count_NA}'] = 1
                            
                # Checking for the existence of a database
                tmNA_UMPNA.insert_many(list_tmna_umpna).execute()
            except Exception:
                msg[f'{today} - Таблица: umpna_tm, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: umpna_tm, выполнение кода завершено!'] = 1
        return(msg)
    # Заполняем таблицу tmNA_UMPNA
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 
                        'unit', 'used', 'value_ust', 'minimum', 'maximum', 'group_ust', 'rule_map_ust']
        msg = self.dop_function.column_check(tmNA_UMPNA, 'umpna_tm', list_default)
        return msg 
    
# Work with filling in the table 'ZD'
class Filling_ZD():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    # Получаем данные с таблицы AI и DI 
    def getting_modul(self):
        msg = {}
        array_di_tag_zd = ('OKC', 'CKC', 'ODC', 'CDC', 'MC', 'OPC', 'DCK', 'MCO', 'MCC', 'KKCC', 'KKCS', 'EC', 'OFC', 'CFC')
        array_do_tag_zd = ('DOB', 'DKB', 'DCB', 'DCOB', 'DCCB')
        with db:
            try:
                try:
                    if self.dop_function.empty_table('di') or self.dop_function.empty_table('do'): 
                        msg[f'{today} - Таблицы: di или do пустая! Заполни таблицу!'] = 2
                        return msg
                except:
                    msg[f'{today} - Таблицы: di или do пустая! Заполни таблицу!'] = 2
                    return msg
                
                # Новый список задвижек из таблицы DI
                self.cursor.execute(f"""SELECT name 
                                        FROM di
                                        WHERE name LIKE '%задвижк%' OR name LIKE '%Задвижк%' OR 
                                              name LIKE '%клап%' OR name LIKE '%Клап%' OR
                                              name LIKE '%клоп%' OR name LIKE '%КЛОП%'""")
                name_zd_new = self.cursor.fetchall()
                list_zd_name_split = []
                for i in name_zd_new: 
                    list_zd_name_split.append(str(i[0]).split(' - ')[0])
                unique_name = set(list_zd_name_split)

                # Существующий список задвижек из таблицы ZD
                self.cursor.execute(f'''SELECT name FROM zd''')
                name_zd_old = self.cursor.fetchall()
                tabl_zd_name = []
                for i in name_zd_old:
                    tabl_zd_name.append(i[0])

                # Количество строк в таблице
                self.cursor.execute(f'''SELECT COUNT(*) FROM zd''')
                count_row = self.cursor.fetchall()[0][0]
                        
                for name in sorted(unique_name):
                    list_zd = []

                    kvo, kvz, mpo, mpz, mufta, error, dist, vmmo, vmmz = '', '', '', '', '', '', '', '', ''
                    close_bru, stop_bru, voltage, isp_opening_chain, isp_closing_chain   = '', '', '', '', ''
                    open_zd, close_zd, stop_zd, open_stop, close_stop = '', '', '', '', ''

                    for tag in array_di_tag_zd:
                        self.cursor.execute(f"""SELECT id, tag, name 
                                                FROM di
                                                WHERE name LIKE '%{name}%' AND tag LIKE '%{tag}%'""")
                        
                        try   : number_id = self.cursor.fetchall()[0][0]
                        except: continue

                        if tag == 'OKC':   kvo = f'DI[{number_id}].Value'
                        if tag == 'CKC':   kvz = f'DI[{number_id}].Value'
                        if tag == 'ODC':   mpo = f'DI[{number_id}].Value'
                        if tag == 'CDC':   mpz = f'DI[{number_id}].Value'
                        if tag == 'MC' : mufta = f'DI[{number_id}].Value'
                        if tag == 'OPC': error = f'DI[{number_id}].Value'
                        if tag == 'DCK':  dist = f'DI[{number_id}].Value'
                        if tag == 'MCO':  vmmo = f'DI[{number_id}].Value'
                        if tag == 'MCC':  vmmz = f'DI[{number_id}].Value'
                        if tag == 'KKCC': close_bru = f'DI[{number_id}].Value'
                        if tag == 'KKCS': stop_bru  = f'DI[{number_id}].Value'
                        if tag == 'EC' :  voltage = f'DI[{number_id}].Value'
                        if tag == 'OFC':  isp_opening_chain = f'DI[{number_id}].Value'
                        if tag == 'CFC':  isp_closing_chain = f'DI[{number_id}].Value'

                    for tag in array_do_tag_zd:    
                        self.cursor.execute(f"""SELECT id, tag, name 
                                                FROM "do"
                                                WHERE name LIKE '%{name}%' AND tag LIKE '%{tag}%'""")
                        
                        try   : number_id = self.cursor.fetchall()[0][0]
                        except: continue
                        
                        if tag == 'DOB' : open_zd    = f'ctrlDO[{number_id}]'
                        if tag == 'DKB' : close_zd   = f'ctrlDO[{number_id}]'
                        if tag == 'DCB' : stop_zd    = f'ctrlDO[{number_id}]'
                        if tag == 'DCOB': open_stop  = f'ctrlDO[{number_id}]'
                        if tag == 'DCCB': close_stop = f'ctrlDO[{number_id}]'
                    
                    if kvo == '' and kvz == '': continue

                    if self.dop_function.str_find(str(name).lower, {'клапа'}) or self.dop_function.str_find(str(name).lower, {'клоп'}):
                        klapan = '1'
                    else: 
                        klapan = '0'

                    if name in tabl_zd_name:
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.KVO, 'KVO', kvo))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.KVZ, 'KVZ', kvz))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.MPO, 'MPO', mpo))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.MPZ, 'MPZ', mpz))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.Mufta, 'Mufta', mufta))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.Drive_failure, 'Drive_failure', error))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.Dist, 'Dist', dist))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.VMMO, 'VMMO', vmmo))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.VMMZ, 'VMMZ', vmmz))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.Close_BRU, 'Close_BRU', close_bru))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.Stop_BRU, 'Stop_BRU', stop_bru))

                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.Voltage, 'Voltage', voltage))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.Serviceability_opening_circuits, 'Serviceability_opening_circuits', isp_opening_chain))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.Serviceability_closening_circuits, 'Serviceability_closening_circuits', isp_closing_chain))

                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.Open, 'Open', open_zd))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.Close, 'Close', close_zd))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.Stop, 'Stop', stop_zd))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.Opening_stop, 'Opening_stop', open_stop))
                        msg.update(self.dop_function.update_signal_dop(ZD, "zd", name, ZD.Closeing_stop, 'Closeing_stop', close_stop))

                    else:
                        count_row += 1
        
                        msg[f'{today} - Таблица: zd, добавлена новая задвижка: ZD[{count_row}], {name}'] = 1
                        list_zd.append(dict(variable = f'ZD[{count_row}]',
                                            name = name,
                                            short_name = '',
                                            exists_interface = '',
                                            KVO = kvo,
                                            KVZ = kvz,
                                            MPO = mpo,
                                            MPZ = mpz,
                                            Dist = dist,
                                            Mufta = mufta,
                                            Drive_failure = error,
                                            Open = open_zd,
                                            Close = close_zd,
                                            Stop = stop_zd,
                                            Opening_stop = open_stop,
                                            Closeing_stop = close_stop,
                                            KVO_i = '',
                                            KVZ_i = '',
                                            MPO_i = '',
                                            MPZ_i = '',
                                            Dist_i = '',
                                            Mufta_i = '',
                                            Drive_failure_i = '',
                                            Open_i = '',
                                            Close_i = '',
                                            Stop_i = '',
                                            Opening_stop_i = '',
                                            Closeing_stop_i = '',
                                            No_connection = '',
                                            Close_BRU = close_bru,
                                            Stop_BRU = stop_bru,
                                            Voltage = voltage,
                                            Voltage_CHSU = '',
                                            Voltage_in_signaling_circuits = '',
                                            Serviceability_opening_circuits = isp_opening_chain,
                                            Serviceability_closening_circuits = isp_closing_chain,
                                            VMMO = vmmo,
                                            VMMZ = vmmz,
                                            Freeze_on_suspicious_change = '',
                                            Is_klapan = klapan,
                                            Opening_percent = '',
                                            Pic = '',

                                            Type_BUR_ZD = '', tabl_msg='TblValves',
                                            AlphaHMI = '',AlphaHMI_PIC1 = '',AlphaHMI_PIC1_Number_kont = '',
                                            AlphaHMI_PIC2 = '',AlphaHMI_PIC2_Number_kont = '',AlphaHMI_PIC3 = '',
                                            AlphaHMI_PIC3_Number_kont = '',AlphaHMI_PIC4 = '',AlphaHMI_PIC4_Number_kont = ''))

                        # Checking for the existence of a database
                        ZD.insert_many(list_zd).execute()
                if len(msg) == 0: msg[f'{today} - Таблица: zd, обновление завершено, изменений не обнаружено!'] = 1
                
                # Существование ZD в таблице ZD
                for zd in tabl_zd_name:
                    if zd not in unique_name:
                        msg[f'{today} - Таблица: zd, {zd} не существует в таблице DI'] = 3
            except Exception:
                msg[f'{today} - Таблица: zd, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: zd, выполнение кода завершено!'] = 1
        return(msg)
    # Заполняем таблицу ZD
    def column_check(self):
        list_default = ['variable', 'name', 'short_name', 'exists_interface', 'KVO', 'KVZ', 'MPO', 'MPZ', 'Dist',
                        'Mufta', 'Drive_failure', 'Open', 'Close', 'Stop', 'Opening_stop', 'Closeing_stop', 'KVO_i', 'KVZ_i',
                        'MPO_i', 'MPZ_i', 'Dist_i', 'Mufta_i', 'Drive_failure_i', 'Open_i', 'Close_i', 'Stop_i', 'Opening_stop_i',
                        'Closeing_stop_i', 'No_connection', 'Close_BRU', 'Stop_BRU', 'Voltage', 'Voltage_CHSU', 
                        'Voltage_in_signaling_circuits', 'Serviceability_opening_circuits', 'Serviceability_closening_circuits', 'VMMO', 'VMMZ', 
                        'Freeze_on_suspicious_change', 'Is_klapan', 'Opening_percent', 'Pic', 'Type_BUR_ZD', 'tabl_msg',
                        'AlphaHMI', 'AlphaHMI_PIC1', 'AlphaHMI_PIC1_Number_kont', 'AlphaHMI_PIC2',
                        'AlphaHMI_PIC2_Number_kont','AlphaHMI_PIC3', 'AlphaHMI_PIC3_Number_kont', 
                        'AlphaHMI_PIC4', 'AlphaHMI_PIC4_Number_kont']
        msg = self.dop_function.column_check(ZD, 'zd', list_default)
        return msg 
# Work with filling in the table 'ZD_tm'
class Filling_ZD_tm():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    # Получаем данные с таблицы ZD 
    def getting_modul(self):
        msg = {}
        count_ZD = 0
        list_zd_tm = []
        time_ust = [('Время переходных процессов' , 'T1', '500', 'мс'), 
                    ('Ожидание прихода сигнала от МП после команды на открытие/закрытие', 'T2', '2', 'c'),
                    ('Время схода с КВЗ/КВО', 'T3', '10', 'c'),
                    ('Время хода вала', 'T4', '60', 'c'),
                    ('Время на отключение МП в крайних положениях', 'T5', '2', 'c'),
                    ('Время на возврат напряжения при стопе по месту', 'T6', '3', 'c'),
                    ('Время выполнения команды на открытие при имитации задвижки', 'T7', '20', 'c'),
                    ('Время на подачу команды СТОП', 'T8', '2', 'c'),
                    ('Время на ожидание возврата концевиков после команды стоп', 'T9', '1', 'c'),
                    ('Время на выполнение команд с БРУ', 'T10', '3', 'c'),
                    ('Время на проверку несправности цепей включения', 'T11', '2', 'c'),
                    ('Время на проверку несправности цепей отключения', 'T12', '2', 'c'),
                    ('Время рассогласования между сигналами по физическому и интерфейсному каналу', 'T13', '2', 'c'),
                    ('Время на задержку при подозрительных переходах', 'T14', '2', 'c'),
                    ('Резерв', 'T15', '0', 'c')] 
        with db:
            try:
                if self.dop_function.empty_table('zd'): 
                    msg[f'{today} - Таблицы: zd пустая! Заполни таблицу!'] = 2
                    return msg
                
                self.cursor.execute(f'''SELECT name FROM zd''')
                for i in self.cursor.fetchall():
                    count_ZD += 1
                    for ust in time_ust:
                        used = '0' if ust[0] == 'Резерв' else '1' 
                        list_zd_tm.append(dict(variable = '',
                                            tag  = f'HZD{count_ZD}_{ust[1]}',
                                            name = f'{i[0]}. {ust[0]}',
                                            unit = ust[3],
                                            used = used,
                                            value_ust = f'{ust[2]}',
                                            minimum = '0',
                                            maximum = '65535',
                                            group_ust = 'Временные уставки задвижек',
                                            rule_map_ust = 'Временные уставки'))
                            
                # Checking for the existence of a database
                ZD_tm.insert_many(list_zd_tm).execute()
            except Exception:
                msg[f'{today} - Таблица: zd_tm, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: zd_tm, выполнение кода завершено!'] = 1
        return(msg)
    # Заполняем таблицу zd_tm
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'unit', 'used', 
                        'value_ust', 'minimum', 'maximum', 'group_ust', 'rule_map_ust']
        msg = self.dop_function.column_check(ZD_tm, 'zd_tm', list_default)
        return msg 
    
# Work with filling in the table 'VS'
class Filling_VS():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    # Получаем данные с таблицы AI и DI 
    def getting_modul(self):
        msg = {}
        array_di_tag_vs = ('MPC', 'EC')
        array_do_tag_vs = ('ABB', 'ABO')
        array_tag_opc_vs = ('авар', 'Авар', 'исправн', 'Исправн')

        with db:
            try:
                try:
                    if self.dop_function.empty_table('di') or self.dop_function.empty_table('do'): 
                        msg[f'{today} - Таблицы: di или do пустая! Заполни таблицу!'] = 2
                        return msg
                except:
                    msg[f'{today} - Таблицы: di или do пустая! Заполни таблицу!'] = 2
                    return msg
                
                # Новый список вспомсистем из таблицы DI
                self.cursor.execute(f"""SELECT tag, name 
                                        FROM di
                                        WHERE tag LIKE '%MPC%'""")
                vs_name = self.cursor.fetchall()
                list_vs_name_split = []
                for i in vs_name: 
                    if   self.dop_function.str_find(i[1], {'- сигнал от МП'}):
                        list_vs_name_split.append(str(i[1]).split('- сигнал от МП')[0])
                    elif self.dop_function.str_find(i, {'-сигнал от МП'}):
                        list_vs_name_split.append(str(i[1]).split('-сигнал от МП')[0])
                    elif self.dop_function.str_find(i, {'- включен'}):
                        list_vs_name_split.append(str(i[1]).split('- включен')[0])
                    elif self.dop_function.str_find(i, {'-включен'}):
                        list_vs_name_split.append(str(i[1]).split('-включен')[0])
                    elif self.dop_function.str_find(i, {'.Включен'}):
                        list_vs_name_split.append(str(i[1]).split('.Включен')[0])
                    elif self.dop_function.str_find(i, {'. Включен'}):
                        list_vs_name_split.append(str(i[1]).split('. Включен')[0])
                unique_name = set(list_vs_name_split)

                # Существующий список вспомсистем из таблицы VS
                self.cursor.execute(f'''SELECT name FROM vs''')
                exists_vs = self.cursor.fetchall()
                tabl_vs_name = []
                for i in exists_vs:
                    tabl_vs_name.append(i[0])

                # Количество строк в таблице
                self.cursor.execute(f'''SELECT COUNT(*) FROM vs''')
                count_row = self.cursor.fetchall()[0][0]
                        
                for name in sorted(unique_name):
                    list_vs = []
                    mp, voltage, isp_opening_chain, open_vs, close_vs, error = '', '', '', '', '', ''

                    # Принадлежность OPC тега
                    for tag in array_tag_opc_vs:  
                        self.cursor.execute(f"""SELECT id, tag, name 
                                                FROM di
                                                WHERE name LIKE '%{name}%' AND name LIKE '%{tag}%' AND tag LIKE '%OPC%'""")
                        
                        try   : number_id = self.cursor.fetchall()[0][0]
                        except: continue

                        if tag == 'авар': 
                            error = f'DI[{number_id}].Value'
                        elif tag == 'Авар' : 
                            error = f'DI[{number_id}].Value'
                        elif tag == 'исправн' : 
                            isp_opening_chain = f'DI[{number_id}].Value'
                        elif tag == 'Исправн' : 
                            isp_opening_chain = f'DI[{number_id}].Value'

                    for tag in array_di_tag_vs:
                        self.cursor.execute(f"""SELECT id, tag, name
                                                FROM di
                                                WHERE name LIKE '%{name}%' AND tag LIKE '%{tag}%'""")
                        
                        try   : number_id = self.cursor.fetchall()[0][0]
                        except: continue

                        if tag == 'MPC': mp      = f'DI[{number_id}].Value'
                        if tag == 'EC' : voltage = f'DI[{number_id}].Value'
                        
                    for tag in array_do_tag_vs:    
                        self.cursor.execute(f"""SELECT id, tag, name 
                                                FROM "do"
                                                WHERE name LIKE '%{name}%' AND tag LIKE '%{tag}%'""")
                        
                        try   : number_id = self.cursor.fetchall()[0][0]
                        except: continue
                        
                        if tag == 'ABB': open_vs  = f'ctrlDO[{number_id}]'
                        if tag == 'ABO': close_vs = f'ctrlDO[{number_id}]'

                    # Давление на выходе
                    new_name = str(name).strip()
                    new_name = str(new_name).replace('ой', 'ом')
                    new_name = str(new_name).replace('сос', 'соса')
                    new_name = str(new_name).replace('ой', 'ого')
                    new_name = str(new_name).replace('ый', 'ом')
                    new_name = str(new_name).replace('ор', 'оре')
                    new_name = str(new_name).replace('ель', 'еля')
                    new_name = str(new_name).replace('Нас', 'нас')
                    new_name = str(new_name).replace('Масл', 'масл')
                    new_name = str(new_name).replace('Погр', 'погр')
                    new_name = str(new_name).replace('Подп', 'подп')
                    new_name = str(new_name).replace('Прит', 'прит')
                    new_name = str(new_name).replace('Вытяж', 'вытяж')

                    self.cursor.execute(f"""SELECT id, name 
                                            FROM ai
                                            WHERE name LIKE '%{new_name}%'""")
                    try: 
                        number_id = self.cursor.fetchall()[0][0]
                        pressure_norm = f'AI[{number_id}].Norm'
                        pressure_ndv  = f'AI[{number_id}].Ndv'
                    except:
                        pressure_norm = f''
                        pressure_ndv  = f''

                    if name in tabl_vs_name:
                        msg.update(self.dop_function.update_signal_dop(VS, "vs", name, VS.MP, 'MP', mp))
                        msg.update(self.dop_function.update_signal_dop(VS, "vs", name, VS.Voltage, 'Voltage', voltage))
                        msg.update(self.dop_function.update_signal_dop(VS, "vs", name, VS.Serviceability_of_circuits_of_inclusion, 'Serviceability_of_circuits_of_inclusion', isp_opening_chain))
                        msg.update(self.dop_function.update_signal_dop(VS, "vs", name, VS.External_alarm, 'External_alarm', error))

                        msg.update(self.dop_function.update_signal_dop(VS, "vs", name, VS.VKL, 'VKL', open_vs))
                        msg.update(self.dop_function.update_signal_dop(VS, "vs", name, VS.OTKL, 'OTKL', close_vs))

                        msg.update(self.dop_function.update_signal_dop(VS, "vs", name, VS.Pressure_is_True, 'Pressure_is_True', pressure_norm))
                        msg.update(self.dop_function.update_signal_dop(VS, "vs", name, VS.Pressure_sensor_defective, 'Pressure_sensor_defective', pressure_ndv))

                    else:
                        count_row += 1
                        
                        msg[f'{today} - Таблица: vs, добавлена новая вспомсистема: VS[{count_row}], {name}'] = 1
                        list_vs.append(dict(variable = f'ZD[{count_row}]',
                                            name = name,
                                            short_name = '',
                                            group = '',
                                            number_in_group = '',
                                            MP = mp,
                                            Pressure_is_True = pressure_norm,
                                            Voltage = voltage,
                                            Voltage_Sch = '',
                                            Serviceability_of_circuits_of_inclusion = isp_opening_chain,
                                            External_alarm = error,
                                            Pressure_sensor_defective = pressure_ndv,
                                            VKL = open_vs,
                                            OTKL = close_vs,
                                            Not_APV = '0',
                                            Pic = '',
                                            table_msg = 'TblAuxSyses',
                                            Is_klapana_interface_auxsystem = '0',
                                            
                                            AlphaHMI = '',AlphaHMI_PIC1 = '',AlphaHMI_PIC1_Number_kont = '',
                                            AlphaHMI_PIC2 = '',AlphaHMI_PIC2_Number_kont = '',AlphaHMI_PIC3 = '',
                                            AlphaHMI_PIC3_Number_kont = '',AlphaHMI_PIC4 = '',AlphaHMI_PIC4_Number_kont = ''))

                        # Checking for the existence of a database
                        VS.insert_many(list_vs).execute()
                if len(msg) == 0: msg[f'{today} - Таблица: vs, обновление завершено, изменений не обнаружено!'] = 1
                
                # Существование вспомсистемы в таблице VS
                for vs in tabl_vs_name:
                    if vs not in unique_name:
                        msg[f'{today} - Таблица: vs, {vs} не существует в таблице DI'] = 3
            except Exception:
                msg[f'{today} - Таблица: vs, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: vs, выполнение кода завершено!'] = 1
        return(msg)
    # Заполняем таблицу VS
    def column_check(self):
        list_default = ['variable', 'name', 'short_name', 'group', 'number_in_group', 'MP', 'Pressure_is_True', 'Voltage', 'Voltage_Sch', 
                        'Serviceability_of_circuits_of_inclusion', 'External_alarm', 'Pressure_sensor_defective', 'VKL', 'OTKL', 'Not_APV',
                        'Pic', 'table_msg', 'Is_klapana_interface_auxsystem',
                        'AlphaHMI', 'AlphaHMI_PIC1', 'AlphaHMI_PIC1_Number_kont', 'AlphaHMI_PIC2',
                        'AlphaHMI_PIC2_Number_kont','AlphaHMI_PIC3', 'AlphaHMI_PIC3_Number_kont', 
                        'AlphaHMI_PIC4', 'AlphaHMI_PIC4_Number_kont']
        msg = self.dop_function.column_check(VS, 'vs', list_default)
        return msg 
# Work with filling in the table 'VS_tm'
class Filling_VS_tm():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    # Получаем данные с таблицы VS
    def getting_modul(self):
        msg = {}
        count_VS = 0
        list_vs_tm = []

        time_ust = [('Выдержка времени на ожидание срабатывания / исчезновения МП после включения / отключения' , 'T1', '2', 'с'), 
                    ('Выдержка времени на ожидание набора давления после появления сигнала МП в процессе пуска агрегата вспомсистемы', 'T2', '10', 'c'),
                    ('Выдержка времени на ожидание спада давления после снятия сигнала МП в процессе остановки агрегата вспомсистемы', 'T3', '5', 'c'),
                    ('Выдержка времени на возврат напряжения при стопе по месту', 'T4', '3', 'c'),
                    ('Выдержка времени на контроль давления во время работы', 'T5', '5', 'c'),
                    ('Выдержка времени для перевода неработающего агрегата вспомсистемы в режим ремонтный при исчезновении напряжения в схеме управления', 'T6', '40', 'c'),
                    ('Выдержка времени на запаздывание сигналов исчезновения МП и сигнала наличия напряжения от СШ (при кратковременных исчезновениях напряжения на секции шин)', 'T7', '0', 'c'),
                    ('Выдержка времени на перевод пожарного насоса в ремонтный режим при неисправности цепей включения', 'T8', '40', 'c')] 
        with db:
            try:
                if self.dop_function.empty_table('vs'): 
                    msg[f'{today} - Таблицы: vs пустая! Заполни таблицу!'] = 2
                    return msg
                
                self.cursor.execute(f'''SELECT name FROM vs''')
                for i in self.cursor.fetchall():
                    count_VS += 1
                    for ust in time_ust:
                        used = '0' if ust[0] == 'Резерв' else '1' 
                        list_vs_tm.append(dict(variable = '',
                                            tag  = f'HVS{count_VS}_{ust[1]}',
                                            name = f'{i[0]}. {ust[0]}',
                                            unit = ust[3],
                                            used = used,
                                            value_ust = f'{ust[2]}',
                                            minimum = '0',
                                            maximum = '65535',
                                            group_ust = 'Временные уставки вспомсистем',
                                            rule_map_ust = 'Временные уставки'))
                            
                # Checking for the existence of a database
                VS_tm.insert_many(list_vs_tm).execute()
            except Exception:
                msg[f'{today} - Таблица: vs_tm, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: vs_tm, выполнение кода завершено!'] = 1
        return(msg)
    # Заполняем таблицу vs_tm
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'unit', 'used', 
                        'value_ust', 'minimum', 'maximum', 'group_ust', 'rule_map_ust']
        msg = self.dop_function.column_check(VS_tm, 'vs_tm', list_default)
        return msg 
# Work with filling in the table 'VSGRP'
class Filling_VSGRP():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    # Заполняем таблицу VSGRP
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'fire_or_watering', 'Number_of_auxsystem_in_group',
                        'WarnOff_flag_if_one_auxsystem_in_the_group_is_running']
        msg = self.dop_function.column_check(VSGRP, 'vsgrp', list_default)
        return msg 
# Work with filling in the table 'VSGRP_tm'
class Filling_VSGRP_tm():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    # Получаем данные с таблицы VS
    def getting_modul(self):
        msg = {}
        count_VSGRP = 0
        list_vsgrp_tm = []

        time_ust = [('Выдержка времени на выполнение АПВ' , 'T1', '1', 'с')] 
        with db:
            if self.dop_function.empty_table('vs'): 
                msg[f'{today} - Таблицы: VSGRP пустая! Заполни таблицу!'] = 2
                return msg
            
            self.cursor.execute(f'''SELECT name FROM vsgrp''')
            for i in self.cursor.fetchall():
                count_VSGRP += 1
                for ust in time_ust:
                    used = '0' if ust[0] == 'Резерв' else '1' 
                    list_vsgrp_tm.append(dict(variable = '',
                                              tag  = f'HVSGRP{count_VSGRP}_{ust[1]}',
                                              name = f'{i[0]}. {ust[0]}',
                                              unit = ust[3],
                                              used = used,
                                              value_ust = f'{ust[2]}',
                                              minimum = '0',
                                              maximum = '65535',
                                              group_ust = 'Временные уставки вспомсистем',
                                              rule_map_ust = 'Временные уставки'))
                        
            # Checking for the existence of a database
            VSGRP_tm.insert_many(list_vsgrp_tm).execute()
        msg[f'{today} - Таблица: vsgrp_tm, выполнение кода завершено!'] = 1
        return(msg)
    # Заполняем таблицу vsgrp_tm
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'unit', 'used', 
                        'value_ust', 'minimum', 'maximum', 'group_ust', 'rule_map_ust']
        msg = self.dop_function.column_check(VSGRP_tm, 'vsgrp_tm', list_default)
        return msg 
    
# Work with filling in the table 'UTS'
class Filling_UTS():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    # Получаем данные с таблицы AI и DI 
    def getting_modul(self, bool_uts_upts):
        if bool_uts_upts: 
            tabl_used  = 'upts'
            model_used = UPTS
            variable   = 'UPTS' 
        else:
            tabl_used  = 'uts'
            model_used = UTS
            variable   = 'UTS' 

        msg = {}
        list_uts = []
        with db:
            try:
                try:
                    if self.dop_function.empty_table('do'): 
                        msg[f'{today} - Таблица: do пустая! Заполни таблицу!'] = 2
                        return msg
                except:
                    msg[f'{today} - Таблица: do пустая! Заполни таблицу!'] = 2
                    return msg
                
                # Новый список из таблицы DI
                self.cursor.execute(f"""SELECT id, tag, name, uso, basket, module, channel
                                        FROM "do"
                                        WHERE (name LIKE '%Табл%' AND tag LIKE '%BB%')  OR
                                              (name LIKE '%Сирен%' AND tag LIKE '%BB%') OR
                                              (name LIKE '%Звон%' AND tag LIKE '%BB%')  OR
                                              (name LIKE '%табл%' AND tag LIKE '%BB%')  OR
                                              (name LIKE '%сирен%' AND tag LIKE '%BB%') OR
                                              (name LIKE '%звон%' AND tag LIKE '%BB%') OR
                                              (name LIKE '%ОТВ%' OR name LIKE '%отв%') OR
                                              (name LIKE '%сигнализац%')
                                        ORDER BY tag""")
                list_uts_do = self.cursor.fetchall()
                # Количество строк в таблице
                self.cursor.execute(f"""SELECT COUNT(*) FROM {tabl_used}""")
                count_row = self.cursor.fetchall()[0][0]

                for uts_do in list_uts_do:

                    coincidence = model_used.select().where(model_used.uso     == uts_do[3],
                                                            model_used.basket  == uts_do[4],
                                                            model_used.module  == uts_do[5],
                                                            model_used.channel == uts_do[6])
                    if bool(coincidence):
                        exist_vkl  = model_used.select().where(model_used.VKL  == f'ctrlDO[{uts_do[0]}]')
                        exist_tag  = model_used.select().where(model_used.tag  == uts_do[1])
                        exist_name = model_used.select().where(model_used.name == uts_do[2])

                        if not bool(exist_vkl):
                            self.cursor.execute(f"""SELECT id, tag 
                                                    FROM "do"
                                                    WHERE uso='{uts_do[3]}' AND 
                                                          basket={uts_do[4]} AND 
                                                          module={uts_do[5]} AND 
                                                          channel={uts_do[6]}""")
                            for id_, vkl_ in self.cursor.fetchall():
                                msg[f'{today} - Таблица: {tabl_used}, у сигнала в таблице do обновлена команда включить: id = {id_}, ({vkl_}) ctrlDO[{uts_do[0]}]'] = 3
                            self.cursor.execute(f"""UPDATE {tabl_used}
                                                    SET "VKL"='ctrlDO[{uts_do[0]}]'
                                                    WHERE uso='{uts_do[3]}' AND 
                                                          basket={uts_do[4]} AND 
                                                          module={uts_do[5]} AND 
                                                          channel={uts_do[6]}""")

                        if not bool(exist_tag):
                            self.cursor.execute(f"""SELECT id, tag 
                                                    FROM "do"
                                                    WHERE uso='{uts_do[3]}' AND 
                                                          basket={uts_do[4]} AND 
                                                          module={uts_do[5]} AND 
                                                          channel={uts_do[6]}""")
                            for id_, tag_ in self.cursor.fetchall():
                                msg[f'{today} - Таблица: {tabl_used}, у сигнала в таблице do обновлен tag: id = {id_}, ({tag_}) {uts_do[1]}'] = 3
                            self.cursor.execute(f"""UPDATE {tabl_used}
                                                    SET "tag"='{uts_do[1]}' 
                                                    WHERE uso='{uts_do[3]}' AND 
                                                          basket={uts_do[4]} AND 
                                                          module={uts_do[5]} AND 
                                                          channel={uts_do[6]}""")

                        if not bool(exist_name):
                            self.cursor.execute(f"""SELECT id, name 
                                                    FROM "do"
                                                    WHERE uso='{uts_do[3]}' AND 
                                                          basket={uts_do[4]} AND 
                                                          module={uts_do[5]} AND 
                                                          channel={uts_do[6]}""")
                            for id_, name_ in self.cursor.fetchall():
                                msg[f'{today} - Таблица: {tabl_used}, у сигнала в таблице do обновлено name: id = {id_}, ({uts_do[1]}), {uts_do[2]}'] = 3
                            self.cursor.execute(f"""UPDATE {tabl_used}
                                                    SET "name"='{uts_do[2]}' 
                                                    WHERE uso='{uts_do[3]}' AND 
                                                          basket={uts_do[4]} AND 
                                                          module={uts_do[5]} AND 
                                                          channel={uts_do[6]}""")
                        continue
                    count_row += 1
                    msg[f'{today} - Таблица: {tabl_used}, добавлен новый сигнал: id = {uts_do[0]}, ({uts_do[1]}), {uts_do[2]}'] = 1
                    siren = '1' if (self.dop_function.str_find(uts_do[2], {'сирен'}) or self.dop_function.str_find(uts_do[2], {'Cирен'})) else '0' 
                    list_uts.append(dict(variable = f'{variable}[{count_row}]',
                                         tag = f'{uts_do[1]}',
                                         name = f'{uts_do[2]}',
                                         location = '',
                                         VKL = f'ctrlDO[{uts_do[0]}]',
                                         siren = siren, 
                                         Does_not_require_autoshutdown = '0', 
                                         Serviceability_of_circuits_of_inclusion = '',
                                         Examination = '', 
                                         Kvit = '',
                                         Pic = '',
                                         number_list_VU = '',
                                         order_number_for_VU = '', 
                                         uso = f'{uts_do[3]}', 
                                         basket = f'{uts_do[4]}', 
                                         module = f'{uts_do[5]}', 
                                         channel = f'{uts_do[6]}'))

                # Checking for the existence of a database
                model_used.insert_many(list_uts).execute()
            except Exception:
                msg[f'{today} - Таблица: {tabl_used}, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: {tabl_used}, выполнение кода завершено!'] = 1
        return(msg)
    # Заполняем таблицу UTS
    def column_check(self, bool_uts_upts):
        list_default = ['variable', 'tag', 'name', 'location', 'VKL', 'Serviceability_of_circuits_of_inclusion', 'siren', 'Does_not_require_autoshutdown', 'Examination',
                        'Kvit', 'Pic', 'number_list_VU', 'order_number_for_VU', 'uso', 'basket', 'module', 'channel']
        if bool_uts_upts:
            msg = self.dop_function.column_check(UPTS, 'upts', list_default)
        else:
            msg = self.dop_function.column_check(UTS, 'uts', list_default)
        return msg 
# Work with filling in the table 'UTS_tm'
class Filling_UTS_tm():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    # Получаем данные с таблицы UTS_tm
    def getting_modul(self):
        msg = {}
        count_UTS = 0
        list_uts_tm = []

        time_ust = [('Время непрерывной работы' , 'T1', '1', 'с'), 
                    ('Время паузы работы', 'T2', '1', 'c')] 
        with db:
            try:
                if self.dop_function.empty_table('uts'): 
                    msg[f'{today} - Таблицы: uts пустая! Заполни таблицу!'] = 2
                    return msg
                
                self.cursor.execute(f'''SELECT name FROM uts''')
                for i in self.cursor.fetchall():
                    count_UTS += 1
                    for ust in time_ust:
                        used = '0' if ust[0] == 'Резерв' else '1' 
                        list_uts_tm.append(dict(variable = '',
                                                tag  = f'HUTS[{count_UTS}]_{ust[1]}',
                                                name = f'{i[0]}. {ust[0]}',
                                                unit = ust[3],
                                                used = used,
                                                value_ust = f'{ust[2]}',
                                                minimum = '0',
                                                maximum = '65535',
                                                group_ust = 'Временные уставки сирен и табло',
                                                rule_map_ust = 'Временные уставки'))
                            
                # Checking for the existence of a database
                UTS_tm.insert_many(list_uts_tm).execute()
            except Exception:
                msg[f'{today} - Таблица: uts_tm, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: uts_tm, выполнение кода завершено!'] = 1
        return(msg)
    # Заполняем таблицу uts_tm
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'unit', 'used', 
                        'value_ust', 'minimum', 'maximum', 'group_ust', 'rule_map_ust']
        msg = self.dop_function.column_check(UTS_tm, 'uts_tm', list_default)
        return msg 

# Work with filling in the table 'VV'
class Filling_VV():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    # Получаем данные с таблицы DI 
    def getting_modul(self):
        msg = {}
        list_vv = []
        with db:
            try:
                try:
                    if self.dop_function.empty_table('di'): 
                        msg[f'{today} - Таблица: di пустая! Заполни таблицу!'] = 2
                        return msg
                except:
                    msg[f'{today} - Таблица: di пустая! Заполни таблицу!'] = 2
                    return msg
                
                # Cписок ВВ из таблицы DI
                self.cursor.execute(f'''SELECT id, tag, name
                                        FROM di
                                        WHERE (name LIKE '%ввода%' AND tag LIKE '%MBC%') OR
                                              (name LIKE '%СВВ%' AND tag LIKE '%MBC%') OR
                                              (name LIKE '%ССВ%' AND tag LIKE '%MBC%')''')
                list_vv_di = self.cursor.fetchall()

                # Существующий список из таблицы VV
                self.cursor.execute(f'''SELECT name FROM vv''')
                name_vv_old = self.cursor.fetchall()
                tabl_vv_name = []
                for i in name_vv_old:
                    tabl_vv_name.append(i[0])

                # Количество строк в таблице
                self.cursor.execute(f'''SELECT COUNT(*) FROM vv''')
                count_row = self.cursor.fetchall()[0][0]
                
                # Короткое имя
                list_name_vv = []
                for vv_di in list_vv_di:
                    name_vv = vv_di[2]

                    if self.dop_function.str_find(name_vv, {'включ'}) : name = str(name_vv).replace('включен', '')
                    if self.dop_function.str_find(name_vv, {'отключ'}): name = str(name_vv).replace('отключен', '')
                    
                    try   : list_name_vv.append(str(name).split('.')[1].strip())
                    except: list_name_vv.append(str(name))
                set_name_vv = set(list_name_vv)

                for set_name in sorted(set_name_vv):
                    vkl_vv  = ''
                    otkl_vv = ''
                    self.cursor.execute(f"""SELECT id, name
                                            FROM di
                                            WHERE name LIKE '%{set_name}%'""")
                    list_vv_signals = self.cursor.fetchall()
                    for signal in list_vv_signals:
                        id_vv   = signal[0]
                        name_vv = signal[1]
                    
                        if self.dop_function.str_find(name_vv, {'включ'}) : vkl_vv  = f'DI[{id_vv}].Value'
                        if self.dop_function.str_find(name_vv, {'отключ'}): otkl_vv = f'DI[{id_vv}].Value'

                    if set_name in tabl_vv_name:
                        msg.update(self.dop_function.update_signal_dop(VV, "vv", set_name, VV.VV_vkl, 'VV_vkl', vkl_vv))
                        msg.update(self.dop_function.update_signal_dop(VV, "vv", set_name, VV.otkl_vv, 'otkl_vv', otkl_vv))
                    else:
                        msg[f'{today} - Таблица: vv, добавлен новый сигнал: id = {id_vv}, {name_vv}'] = 3
                        count_row += 1
                        list_vv.append(dict(variable = f'VV[{count_row}]',
                                            name = set_name,
                                            VV_vkl  = vkl_vv,
                                            VV_otkl = otkl_vv,
                                            Pic = ''))

                # Checking for the existence of a database
                VV.insert_many(list_vv).execute()
                msg[f'{today} - Таблица: vv заполнена'] = 1
            except Exception:
                 msg[f'{today} - Таблица: vv, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: vv, выполнение кода завершено!'] = 1
        return(msg)
    # Заполняем таблицу VV
    def column_check(self):
        list_default = ['variable', 'name', 'VV_vkl', 'VV_otkl', 'Pic']
        msg = self.dop_function.column_check(VV, 'vv', list_default)
        return msg 

# Work with filling in the table 'PI'
class Filling_PI():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    # Получаем данные с таблицы AI и DI 
    def getting_modul(self):
        msg = {}
        list_pi = []
        with db:
            try:
                try:
                    if self.dop_function.empty_table('ai'): 
                        msg[f'{today} - Таблица: ai пустая! Заполни таблицу!'] = 2
                        return msg
                except:
                    msg[f'{today} - Таблица: ai пустая! Заполни таблицу!'] = 2
                    return msg
                
                # Новый список из таблицы DI
                self.cursor.execute(f"""SELECT id, tag, name
                                        FROM ai
                                        WHERE (name LIKE '%адрес%' AND name LIKE '%пусков%') OR
                                              (name LIKE '%пожар%' AND name LIKE '%дымов%')  OR
                                              (name LIKE '%теплов%') 
                                        ORDER BY tag""")
                list_pi_ai = self.cursor.fetchall()

                # Существующий список из таблицы PI
                self.cursor.execute(f'''SELECT name FROM pi''')
                name_pi_old = self.cursor.fetchall()
                tabl_pi_name = []
                for i in name_pi_old:
                    tabl_pi_name.append(i[0])

                # Количество строк в таблице
                self.cursor.execute(f'''SELECT COUNT(*) FROM pi''')
                count_row = self.cursor.fetchall()[0][0]

                for new_list_pi in list_pi_ai:
                    number_ai = new_list_pi[0]
                    tag_ai    = new_list_pi[1]
                    name_ai   = new_list_pi[2]

                    # Type PI
                    if self.dop_function.str_find(name_ai, {'адресн'}) : type_pi  = '4'
                    elif self.dop_function.str_find(name_ai, {'дымов'}): type_pi  = '3'
                    elif self.dop_function.str_find(name_ai, {'теплов'}): type_pi  = '5'
                    else: type_pi = ''
                    # Attention
                    if self.dop_function.str_find(name_ai, {'шле'}) or self.dop_function.str_find(name_ai, {'шлейф'}): 
                        attention  = f'stateAI[{number_ai}].state.reg'
                    else: 
                        attention = ''
                    # Reset
                    try:
                        self.cursor.execute(f"""SELECT id, tag
                                                FROM "do"
                                                WHERE tag LIKE '%{tag_ai}%'""")
                        list_pi_do = self.cursor.fetchall()
                        ctrl_DO = f'ctrlDO[{list_pi_do[0][0]}]'
                    except Exception:
                        ctrl_DO = ''

                    fire_0  = f'stateAI[{number_ai}].state.reg'
                    fault_1 = f'stateAI[{number_ai}].state.reg'
                    fault_2 = f'stateAI[{number_ai}].state.reg'

                    if name_ai in tabl_pi_name:
                        msg.update(self.dop_function.update_signal_dop(PI, "pi", name_ai, PI.tag, 'tag', tag_ai))
                        msg.update(self.dop_function.update_signal_dop(PI, "pi", name_ai, PI.name, 'name', name_ai))
                        msg.update(self.dop_function.update_signal_dop(PI, "pi", name_ai, PI.Type_PI, 'Type_PI', type_pi))
                        msg.update(self.dop_function.update_signal_dop(PI, "pi", name_ai, PI.Fire_0, 'Fire_0', fire_0))
                        msg.update(self.dop_function.update_signal_dop(PI, "pi", name_ai, PI.Attention_1, 'Attention_1', attention))
                        msg.update(self.dop_function.update_signal_dop(PI, "pi", name_ai, PI.Fault_1_glass_pollution_broken_2, 'Fault_1_glass_pollution_broken_2', fault_1))
                        msg.update(self.dop_function.update_signal_dop(PI, "pi", name_ai, PI.Fault_2_fault_KZ_3, 'Fault_2_fault_KZ_3', fault_2))
                        msg.update(self.dop_function.update_signal_dop(PI, "pi", name_ai, PI.Reset_Link, 'Reset_Link', ctrl_DO))
                    else:
                        msg[f'{today} - Таблица: pi, добавлен новый сигнал: id = {number_ai}, {name_ai}'] = 3
                        count_row += 1
                        list_pi.append(dict(variable = f'PI[{count_row}]',
                                            tag = tag_ai,
                                            name = name_ai,
                                            Type_PI = type_pi,
                                            Fire_0 = f'stateAI[{number_ai}].state.reg',
                                            Attention_1 = attention,
                                            Fault_1_glass_pollution_broken_2 = f'stateAI[{number_ai}].state.reg',
                                            Fault_2_fault_KZ_3 = f'stateAI[{number_ai}].state.reg',
                                            Yes_connection_4 = '',
                                            Frequency_generator_failure_5 = '',
                                            Parameter_loading_error_6 = '',
                                            Communication_error_module_IPP_7 = '',
                                            Supply_voltage_fault_8 = '',
                                            Optics_contamination_9 = '',
                                            IK_channel_failure_10 = '',
                                            UF_channel_failure_11 = '',
                                            Loading_12 = '',
                                            Test_13 = '',
                                            Reserve_14 = '',
                                            Reset_Link = ctrl_DO,
                                            Reset_Request = '0',
                                            Through_loop_number_for_interface = '0',
                                            location = '',
                                            Pic = '',
                                            Normal = ''))

                # Checking for the existence of a database
                PI.insert_many(list_pi).execute()
                if len(msg) == 0: msg[f'{today} - Таблица: pi, обновление завершено, изменений не обнаружено!'] = 1
            except Exception:
                msg[f'{today} - Таблица: pi, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: pi, выполнение кода завершено!'] = 1
        return(msg)
    # Заполняем таблицу VS
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'Type_PI', 'Fire_0', 'Attention_1', 'Fault_1_glass_pollution_broken_2', 
                        'Fault_2_fault_KZ_3', 'Yes_connection_4', 'Frequency_generator_failure_5', 
                        'Parameter_loading_error_6', 'Communication_error_module_IPP_7', 'Supply_voltage_fault_8', 'Optics_contamination_9',
                        'IK_channel_failure_10', 'UF_channel_failure_11', 'Loading_12', 'Test_13', 'Reserve_14',
                        'Reset_Link', 'Reset_Request', 'Through_loop_number_for_interface', 'location', 'Pic','Normal']
        msg = self.dop_function.column_check(PI, 'pi', list_default)
        return msg 
    
# Work with filling in the table 'PZ_tm'
class Filling_PZ_tm():
    def __init__(self):
        self.cursor   = db.cursor()
        self.dop_function = General_functions()
    # Получаем данные с таблицы PZ_tm
    def getting_modul(self):
        msg = {}
        count_PZ = 0
        list_pz_tm = []

        time_ust = [('Задержка атаки' , 'T1', '10', 'с'), 
                    ('Задержка на возникновение запроса об остановке тушения', 'T2', '30', 'c'),
                    ('Длительность атаки', 'T3', '60', 'c'),
                    ('Контроль процесса пуска тушения', 'T4', '20', 'c'),
                    ('Контроль процесса останова тушения', 'T5', '20', 'c'),
                    ('Инерционность системы', 'T6', '50', 'c'),
                    ('Задержка включения насосов с момента окончания задержки атаки', 'T7', '0', 'c'),
                    ('Выдержка времения на включение следующего насоса при включении нескольких насосов', 'T8', '10', 'c'),
                    ('Задержка открытия задвижек с момента окончания задержки атаки', 'T9', '10', 'c'),] 
        with db:
            try:                
                try:
                    if self.dop_function.empty_table('pz'): 
                        msg[f'{today} - Таблица: pz пустая или не существует! Заполни таблицу!'] = 2
                        return msg
                except:
                    msg[f'{today} - Таблица: pz пустая или не существует!'] = 2
                    return msg
                
                self.cursor.execute(f'''SELECT name FROM pz''')
                for i in self.cursor.fetchall():
                    count_PZ += 1
                    for ust in time_ust:
                        used = '0' if ust[0] == 'Резерв' else '1' 
                        list_pz_tm.append(dict(variable = '',
                                                tag  = f'HUTS[{count_PZ}]_{ust[1]}',
                                                name = f'{i[0]}. {ust[0]}',
                                                unit = ust[3],
                                                used = used,
                                                value_ust = f'{ust[2]}',
                                                minimum = '0',
                                                maximum = '65535',
                                                group_ust = 'Временные уставки пожарных зон',
                                                rule_map_ust = 'Временные уставки'))
                            
                # Checking for the existence of a database
                PZ_tm.insert_many(list_pz_tm).execute()
            except Exception:
                msg[f'{today} - Таблица: pz_tm, ошибка при заполнении: {traceback.format_exc()}'] = 2
            msg[f'{today} - Таблица: pz_tm, выполнение кода завершено!'] = 1
        return(msg)
    # Заполняем таблицу pz_tm
    def column_check(self):
        list_default = ['variable', 'tag', 'name', 'unit', 'used', 
                        'value_ust', 'minimum', 'maximum', 'group_ust', 'rule_map_ust']
        msg = self.dop_function.column_check(PZ_tm, 'pz_tm', list_default)
        return msg 

# Changing tables SQL
class Editing_table_SQL():
    def __init__(self):
        self.cursor = db.cursor()
    def editing_sql(self, table_sql):
        unpacking_  = []

        self.cursor.execute(f'SELECT * FROM "{table_sql}" ORDER BY id')
        name_column = next(zip(*self.cursor.description))
        array_name_column = []
        for tabl, name_c in rus_list.items():

            if tabl == table_sql:

                for name in name_column:
                    if name in name_c.keys():

                        for key, value in name_c.items():
                            if name == key:
                                array_name_column.append(value)
                                break
                    else:
                        array_name_column.append(name)

        records = self.cursor.fetchall()
        unpacking_.append(records)

        count_column = len(name_column)
        count_row    = len(records)
        return count_column, count_row, array_name_column, records
    def func_chunks_generators(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    # Поиск названия сигнала для подписи
    def search_name(self, tabl, value):
        try:
            isdigit_num  = re.findall('\d+', str(value))
            self.cursor.execute(f"""SELECT name 
                                    FROM "{tabl}"
                                    WHERE id = {int(isdigit_num[0])}""")
            name_row = self.cursor.fetchall()[0][0]
            return name_row
        except:
            return ''
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

            array_name_column = []
            for tabl, name_c in rus_list.items():

                if tabl == table_used:

                    for name in name_column:
                        if name in name_c.keys():

                            for key, value in name_c.items():
                                if name == key:
                                    array_name_column.append(value)
                                    break
                        else:
                            array_name_column.append(name)

            records = self.cursor.fetchall()
            unpacking.append(records)

            count_column = len(name_column)
            count_row    = len(records)
            return count_column, count_row, array_name_column, records, msg
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
    def update_row_tabl(self, column, text_cell, text_cell_id, table_used, hat_name, flag_NULL):
        msg = {}
        active_column = list(hat_name)[column]
        try:
            if flag_NULL:
                self.cursor.execute(f"""UPDATE {table_used} 
                                        SET "{active_column}"= NULL
                                        WHERE id={text_cell_id}""")
            else:
                self.cursor.execute(f"""UPDATE {table_used} 
                                        SET "{active_column}"='{text_cell}' 
                                        WHERE id={text_cell_id}""")
            return msg
        except Exception:
            msg[f'{today} - Таблица: {table_used}, ошибка при изменении ячейки: {traceback.format_exc()}'] = 2
            return msg
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
    def type_column(self, table_used):
        msg       = {}
        type_list = []
        try:
            self.cursor.execute(f"""SELECT column_name, data_type
                                    FROM information_schema.columns
                                    WHERE table_schema = 'public' AND table_name = '{table_used}'""")
            for tabl, name_c in rus_list.items():

                if tabl == table_used:

                    for i in self.cursor.fetchall():
                        column_name = i[0]
                        data_type   = i[1]

                        if column_name in name_c.keys():

                            for key, value in name_c.items():
                                if column_name == key:
                                    list_a = [column_name, value, data_type]
                                    type_list.append(list_a)
                                    break
        except Exception:
            msg[f'{today} - Окно тип данных: ошибка: {traceback.format_exc()}'] = 2

        return type_list, msg

# Generate data SQL
class Generate_database_SQL():
    def __init__(self):
        self.dop_function = General_functions()
    def check_database_connect(self, dbname, user, password, host, port):
        try:
            connect = psycopg2.connect(f"dbname={dbname} user={user} host={host} password={password} port={port} connect_timeout=1 ")
            connect.close()
            return True
        except:
            return False
    def define_number_msg(self, cursor, tag):
        kod_msg     = 0
        addr_offset = 0
        try:
            cursor.execute(f"""SELECT index, count 
                               FROM msg
                               WHERE tag ='{tag}'""")
            for i in cursor.fetchall():
                kod_msg = i[0]
                addr_offset = i[1]
        except Exception:
            return kod_msg, addr_offset
        return kod_msg, addr_offset
    # Запись скрипта в файл
    def write_file(self, list_str, tabl, name_file):
        msg = {}
        # Создаём файл запроса
        path_request = f'{path_location_file}\\{name_file}.sql'
        if not os.path.exists(path_request):
            file = codecs.open(path_request, 'w', 'utf-8')
        else:
            os.remove(path_request)
            file = codecs.open(path_request, 'w', 'utf-8')

        if path_location_file == '' or path_location_file is None or len(path_location_file) == 0:
            msg[f'{today} - Сообщения {tabl}: не указана конечная папка'] = 2
            return msg
        begin = ('\tCREATE SCHEMA IF NOT EXISTS messages;\n'
                 '\tCREATE TABLE IF NOT EXISTS messages.OPMessages(\n'
                 '\t\tCategory INT NOT NULL,\n'
                 '\t\tMessage VARCHAR(1024),\n'
                 '\t\tIsAck BOOLEAN NOT NULL,\n'
                 '\t\tSoundFile VARCHAR(1024),\n'
                 '\t\tIsCycle BOOLEAN NOT NULL,\n'
                 '\t\tIsSound BOOLEAN NOT NULL,\n'
                 '\t\tIsHide BOOLEAN NOT NULL,\n'
                 '\t\tPriority INT NOT NULL,\n'
                 '\t\tIsAlert BOOLEAN NOT NULL,\n'
                 '\t\tCONSTRAINT OPMessages_pkey PRIMARY KEY (Category)\n'
                 '\t);\n'
                'BEGIN TRANSACTION;\n')
        file.write(begin)
        for i in list_str:
            for j in i:
                delete = j['delete']
                file.write(delete)
                insert = j['insert']
                file.write(insert)
        file.write(f'COMMIT;')
        file.close()
        return msg
    def write_in_sql(self, list_tabl, flag_write_db):
        msg = {}
        if len(list_tabl) == 0: return
        for tabl in list_tabl:
            if tabl == 'AI': 
                cursor = db.cursor()
                msg.update(self.gen_msg_ai(cursor, flag_write_db))
                continue
            if tabl == 'DI': 
                cursor = db.cursor()
                msg.update(self.gen_msg_general(cursor, flag_write_db, 'di', 'DI', 'PostgreSQL_Messages-DI'))
                continue
            if tabl == 'ZD': 
                cursor = db.cursor()
                msg.update(self.gen_msg_general(cursor, flag_write_db, 'zd', 'ZD', 'PostgreSQL_Messages-ZD'))
                continue
            if tabl == 'VS': 
                cursor = db.cursor()
                msg.update(self.gen_msg_general(cursor, flag_write_db, 'vs', 'VS', 'PostgreSQL_Messages-VS'))
                continue
            if tabl == 'VV': 
                cursor = db.cursor()
                msg.update(self.gen_msg_defence(cursor, flag_write_db, 'vv', 'VV', 'PostgreSQL_Messages-VV', 'TblHighVoltageSwitches'))
                continue
            if tabl == 'UTS': 
                cursor = db.cursor()
                msg.update(self.gen_msg_uts_upts(cursor, flag_write_db, 'uts', 'upts', 'PostgreSQL_Messages-UTS'))
                continue
            if tabl == 'UPTS': 
                cursor = db.cursor()
                msg.update(self.gen_msg_uts_upts(cursor, flag_write_db, 'upts', 'UPTS', 'PostgreSQL_Messages-UPTS'))
                continue
            if tabl == 'UMPNA': 
                cursor = db.cursor()
                msg.update(self.gen_msg_umpna(cursor, flag_write_db, 'umpna', 'UMPNA', 'PostgreSQL_Messages-Pumps'))
                cursor = db.cursor()
                msg.update(self.gen_msg_umpna(cursor, flag_write_db, 'umpna', 'KTPRAS_1', 'PostgreSQL_Messages-KTPRAS_1'))
                continue
            if tabl == 'KTPR': 
                cursor = db.cursor()
                msg.update(self.gen_msg_defence(cursor, flag_write_db, 'ktpr', 'KTPR', 'PostgreSQL_Messages-KTPR', 'TblStationDefences'))
                continue
            if tabl == 'KTPRA': 
                cursor = db.cursor()
                msg.update(self.gen_msg_defence(cursor, flag_write_db, 'ktpra', 'KTPRA', 'PostgreSQL_Messages-KTPRA', 'TblPumpDefences'))
                continue
            if tabl == 'GMPNA': 
                cursor = db.cursor()
                msg.update(self.gen_msg_defence(cursor, flag_write_db, 'gmpna', 'GMPNA', 'PostgreSQL_Messages-GMPNA', 'TblPumpReadineses'))
                continue
            if tabl == 'KTPRS': 
                cursor = db.cursor()
                msg.update(self.gen_msg_defence(cursor, flag_write_db, 'ktprs', 'KTPRS', 'PostgreSQL_Messages-KTPRS', 'TblLimitParameters'))
                continue
        return msg
    def gen_msg_ai(self, cursor, flag_write_db):
        with db:
            msg = {}
            gen_list = []
            try:
                kod_msg, addr_offset = self.define_number_msg(cursor, 'AI')
                if addr_offset == 0 or kod_msg is None or addr_offset is None: 
                    msg[f'{today} - Сообщения ai: ошибка. Адреса из таблицы msg не определены'] = 2
                    return msg
                cursor.execute(f"""SELECT id, name, group_analog FROM ai""")
                list_ai = cursor.fetchall()
                for analog in list_ai:
                    id_ai    = analog[0]
                    name_ai  = analog[1]
                    group_ai = analog[2]

                    start_addr = kod_msg + ((id_ai - 1) * int(addr_offset))
                    try:
                        cursor.execute(f"""SELECT "Table_msg" 
                                           FROM ai_grp
                                           WHERE name_group='{group_ai}'""")
                        list_group = cursor.fetchall()[0][0]
                        path = f'{path_sample}\{list_group}.xml'
                        if not os.path.isfile(path):
                            msg[f'{today} - Сообщения ai: отсутствует шаблон! {id_ai} - {name_ai}'] = 2
                            continue
                        gen_list.append(self.dop_function.parser_sample(path, start_addr, name_ai, flag_write_db, 'AI'))
                    except Exception:
                        msg[f'{today} - Сообщения ai: отсутствует шаблон: {id_ai} - {name_ai}'] = 2
                        continue
                if not flag_write_db:
                    msg.update(self.write_file(gen_list, 'AI', 'PostgreSQL_Messages-AI'))
                    msg[f'{today} - Сообщения ai: файл скрипта создан'] = 1
                    return(msg)
            except Exception:
                msg[f'{today} - Сообщения ai: ошибка генерации: {traceback.format_exc()}'] = 2
            msg[f'{today} - Сообщения ai: генерация в базу завершена'] = 1
        return(msg)
    def gen_msg_umpna(self, cursor, flag_write_db, tabl, sign, script_file):
                with db:
                    msg = {}
                    gen_list = []
                    try:
                        kod_msg, addr_offset = self.define_number_msg(cursor, sign)
                        if addr_offset == 0 or kod_msg is None or addr_offset is None: 
                            msg[f'{today} - Сообщения {tabl}: ошибка. Адреса из таблицы msg не определены'] = 2
                            return msg
                        
                        cursor.execute(f"""SELECT id, name, tabl_msg, replacement_uso_signal_vv_1, replacement_uso_signal_vv_2
                                           FROM "{tabl}" ORDER BY id""")
                        list_signal = cursor.fetchall()
                        for signal in list_signal:
                            id_       = signal[0]
                            name      = signal[1]
                            table_msg = signal[2]
                            cabinet_1 = signal[3]
                            cabinet_2 = signal[4]

                            if sign == 'KTPRAS_1': table_msg = 'TblPumpsKTPRAS'

                            start_addr = kod_msg + ((id_ - 1) * int(addr_offset))
                            path = f'{path_sample}\{table_msg}.xml'
                            if not os.path.isfile(path):
                                msg[f'{today} - Сообщения {tabl}: отсутствует шаблон!{id_} - {name}'] = 2
                                continue
                            gen_list.append(self.dop_function.parser_sample(path, start_addr, name, flag_write_db, sign, cabinet_1, cabinet_2))
                        if not flag_write_db:
                            msg.update(self.write_file(gen_list, sign, script_file))
                            msg[f'{today} - Сообщения {tabl}: файл скрипта создан'] = 1
                            return(msg)
                    except Exception:
                        msg[f'{today} - Сообщения {tabl}: ошибка генерации: {traceback.format_exc()}'] = 2
                    msg[f'{today} - Сообщения {tabl}: генерация в базу завершена!'] = 1
                return(msg)
    def gen_msg_uts_upts(self, cursor, flag_write_db, tabl, sign, script_file):
            with db:
                msg = {}
                gen_list = []
                try:
                    kod_msg, addr_offset = self.define_number_msg(cursor, sign)
                    if addr_offset == 0 or kod_msg is None or addr_offset is None: 
                        msg[f'{today} - Сообщения {tabl}: ошибка. Адреса из таблицы msg не определены'] = 2
                        return msg

                    cursor.execute(f"""SELECT id, name FROM "{tabl}" ORDER BY id""")
                    list_signal = cursor.fetchall()
                    for signal in list_signal:
                        id_       = signal[0]
                        name      = signal[1]

                        start_addr = kod_msg + ((id_ - 1) * int(addr_offset))
                        path = f'{path_sample}\{table_msg}.xml'
                        if not os.path.isfile(path):
                            msg[f'{today} - Сообщения {tabl}: в папке отсутствует шаблон - {table_msg}'] = 2
                            return msg

                        gen_list.append(self.dop_function.parser_sample(path, start_addr, name, flag_write_db, sign))

                    if not flag_write_db:
                        msg.update(self.write_file(gen_list, sign, script_file))
                        msg[f'{today} - Сообщения {tabl}: файл скрипта создан'] = 1
                        return(msg)
                except Exception:
                    msg[f'{today} - Сообщения {tabl}: ошибка генерации: {traceback.format_exc()}'] = 2
                msg[f'{today} - Сообщения {tabl}: генерация в базу завершена!'] = 1
            return(msg)
    def gen_msg_defence(self, cursor, flag_write_db, tabl, sign, script_file, table_msg):
            with db:
                msg = {}
                gen_list = []
                try:
                    kod_msg, addr_offset = self.define_number_msg(cursor, sign)
                    if addr_offset == 0 or kod_msg is None or addr_offset is None: 
                        msg[f'{today} - Сообщения {tabl}: ошибка. Адреса из таблицы msg не определены'] = 2
                        return msg
                    
                    if sign == 'KTPRA' or sign == 'GMPNA':
                        cursor.execute(f"""SELECT id, name, "NA" FROM "{tabl}" ORDER BY id""")
                    else:
                        cursor.execute(f"""SELECT id, name FROM "{tabl}" ORDER BY id""")
                    list_signal = cursor.fetchall()
                    for signal in list_signal:
                        id_       = signal[0]
                        name      = signal[1]
                        if sign == 'KTPRA' or sign == 'GMPNA':
                            na    = signal[2]

                        start_addr = kod_msg + ((id_ - 1) * int(addr_offset))
                        path = f'{path_sample}\{table_msg}.xml'
                        if not os.path.isfile(path):
                            msg[f'{today} - Сообщения {tabl}: в папке отсутствует шаблон - {table_msg}'] = 2
                            return msg
                        if sign == 'KTPRA' or sign == 'GMPNA':
                            gen_list.append(self.dop_function.parser_sample(path, start_addr, f'{na}. {name}', flag_write_db, sign))
                        else:
                            gen_list.append(self.dop_function.parser_sample(path, start_addr, name, flag_write_db, sign))
                    if not flag_write_db:
                        msg.update(self.write_file(gen_list, sign, script_file))
                        msg[f'{today} - Сообщения {tabl}: файл скрипта создан'] = 1
                        return(msg)
                except Exception:
                    msg[f'{today} - Сообщения {tabl}: ошибка генерации: {traceback.format_exc()}'] = 2
                msg[f'{today} - Сообщения {tabl}: генерация в базу завершена!'] = 1
            return(msg)
    def gen_msg_general(self, cursor, flag_write_db, tabl, sign, script_file):
            with db:
                msg = {}
                gen_list = []
                try:
                    kod_msg, addr_offset = self.define_number_msg(cursor, sign)
                    if addr_offset == 0 or kod_msg is None or addr_offset is None: 
                        msg[f'{today} - Сообщения {tabl}: ошибка. Адреса из таблицы msg не определены'] = 2
                        return msg
                    
                    cursor.execute(f"""SELECT id, name, tabl_msg FROM "{tabl}" ORDER BY id""")
                    list_signal = cursor.fetchall()
                    for signal in list_signal:
                        id_       = signal[0]
                        name      = signal[1]
                        table_msg = signal[2]

                        start_addr = kod_msg + ((id_ - 1) * int(addr_offset))
                        path = f'{path_sample}\{table_msg}.xml'
                        if not os.path.isfile(path):
                            msg[f'{today} - Сообщения {tabl}: отсутствует шаблон!{id_} - {name}'] = 2
                            continue
                        gen_list.append(self.dop_function.parser_sample(path, start_addr, name, flag_write_db, sign))
                    if not flag_write_db:
                        msg.update(self.write_file(gen_list, sign, script_file))
                        msg[f'{today} - Сообщения {tabl}: файл скрипта создан'] = 1
                        return(msg)
                except Exception:
                    msg[f'{today} - Сообщения {tabl}: ошибка генерации: {traceback.format_exc()}'] = 2
                msg[f'{today} - Сообщения {tabl}: генерация в базу завершена!'] = 1
            return(msg)