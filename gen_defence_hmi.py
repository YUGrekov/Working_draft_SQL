from lxml import etree
import openpyxl
import uuid
import math
import shutil
import os
from loguru import logger

reset_button_designed = {'1' : ['X'       , '901', '2'],
                         '2' : ['Y'       , ''   , '2'],
                         '3' : ['Rotation', '0'  , '2'],
                         '4' : ['Width'   , '200', '2'],
                         '5' : ['Height'  , '30' , '2'],

}
reset_button_init_KTPR = {'2' : ['IsKTPRA'                           , ''  , '4'],
}
reset_button_init_KTPRA= {'2' : ['IsKTPRA'                           , ''  , '4'],
                          '3' : ['MAnumber'                          , ''  , '4'],
}

attrib_defence_top = {'1' : ['X'       , '1'  , '4'],
                      '2' : ['Y'       , '1'  , '4'],
                      '3' : ['Rotation', '0'  , '4'],
                      '4' : ['Width'   , '800', '4'],
                      '5' : ['Height'  , '26' , '4'],
                      '6' : ['Visible' , ''   , '4']
}
attrib_defence_row_design = {'1' : ['X'       , '0'  , '4'],
                             '2' : ['Y'       , 26   , '4'],
                             '3' : ['Rotation', '0'  , '4'],
                             '4' : ['Width'   , '800', '4'],
                             '5' : ['Height'  , '25' , '4'],
}

attrib_row_init_KTPR = {'1' : ['_link_init_ApSource_type_defence_row'    , '4'],
                        '2' : ['_init_group_number'                      , '4'],
                        '3' : ['_init_row_number'                        , '4'],
                        '4' : ['_def_name'                               , '4'],
                        '5' : ['_def_number'                             , '4'],
                        '6' : ['_link_init_ApSource_type_defence_row_cmd', '4'],
                        '7' : ['_def_number_inarray'                     , '4'],
                        '8' : ['IsKTPRA'                                 , '4'],
}
attrib_row_init_KTPRA = {'1' : ['_link_init_ApSource_type_defence_row'    , '4'],
                         '2' : ['_init_group_number'                      , '4'],
                         '3' : ['_init_row_number'                        , '4'],
                         '4' : ['_def_name'                               , '4'],
                         '5' : ['_def_number'                             , '4'],
                         '6' : ['_link_init_ApSource_type_defence_row_cmd', '4'],
                         '7' : ['_def_number_inarray'                     , '4'],
                         '8' : ['IsKTPRA'                                 , '4'],
                         '9' : ['MAnumber'                                , '4']
}
attrib_row_init_GMPNA = {'1' : ['_link_init_ApSource_type_readiness_row'    , '4'],
                         '2' : ['_init_group_number'                        , '4'],
                         '3' : ['_init_row_number'                          , '4'],
                         '4' : ['_readiness_name'                           , '4'],
                         '5' : ['_readiness_number'                         , '4'],
                         '6' : ['_link_init_ApSource_type_readiness_row_cmd', '4'],
                         '7' : ['_readiness_number_inarray'                 , '4'],
                         '9' : ['MAnumber'                                  , '4']
}

button_designed = {'1' : ['X'       , '1'  , '4'],
                   '2' : ['Y'       , '657', '4'],
                   '3' : ['Rotation', '0'  , '4'],
                   '4' : ['Width'   , '46' , '4'],
                   '5' : ['Height'  , '36' , '4'],
}
button_init = {'1' : ['page_number'     , '4'],
               '2' : ['VisibleObject'   , '4'],
               '3' : ['UnVisibleObject1', '4'],
               '4' : ['UnVisibleObject2', '4'],
               '5' : ['UnVisibleObject3', '4'],
               '6' : ['UnVisibleObject4', '4'],
               '7' : ['UnVisibleObject5', '4'],
               '8' : ['UnVisibleObject6', '4'],
               '9' : ['UnVisibleObject7', '4'],
               '10': ['UnVisibleObject8', '4'],
               '11': ['_link_init_ApSource_type_defence_button', '4']
}

# Метод для поиска в строке - Общий
def str_find(str1, arr):
    i = 0
    for el in arr:
        if str(str1).find(el) > -1:
            return True

