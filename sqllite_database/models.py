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
            'ai': ['№','Переменная', 'Идентификатор','Название','Ссылка на входное значение сигнала','Ссылка на исправность канала','Группа аналогов',
                   'Группа уставок аналогов', 'Единица измерения', 'Подпись для ВУ', 'Давление нефти/ нефтепродукта (флаг для пересчета в кгс/см2)', 'Номер НА или вспом.', 
                   'Вибрация насоса', 'Вибрация ЭД', 'Ток ЭД НА', 'Давление на вых. вспом.', '№ уставки мин. авар.', 
                   '№ уставки мин. пред.', '№ уставки макс. пред.', '№ уставки макс. авар.', 'Пол. мин.', 'Пол. макс.', 'Инж. Мин.', 'Инж. Макс.', 'Достоверность мин.', 
                   'Достоверность макс.', 'Гистерезис', 'Фильтрация', 
                   'Мин.6', 'Мин.5', 'Мин.4', 'Мин.3', 'Мин.2', 'Мин.', 'Макс.', 'Макс.2', 'Макс.3', 'Макс.4', 'Макс.5', 'Макс.6', 
                   'Отображаемая точность значения', 'Номера листов на которых данный сигнал участвует в формировании рамки квитирования', 'Группа сброса трендов', 
                   'Гистерезис ТИ', 'Единица измерения физической величины (АЦП)', 'Правило для карты уставок', 'Предохранитель',
                   'Шкаф', 'Корзина', 'Модуль', 'Канал'],
            'ktpr': ['№','Переменная', 'Идентификатор','Название',
                     'Аварийный параметр(pInput)', 'Запрет маскирования(1 - запрет)', 'Автоматическая деблокировка защиты(1 - разрешена)', 'Отключение ПНС с выдержкой времени до 5 с после отключения всех МНА',
                     'Битовая маска принадлежности защиты группе(1 в N бите - разрешение сработки данной защиты на N группе (плече))', 'Тип остановки НА(0-None, 1-ManageStop, 2-ElectricStop, 3-ManageStopOffVV, 4-ChRPAlarmStop, 5-StopAuto, 6-StopAuto2, 7-PovtorOtkl)',
                     '''Тип остановки насосной станции(описание РД242, ч1, стр61, табл.9.3,п.8, 
                     1 - StopAllInShoulder - одновремменная остановка всех НА в плече, 
                     2 - StopOneByOneInShoulder - последовательная остановка всех НА в плече, 
                     3 - StopFirstNextInShoulder - отключение первого по потоку нефти/нефтепродукта НА, и отключения следующего при сохранении аврийного параметра, 
                     4 - StopOnlyirstInShoulder - отключение первого по потоку нефти/нефтепродукта НА, 
                     5 - StopAllInSubShoulder - одновреммення остановка всех ПН в подплече)''',

                     'Закрытие задвижек на входе НПС', 'Закрытие задвижек на выходе НПС', 'Закрытие задвижек между ПНС и МНС', 'Закрытие задвижек между РП и ПНС', 
                     'Закрытие задвижек на входе и выходе МНС', 'Закрытие задвижек на входе и выходе ПНС', 'Закрытие задвижек на входе и выходе МНА', 'Закрытие задвижек на входе и выходе ПНА', 
                     'Закрытие задвижек на входе узла РД', 'Закрытие задвижек на выходе узла РД', 'Закрытие задвижек на входе ССВД', 'Закрытие задвижек на входе ФГУ', 
                     'Закрытие секущей задвижки узла подключения объекта нефтедобычи/ нефтепереработки', 'Закрытие задвижек на входе РП', 'Резерв(14 бит)', 'Резерв(15 бит)',

                     'Отключение маслонасосов', 'Отключение маслонасосов после сигнала "остановлен" НА', 'Отключение насосов оборотного водоснабжения', 'Отключение насосов откачки из емкостей сбора утечек МНС', 
                     'Отключение насосов откачки из емкостей сбора утечек ПНС', 'Отключение насосов откачки из емкостей ССВД', 'Отключение беспромвальных вентиляторов электрозала', 
                     'Отключение подпорных вентиляторов ЭД', 'Отключение подпорных вентиляторов электрозала', 'Отключение компрессоров подпора воздуха ЭД', 
                     'Отключение насосов, обеспечивающих подкачку нефти/нефтепродукта от объектов нефтедобычи/нефтепереработки', 'Отключение насосов прокачки нефти/нефтепродукта через БИК', 
                     'Отключение насосов хозяйственно-питьевого водоснабжения', 'Отключение насосов артскважин', 'Отключение АВО', 'Отключение вентиляторов водоохлаждения системы оборотного водоснабжения', 
                    
                     'Отключение вытяжных вентиляторов насосного зала МНС', 'Отключение вытяжных вентиляторов насосного зала ПНС', 'Отключение вытяжных вентиляторов в помещении централизованной маслосистемы', 
                     'Отключение вытяжных вентиляторов маслоприямка в электрозале', 'Отключение вытяжных вентиляторов в помещении РД', 'Отключение вытяжных вентиляторов в помещении ССВД', 
                     'Отключение крышных вентиляторов насосного зала МНС', 'Отключение крышных вентиляторов насосного зала ПНС', 'Отключение приточных вентиляторов насосного зала МНС и закрытие огнезадерживающих клапанов', 
                     'Отключение приточных вентиляторов насосного зала ПНС и закрытие огнезадерживающих клапанов', 'Отключение приточных вентиляторов в помещении централизованной маслосистемы и закрытие огнезадерживающих клапанов', 
                     'Отключение приточного вентилятора помещения РД', 'Отключение приточного вентилятора помещения ССВД', 'Отключение приточных вентиляторов помещения компрессорной подпора воздуха ЭД и закрытие огнезадерживающих клапанов', 
                     'Отключение приточного вентилятора помещения БИК', 'Отключение приточного вентилятора помещения СИКН', 

                     'Закрытие воздушных клапанов (жалюзийных решёток) насосного зала', 'Закрытие воздушных клапанов (жалюзийных решёток) помещения компрессорной подпора воздуха ЭД', 
                     'Отключение электронагревателей масла', 'Отключение электронагревателей емкости сбора утечек МНС', 'Отключение электронагревателей емкости сбора утечек ПНС', 
                     'Отключение электронагревателей емкости сбора утечек СИКН', 'Отключение воздушных охладителей системы запирания торцовых уплотнений всех МНА', 
                     'Отключение воздушных охладителей системы запирания торцовых уплотнений отключенных НА', 'Отключение внешнего контура охлаждения ЧРП МНА', 
                     'Отключение внешнего контура охлаждения ЧРП ПНА', 'Отключение насосов системы запирания', 'Отключение насосов прокачки нефти/нефтепродукта через оперативный БИК', 
                     'Отключение насосов откачки из емкостей сбора утечек всех СИКН', 'Отключение антиконденсационных электронагревателей ЭД', 'Защита по пожару', 'Резерв(15 бит)', 

                     'Временная уставка', 'Номера листов на которых данный сигнал участвует в формировании рамки квитирования',
                   'Группа уставок', 'Правило для карты уставок', 'Номер листа (для ВУ)', 'Номер защиты (для ВУ)'],
            'ktpra': ['№','Переменная', 'Идентификатор','Название', 
                    'Имя НА', 'Аварийный параметр', '''Тип остановки(0 - None,\n1 - ManageStop,\n2 - ElectricStop,\n3 - ManageStopOffVV,\n4 - ChRPAlarmStop,\n5 - StopAuto,\n6 - StopAuto2,\n7 - PovtorOtkl1)''',  
                    'Флаг необходимости АВР НА при срабатывании защиты' , 'Флаг необходимости закрытия агрегатных задвижек НА при срабатывании защиты', 
                    'Флаг запрета маскирования', 'Временная уставка', 
                    'Номера листов на которых данный сигнал участвует в формировании рамки квитирования', 'Группа уставок', 'Правило для карты уставок', 
                    'Номер листа (для ВУ)', 'Номер защиты (для ВУ)', 'Номер агрегата (для ВУ)'],
            'ktprs': ['№','Переменная', 'Идентификатор','Название', 'Сработка', 'Ссылка на значение', 'Приоритет сообщ. при 0', 'Приоритет сообщ. при 1',
                   'Запрет выдачи сообщений', 'Номера листов на которых данный сигнал участвует в формировании рамки квитирования'],
            'gmpna': ['№','Переменная', 'Идентификатор','Название', 'Название для ЧРП в местном режиме', 'Имя НА', 'Использовать временную уставку', 'Уставка',
                    'Группа уставок', 'Правило для карты уставок', 'Номер листа (для ВУ)', 'Номер защиты (для ВУ)', 'Номер агрегата (для ВУ)'],
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
class KTPR(BaseModel):
    variable = CharField(null = True)
    tag  = CharField(null = True)
    name = CharField(null = True)

    avar_parameter = CharField(null = True)
    prohibition_masking = CharField(null = True)
    auto_unlock_protection = CharField(null = True)
    shutdown_PNS_a_time_delay_up_5s_after_turning_off_all_NA = CharField(null = True)
    bitmask_protection_group_membership = CharField(null = True)
    stop_type_NA = CharField(null = True)
    pump_station_stop_type = CharField(null = True)
    
    closing_gate_valves_at_the_inlet_NPS = CharField(null = True)
    closing_gate_valves_at_the_outlet_NPS = CharField(null = True)
    closing_gate_valves_between_PNS_and_MNS = CharField(null = True)
    closing_gate_valves_between_RP_and_PNS = CharField(null = True)
    closing_valves_inlet_and_outlet_MNS = CharField(null = True)
    closing_valves_inlet_and_outlet_PNS = CharField(null = True)
    closing_valves_inlet_and_outlet_MNA = CharField(null = True)
    closing_valves_inlet_and_outlet_PNA = CharField(null = True)
    closing_valves_inlet_RD = CharField(null = True)
    closing_valves_outlet_RD = CharField(null = True)
    closing_valves_inlet_SSVD = CharField(null = True)
    closing_valves_inlet_FGU = CharField(null = True)
    closing_secant_valve_connection_unit__oil_production_oil_refining_facility = CharField(null = True)
    closing_valves_inlet_RP = CharField(null = True)
    reserve_protect_14 = CharField(null = True)
    reserve_protect_15 = CharField(null = True)

    shutdown_oil_pumps = CharField(null = True)
    shutdown_oil_pumps_after_signal_stopped_NA = CharField(null = True)
    shutdown_circulating_water_pumps = CharField(null = True)
    shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_MNS = CharField(null = True)
    shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_PNS = CharField(null = True)
    shutdown_pumps_pumping_out_from_tanks_SSVD = CharField(null = True)
    switching_off_the_electric_room_fans = CharField(null = True)
    shutdown_of_booster_fans_ED = CharField(null = True)
    shutdown_of_retaining_fans_of_the_electrical_room = CharField(null = True)
    shutdown_of_ED_air_compressors = CharField(null = True)
    shutdown_pumps_providing_oil_oil_product_pumping_from_oil_production_oil_refining_facilities = CharField(null = True)
    disabling_pumps_for_pumping_oil_oil_products_through_BIC = CharField(null = True)
    shutdown_domestic_and_drinking_water_pumps = CharField(null = True)
    shutdown_of_art_well_pumps = CharField(null = True)
    AVO_shutdown = CharField(null = True)
    shutdown_of_water_cooling_fans_circulating_water_supply_system = CharField(null = True)

    shutdown_exhaust_fans_of_the_pumping_room_of_the_MNS = CharField(null = True)
    shutdown_of_exhaust_fans_of_the_pumping_room_PNS = CharField(null = True)
    shutdown_of_exhaust_fans_in_the_centralized_oil_system_room = CharField(null = True)
    shutdown_of_exhaust_fans_oil_pit_in_the_electrical_room = CharField(null = True)
    shutdown_of_exhaust_fans_in_the_RD_room = CharField(null = True)
    shutdown_of_exhaust_fans_in_the_SSVD_room = CharField(null = True)
    shutdown_of_the_roof_fans_of_the_MNS_pump_room = CharField(null = True)
    shutdown_of_the_roof_fans_of_the_PNS_pump_room = CharField(null = True)
    switching_off_the_supply_fans_pumping_room_of_the_MNS_and_closing_the_fire_dampers = CharField(null = True)
    switching_off_the_supply_fans_pumping_room_of_the_PNS_and_closing_the_fire_dampers = CharField(null = True)
    switch_off_the_supply_fans_in_the_centralized_oil_system_room_and_close_the_fire_dampers = CharField(null = True)
    switching_off_the_supply_fan_of_the_RD_room = CharField(null = True)
    switching_off_the_supply_fan_of_the_SSVD_room = CharField(null = True)
    switching_off_the_supply_fans_of_the_ED_air_compressor_room_and_closing_the_fire_dampers = CharField(null = True)
    switching_off_the_supply_fan_of_the_BIK_room = CharField(null = True)
    switching_off_the_supply_fan_of_the_SIKN_room = CharField(null = True)
    
    closing_the_air_valves_louvered_grilles_of_the_pump_room = CharField(null = True)
    closing_of_air_valves_louvered_grilles_of_the_compressor_room_of_the_ED_air_overpressure = CharField(null = True)
    shutdown_of_electric_oil_heaters = CharField(null = True)
    shutdown_of_the_electric_heaters_of_the_leakage_collection_tank_MNS = CharField(null = True)
    shutdown_of_the_electric_heaters_of_the_leakage_collection_tank_PNS = CharField(null = True)
    shutdown_of_electric_heaters_of_the_SIKN_leak_collection_tank = CharField(null = True)
    shutdown_of_air_coolers_of_the_locking_system_of_mechanical_seals_of_all_MNA = CharField(null = True)
    shutdown_of_air_coolers_of_the_locking_system_of_mechanical_seals_disconnected_NA = CharField(null = True)
    shutdown_of_the_external_cooling_circuit_ChRP_MNA = CharField(null = True)
    shutdown_of_the_external_cooling_circuit_ChRP_PNA = CharField(null = True)
    shutdown_of_locking_system_pumps = CharField(null = True)
    shutdown_of_pumps_for_pumping_oil_oil_products_through_the_operational_BIK = CharField(null = True)
    shutdown_of_pumping_pumps_from_leakage_collection_tanks_of_all_SIKN = CharField(null = True)
    shutdown_of_anticondensation_electric_heaters_ED = CharField(null = True)
    fire_protection = CharField(null = True)
    reserve_aux_15 = CharField(null = True)

    time_ust = CharField(null = True)
    PIC = CharField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    number_list_VU = IntegerField(null = True)
    number_protect_VU = IntegerField(null = True)
    
    class Meta:
        table_name = 'ktpr'
