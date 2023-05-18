from peewee import *
from playhouse.migrate import *

from graphic_part import Window
# from PyQt5.QtWidgets import QApplication
# app = QApplication([])

# win_ = Window()
# path_prj = win_.file_prj()

path_to_exel = f'D:\\Development\\New_SQL_generator\\Working_draft_SQL\\sqllite_database\\Салым-4_кор14_ЗПСИ.xlsm'
path_to_base = f'D:\\Development\\New_SQL_generator\\Working_draft_SQL\\sqllite_database\\asutp.db'

# with open(path_prj) as paths:
#     for string in paths:
#         split_str = string.strip().split(': ')
#         if split_str[0] == 'path_to_kzfkp':
#             path_to_exel = split_str[1]
#         if split_str[0] == 'path_to_base':
#             path_to_base = split_str[1]

db = SqliteDatabase(path_to_base)
migrator = SqliteMigrator(db)

class BaseModel(Model):
    class Meta:
        database = db

class Signals(BaseModel):
    type_signal = CharField(null = True)
    uso         = CharField(null = True)
    tag         = CharField(null = True)
    description = CharField(null = True)
    scheme      = CharField(null = True)
    klk         = CharField(null = True)
    contact     = CharField(null = True)
    basket      = CharField(null = True)
    module      = CharField(null = True)
    channel     = CharField(null = True)

    class Meta:
        table_name = 'signals'

class HardWare(BaseModel):
    uso          = CharField(null = True)
    basket       = CharField(null = True)
    powerLink_ID = CharField(null = True)
    type_0       = CharField(null = True)
    variable_0   = CharField(null = True)
    type_1       = CharField(null = True)
    variable_1   = CharField(null = True)
    type_2       = CharField(null = True)
    variable_2   = CharField(null = True)
    type_3       = CharField(null = True)
    variable_3   = CharField(null = True)
    type_4       = CharField(null = True)
    variable_4   = CharField(null = True)
    type_5       = CharField(null = True)
    variable_5   = CharField(null = True)
    type_6       = CharField(null = True)
    variable_6   = CharField(null = True)
    type_7       = CharField(null = True)
    variable_7   = CharField(null = True)
    type_8       = CharField(null = True)
    variable_8   = CharField(null = True)
    type_9       = CharField(null = True)
    variable_9   = CharField(null = True)
    type_10      = CharField(null = True)
    variable_10  = CharField(null = True)
    type_11      = CharField(null = True)
    variable_11  = CharField(null = True)
    type_12      = CharField(null = True)
    variable_12  = CharField(null = True)
    type_13      = CharField(null = True)
    variable_13  = CharField(null = True)
    type_14      = CharField(null = True)
    variable_14  = CharField(null = True)
    type_15      = CharField(null = True)
    variable_15  = CharField(null = True)
    type_16      = CharField(null = True)
    variable_16  = CharField(null = True)
    type_17      = CharField(null = True)
    variable_17  = CharField(null = True)
    type_18      = CharField(null = True)
    variable_18  = CharField(null = True)
    type_19      = CharField(null = True)
    variable_19  = CharField(null = True)
    type_20      = CharField(null = True)
    variable_20  = CharField(null = True)
    type_21      = CharField(null = True)
    variable_21  = CharField(null = True)
    type_22      = CharField(null = True)
    variable_22  = CharField(null = True)
    type_23      = CharField(null = True)
    variable_23  = CharField(null = True)
    type_24      = CharField(null = True)
    variable_24  = CharField(null = True)
    type_25      = CharField(null = True)
    variable_25  = CharField(null = True)
    type_26      = CharField(null = True)
    variable_26  = CharField(null = True)
    type_27      = CharField(null = True)
    variable_27  = CharField(null = True)
    type_28      = CharField(null = True)
    variable_28  = CharField(null = True)
    type_29      = CharField(null = True)
    variable_29  = CharField(null = True)
    type_30      = CharField(null = True)
    variable_30  = CharField(null = True)
    type_31      = CharField(null = True)
    variable_31  = CharField(null = True)
    type_32      = CharField(null = True) 
    variable_32  = CharField(null = True)

    class Meta:
        table_name = 'hardware'