# Поиск максимального количества агрегатов
@logger.catch
def read_max_pump(data, list_active):
    count_row = 0
    # номера столбцов таблицы
    if list_active  == 'KTPRA':
        int_description = 3
        int_pump        = 17
    elif list_active  == 'GMPNA':
        int_description = 3
        int_pump        = 12
    max_value_pump = 0

    if list_active == 'KTPR' or list_active == 'KTPRP':
        logger.info(f'Генерация листа защит {list_active}')
        return 1
    else:
        for item in data:
            count_row += 1
            if count_row > 3:
                description_defence = str(item[int_description].value)
                pump_max            = str(item[int_pump].value)
                # Если резерв пропускаем итерацию
                if (not (str_find(description_defence, ('none', 'None')))) and \
                   (str(description_defence).lower() != 'резерв'):
                    # Количество агрегатов(это количество новых картинок), если это листы KTPRA и GMPNA
                    if int(pump_max) > max_value_pump:
                        max_value_pump = int(pump_max)
        logger.info(f'Генерация листов защит {list_active} для {max_value_pump} агрегатов')
        return max_value_pump

# Поиск максимального количества защит и листов защит
@logger.catch
def read_defence(data, list_active, pumps):
    count_row = 0
    # номера столбцов таблицы
    if list_active == 'KTPR':
        int_name_defence     = 3
        int_number_max       = 85
        int_value_number_max = 86
        flag_KTPR            = True
    elif list_active == 'KTPRP':
        int_name_defence     = 3
        int_number_max       = 7
        int_value_number_max = 8
        flag_KTPR            = True
    elif list_active  == 'KTPRA':
        int_name_defence     = 3
        int_number_max       = 15
        int_value_number_max = 16
        int_pump             = 17
        flag_KTPR            = False
    elif list_active  == 'GMPNA':
        int_name_defence     = 3
        int_number_max       = 10
        int_value_number_max = 11
        int_pump             = 12
        flag_KTPR            = False
    max_value   = 0
    max_value_1 = 0

    for item in data:
        count_row += 1
        if count_row > 3:
            # Если резерв пропускаем итерацию
            number_max          = item[int_number_max].value
            value_number_max    = item[int_value_number_max].value
            description_defence = item[int_name_defence].value

            if number_max is None or value_number_max is None: continue

            if not flag_KTPR:
                pump_number = str(item[int_pump].value)
                if (not (str_find(description_defence, ('none', 'None')))) and \
                   (str(description_defence).lower() != 'резерв') and \
                   pump_number == str(pumps):

                    # Максимальное число защит на листе
                    if (int(value_number_max) > max_value_1):
                        max_value_1 = int(value_number_max)
                    # Максимальное число страниц на листе
                    if int(number_max) > max_value:
                        max_value = int(number_max)
            else:
                if (not (str_find(description_defence, ('none', 'None')))) and \
                   (str(description_defence).lower() != 'резерв'):

                        # Максимальное число защит на листе
                    if (int(value_number_max) > max_value_1):
                        max_value_1 = int(value_number_max)
                    # Максимальное число страниц на листе
                    if int(number_max) > max_value:
                        max_value = int(number_max)
        # Еcли количество страниц > 1 добавляем кнопки переключения
    if max_value > 1:
        button_bool = True
    else:
        button_bool = False
    return max_value, button_bool, max_value_1