class KTPRA(BaseModel):
    variable = CharField(null = True)
    tag  = CharField(null = True)
    name = CharField(null = True)
    NA = CharField(null = True)
    avar_parameter = CharField(null = True)
    stop_type = CharField(null = True)
    AVR = CharField(null = True)
    close_valves = CharField(null = True)
    prohibition_of_masking = CharField(null = True)
    time_setting = CharField(null = True)
    PIC = CharField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    number_list_VU = IntegerField(null = True)
    number_protect_VU = IntegerField(null = True)
    number_pump_VU = IntegerField(null = True)
    
    class Meta:
        table_name = 'ktpra'
class KTPRS(BaseModel):
    variable = CharField(null = True)
    tag  = CharField(null = True)
    name = CharField(null = True)
    drawdown = CharField(null = True)
    reference_to_value = CharField(null = True)
    priority_msg_0 = CharField(null = True)
    priority_msg_1 = CharField(null = True)
    prohibition_issuing_msg = CharField(null = True)
    PIC = CharField(null = True)
    
    class Meta:
        table_name = 'ktprs'
class GMPNA(BaseModel):
    variable = CharField(null = True)
    tag  = CharField(null = True)
    name = CharField(null = True)
    name_for_Chrp_in_local_mode = CharField(null = True)
    NA = CharField(null = True)
    time_setting = CharField(null = True)
    setting = CharField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    number_list_VU = IntegerField(null = True)
    number_protect_VU = IntegerField(null = True)
    number_pump_VU = IntegerField(null = True)
    
    class Meta:
        table_name = 'gmpna'
