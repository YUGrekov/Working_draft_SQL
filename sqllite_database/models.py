from peewee import *
from playhouse.migrate import *



db = SqliteDatabase(f'D:\Development\Py_development\Generator_Exel\sqllite_database\\test.db')
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










# class Diagnostics(BaseModel):
#     Identifier   = CharField()
#     USO          = CharField(null = True)
#     Basket       = CharField(null = True)
#     PowerLink_ID = CharField(null = True)
#     _00          = CharField(null = True)
#     _01          = CharField(null = True)
#     _02          = CharField(null = True)
#     _03          = CharField(null = True)
#     _04          = CharField(null = True)
#     _05          = CharField(null = True)
#     _06          = CharField(null = True)
#     _07          = CharField(null = True)
#     _08          = CharField(null = True)
#     _09          = CharField(null = True)
#     _10          = CharField(null = True)
#     _11          = CharField(null = True)
#     _12          = CharField(null = True)
#     _13          = CharField(null = True)
#     _14          = CharField(null = True)
#     _15          = CharField(null = True)
#     _16          = CharField(null = True)
#     _17          = CharField(null = True)
#     _18          = CharField(null = True)
#     _19          = CharField(null = True)
#     _20          = CharField(null = True)
#     _21          = CharField(null = True)
#     _22          = CharField(null = True)
#     _23          = CharField(null = True)
#     _24          = CharField(null = True)
#     _25          = CharField(null = True)
#     _26          = CharField(null = True)
#     _27          = CharField(null = True)
#     _28          = CharField(null = True)
#     _29          = CharField(null = True)
#     _30          = CharField(null = True)
#     _31          = CharField(null = True)
#     _32          = CharField(null = True)

