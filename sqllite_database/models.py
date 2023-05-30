from peewee import *
from playhouse.migrate import *

from graphic_part import Window
# from PyQt5.QtWidgets import QApplication
# app = QApplication([])

# win_ = Window()
# path_prj = win_.file_prj()

path_to_exel = f'D:\\Development\\New_SQL_generator\\Working_draft_SQL\\sqllite_database\\П3 - КЗФКП Аксинино-2_MK500_20230405.xlsx'
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

rus_list = {'signals': ['№', 'Тип сигнала', 'Шкаф', 'Идентификатор', 'Наименование', 'Схема', 'Клеммник', 'Контакт', 'Корзина', 'Модуль', 'Канал'],
            'di': ['№','Переменная', 'Идентификатор','Название','Ссылка на входное значение сигнала','Ссылка на исправность канала','Инвертировать входное значение','Значение, выставляемое в stateDI[..].Value при неиcправности канала',
                    'Приоритет при 0','Приоритет при 1','Выдавать сообщения по изменению сигнала','В pNC_AI должна быть ссылка на stateDI[..].state "Неисправность цепей". Значение сигнала из pValue',
                    'В pNC_AI должна быть ссылка на stateAI[..]state. Значение из Warn, КЗ из MTMax, обрыв из LTMin. pValue игнорируется','В pNC_AI должна быть ссылка на stateAI[..]state. Значение из Avar, КЗ из MTMax, обрыв из LTMin. pValue игнорируется',
                    'Ссылка на stateDI "Неисправность цепей" или stateAI, контролирующий обрыв или КЗ','TS ID для быстрых сигналов','При потере связи модуля с КЦ формировать сигнализацию и сообщение о неисправности',
                    'Номера листов на которых данный сигнал участвует в формировании рамки квитирования','Имя xml файла-шаблона с сообщениями данного сигнала',
                    'Группа для группировки сообщений в архивном журнале:Общие,Диагностика,Энергоснабжение', 'Приоритет  сообщения при 0', 'Приоритет  сообщения при 1', 'Короткое название', 
                    'Шкаф', 'Корзина', 'Модуль', 'Канал'],
            'do': ['№','Переменная', 'Идентификатор','Название','Ссылка на входное значение сигнала','Ссылка на исправность канала',
                   'Короткое название','Шкаф', 'Корзина', 'Модуль', 'Канал'],
            'hardware': ['№', 'Переменная', 'Идентификатор\n(не генерится!)', 'Шкаф', 'Корзина', 'PowerLink ID', 
                         'Тип модуля 0',  'Переменная модуля 0',  'Тип модуля 1',  'Переменная модуля 1',  'Тип модуля 2',  'Переменная модуля 2',
                         'Тип модуля 3',  'Переменная модуля 3',  'Тип модуля 4',  'Переменная модуля 4',  'Тип модуля 5',  'Переменная модуля 5',
                         'Тип модуля 6',  'Переменная модуля 6',  'Тип модуля 7',  'Переменная модуля 7',  'Тип модуля 8',  'Переменная модуля 8',
                         'Тип модуля 9',  'Переменная модуля 9',  'Тип модуля 10', 'Переменная модуля 10', 'Тип модуля 11', 'Переменная модуля 11',
                         'Тип модуля 12', 'Переменная модуля 12', 'Тип модуля 13', 'Переменная модуля 13', 'Тип модуля 14', 'Переменная модуля 14',
                         'Тип модуля 15', 'Переменная модуля 15', 'Тип модуля 16', 'Переменная модуля 16', 'Тип модуля 17', 'Переменная модуля 17',
                         'Тип модуля 18', 'Переменная модуля 18', 'Тип модуля 19', 'Переменная модуля 19', 'Тип модуля 20', 'Переменная модуля 20',
                         'Тип модуля 21', 'Переменная модуля 21', 'Тип модуля 22', 'Переменная модуля 22', 'Тип модуля 23', 'Переменная модуля 23',
                         'Тип модуля 24', 'Переменная модуля 24', 'Тип модуля 25', 'Переменная модуля 25', 'Тип модуля 26', 'Переменная модуля 26',
                         'Тип модуля 27', 'Переменная модуля 27', 'Тип модуля 28', 'Переменная модуля 28', 'Тип модуля 29', 'Переменная модуля 29',
                         'Тип модуля 30', 'Переменная модуля 30', 'Тип модуля 31', 'Переменная модуля 31', 'Тип модуля 32', 'Переменная модуля 32'],
            'uso': ['№', 'Переменная', 'Название', 'Температура шкафа', 'Двери открыты', 
                         'Сигнал 1', 'Сигнал 2', 'Сигнал 3', 'Сигнал 4', 'Сигнал 5', 'Сигнал 6', 'Сигнал 7', 'Сигнал 8',
                         'Сигнал 9', 'Сигнал 10', 'Сигнал 11', 'Сигнал 12', 'Сигнал 13', 'Сигнал 14', 'Сигнал 15', 'Сигнал 16',
                         'Сигнал 17', 'Сигнал 18', 'Сигнал 19', 'Сигнал 20', 'Сигнал 21', 'Сигнал 22', 'Сигнал 23', 'Сигнал 24',
                         'Сигнал 25', 'Сигнал 26', 'Сигнал 27', 'Сигнал 28', 'Сигнал 29', 'Сигнал 30', 'Сигнал 31', 'Сигнал 32'],
            'ao': ['№','Переменная', 'Идентификатор','Название','Ссылка на входное значение сигнала',
                   'Ссылка на исправность канала', 'Шкаф', 'Корзина', 'Модуль', 'Канал'],
            'ai': ['№','Переменная', 'Идентификатор','Название','Ссылка на входное значение сигнала','Ссылка на исправность канала','Группа аналогов','Группа уставок аналогов', 'Единица измерения', 
                   'Подпись для ВУ', 'Давление нефти/ нефтепродукта (флаг для пересчета в кгс/см2)', 'Номер НА или вспом.', 'Вибрация насоса', 'Вибрация ЭД', 'Ток ЭД НА', 'Давление на вых. вспом.', '№ уставки мин. авар.', 
                   '№ уставки мин. пред.', '№ уставки макс. пред.', '№ уставки макс. авар.', 'Пол. мин.', 'Пол. макс.', 'Инж. Мин.', 'Инж. Макс.', 'Достоверность мин.', 'Достоверность макс.', 
                   'Гистерезис', 'Фильтрация', 'Мин.6', 'Мин.5', 'Мин.4', 'Мин.3', 'Мин.2', 'Мин.', 'Макс.', 'Макс.2', 'Макс.3', 'Макс.4', 'Макс.5', 'Макс.6', 'Отображаемая точность значения',
                   'Номера листов на которых данный сигнал участвует в формировании рамки квитирования', 'Группа сброса трендов', 'Гистерезис ТИ', 
                   'Единица измерения физической величины (АЦП)', 'Правило для карты уставок', 'Предохранитель',
                   'Шкаф', 'Корзина', 'Модуль', 'Канал'],
                         
                }
