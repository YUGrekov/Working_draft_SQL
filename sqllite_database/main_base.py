from models import *
import openpyxl as wb
from datetime import datetime
today = datetime.now()



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
            scheme      = row['scheme']
            basket      = row['basket']

            list_type = ['CPU', 'PSU', 'CN', 'MN', 'AI','AO', 'DI', 'RS','DO']
            for value in list_type:
                if str(scheme).find(value) != -1: 
                    type_signal = value

            dict_column = {'type_signal' : type_signal,
                           'uso'         : uso,
                           'tag'         : row['tag'],
                           'description' : row['description'],
                           'scheme'      : row['scheme'],
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
        # Create tabl
        with db.atomic():
            db.create_tables([Signals])
        # Checking if a column exists
        column_tabl  = []
        new_column   = []
        list_default = ['id', 'type_signal', 'uso', 'tag', 'description', 'scheme', 'klk', 'contact', 'basket', 'module', 'channel']
        
        for data_column in db.get_columns('signals'):
            if data_column[0] in list_default: column_tabl.append(data_column[0])
        
        for lst in list_default:
            if lst not in column_tabl: 
                msg[f'{today} - Отсутствует обязательный столбец таблицы signals: {lst}'] = 2
                new_column.append(lst)
        
        for new_name in new_column:
            msg[f'{today} - Столбец: {new_name} добавлен в таблицу signals'] = 3
            migrate(migrator.add_column('signals', new_name, IntegerField(null=True)))
        # Checking for the existence of a database
        with db.atomic():
            Signals.insert_many(data).execute()

        msg[f'{today} - Добавлено новое УСО: {uso}'] = 1
        return(msg)
    # Update Database
    def update_for_sql(self, data, uso):
        msg = {}
        with db:
            # Checking if a column exists
            column_tabl  = []
            new_column   = []
            list_default = ['id', 'type_signal', 'uso', 'tag', 'description', 'scheme', 'klk', 'contact', 'basket', 'module', 'channel']
            for data_column in db.get_columns('signals'):
                if data_column[0] in list_default: column_tabl.append(data_column[0])
            for lst in list_default:
                if lst not in column_tabl: 
                    msg[f'{today} - Отсутствует обязательный столбец таблицы signals: {lst}'] = 2
                    new_column.append(lst)
            for new_name in new_column:
                msg[f'{today} - Столбец: {new_name} добавлен в таблицу signals'] = 3
                migrate(migrator.add_column('signals', new_name, IntegerField(null=True)))

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
                                    type_kod = value
                                    type_mod = key
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
        # Logs
        msg = {}
        # Create tabl
        with db.atomic():
            db.create_tables([HardWare])
        # Checking if a column exists
        column_tabl  = []
        new_column   = []
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
        
        for data_column in db.get_columns('hardware'):
            if data_column[0] in list_default: column_tabl.append(data_column[0])
        
        for lst in list_default:
            if lst not in column_tabl: 
                msg[f'{today} - Отсутствует обязательный столбец таблицы hardware: {lst}'] = 2
                new_column.append(lst)
        
        for new_name in new_column:
            msg[f'{today} - Столбец: {new_name} добавлен в таблицу hardware'] = 3
            migrate(migrator.add_column('hardware', new_name, IntegerField(null=True)))
    # Removing all rows
    def clear_tabl(self):
        msg = {}
        self.cursor.execute(f'''DELETE FROM hardware''')
        msg[f'{today} - Таблица: hardware полностью очищена'] = 1
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


