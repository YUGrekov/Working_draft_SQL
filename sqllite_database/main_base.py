from models import *
import openpyxl as wb
from peewee import *
import os



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
    # Close connect Exel
    def close_connect(self):
        self.connect.close()
    # Importing into SQL
    def import_for_sql(self, name_db, path, data):
        # Checking if a column exists
        column_tabl  = []
        new_column   = []
        list_default = ['id', 'type_signal', 'uso', 'tag', 'description', 'scheme', 'klk', 'contact', 'basket', 'module', 'channel']
        for data_column in db.get_columns('signals'):
            if data_column[0] in list_default: column_tabl.append(data_column[0])
        for lst in list_default:
            if lst not in column_tabl: 
                print(f'Отсутствует обязательный столбец таблицы signals: {lst}')
                new_column.append(lst)
        for new_name in new_column:
            print(f'Столбец {new_name} добавлен в таблицу signals')
            migrate(migrator.add_column('signals', new_name, IntegerField(null=True)))

        # Checking for the existence of a database
        if not os.path.exists(path):
            print(f'База данных: {name_db} отсутствует. Создана новая база')
        else:
            print(f'База данных: {name_db} найдена. Создано подключение')
        with db.atomic():
            db.create_tables([Signals])
            Signals.insert_many(data).execute()
    # Update Database
    def update_for_sql(self, name_db, path, data, uso):
        with db:
            # Checking if a column exists
            column_tabl  = []
            new_column   = []
            list_default = ['id', 'type_signal', 'uso', 'tag', 'description', 'scheme', 'klk', 'contact', 'basket', 'module', 'channel']
            for data_column in db.get_columns('signals'):
                if data_column[0] in list_default: column_tabl.append(data_column[0])
            for lst in list_default:
                if lst not in column_tabl: 
                    print(f'Отсутствует обязательный столбец таблицы signals: {lst}')
                    new_column.append(lst)
            for new_name in new_column:
                print(f'Столбец {new_name} добавлен в таблицу signals')
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
                            print(row_sql['id'])
                            Signals.update(
                                tag        =row_exel['tag'],
                                description=row_exel['description'],
                                scheme     =row_exel['scheme'],
                                klk        =row_exel['klk'],
                                contact    =row_exel['contact'],
                            ).where(Signals.id == row_sql['id']).execute()
                            continue
                    else:
                        continue
    # Removing all rows
    def clear_tabl(self):
        for row_sql in Signals.select().dicts():
            Signals.get(Signals.id == row_sql['id']).delete_instance()
        print('Таблица очищена')

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
        
        






# a = Editing_table_SQL()
# a.add_new_column('signals', '125')

