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
            basket = row['basket']
            dict_column = { 'type_signal' : row['type_signal'],
                            'uso'         : uso,
                            'tag'         : row['tag'],
                            'description' : row['description'],
                            'scheme'      : row['scheme'],
                            'klk'         : row['klk'],
                            'contact'     : row['contact'],
                            'basket'      : row['basket'],
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
    def getting_modul(self):
        with db:
            for row_sql in Signals.select().dicts():
                uso    = row_sql['uso']
                basket = row_sql['basket']

                self.cursor.execute(f'''SELECT * 
                                        FROM signals 
                                        WHERE uso="{uso}" AND basket="{basket}"''')
                
                print(self.cursor.fetchone())




        
    def import_for_sql(self):
        # Logs
        msg = {}

        # Create tabl
        with db.atomic():
            db.create_tables([HardWare])

        # Checking if a column exists
        column_tabl  = []
        new_column   = []
        list_default = ['symbol', 'uso', 'basket', 'powerLink_ID', 
                        'type_00', 'variable_00', 'type_01', 'variable_01', 'type_02', 'variable_02', 
                        'type_03', 'variable_03', 'type_04', 'variable_04', 'type_05', 'variable_05', 
                        'type_06', 'variable_06', 'type_07', 'variable_07', 'type_08', 'variable_08',
                        'type_09', 'variable_09', 'type_10', 'variable_10', 'type_11', 'variable_11', 
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
        
        self.getting_modul()

        # Checking for the existence of a database
        #with db.atomic():
        #    Signals.insert_many(data).execute()

       # msg[f'{today} - Добавлено новое УСО: {uso}'] = 1

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
        print(f'Таблица очищена: {table_used}')
    # Table selection window
    def get_tabl(self):
        return db.get_tables()