class UMPNA(BaseModel):
    variable = CharField(null = True)
    tag  = CharField(null = True)
    name = CharField(null = True)

    vv_included = CharField(null = True)
    vv_double_included = CharField(null = True)
    vv_disabled = CharField(null = True)
    vv_double_disabled = CharField(null = True)
    current_greater_than_noload_setting = CharField(null = True)
    serviceability_of_circuits_of_inclusion_of_VV = CharField(null = True)
    serviceability_of_circuits_of_shutdown_of_VV = CharField(null = True)
    serviceability_of_circuits_of_shutdown_of_VV_double = CharField(null = True)

    stop_1 = CharField(null = True)
    stop_2 = CharField(null = True)
    stop_3 = CharField(null = True)
    stop_4 = CharField(null = True)

    monitoring_the_presence_of_voltage_in_the_control_current_circuits = IntegerField(null = True)
    voltage_presence_flag_in_the_ZRU_motor_cell = IntegerField(null = True)
    vv_trolley_rolled_out = IntegerField(null = True)
    remote_control_mode_of_the_RZiA_controller = CharField(null = True)
    availability_of_communication_with_the_RZiA_controller = CharField(null = True)
    the_state_of_the_causative_agent_of_ED = CharField(null = True)
    engine_prepurge_end_flag = CharField(null = True)
    flag_for_the_presence_of_safe_air_boost_pressure_in_the_engine_housing = CharField(null = True)
    flag_for_the_presence_of_safe_air_boost_pressure_in_the_exciter_housing = CharField(null = True)
    engine_purge_valve_closed_flag = CharField(null = True)
    oil_system_oil_temperature_flag_is_above_10_at_the_cooler_outlet_for_an_individual_oil_system = CharField(null = True)
    flag_for_the_minimum_oil_level_in_the_oil_tank_for_an_individual_oil_system = CharField(null = True)
    flag_for_the_presence_of_the_minimum_level_of_the_barrier_liquid_in_the_tank_of_the_locking_system = CharField(null = True)
    generalized_flag_for_the_presence_of_barrier_fluid_pressure_to_the_mechanical_seal = CharField(null = True)
    command_to_turn_on_the_vv_only_for_UMPNA = CharField(null = True)
    command_to_turn_off_the_vv_output_1 = CharField(null = True)
    command_to_turn_off_the_vv_output_2 = CharField(null = True)
    NA_Chrp = CharField(null = True)
    type_NA_MNA = CharField(null = True)
    pump_type_NM = CharField(null = True)
    parametr_KTPRAS_1 = CharField(null = True)
    number_of_delay_scans_of_the_analysis_of_the_health_of_the_control_circuits_NA_MNA = CharField(null = True)
    unit_number_of_the_auxiliary_system_start_up_oil_pump_for_an_individual_oil_system = CharField(null = True)
    NPS_number_1_or_2_which_the_AT_belongs = CharField(null = True)
    achr_protection_number_in_the_array_of_station_protections = CharField(null = True)
    saon_protection_number_in_the_array_of_station_protections = CharField(null = True)

    gmpna_49 = CharField(null = True)
    gmpna_50 = CharField(null = True)
    gmpna_51 = CharField(null = True)
    gmpna_52 = CharField(null = True)
    gmpna_53 = CharField(null = True)
    gmpna_54 = CharField(null = True)
    gmpna_55 = CharField(null = True)
    gmpna_56 = CharField(null = True)
    gmpna_57 = CharField(null = True)
    gmpna_58 = CharField(null = True)
    gmpna_59 = CharField(null = True)
    gmpna_60 = CharField(null = True)
    gmpna_61 = CharField(null = True)
    gmpna_62 = CharField(null = True)
    gmpna_63 = CharField(null = True)
    gmpna_64 = CharField(null = True)

    PIC = CharField(null = True)
    replacement_uso_signal_vv_1 = CharField(null = True)
    replacement_uso_signal_vv_2 = CharField(null = True)

    class Meta:
        table_name = 'gmpna'