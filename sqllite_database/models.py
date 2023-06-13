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

rus_list = {'signals': {'id':'№', 'type_signal':'Тип сигнала', 'uso':'Шкаф', 'tag':'Идентификатор', 'description':'Наименование', 
                        'schema':'Схема', 'klk':'Клеммник', 'contact':'Контакт', 'basket':'Корзина', 'module':'Модуль', 'channel':'Канал'},
            
            'di': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 
                   'pValue':'Ссылка на входное значение сигнала', 'pHealth':'Ссылка на исправность канала','Inv':'Инвертировать входное значение',
                   'ErrValue':'Значение, выставляемое в stateDI[..].Value при неиcправности канала',
                   'priority_0':'Приоритет при 0', 'priority_1':'Приоритет при 1', 'Msg':'Выдавать сообщения по изменению сигнала',
                   'isDI_NC':'В pNC_AI должна быть ссылка на stateDI[..].state "Неисправность цепей". Значение сигнала из pValue',
                   'isAI_Warn':'В pNC_AI должна быть ссылка на stateAI[..]state. Значение из Warn, КЗ из MTMax, обрыв из LTMin. pValue игнорируется',
                   'isAI_Avar':'В pNC_AI должна быть ссылка на stateAI[..]state. Значение из Avar, КЗ из MTMax, обрыв из LTMin. pValue игнорируется',
                   'pNC_AI':'Ссылка на stateDI "Неисправность цепей" или stateAI, контролирующий обрыв или КЗ',
                   'TS_ID':'TS ID для быстрых сигналов', 'isModuleNC':'При потере связи модуля с КЦ формировать сигнализацию и сообщение о неисправности',
                   'Pic':'Номера листов на которых данный сигнал участвует в формировании рамки квитирования', 
                   'tabl_msg':'Имя xml файла-шаблона с сообщениями данного сигнала',
                   'group_diskrets':'Группа для группировки сообщений в архивном журнале:Общие,Диагностика,Энергоснабжение', 'msg_priority_0':'Приоритет  сообщения при 0', 
                   'msg_priority_1':'Приоритет  сообщения при 1', 'short_title':'Короткое название', 
                   'uso':'Шкаф', 'basket':'Корзина', 'module':'Модуль', 'channel':'Канал'},
            
            'do': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'pValue':'Ссылка на входное значение сигнала', 
                   'pHealth':'Ссылка на исправность канала', 'short_title':'Короткое название',
                   'uso':'Шкаф', 'basket':'Корзина', 'module':'Модуль', 'channel':'Канал'},
            
            'hardware': {'id':'№', 'tag':'Идентификатор\n(не генерится!)', 'uso':'Шкаф', 'basket':'Корзина',
                         'type_0':'Тип модуля 0',   'variable_0':'Переменная модуля 0',   'type_1':'Тип модуля 1',   'variable_1':'Переменная модуля 1',  
                         'type_2':'Тип модуля 2',   'variable_2':'Переменная модуля 2',   'type_3':'Тип модуля 3',   'variable_3':'Переменная модуля 3',  
                         'type_4':'Тип модуля 4',   'variable_4':'Переменная модуля 4',   'type_5':'Тип модуля 5',   'variable_5':'Переменная модуля 5',
                         'type_6':'Тип модуля 6',   'variable_6':'Переменная модуля 6',   'type_7':'Тип модуля 7',   'variable_7':'Переменная модуля 7',  
                         'type_8':'Тип модуля 8',   'variable_6':'Переменная модуля 8',   'type_9':'Тип модуля 9',   'variable_9':'Переменная модуля 9',  
                         'type_10':'Тип модуля 10', 'variable_10':'Переменная модуля 10', 'type_11':'Тип модуля 11', 'variable_11':'Переменная модуля 11',
                         'type_12':'Тип модуля 12', 'variable_12':'Переменная модуля 12', 'type_13':'Тип модуля 13', 'variable_13':'Переменная модуля 13', 
                         'type_14':'Тип модуля 14', 'variable_14':'Переменная модуля 14', 'type_15':'Тип модуля 15', 'variable_15':'Переменная модуля 15', 
                         'type_16':'Тип модуля 16', 'variable_16':'Переменная модуля 16', 'type_17':'Тип модуля 17', 'variable_17':'Переменная модуля 17',
                         'type_18':'Тип модуля 18', 'variable_18':'Переменная модуля 18', 'type_19':'Тип модуля 19', 'variable_19':'Переменная модуля 19', 
                         'type_20':'Тип модуля 20', 'variable_20':'Переменная модуля 20', 'type_21':'Тип модуля 21', 'variable_21':'Переменная модуля 21', 
                         'type_22':'Тип модуля 22', 'variable_22':'Переменная модуля 22', 'type_23':'Тип модуля 23', 'variable_23':'Переменная модуля 23',
                         'type_24':'Тип модуля 24', 'variable_24':'Переменная модуля 24', 'type_25':'Тип модуля 25', 'variable_25':'Переменная модуля 25', 
                         'type_26':'Тип модуля 26', 'variable_26':'Переменная модуля 26', 'type_27':'Тип модуля 27', 'variable_27':'Переменная модуля 27', 
                         'type_28':'Тип модуля 28', 'variable_28':'Переменная модуля 28', 'type_29':'Тип модуля 29', 'variable_29':'Переменная модуля 29',
                         'type_30':'Тип модуля 30', 'variable_30':'Переменная модуля 30', 'type_31':'Тип модуля 31', 'variable_31':'Переменная модуля 31', 
                         'type_32':'Тип модуля 32', 'variable_32':'Переменная модуля 32'},
            
            'uso': {'id':'№','variable':'Переменная', 'name':'Название', 'temperature':'Температура шкафа', 'door':'Двери открыты', 
                         'signal_1':'Сигнал 1', 'signal_2':'Сигнал 2', 'signal_3':'Сигнал 3', 'signal_4':'Сигнал 4', 'signal_1':'Сигнал 5', 
                         'signal_6':'Сигнал 6', 'signal_7':'Сигнал 7', 'signal_8':'Сигнал 8', 'signal_9':'Сигнал 9', 'signal_10':'Сигнал 10', 
                         'signal_11':'Сигнал 11', 'signal_12':'Сигнал 12', 'signal_13':'Сигнал 13', 'signal_14':'Сигнал 14', 'signal_15':'Сигнал 15', 
                         'signal_16':'Сигнал 16', 'signal_17':'Сигнал 17', 'signal_18':'Сигнал 18', 'signal_19':'Сигнал 19', 'signal_20':'Сигнал 20', 
                         'signal_21':'Сигнал 21', 'signal_22':'Сигнал 22', 'signal_23':'Сигнал 23', 'signal_24':'Сигнал 24', 'signal_25':'Сигнал 25', 
                         'signal_26':'Сигнал 26', 'signal_27':'Сигнал 27', 'signal_28':'Сигнал 28', 'signal_29':'Сигнал 29', 'signal_30':'Сигнал 30', 
                         'signal_31':'Сигнал 31', 'signal_32':'Сигнал 32'},
            
            'ao': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'pValue':'Ссылка на входное значение сигнала',
                   'pHealth':'Ссылка на исправность канала', 'uso':'Шкаф', 'basket':'Корзина', 'module':'Модуль', 'channel':'Канал'},
            
            'ai': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'pValue':'Ссылка на входное значение сигнала',
                   'pHealth':'Ссылка на исправность канала','group_analog':'Группа аналогов',
                   'group_ust_analog':'Группа уставок аналогов', 'unit':'Единица измерения', 'sign_VU':'Подпись для ВУ', 
                   'flag_MPa_kgccm2':'Давление нефти/ нефтепродукта (флаг для пересчета в кгс/см2)', 'number_NA_or_aux':'Номер НА или вспом.', 
                   'vibration_pump':'Вибрация насоса', 'vibration_motor':'Вибрация ЭД', 'current_motor':'Ток ЭД НА', 
                   'aux_outlet_pressure':'Давление на вых. вспом.', 'number_ust_min_avar':'№ уставки мин. авар.', 
                   'number_ust_min_pred':'№ уставки мин. пред.', 'number_ust_max_pred':'№ уставки макс. пред.', 'number_ust_max_avar':'№ уставки макс. авар.', 
                   'field_min':'Пол. мин.', 'field_max':'Пол. макс.', 'eng_min':'Инж. Мин.', 'eng_max':'Инж. Макс.', 'reliability_min':'Достоверность мин.', 
                   'reliability_max':'Достоверность макс.', 'hysteresis':'Гистерезис', 'filtration':'Фильтрация', 
                   'ust_min_6':'Мин.6', 'ust_min_5':'Мин.5', 'ust_min_4':'Мин.4', 'ust_min_3':'Мин.3', 'ust_min_2':'Мин.2', 'ust_min':'Мин.', 
                   'ust_max':'Макс.', 'ust_max_2':'Макс.2', 'ust_max_3':'Макс.3', 'ust_max_4':'Макс.4', 'ust_max_5':'Макс.5', 'ust_max62':'Макс.6', 
                   'value_precision':'Отображаемая точность значения', 'Pic':'Номера листов на которых данный сигнал участвует в формировании рамки квитирования', 
                   'group_trend':'Группа сброса трендов', 'hysteresis_TI':'Гистерезис ТИ', 'unit_physical_ACP':'Единица измерения физической величины (АЦП)',
                   'setpoint_map_rule':'Правило для карты уставок', 'fuse':'Предохранитель',
                   'uso':'Шкаф', 'basket':'Корзина', 'module':'Модуль', 'channel':'Канал'},
            
            'ktpr': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название',
                     'avar_parameter':'Аварийный параметр(pInput)', 
                     'prohibition_masking':'Запрет маскирования(1 - запрет)', 
                     'auto_unlock_protection':'Автоматическая деблокировка защиты(1 - разрешена)', 
                     'shutdown_PNS_a_time_delay_up_5s_after_turning_off_all_NA':'Отключение ПНС с выдержкой времени до 5 с после отключения всех МНА',
                     'bitmask_protection_group_membership':'Битовая маска принадлежности защиты группе(1 в N бите - разрешение сработки данной защиты на N группе (плече))', 
                     'stop_type_NA':'Тип остановки НА(0-None, 1-ManageStop, 2-ElectricStop, 3-ManageStopOffVV, 4-ChRPAlarmStop, 5-StopAuto, 6-StopAuto2, 7-PovtorOtkl)',
                     'pump_station_stop_type':'''Тип остановки насосной станции(описание РД242, ч1, стр61, табл.9.3,п.8, 
                     1 - StopAllInShoulder - одновремменная остановка всех НА в плече, 
                     2 - StopOneByOneInShoulder - последовательная остановка всех НА в плече, 
                     3 - StopFirstNextInShoulder - отключение первого по потоку нефти/нефтепродукта НА, и отключения следующего при сохранении аврийного параметра, 
                     4 - StopOnlyirstInShoulder - отключение первого по потоку нефти/нефтепродукта НА, 
                     5 - StopAllInSubShoulder - одновреммення остановка всех ПН в подплече)''',

                     'closing_gate_valves_at_the_inlet_NPS':'Закрытие задвижек на входе НПС', 
                     'closing_gate_valves_at_the_outlet_NPS':'Закрытие задвижек на выходе НПС', 
                     'closing_gate_valves_between_PNS_and_MNS':'Закрытие задвижек между ПНС и МНС', 
                     'closing_gate_valves_between_RP_and_PNS':'Закрытие задвижек между РП и ПНС', 
                     'closing_valves_inlet_and_outlet_MNS':'Закрытие задвижек на входе и выходе МНС', 
                     'closing_valves_inlet_and_outlet_PNS':'Закрытие задвижек на входе и выходе ПНС', 
                     'closing_valves_inlet_and_outlet_MNA':'Закрытие задвижек на входе и выходе МНА', 
                     'closing_valves_inlet_and_outlet_PNA':'Закрытие задвижек на входе и выходе ПНА', 
                     'closing_valves_inlet_RD':'Закрытие задвижек на входе узла РД', 
                     'closing_valves_outlet_RD':'Закрытие задвижек на выходе узла РД', 
                     'closing_valves_inlet_SSVD':'Закрытие задвижек на входе ССВД', 
                     'closing_valves_inlet_FGU':'Закрытие задвижек на входе ФГУ', 
                     'closing_secant_valve_connection_unit__oil_production_oil_refining_facility':'Закрытие секущей задвижки узла подключения объекта нефтедобычи/ нефтепереработки',
                     'closing_valves_inlet_RP':'Закрытие задвижек на входе РП', 
                     'reserve_protect_14':'Резерв(14 бит)', 
                     'reserve_protect_15':'Резерв(15 бит)',

                     'shutdown_oil_pumps':'Отключение маслонасосов', 
                     'shutdown_oil_pumps_after_signal_stopped_NA':'Отключение маслонасосов после сигнала "остановлен" НА', 
                     'shutdown_circulating_water_pumps':'Отключение насосов оборотного водоснабжения', 
                     'shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_MNS':'Отключение насосов откачки из емкостей сбора утечек МНС', 
                     'shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_PNS':'Отключение насосов откачки из емкостей сбора утечек ПНС', 
                     'shutdown_pumps_pumping_out_from_tanks_SSVD':'Отключение насосов откачки из емкостей ССВД',
                     'switching_off_the_electric_room_fans':'Отключение беспромвальных вентиляторов электрозала', 
                     'shutdown_of_booster_fans_ED':'Отключение подпорных вентиляторов ЭД', 
                     'shutdown_of_retaining_fans_of_the_electrical_room':'Отключение подпорных вентиляторов электрозала', 
                     'shutdown_of_ED_air_compressors':'Отключение компрессоров подпора воздуха ЭД', 
                     'shutdown_pumps_providing_oil_oil_product_pumping_from_oil_production_oil_refining_facilities':'Отключение насосов, обеспечивающих подкачку нефти/нефтепродукта от объектов нефтедобычи/нефтепереработки', 
                     'disabling_pumps_for_pumping_oil_oil_products_through_BIC':'Отключение насосов прокачки нефти/нефтепродукта через БИК', 
                     'shutdown_domestic_and_drinking_water_pumps':'Отключение насосов хозяйственно-питьевого водоснабжения', 
                     'shutdown_of_art_well_pumps':'Отключение насосов артскважин', 
                     'AVO_shutdown':'Отключение АВО', 
                     'shutdown_of_water_cooling_fans_circulating_water_supply_system':'Отключение вентиляторов водоохлаждения системы оборотного водоснабжения', 
                    
                     'shutdown_exhaust_fans_of_the_pumping_room_of_the_MNS':'Отключение вытяжных вентиляторов насосного зала МНС', 
                     'shutdown_of_exhaust_fans_of_the_pumping_room_PNS':'Отключение вытяжных вентиляторов насосного зала ПНС', 
                     'shutdown_of_exhaust_fans_in_the_centralized_oil_system_room':'Отключение вытяжных вентиляторов в помещении централизованной маслосистемы', 
                     'shutdown_of_exhaust_fans_oil_pit_in_the_electrical_room':'Отключение вытяжных вентиляторов маслоприямка в электрозале', 
                     'shutdown_of_exhaust_fans_in_the_RD_room':'Отключение вытяжных вентиляторов в помещении РД', 
                     'shutdown_of_exhaust_fans_in_the_SSVD_room':'Отключение вытяжных вентиляторов в помещении ССВД', 
                     'shutdown_of_the_roof_fans_of_the_MNS_pump_room':'Отключение крышных вентиляторов насосного зала МНС', 
                     'shutdown_of_the_roof_fans_of_the_PNS_pump_room':'Отключение крышных вентиляторов насосного зала ПНС', 
                     'switching_off_the_supply_fans_pumping_room_of_the_MNS_and_closing_the_fire_dampers':'Отключение приточных вентиляторов насосного зала МНС и закрытие огнезадерживающих клапанов', 
                     'switching_off_the_supply_fans_pumping_room_of_the_PNS_and_closing_the_fire_dampers':'Отключение приточных вентиляторов насосного зала ПНС и закрытие огнезадерживающих клапанов', 
                     'switch_off_the_supply_fans_in_the_centralized_oil_system_room_and_close_the_fire_dampers':'Отключение приточных вентиляторов в помещении централизованной маслосистемы и закрытие огнезадерживающих клапанов', 
                     'switching_off_the_supply_fan_of_the_RD_room':'Отключение приточного вентилятора помещения РД', 
                     'switching_off_the_supply_fan_of_the_SSVD_room':'Отключение приточного вентилятора помещения ССВД', 
                     'switching_off_the_supply_fans_of_the_ED_air_compressor_room_and_closing_the_fire_dampers':'Отключение приточных вентиляторов помещения компрессорной подпора воздуха ЭД и закрытие огнезадерживающих клапанов', 
                     'switching_off_the_supply_fan_of_the_BIK_room':'Отключение приточного вентилятора помещения БИК', 
                     'switching_off_the_supply_fan_of_the_SIKN_room':'Отключение приточного вентилятора помещения СИКН', 

                     'closing_the_air_valves_louvered_grilles_of_the_pump_room':'Закрытие воздушных клапанов (жалюзийных решёток) насосного зала', 
                     'closing_of_air_valves_louvered_grilles_of_the_compressor_room_of_the_ED_air_overpressure':'Закрытие воздушных клапанов (жалюзийных решёток) помещения компрессорной подпора воздуха ЭД', 
                     'shutdown_of_electric_oil_heaters':'Отключение электронагревателей масла', 
                     'shutdown_of_the_electric_heaters_of_the_leakage_collection_tank_MNS':'Отключение электронагревателей емкости сбора утечек МНС', 
                     'shutdown_of_the_electric_heaters_of_the_leakage_collection_tank_PNS':'Отключение электронагревателей емкости сбора утечек ПНС', 
                     'shutdown_of_electric_heaters_of_the_SIKN_leak_collection_tank':'Отключение электронагревателей емкости сбора утечек СИКН', 
                     'shutdown_of_air_coolers_of_the_locking_system_of_mechanical_seals_of_all_MNA':'Отключение воздушных охладителей системы запирания торцовых уплотнений всех МНА', 
                     'shutdown_of_air_coolers_of_the_locking_system_of_mechanical_seals_disconnected_NA':'Отключение воздушных охладителей системы запирания торцовых уплотнений отключенных НА', 
                     'shutdown_of_the_external_cooling_circuit_ChRP_MNA':'Отключение внешнего контура охлаждения ЧРП МНА', 
                     'shutdown_of_the_external_cooling_circuit_ChRP_PNA':'Отключение внешнего контура охлаждения ЧРП ПНА', 
                     'shutdown_of_locking_system_pumps':'Отключение насосов системы запирания',
                     'shutdown_of_pumps_for_pumping_oil_oil_products_through_the_operational_BIK':'Отключение насосов прокачки нефти/нефтепродукта через оперативный БИК', 
                     'shutdown_of_pumping_pumps_from_leakage_collection_tanks_of_all_SIKN':'Отключение насосов откачки из емкостей сбора утечек всех СИКН', 
                     'shutdown_of_anticondensation_electric_heaters_ED':'Отключение антиконденсационных электронагревателей ЭД', 
                     'fire_protection':'Защита по пожару', 
                     'reserve_aux_15':'Резерв(15 бит)', 

                     'time_ust':'Временная уставка', 
                     'Pic':'Номера листов на которых данный сигнал участвует в формировании рамки квитирования',
                     'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок', 'number_list_VU':'Номер листа (для ВУ)', 'number_protect_VU':'Номер защиты (для ВУ)'},
            
            'ktpra': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'NA':'Имя НА', 'avar_parameter':'Аварийный параметр', 
                    'stop_type':'''Тип остановки(0 - None,\n1 - ManageStop,\n2 - ElectricStop,\n3 - ManageStopOffVV,\n4 - ChRPAlarmStop,\n5 - StopAuto,\n6 - StopAuto2,\n7 - PovtorOtkl1)''',  
                    'AVR':'Флаг необходимости АВР НА при срабатывании защиты' , 'close_valves':'Флаг необходимости закрытия агрегатных задвижек НА при срабатывании защиты', 
                    'prohibition_of_masking':'Флаг запрета маскирования', 'time_setting':'Временная уставка', 
                    'Pic':'Номера листов на которых данный сигнал участвует в формировании рамки квитирования', 'group_ust':'Группа уставок', 
                    'rule_map_ust':'Правило для карты уставок', 
                    'number_list_VU':'Номер листа (для ВУ)', 'number_protect_VU':'Номер защиты (для ВУ)', 'number_pump_VU':'Номер агрегата (для ВУ)'},
            
            'ktprs': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название',
                       'drawdown':'Сработка', 'reference_to_value':'Ссылка на значение', 'priority_msg_0':'Приоритет сообщ. при 0', 
                       'priority_msg_1':'Приоритет сообщ. при 1',
                       'prohibition_issuing_msg':'Запрет выдачи сообщений', 
                       'Pic':'Номера листов на которых данный сигнал участвует в формировании рамки квитирования'},
            
            'gmpna': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 
                      'name_for_Chrp_in_local_mode':'Название для ЧРП в местном режиме', 'NA':'Имя НА', 'time_setting':'Использовать временную уставку', 
                      'setting':'Уставка', 'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок', 
                      'number_list_VU':'Номер листа (для ВУ)', 'number_protect_VU':'Номер защиты (для ВУ)', 'number_pump_VU':'Номер агрегата (для ВУ)'},
            
            'umpna':{'id':'№','variable':'Переменная', 'name':'Название', 'vv_included':'ВВ Включен', 'vv_double_included':'ВВ Включен дубль', 'vv_disabled':'ВВ отключен', 'vv_double_disabled':'ВВ отключен дубль', 
                     'current_greater_than_noload_setting':'Сила тока >  уставки холостого хода', 'serviceability_of_circuits_of_inclusion_of_VV':'Исправность цепей включения ВВ',
                     'serviceability_of_circuits_of_shutdown_of_VV':'Исправность цепей отключения ВВ', 'serviceability_of_circuits_of_shutdown_of_VV_double':'Исправность цепей отключения ВВ дубль', 'stop_1':'Стоп 1', 
                     'stop_2':'Стоп 2', 'stop_3':'Стоп 3', 'stop_4':'Стоп 4', 
                     'monitoring_the_presence_of_voltage_in_the_control_current_circuits':'Сигнал «Контроль наличия напряжения в цепях оперативного тока»', 
                     'voltage_presence_flag_in_the_ZRU_motor_cell':'Флаг наличия напряжения в двигательной ячейке ЗРУ', 'vv_trolley_rolled_out':'Тележка ВВ выкачена', 
                     'remote_control_mode_of_the_RZiA_controller':'Дистанционный режим управления контроллера РЗиА', 
                     'availability_of_communication_with_the_RZiA_controller':'Наличие связи с контроллером РЗиА', 
                     'the_state_of_the_causative_agent_of_ED':'Состояние возбудителя ЭД', 'engine_prepurge_end_flag':'Флаг окончания предпусковой продувки двигателя', 
                     'flag_for_the_presence_of_safe_air_boost_pressure_in_the_engine_housing':'Флаг наличия безопасного давления подпора воздуха в корпусе двигателя', 
                     'flag_for_the_presence_of_safe_air_boost_pressure_in_the_exciter_housing':'Флаг наличия безопасного давления подпора воздуха в корпусе возбудителя', 
                     'engine_purge_valve_closed_flag':'Флаг закрытого положения клапана продувки двигателя', 
                     'oil_system_oil_temperature_flag_is_above_10_at_the_cooler_outlet_for_an_individual_oil_system':'Флаг температуры масла маслосистемы выше 10гр.С на выходе охладителя (для индивидуальной маслосистемы)', 
                     'flag_for_the_minimum_oil_level_in_the_oil_tank_for_an_individual_oil_system':'Флаг предельного минимального уровня масла в маслобаке (для индивидуальной маслосистемы)', 
                     'flag_for_the_presence_of_the_minimum_level_of_the_barrier_liquid_in_the_tank_of_the_locking_system':'Флаг наличия минимального уровня запирающей жидкости в баке системы запирания',
                     'generalized_flag_for_the_presence_of_barrier_fluid_pressure_to_the_mechanical_seal':'Обобщенный флаг наличия давления запирающей жидкости к торцевому уплотнению', 
                     'command_to_turn_on_the_vv_only_for_UMPNA':'Команда на включение ВВ (только для UMPNA)', 
                     'command_to_turn_off_the_vv_output_1':'Команда на отключение ВВ (выход 1)',
                     'command_to_turn_off_the_vv_output_2':'Команда на отключение ВВ (выход 2)', 'NA_Chrp':'НА с ЧРП', 'type_NA_MNA':'Тип НА - МНА(1 - МНА, 0 - ПНА)', 'pump_type_NM':'Насос типа НМ(1 - НМ)', 
                     'parametr_KTPRAS_1':'Параметр для KTPRAS_1', 
                     'number_of_delay_scans_of_the_analysis_of_the_health_of_the_control_circuits_NA_MNA':'Количество сканов задержки анализа исправности цепей управления ВВ НА', 
                     'unit_number_of_the_auxiliary_system_start_up_oil_pump_for_an_individual_oil_system':'Номер агрегата вспомсистемы "пуско-резервный маслонасос" (для индивидуальной маслосистемы)', 
                     'NPS_number_1_or_2_which_the_AT_belongs':'Номер НПС (1 или 2), к которой относится НА', 
                     'achr_protection_number_in_the_array_of_station_protections':'Номер защиты АЧР в массиве станционных защит', 
                     'saon_protection_number_in_the_array_of_station_protections':'Номер защиты САОН в массиве станционных защит', 
                     'gmpna_49':'GMPNA_[49]', 'gmpna_50':'GMPNA_[50]', 'gmpna_51':'GMPNA_[51]', 'gmpna_52':'GMPNA_[52]', 'gmpna_53':'GMPNA_[53]', 'gmpna_54':'GMPNA_[54]',
                     'gmpna_55':'GMPNA_[55]', 'gmpna_56':'GMPNA_[56]', 'gmpna_57':'GMPNA_[57]', 'gmpna_58':'GMPNA_[58]', 'gmpna_59':'GMPNA_[59]', 'gmpna_51':'GMPNA_[60]', 
                     'gmpna_51':'GMPNA_[61]', 'gmpna_51':'GMPNA_[62]', 'gmpna_51':'GMPNA_[63]', 'gmpna_51':'GMPNA_[64]', 
                     'Pic':'Номера листов на которых данный сигнал участвует в формировании рамки квитирования', 
                     'replacement_uso_signal_vv_1':'Замена %1 - УСО сигналов ВВ 1\n(Строка для замены %1 в сообщениях)', 
                     'replacement_uso_signal_vv_2':'Замена %2 - УСО сигналов ВВ 2\n(Строка для замены %2 в сообщениях)'},
            
            'umpna_tm': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'unit':'Единица измерения', 'used':'Используется', 'value_ust':'Значение уставки', 'minimum':'Минимум', 
                       'maximum':'Максимум', 'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок'},
            
            'zd': {'id':'№','variable':'Переменная', 'name':'Название', 'short_name':'Короткое название', 'exists_interface':'Наличие ИНТЕРФЕЙСА', 'KVO':'КВО', 'KVZ':'КВЗ', 'MPO':'МПО', 
                   'MPZ':'МПЗ', 'Dist':'Дист_ф', 'Mufta':'Муфта', 'Drive_failure':'Авария привода', 'Open':'Открыть', 'Close':'Закрыть', 'Stop':'Остановить', 'Opening_stop':'Открытие остановить', 
                   'Closeing_stop':'Закрытие остановить', 'KVO_i':'КВО_и', 'KVZ_i':'КВЗ_и', 'MPO_i':'МПО_и', 'MPZ_i':'МПЗ_и', 'Dist_i':'Дист_и', 'Mufta_i':'Муфта_и','Drive_failure_i':'Авария привода_и', 
                   'Open_i':'Открыть_и', 'Close_i':'Закрыть_и', 'Stop_i':'Остановить_и', 'Opening_stop_i':'Открытие остановить_и','Closeing_stop_i':'Закрытие остановить_и', 'No_connection':'Отсутствие связи', 
                   'Close_BRU':'Закрыть с БРУ', 'Stop_BRU':'Стоп с БРУ', 'Voltage':'Напряжение', 'Voltage_CHSU':'Напряжение ЩСУ', 'Voltage_in_signaling_circuits':'Напряжение в цепях сигнализации', 
                   'Serviceability_opening_circuits':'Исправность цепей открытия', 'Serviceability_closening_circuits':'Исправность цепей закрытия', 'VMMO':'ВММО', 'VMMZ':'ВММЗ', 
                   'Freeze_on_suspicious_change':'Замораживать при подозрительном изм', 'Is_klapan':'Это клапан', 'Opening_percent':'Процент открытия', 'Pic':'Pic', 'Type_BUR_ZD':'Тип БУР задвижки', 
                   'AlphaHMI':'AlphaHMI', 'AlphaHMI_PIC1':'AlphaHMI_PIC1', 'AlphaHMI_PIC1_Number_kont':'AlphaHMI_PIC1_Number_kont', 'AlphaHMI_PIC2':'AlphaHMI_PIC2',
                   'AlphaHMI_PIC2_Number_kont':'AlphaHMI_PIC2_Number_kont','AlphaHMI_PIC3':'AlphaHMI_PIC3', 'AlphaHMI_PIC3_Number_kont':'AlphaHMI_PIC3_Number_kont', 
                   'AlphaHMI_PIC4':'AlphaHMI_PIC4', 'AlphaHMI_PIC4_Number_kont':'AlphaHMI_PIC4_Number_kont'},

            'zd_tm': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'unit':'Единица измерения', 'used':'Используется', 'value_ust':'Значение уставки', 'minimum':'Минимум', 
                       'maximum':'Максимум', 'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок'},

            'vs': {'id':'№','variable':'Переменная', 'name':'Название', 'short_name':'Короткое название', 'group':'Группа', 'number_in_group':'Номер в группе', 'MP':'МП', 'Pressure_is_True':'Давление норма', 
                   'Voltage':'Напряжение', 'Voltage_Sch':'Напряжение на СШ', 'Serviceability_of_circuits_of_inclusion':'Исправность цепей включения', 'External_alarm':'Внешняя авария', 'Pressure_sensor_defective':'Датчик давления неисправен', 
                   'VKL':'Включить', 'OTKL':'Отключить', 'Not_APV':'АПВ не требуется', 'Pic':'Pic', 'Table_msg':'Таблица сообщений', 'Is_klapana_interface_auxsystem':'Это клапан/интерфейсная вспомсистема',
                   'AlphaHMI':'AlphaHMI', 'AlphaHMI_PIC1':'AlphaHMI_PIC1', 'AlphaHMI_PIC1_Number_kont':'AlphaHMI_PIC1_Number_kont', 'AlphaHMI_PIC2':'AlphaHMI_PIC2',
                   'AlphaHMI_PIC2_Number_kont':'AlphaHMI_PIC2_Number_kont','AlphaHMI_PIC3':'AlphaHMI_PIC3', 'AlphaHMI_PIC3_Number_kont':'AlphaHMI_PIC3_Number_kont', 
                   'AlphaHMI_PIC4':'AlphaHMI_PIC4', 'AlphaHMI_PIC4_Number_kont':'AlphaHMI_PIC4_Number_kont'},

            'vs_tm': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'unit':'Единица измерения', 'used':'Используется', 'value_ust':'Значение уставки', 'minimum':'Минимум', 
                       'maximum':'Максимум', 'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок'},

            'vsgrp': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'fire_or_watering':'Пож или водоорош', 'Number_of_auxsystem_in_group':'Количество вспомсистем в группе',
                      'WarnOff_flag_if_one_auxsystem_in_the_group_is_running':'Требуется выставлять флаг WarnOff если работает одна вспомсистема в группе'},

            'vsgrp_tm': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'unit':'Единица измерения', 'used':'Используется', 'value_ust':'Значение уставки', 'minimum':'Минимум', 
                       'maximum':'Максимум', 'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок'},

            'uts': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'location':'Место_установки', 'VKL':'Включить', 'siren':'Сирена', 'Does_not_require_autoshutdown':'Не требует автоотключения', 
                    'Examination':'Проверка', 'Kvit':'Квитирование', 'Pic':'Pic', 'number_list_VU':'Номер листа для ВУ', 'order_number_for_VU':'Номер порядка для ВУ', 
                    'uso':'Шкаф', 'basket':'Корзина', 'module':'Модуль', 'channel':'Канал'},

            'uts_tm': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'unit':'Единица измерения', 'used':'Используется', 'value_ust':'Значение уставки', 'minimum':'Минимум', 
                       'maximum':'Максимум', 'group_ust':'Группа уставок', 'rule_map_ust':'Правило для карты уставок'},

            'vv': {'id':'№','variable':'Переменная', 'name':'Название', 'VV_vkl':'Высоковольтный выключатель включен', 'VV_otkl':'Высоковольтный выключатель отключен', 'Pic':'Pic'},
            
            'pi': {'id':'№','variable':'Переменная', 'tag':'Идентификатор', 'name':'Название', 'Type_PI':'Тип_ПИ(1 - пламени, 2 - тепловой, 3 - дымовой, 4 - АПУ, 5 - тепловой аналоговый)', 
                   'Fire_0':'Пожар 0', 'Attention_1':'Внимание 1', 'Fault_1_glass_pollution_broken_2':'Неисправность 1 загрязнение стекла обрыв 2', 'Fault_2_fault_KZ_3':'Неисправность 2 неисправность КЗ 3', 
                   'Yes_connection_4':'Есть связь 4', 'Frequency_generator_failure_5':'Неисправность генератора частоты 5','Parameter_loading_error_6':'Ошибка загрузки параметров 6', 
                   'Communication_error_module_IPP_7':'Ошибка связи с модулем ИПП 7', 'Supply_voltage_fault_8':'Неисправность напряжения питания 8', 'Optics_contamination_9':'Загрязнение оптики 9',
                   'IK_channel_failure_10':'Неисправность ИК канала_10', 'UF_channel_failure_11':'Неисправность УФ канала_11', 'Loading_12':'Загрузка 12', 'Test_13':'Тест 13', 'Reserve_14':'Резерв 14',
                   'Reset_Link':'Сброс ссылка', 'Reset_Request':'Сброс запроса', 'Through_loop_number_for_interface':'Сквозной номер шлейфа для интерфейсных', 'location':'Место установки', 'Pic':'Pic','Normal':'Норма'}, 
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
    Pic = CharField(null = True)
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
    Pic = CharField(null = True)
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
    Pic = CharField(null = True)
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
    Pic = CharField(null = True)
    
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
class tmNA_UMPNA(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    unit = CharField(null = True)
    used = CharField(null = True)
    value_ust = CharField(null = True)
    minimum = CharField(null = True)
    maximum = CharField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    class Meta:
        table_name = 'tmna_umpna'
class UMPNA(BaseModel):
    variable = CharField(null = True)
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

    monitoring_the_presence_of_voltage_in_the_control_current_circuits = CharField(null = True)
    voltage_presence_flag_in_the_ZRU_motor_cell = CharField(null = True)
    vv_trolley_rolled_out = CharField(null = True)
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

    Pic = CharField(null = True)
    replacement_uso_signal_vv_1 = CharField(null = True)
    replacement_uso_signal_vv_2 = CharField(null = True)

    class Meta:
        table_name = 'umpna'
class ZD(BaseModel):
    variable = CharField(null = True)
    name = CharField(null = True)
    short_name = CharField(null = True)
    exists_interface = CharField(null = True)

    KVO = CharField(null = True)
    KVZ = CharField(null = True)
    MPO = CharField(null = True)
    MPZ = CharField(null = True)
    Dist = CharField(null = True)
    Mufta = CharField(null = True)
    Drive_failure = CharField(null = True)
    Open = CharField(null = True)
    Close = CharField(null = True)
    Stop = CharField(null = True)
    Opening_stop = CharField(null = True)
    Closeing_stop = CharField(null = True)

    KVO_i = CharField(null = True)
    KVZ_i  = CharField(null = True)
    MPO_i  = CharField(null = True)
    MPZ_i  = CharField(null = True)
    Dist_i  = CharField(null = True)
    Mufta_i  = CharField(null = True)
    Drive_failure_i  = CharField(null = True)
    Open_i  = CharField(null = True)
    Close_i  = CharField(null = True)
    Stop_i  = CharField(null = True)
    Opening_stop_i  = CharField(null = True)
    Closeing_stop_i  = CharField(null = True)
    
    No_connection = CharField(null = True)
    Close_BRU = CharField(null = True)
    Stop_BRU = CharField(null = True)
    Voltage = CharField(null = True)
    Voltage_CHSU= CharField(null = True)
    Voltage_in_signaling_circuits = CharField(null = True)
    Serviceability_opening_circuits = CharField(null = True)
    Serviceability_closening_circuits = CharField(null = True)
    VMMO = CharField(null = True)
    VMMZ = CharField(null = True)
    Freeze_on_suspicious_change = CharField(null = True)
    Is_klapan = CharField(null = True)
    Opening_percent = CharField(null = True)
    Pic = CharField(null = True)
    Type_BUR_ZD = CharField(null = True)

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
        table_name = 'zd'
class ZD_tm(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    unit = CharField(null = True)
    used = CharField(null = True)
    value_ust = CharField(null = True)
    minimum = CharField(null = True)
    maximum = CharField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    class Meta:
        table_name = 'zd_tm'
class VS(BaseModel):
    variable = CharField(null = True)
    name = CharField(null = True)
    short_name = CharField(null = True)
    group = CharField(null = True)
    number_in_group = CharField(null = True)
    MP = CharField(null = True)
    Pressure_is_True = CharField(null = True)
    Voltage = CharField(null = True)
    Voltage_Sch = CharField(null = True)
    Serviceability_of_circuits_of_inclusion = CharField(null = True)
    External_alarm = CharField(null = True)
    Pressure_sensor_defective = CharField(null = True)
    VKL = CharField(null = True)
    OTKL = CharField(null = True)
    Not_APV = CharField(null = True)
    Pic = CharField(null = True)
    Table_msg = CharField(null = True)
    Is_klapana_interface_auxsystem = CharField(null = True)
    
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
        table_name = 'vs'
class VS_tm(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    unit = CharField(null = True)
    used = CharField(null = True)
    value_ust = CharField(null = True)
    minimum = CharField(null = True)
    maximum = CharField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    class Meta:
        table_name = 'vs_tm'   
class VSGRP(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    fire_or_watering = CharField(null = True)
    Number_of_auxsystem_in_group = CharField(null = True)
    WarnOff_flag_if_one_auxsystem_in_the_group_is_running = CharField(null = True)

    class Meta:
        table_name = 'vsgrp'
class VSGRP_tm(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    unit = CharField(null = True)
    used = CharField(null = True)
    value_ust = CharField(null = True)
    minimum = CharField(null = True)
    maximum = CharField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    class Meta:
        table_name = 'vsgrp_tm'
class UTS(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    location = CharField(null = True)
    VKL = CharField(null = True)
    siren = CharField(null = True)
    Does_not_require_autoshutdown = CharField(null = True)
    Examination = CharField(null = True)
    Kvit = CharField(null = True)
    Pic = CharField(null = True)
    number_list_VU = CharField(null = True)
    order_number_for_VU = CharField(null = True)
    uso = CharField(null = True)
    basket = IntegerField(null = True)
    module = IntegerField(null = True)
    channel = IntegerField(null = True)

    class Meta:
        table_name = 'uts'
class UTS_tm(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    unit = CharField(null = True)
    used = CharField(null = True)
    value_ust = CharField(null = True)
    minimum = CharField(null = True)
    maximum = CharField(null = True)
    group_ust = CharField(null = True)
    rule_map_ust = CharField(null = True)

    class Meta:
        table_name = 'uts_tm'   
class VV(BaseModel):
    variable = CharField(null = True)
    name = CharField(null = True)
    VV_vkl = CharField(null = True)
    VV_otkl = CharField(null = True)
    Pic = CharField(null = True)

    class Meta:
        table_name = 'vv'   
class PI(BaseModel):
    variable = CharField(null = True)
    tag = CharField(null = True)
    name = CharField(null = True)
    Type_PI = CharField(null = True)
    Fire_0 = CharField(null = True)
    Attention_1 = CharField(null = True)
    Fault_1_glass_pollution_broken_2 = CharField(null = True)
    Fault_2_fault_KZ_3 = CharField(null = True)
    Yes_connection_4 = CharField(null = True)
    Frequency_generator_failure_5 = CharField(null = True)
    Parameter_loading_error_6 = CharField(null = True)
    Communication_error_module_IPP_7 = CharField(null = True)
    Supply_voltage_fault_8 = CharField(null = True)
    Optics_contamination_9 = CharField(null = True)
    IK_channel_failure_10 = CharField(null = True)
    UF_channel_failure_11 = CharField(null = True)
    Loading_12 = CharField(null = True)
    Test_13 = CharField(null = True)
    Reserve_14 = CharField(null = True)
    Reset_Link = CharField(null = True)
    Reset_Request = CharField(null = True)
    Through_loop_number_for_interface = CharField(null = True)
    location = CharField(null = True)
    Pic = CharField(null = True)
    Normal = CharField(null = True)

    class Meta:
        table_name = 'pi'  