class Signals(BaseModel):
    type_signal = CharField(null = True)
    uso         = CharField(null = True)
    tag         = CharField(null = True)
    description = CharField(null = True)
    schema      = CharField(null = True)
    klk         = CharField(null = True)
    contact     = CharField(null = True)
    basket      = IntegerField(null = True)
    module      = IntegerField(null = True)
    channel     = IntegerField(null = True)

    class Meta:
        table_name = 'signals'
class HardWare(BaseModel):
    tag          = CharField(null = True)
    uso          = CharField(null = True)
    basket       = IntegerField(null = True)
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
class AI(BaseModel):
    variable = CharField(null = True)
    tag              = CharField(null = True)
    name             = CharField(null = True)
    pValue           = CharField(null = True)
    pHealth          = CharField(null = True)
    group_analog     = CharField(null = True)
    group_ust_analog = CharField(null = True)
    unit             = CharField(null = True)
    sign_VU          = CharField(null = True)
    flag_MPa_kgccm2  = CharField(null = True)

    number_NA_or_aux = CharField(null = True)
    vibration_pump   = CharField(null = True)
    vibration_motor  = CharField(null = True)
    current_motor    = CharField(null = True)
    aux_outlet_pressure = CharField(null = True)

    number_ust_min_avar = CharField(null = True)
    number_ust_min_pred = CharField(null = True)
    number_ust_max_pred = CharField(null = True)
    number_ust_max_avar = CharField(null = True)

    field_min = CharField(null = True)
    field_max = CharField(null = True)
    eng_min = CharField(null = True)
    eng_max = CharField(null = True)
    reliability_min = CharField(null = True)
    reliability_max = CharField(null = True)
    hysteresis = CharField(null = True)
    filtration = CharField(null = True)

    ust_min_6 = CharField(null = True)
    ust_min_5 = CharField(null = True)
    ust_min_4 = CharField(null = True)
    ust_min_3 = CharField(null = True)
    ust_min_2 = CharField(null = True)
    ust_min = CharField(null = True)
    ust_max = CharField(null = True)
    ust_max_2 = CharField(null = True)
    ust_max_3 = CharField(null = True)
    ust_max_4 = CharField(null = True)
    ust_max_5 = CharField(null = True)
    ust_max_6 = CharField(null = True)

    value_precision = CharField(null = True)
    PIC = CharField(null = True)
    group_trend = CharField(null = True)
    hysteresis_TI = CharField(null = True)
    unit_physical_ACP = CharField(null = True)
    setpoint_map_rule = CharField(null = True)
    fuse = CharField(null = True)

    uso = CharField(null = True)
    basket = IntegerField(null = True)
    module = IntegerField(null = True)
    channel = IntegerField(null = True)

    AlphaHMI = CharField(null = True)
    AlphaHMI_PIC1 = CharField(null = True)
    AlphaHMI_PIC1_Number_kont = CharField(null = True)
    AlphaHMI_PIC2 = CharField(null = True)
    AlphaHMI_PIC2_Number_kont = CharField(null = True)
    AlphaHMI_PIC3 = CharField(null = True)
    AlphaHMI_PIC3_Number_kont = CharField(null = True)
    AlphaHMI_PIC4 = CharField(null = True)
    AlphaHMI_PIC4_Number_kont = CharField(null = True)

    class Meta:
        table_name = 'ai'