# Добавление кнопок переключения страниц с защитами
@logger.catch
def button_click(path_file, root, tree, max_value_list, max_value_list_1, num_item,
                 data_inf_button, init_1_target, attrib_top_1, attrib_button):
    count = 0
    for lvl_one in root.iter('type'):
        object = etree.Element('object')
        object.attrib['access-modifier'] = 'private'
        object.attrib['name'] = attrib_top_1 + str(num_item)
        object.attrib['display-name'] = attrib_top_1 + str(num_item)
        object.attrib['uuid'] = str(uuid.uuid1())
        object.attrib['base-type'] = attrib_button
        if attrib_button == 'type_readiness_button':
            object.attrib['base-type-id'] = '3b23edfd-8b38-49af-b25b-94bd39dac56f'
        else:
            object.attrib['base-type-id'] = '2832c785-46a5-4217-ad3d-c0505077e057'
        object.attrib['ver'] = '4'

        for key, value in button_designed.items():
            designed = etree.Element("designed")
            designed.attrib['target'] = value[0]
            # Координаты по X - 1
            if (key == '1') and (num_item == 1):
                designed.attrib['value'] = value[1]
            elif (key == '1') and (num_item > 1):
                designed.attrib['value'] = str(int(value[1]) + (56 * (num_item - 1)))
            # по Y - 2
            elif (key == '2'):
                designed.attrib['value'] = str(((max_value_list_1 + 1) * 26) + 10)
            else:
                designed.attrib['value'] = value[1]
            designed.attrib['ver'] = value[2]
            object.append(designed)

        for key_1, value_1 in button_init.items():
            init = etree.Element("init")
            init.attrib['target'] = value_1[0]
            init.attrib['ver'] = value_1[1]
            if key_1 == '1':
                init.attrib['value'] = str(num_item)
            elif key_1 == '2':
                init.attrib['ref'] = attrib_top_1 + str(num_item)
            elif key_1 != str(num_item + 2) and ((int(key_1) - 2) <= max_value_list):
                init.attrib['ref'] = attrib_top_1 + str(int(key_1) - 2)
            elif key_1 == '11':
                if attrib_button == 'type_readiness_button':
                    init.attrib['target'] = '_link_init_ApSource_type_readiness_button'
                else:
                    init.attrib['target'] = '_link_init_ApSource_type_defence_button'
                init.attrib['ref'] = init_1_target
            else:
                init.attrib['ref'] = 'empty_link'
            object.append(init)
        for item in data_inf_button:
            count += 1
            init_1 = etree.Element("init")
            init_1.attrib['target'] = 'def' + str(count) + '_path'
            init_1.attrib['ver'] = '4'
            init_1.attrib['value'] = item
            object.append(init_1)
        root.append(object)
    tree.write(path_file, pretty_print=True)
    logger.info(f'------ Страница № {num_item} заполнена! ------')

# Внесение изменения в шаблон
@logger.catch
def modification_list_defence(max_value_2, path_file, root, tree, list_active, pump, button_bool, str_pumps):
    if list_active.title == 'KTPR':
        name_title        = 'Карта общестанционных защит'
        name_defence      = 'Form_Station_Defences'
        name_apsoure      = 'ApSource_form_KTPRs'
        name_apsoure_cmd  = 'ApSource_form_KTPRs_Cmd'
        designed_path     = 'KTPRs'
        designed_path_cmd = 'Commands.CmdKTPR'
        reset_cmd         = 'ApSource_form_KTPRs_Cmd'
        name_windows      = 'Form_Station_Defences'
        init_ref          = 'unit.WorkspaceControl.Station_Defences_Control'
        is_IsKTPRA        = 'false'
        reset_button      = reset_button_init_KTPR
        coordinate_Width  = '1102'
    elif list_active.title == 'KTPRP':
        name_title        = 'Карта противопожарных защит'
        name_defence      = 'Form_Station_Defences'
        name_apsoure      = 'ApSource_form_KTPRs'
        name_apsoure_cmd  = 'ApSource_form_KTPRs_Cmd'
        designed_path     = 'KTPRs'
        designed_path_cmd = 'Commands.CmdKTPR'
        reset_cmd         = 'ApSource_form_KTPRs_Cmd'
        name_windows      = 'Form_Station_Defences'
        init_ref          = 'unit.WorkspaceControl.Station_Defences_Control'
        is_IsKTPRA        = 'false'
        reset_button      = reset_button_init_KTPR
        coordinate_Width  = '1102'
    elif list_active.title == 'KTPRA':
        name_title        = 'Карта агрегатных защит ' + str_pumps
        name_defence      = 'Form_MA' + str(pump) + '_Defences'
        name_apsoure      = 'ApSource_form_KTPRAs_MA' + str(pump)
        name_apsoure_cmd  = 'ApSource_form_KTPRAs_MA' + str(pump) + '_Cmd'
        designed_path     = 'KTPRAs.KTPRAs_' + str(pump)
        designed_path_cmd = 'Commands.CmdKTPRA'
        reset_cmd         = 'ApSource_form_KTPRAs_MA' + str(pump) + '_Cmd'
        name_windows      = 'Form_MA' + str(pump) + '_Defences'
        init_ref          = 'unit.WorkspaceControl.NA_' + str(pump) + '_Defences_Control'
        is_IsKTPRA        = 'true'
        reset_button      = reset_button_init_KTPRA
        coordinate_Width  = '1102'
    elif list_active.title == 'GMPNA':
        name_title        = 'Карта агрегатных готовностей ' + str_pumps
        name_defence      = 'Form_MA' + str(pump) + '_Readiness'
        name_apsoure      = 'ApSource_form_GMPNAs_MA' + str(pump)
        name_apsoure_cmd  = 'ApSource_form_GMPNAs_MA' + str(pump) + '_Cmd'
        name_windows      = 'Form_MA' + str(pump) + '_Readiness'
        init_ref          = 'unit.WorkspaceControl.NA_' + str(pump) +  '_Readiness_Control'
        designed_path     = 'GMPNAs.GMPNAs_' + str(pump)
        designed_path_cmd = 'Commands.CmdGMPNAs'
        coordinate_Width  = '857'

    for lvl_one in root.iter('type'):
        # type
        if lvl_one.attrib['name'] == 'name':
            lvl_one.attrib['name'] = name_defence
        if lvl_one.attrib['display-name'] == 'name':
            lvl_one.attrib['display-name'] = name_defence
        if lvl_one.attrib['uuid'] == 'uuid':
            lvl_one.attrib['uuid'] = str(uuid.uuid1())
        for lvl_two in lvl_one.iter('designed'):
            if lvl_two.attrib['value'] == 'coordinate_H':
                if (list_active.title == 'GMPNA') and (button_bool == False):
                    lvl_two.attrib['value'] = str(((max_value_2 + 1) * 26) + 2)
                else:
                    lvl_two.attrib['value'] = str(((max_value_2 + 1) * 26) + 55)

            if lvl_two.attrib['value'] == 'coordinate_W':
                lvl_two.attrib['value'] = coordinate_Width
            if lvl_two.attrib['value'] == 'name_list':
                lvl_two.attrib['value'] = name_title
        # 2 level
        for lvl_two in lvl_one.iter('object'):
            #1
            if lvl_two.attrib['name'] == 'defences':
                lvl_two.attrib['name'] = name_apsoure
            if lvl_two.attrib['display-name'] == 'defences':
                lvl_two.attrib['display-name'] = name_apsoure
            for lvl_three in lvl_two.iter('designed'):
                if lvl_three.attrib['value'] == 'designed_path':
                    lvl_three.attrib['value'] = designed_path
            #2
            if lvl_two.attrib['name'] == 'name':
                lvl_two.attrib['name'] = name_windows
            if lvl_two.attrib['display-name'] == 'name':
                lvl_two.attrib['display-name'] = name_windows
            for lvl_three in lvl_two.iter('init'):
                if lvl_three.attrib['ref'] == '_Control':
                    lvl_three.attrib['ref'] = init_ref
        #3
        # Для готовностей кнопка Деблокировать ВСЕ не нужна
        if list_active.title != 'GMPNA':
            object = etree.Element('object')
            object.attrib['access-modifier'] = 'private'
            object.attrib['name'] = 'type_reset_all_button_1'
            object.attrib['display-name'] = 'type_reset_all_button_1'
            object.attrib['uuid'] = str(uuid.uuid1())
            object.attrib['base-type'] = 'type_reset_all_button'
            object.attrib['base-type-id'] = '63a525da-c1a1-4436-ac7a-4031350c94e2'
            object.attrib['ver'] = '2'
            for key, value in reset_button_designed.items():
                designed = etree.Element("designed")
                designed.attrib['target'] = value[0]
                if key == '2':
                    designed.attrib['value']  = str(((max_value_2 + 1) * 26) + 13)
                else:
                    designed.attrib['value']  = value[1]
                designed.attrib['ver']    = value[2]
                object.append(designed)
            for key, value in reset_button.items():
                    init = etree.Element("init")
                    init.attrib['target'] = value[0]
                    init.attrib['ver'] = value[2]
                    #if key == '1':
                        #init.attrib['ref']  = reset_cmd
                    if key == '2':
                        init.attrib['value'] = is_IsKTPRA
                    elif key == '3':
                        init.attrib['value'] = str(pump)
                    object.append(init)
            root.append(object)
    tree.write(path_file, pretty_print=True)