class AO(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    pValue  = CharField(null = True)
    pHealth = CharField(null = True)

    uso = CharField(null = True)
    basket = IntegerField(null = True)
    module = IntegerField(null = True)
    channel = IntegerField(null = True)

    class Meta:
        table_name = 'ao'
class DI(BaseModel):
    variable = CharField(null = True)
    tag  = CharField(null = True)
    name = CharField(null = True)
    pValue  = CharField(null = True)
    pHealth = CharField(null = True)

    Inv = CharField(null = True)
    ErrValue = CharField(null = True)
    priority_0 = CharField(null = True)
    priority_1 = CharField(null = True)
    Msg = CharField(null = True)
    isDI_NC = CharField(null = True)
    isAI_Warn = CharField(null = True)
    isAI_Avar = CharField(null = True)
    pNC_AI = CharField(null = True)
    TS_ID = CharField(null = True)
    isModuleNC = CharField(null = True)
    Pic = CharField(null = True)
    tabl_msg = CharField(null = True)
    group_diskrets = CharField(null = True)
    msg_priority_0 = CharField(null = True)
    msg_priority_1 = CharField(null = True)
    short_title = CharField(null = True)

    uso = CharField(null = True)
    basket = IntegerField(null = True)
    module = IntegerField(null = True)
    channel = IntegerField(null = True)

    AlphaHMI = CharField(null = True)
    AlphaHMI_PIC1 = CharField(null = True)
    AlphaHMI_PIC1_Number_kont = CharField(null = True)
    AlphaHMI_PIC2 = CharField(null = True)
    AlphaHMI_PIC2_Number_kont = CharField(null = True)
    AlphaHMI_PIC3 = CharField(null = True)
    AlphaHMI_PIC3_Number_kont = CharField(null = True)
    AlphaHMI_PIC4 = CharField(null = True)
    AlphaHMI_PIC4_Number_kont = CharField(null = True)
    
    class Meta:
        table_name = 'di'
class DO(BaseModel):
    variable = CharField(null = True)
    tag  = CharField(null = True)
    name = CharField(null = True)
    pValue  = CharField(null = True)
    pHealth = CharField(null = True)
    short_title = CharField(null = True)

    uso = CharField(null = True)
    basket = IntegerField(null = True)
    module = IntegerField(null = True)
    channel = IntegerField(null = True)

    AlphaHMI = CharField(null = True)
    AlphaHMI_PIC1 = CharField(null = True)
    AlphaHMI_PIC1_Number_kont = CharField(null = True)
    AlphaHMI_PIC2 = CharField(null = True)
    AlphaHMI_PIC2_Number_kont = CharField(null = True)
    AlphaHMI_PIC3 = CharField(null = True)
    AlphaHMI_PIC3_Number_kont = CharField(null = True)
    AlphaHMI_PIC4 = CharField(null = True)
    AlphaHMI_PIC4_Number_kont = CharField(null = True)
    
    class Meta:
        table_name = 'do'
class USO(BaseModel):
    variable = CharField(null = True)
    name = CharField(null = True)
    temperature  = CharField(null = True)
    door = CharField(null = True)
    signal_1 = CharField(null = True)
    signal_2 = CharField(null = True)
    signal_3 = CharField(null = True)
    signal_4 = CharField(null = True)
    signal_5 = CharField(null = True)
    signal_6 = CharField(null = True)
    signal_7 = CharField(null = True)
    signal_8 = CharField(null = True)
    signal_9 = CharField(null = True)
    signal_10 = CharField(null = True)
    signal_11 = CharField(null = True)
    signal_12 = CharField(null = True)
    signal_13 = CharField(null = True)
    signal_14 = CharField(null = True)
    signal_15 = CharField(null = True)
    signal_16 = CharField(null = True)
    signal_17 = CharField(null = True)
    signal_18 = CharField(null = True)
    signal_19 = CharField(null = True)
    signal_20 = CharField(null = True)
    signal_21 = CharField(null = True)
    signal_22 = CharField(null = True)
    signal_23 = CharField(null = True)
    signal_24 = CharField(null = True)
    signal_25 = CharField(null = True)
    signal_26 = CharField(null = True)
    signal_27 = CharField(null = True)
    signal_28 = CharField(null = True)
    signal_29 = CharField(null = True)
    signal_30 = CharField(null = True)
    signal_31 = CharField(null = True)
    signal_32 = CharField(null = True)

    class Meta:
        table_name = 'uso'