@logger.catch
def name_pumps(wb, pump_plus_one):
    int_name    = 3
    int_numbers = 0
    count_row   = 0
    list_active = wb['UMPNA']

    for item in list_active.rows:
        count_row += 1
        if count_row > 3:
            if item[int_numbers].value == pump_plus_one:
                name = item[int_name].value
    return name

@logger.catch
def defense_order(write_data, list_defence, int_pumps, int_active_list,
                  int_number_list_defence, count_def, max_def_list, num_pumps):
    count_row = 0
    data_order = []
    if list_defence == 'KTPR' or list_defence == 'KTPRP':
        for num in range(1, count_def + 1):
            for i in range(1, max_def_list + 1):
                for item in write_data:
                    count_row += 1
                    if count_row > 3:
                        active_list_defence = item[int_active_list].value
                        number_list_defence = item[int_number_list_defence].value

                        if active_list_defence is None: continue
                        if number_list_defence is None: continue

                        if num == active_list_defence:
                            if i == number_list_defence:
                                data_order.append(item)
    else:
        for num in range(1, count_def + 1):
            for i in range(1, max_def_list + 1):
                for item in write_data:
                    count_row += 1
                    if count_row > 3:
                        active_list_defence = item[int_active_list].value
                        number_list_defence = item[int_number_list_defence].value
                        number_pumps        = item[int_pumps].value

                        if active_list_defence is None: continue
                        if number_list_defence is None: continue

                        if num_pumps == number_pumps:
                            if num == active_list_defence:
                                if i == number_list_defence:
                                    data_order.append(item)
    return data_order

@logger.catch
def gen_station_defence(path_file, file_exel, list_defence):
    # Соединение с Exel
    wb = openpyxl.load_workbook(file_exel, read_only=True)
    list_active = wb[list_defence]
    # Максимальное количество рядов и столбцов
    rows = list_active.max_row
    # Массив с данными
    data_inf_button = []
    write_data      = []
    # Прочитаем Exel, и будем данные брать отсюда
    for row in list_active.rows:
        write_data.append(row)

    # Номера столбцов выбранной таблицы
    if   list_active.title == 'KTPR' :
        int_active_list         = 85
        int_number_list_defence = 86
        int_pumps               = ''
        text_end                = 'Лист Общестанционных защит'
        attrib_data_1           = 'ApSource_form_KTPRs'
        attrib_data_2           = 'ApSource_form_KTPRs_Cmd'
        attrib_IsKTPRA          = 'false'
        attrib_top_1            = 'type_defence_top_'
        attrib_top_2            = 'type_defence_top'
        attrib_row_1            = 'type_defence_row_'
        attrib_row_2            = 'type_defence_row'
        attrib_button           = 'type_defence_button'
        attrib_init_row         = attrib_row_init_KTPR
        base_type_id_top        = '6b175e7c-6060-4e11-a416-88a851f6b4a5'
        base_type_id_row        = 'f3cabe63-3788-46d5-a7ff-4bfe9f9a6b19'
    elif list_active.title == 'KTPRP':
        int_active_list         = 7
        int_number_list_defence = 8
        int_pumps               = ''
        text_end                = 'Карта противопожарных защит'
        attrib_data_1           = 'ApSource_form_KTPRs'
        attrib_data_2           = 'ApSource_form_KTPRs_Cmd'
        attrib_IsKTPRA          = 'false'
        attrib_top_1            = 'type_defence_top_'
        attrib_top_2            = 'type_defence_top'
        attrib_row_1            = 'type_defence_row_'
        attrib_row_2            = 'type_defence_row'
        attrib_button           = 'type_defence_button'
        attrib_init_row         = attrib_row_init_KTPR
        base_type_id_top        = '6b175e7c-6060-4e11-a416-88a851f6b4a5'
        base_type_id_row        = 'f3cabe63-3788-46d5-a7ff-4bfe9f9a6b19'
    elif list_active.title == 'KTPRA':
        int_active_list         = 15
        int_number_list_defence = 16
        int_pumps               = 17
        text_end                = 'Листы Агрегатных защит'
        attrib_data_1           = 'ApSource_form_KTPRAs_MA'
        attrib_IsKTPRA          = 'true'
        attrib_top_1            = 'type_defence_top_'
        attrib_top_2            = 'type_defence_top'
        attrib_row_1            = 'type_defence_row_'
        attrib_row_2            = 'type_defence_row'
        attrib_button           = 'type_defence_button'
        attrib_init_row         = attrib_row_init_KTPRA
        base_type_id_top        = '6b175e7c-6060-4e11-a416-88a851f6b4a5'
        base_type_id_row        = 'f3cabe63-3788-46d5-a7ff-4bfe9f9a6b19'
    elif list_active.title == 'GMPNA':
        int_active_list         = 10
        int_number_list_defence = 11
        int_pumps               = 12
        text_end                = 'Листы Агрегатных готовностей'
        attrib_data_1           = 'ApSource_form_GMPNAs_MA'
        attrib_top_1            = 'type_readiness_top_'
        attrib_top_2            = 'type_readiness_top'
        attrib_row_1            = 'type_readiness_row_'
        attrib_row_2            = 'type_readiness_row'
        attrib_button           = 'type_readiness_button'
        attrib_init_row         = attrib_row_init_GMPNA
        base_type_id_top        = 'b08a935f-b03d-42e0-96c4-dc639b70d499'
        base_type_id_row        = '48231209-9a9f-42cf-9b38-ef1ef5cc7403'
    # Общие для всех листов номера столбцов
    int_number       = 0
    int_name_defence = 3

    # Максимальное число агрегатов
    max_value_pump = read_max_pump(write_data, list_defence)

    # Цикл по агрегатныи защитам и готовностям. Для общестанционных цикл = 1
    for pump in range(max_value_pump):
        str_pumps     = ''
        pump_plus_one = pump + 1
        # Для KTPR не нужно это сообщение
        if list_active.title != 'KTPR' and list_active.title != 'KTPRP':
            logger.info(f'Агрегат №{pump_plus_one}')
        # Проверим на существование файл, если есть то удалим
        if list_active.title == 'KTPR':
            new_pic_path = path_file + 'Form_Station_Defences.omobj'
        elif list_active.title == 'KTPRP':
            new_pic_path = path_file + 'Form_Station_Defences.omobj'
        elif list_active.title == 'KTPRA':
            new_pic_path = path_file + 'Form_MA' + str(pump_plus_one) + '_Defences.omobj'
        elif list_active.title == 'GMPNA':
            new_pic_path = path_file + 'Form_MA' + str(pump_plus_one) + '_Readiness.omobj'
        if os.path.isfile(new_pic_path):
            os.remove(new_pic_path)
        # В любом случае создадим новый
        shutil.copy2(path_file + 'Form_Defences_default.omobj', new_pic_path)

        # Счетчик всех защит в карте
        counter_defence = 0

        # Максимальное число листов, необходимость переключения страниц,
        max_value_1, button_bool, max_value_2 = read_defence(write_data, list_defence, pump_plus_one)

        # Сортируем защиты в порядке, указанным в Exel
        data_inf = defense_order(write_data, list_active.title, int_pumps, int_active_list,
                                 int_number_list_defence, max_value_1, max_value_2, pump_plus_one)

        # Начало работы с созданным файлом
        parser = etree.XMLParser(remove_blank_text=True)
        tree   = etree.parse(new_pic_path, parser)
        root   = tree.getroot()
        # Узнаем название агрегата агрегатных защит и готовностей
        if list_active.title != 'KTPR' and list_active.title != 'KTPRP':
            str_pumps = name_pumps(wb, pump_plus_one)
        # Исправляем координаты кнопки деблокировки и главного листа
        # И все данные под каждый лист защит
        # Координаты зависят от количества защит на 1 листе
        modification_list_defence(max_value_2, new_pic_path, root, tree, list_active, pump+1, button_bool, str_pumps)

        # Цикл по вкладкам защит,максимум на 240, т.е. 10 листов
        for number_list in range(max_value_1):
            # Счетчики
            count_row = 0
            count_defence_list = 0
            #Уровень первой строчки - type
            for lvl_one in root.iter('type'):
                # Уровень второй, добавляем уровень TOP
                object = etree.Element('object')
                object.attrib['access-modifier'] = 'private'
                object.attrib['name'] = attrib_top_1 + str(number_list + 1)
                object.attrib['display-name'] = attrib_top_1 + str(number_list + 1)
                object.attrib['uuid'] = str(uuid.uuid1())
                object.attrib['base-type'] = attrib_top_2
                object.attrib['base-type-id'] = base_type_id_top
                for key, value in attrib_defence_top.items():
                    designed = etree.Element("designed")
                    designed.attrib['target'] = value[0]
                    if (key == '6') and str(number_list + 1) == '1':
                        designed.attrib['value'] = 'true'
                    elif (key == '6') and str(number_list + 1) != '1':
                        designed.attrib['value'] = 'false'
                    else:
                        designed.attrib['value'] = value[1]
                    designed.attrib['ver'] = value[2]
                    object.append(designed)
                root.append(object)
                # Добавление защит на каждую вкладку
                for lvl_two in lvl_one.iter('object'):
                    if lvl_two.attrib['name'] == attrib_top_1 + str(number_list + 1):

                        if list_active.title != 'KTPR' and list_active.title != 'KTPRP':
                            init_1_target = 'ApSource_form_' + list_active.title + 's_MA' + str(pump_plus_one)
                        else:
                            init_1_target = 'ApSource_form_' + list_active.title + 's'

                        # Ходим по Exel и ищем текущий активный лист
                        for item in data_inf:
                            #count_row += 1
                            #if count_row > 3:
                            # Считываем данные с Exel и анализируем
                            description_defence = str(item[int_name_defence].value)
                            number_defence      = item[int_number].value
                            active_list_defence = str(item[int_active_list].value)
                            number_list_defence = str(item[int_number_list_defence].value)

                            if number_defence is None: continue
                            if list_active.title != 'KTPR' and list_active.title != 'KTPRP':
                                number_pumps = str(item[int_pumps].value)
                            # Номере бита в регистре, т.к. берем остаток, и если остаток = 0, нам надо 4
                            bit_defence_old = int(number_defence) % 4
                            if bit_defence_old == 0:
                                num_bit_defence = '4'
                            else:
                                num_bit_defence = str(bit_defence_old)
                            # Номер регистра
                            num_registry = math.ceil(int(number_defence) / 4)

                            # Разные условия для листов защит
                            if list_active.title == 'KTPR' or list_active.title == 'KTPRP':
                                # Пропускаем резервы и пустую строку, если не совпадает номер листа
                                # if (not (str_find(description_defence, ('none', 'None')))) and \
                                #    (str(description_defence).lower() != 'резерв') and \
                                #    (active_list_defence == str(number_list + 1)):
                                if active_list_defence == str(number_list + 1):

                                    # Массив данных для информации в кнопке переключения
                                    # Т.к. бит 0 будет, когда не будет остатка, т.е. по факту это 4 защита
                                    if num_bit_defence == 0:
                                        data_inf_button.append('Group_' + str(num_registry) + '.' + '4')
                                    else:
                                        data_inf_button.append('Group_' + str(num_registry) + '.' + str(num_bit_defence))
                                    # Увеличиваем номера защит и счетчик всех защит
                                    counter_defence += 1
                                    count_defence_list += 1
                                    # Уровень второй, строчки - object
                                    defence = etree.Element('object')
                                    defence.attrib['access-modifier'] = 'private'
                                    defence.attrib['name'] = attrib_row_1 + str(count_defence_list)
                                    defence.attrib['display-name'] = attrib_row_1 + str(count_defence_list)
                                    defence.attrib['uuid'] = str(uuid.uuid1())
                                    defence.attrib['base-type'] = attrib_row_2
                                    defence.attrib['base-type-id'] = base_type_id_row
                                    defence.attrib['ver'] = '4'
                                    object.append(defence)
                                    # Информация внутри каждого модуля
                                    for key, value in attrib_defence_row_design.items():
                                        defence_info = etree.Element("designed")
                                        defence_info.attrib['target'] = value[0]
                                        if key == '2':
                                            coord_Y = value[1] * (count_defence_list)
                                            defence_info.attrib['value'] = str(coord_Y)
                                        else:
                                            defence_info.attrib['value'] = value[1]
                                        defence_info.attrib['ver'] = value[2]
                                        defence.append(defence_info)

                                    for key, value in attrib_init_row.items():
                                        defence_init = etree.Element("init")
                                        defence_init.attrib['target'] = value[0]
                                        defence_init.attrib['ver'] = value[1]
                                        if   key == '1':
                                            defence_init.attrib['ref'] = attrib_data_1
                                        elif key == '2':
                                            defence_init.attrib['value'] = 'Group_' + str(num_registry)
                                        elif key == '3':
                                            defence_init.attrib['value'] = str(num_bit_defence)
                                        elif key == '4':
                                            defence_init.attrib['value'] = str(description_defence)
                                        elif key == '5':
                                            defence_init.attrib['value'] = str(counter_defence)
                                        #elif key == '6':
                                        #    defence_init.attrib['ref'] = attrib_data_2
                                        elif key == '7':
                                            defence_init.attrib['value'] = str(number_defence)
                                        elif key == '8':
                                            defence_init.attrib['value'] = attrib_IsKTPRA
                                        defence.append(defence_init)
                            else:
                                # Пропускаем резервы и пустую строку, если не совпадает номер агрега и номер листа
                                # if (not (str_find(description_defence, ('none', 'None')))) and \
                                #    (str(description_defence).lower() != 'резерв') and \
                                #    (number_pumps == str(pump_plus_one)) and \
                                #    (active_list_defence == str(number_list + 1)):
                                if (number_pumps == str(pump_plus_one)) and \
                                   (active_list_defence == str(number_list + 1)):

                                    # Массив данных для информации в кнопке переключения
                                    # Т.к. бит 0 будет, когда не будет остатка, т.е. по факту это 4 защита
                                    if num_bit_defence == 0:
                                        data_inf_button.append('Group_' + str(num_registry) + '.' + '4')
                                    else:
                                        data_inf_button.append(
                                            'Group_' + str(num_registry) + '.' + str(num_bit_defence))
                                    # Увеличиваем номера защит и счетчик всех защит
                                    counter_defence += 1
                                    count_defence_list += 1
                                    # Уровень второй, строчки - object
                                    defence = etree.Element('object')
                                    defence.attrib['access-modifier'] = 'private'
                                    defence.attrib['name'] = attrib_row_1 + str(count_defence_list)
                                    defence.attrib['display-name'] = attrib_row_1 + str(count_defence_list)
                                    defence.attrib['uuid'] = str(uuid.uuid1())
                                    defence.attrib['base-type'] = attrib_row_2
                                    defence.attrib['base-type-id'] = base_type_id_row
                                    defence.attrib['ver'] = '4'
                                    object.append(defence)
                                    # Информация внутри каждого модуля
                                    for key, value in attrib_defence_row_design.items():
                                        defence_info = etree.Element("designed")
                                        defence_info.attrib['target'] = value[0]
                                        if key == '2':
                                            coord_Y = value[1] * (count_defence_list)
                                            defence_info.attrib['value'] = str(coord_Y)
                                        else:
                                            defence_info.attrib['value'] = value[1]
                                        defence_info.attrib['ver'] = value[2]
                                        defence.append(defence_info)

                                    for key, value in attrib_init_row.items():
                                        defence_init = etree.Element("init")
                                        defence_init.attrib['target'] = value[0]
                                        defence_init.attrib['ver'] = value[1]
                                        if   key == '1':
                                            defence_init.attrib['ref'] = attrib_data_1 + str(pump_plus_one)
                                        elif key == '2':
                                            defence_init.attrib['value'] = 'Group_' + str(num_registry)
                                        elif key == '3':
                                            defence_init.attrib['value'] = str(num_bit_defence)
                                        elif key == '4':
                                            defence_init.attrib['value'] = str(description_defence)
                                        elif key == '5':
                                            defence_init.attrib['value'] = str(counter_defence)
                                        elif key == '6':
                                            defence_init.attrib['ref'] = attrib_data_1 + str(pump_plus_one) + '_Cmd'
                                        elif key == '7':
                                            defence_init.attrib['value'] = str(number_defence)
                                        elif key == '8':
                                            defence_init.attrib['value'] = attrib_IsKTPRA
                                        elif key == '9':
                                            defence_init.attrib['value'] = str(pump_plus_one)
                                        defence.append(defence_init)
                        # Добавляем кнопку переключения
                        if button_bool == True: button_click(new_pic_path, root, tree, max_value_1, max_value_2,
                                                             number_list + 1, data_inf_button, init_1_target, attrib_top_1, attrib_button)
                        # Массив с данными
                        data_inf_button.clear()

        tree.write(new_pic_path, pretty_print=True)
    logger.info(f'{text_end} успешно заполнен!')