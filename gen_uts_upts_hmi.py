from lxml import etree
from loguru import logger
import openpyxl
import uuid
import math
import shutil
import os

# Метод для поиска в строке - Общий
def str_find(str1, arr):
    i = 0
    for el in arr:
        if str(str1).find(el) > -1:
            return True

def translate(str):
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
            "Ё":"_E",
            "Ж":"J",
            "З":"Z",
            "И":"I",
            "Й":"_I",
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
            "ё":"_e",
            "ж":"j",
            "з":"z",
            "и":"i",
            "й":"_i",
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

attrib_uts_row_design =     {'1' : ['X'       , '0'  , '5'],
                             '2' : ['Y'       ,  26  , '5'],
                             '3' : ['Rotation', '0'  , '5'],
                             '4' : ['Width'   , '854', '5'],
                             '5' : ['Height'  , '26' , '5'],
}
attrib_page_top =    {'1' : ['X'             , '8'         , '5'],
                      '2' : ['Y'             , '53'        , '5'],
                      '3' : ['ZValue'        , '0'         , '5'],
                      '4' : ['Rotation'      , '0'         , '5'],
                      '5' : ['Scale'         , '1'         , '5'],
                      '6' : ['Width'         , '854'       , '5'],
                      '7' : ['Height'        , '26'        , '5'],
                      '8' : ['Opacity'       , '1'         , '5'],
                      '9' : ['Enabled'       , 'true'      , '5'],
                      '10': ['Tooltip'       , ''          , '5'],
                      '11': ['RoundingRadius', '0'         , '5'],
                      '12': ['PenColor'      , '4278190080', '5'],
                      '13': ['PenStyle'      , '1'         , '5'],
                      '14': ['PenWidth'      , '1'         , '5'],
                      '15': ['BrushColor'    , '4278190080', '5'],
                      '16': ['BrushStyle'    , '0'         , '5'],
                      '17': ['Visible'       , ''          , '5']
}
attrib_row_init_UTS =  {'1' : ['_link_init_ApSource_type_uts_row', '5'],
                        '2' : ['_init_uts_tag'                   , '5'],
                        '3' : ['form_show_verify_on'             , '5'],
                        '4' : ['form_show_verify_off'            , '5'],
}
button_designed = {'1' : ['X'       , '8'  , '5'],
                   '2' : ['Y'       , '687', '5'],
                   '3' : ['Rotation', '0'  , '5'],
                   '4' : ['Width'   , '40' , '5'],
                   '5' : ['Height'  , '30' , '5'],
}
button_init = {'1' : ['page_number'     , '5'],
               '2' : ['VisibleObject'   , '5'],
               '3' : ['UnVisibleObject1', '5'],
               '4' : ['UnVisibleObject2', '5'],
               '5' : ['UnVisibleObject3', '5'],
               '6' : ['UnVisibleObject4', '5'],
               '7' : ['UnVisibleObject5', '5'],
               '8' : ['UnVisibleObject6', '5'],
               '9' : ['UnVisibleObject7', '5'],
               '10': ['UnVisibleObject8', '5'],
               '11': ['_link_init_ApSource_type_uts_button', '5']
}

# Поиск максимального количества табло и сирен и листов с табло и сиренами
def read_uts_upts(data, list_active):
    count_row = 0
    # номера столбцов таблицы
    if list_active == 'UTS':
        int_number_max       = 11
        int_value_number_max = 12
    elif list_active == 'UPTS':
        int_number_max       = 10
        int_value_number_max = 11
    max_value   = 0
    max_value_1 = 0

    for item in data:
        count_row += 1
        if count_row > 3:
            # Если резерв пропускаем итерацию
            number_max          = str(item[int_number_max].value)
            value_number_max    = str(item[int_value_number_max].value)
            # Максимальное число табло и сирен на листе
            if value_number_max != 'None':
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
def button_click(path_file, root, tree, max_value_list, max_value_list_1, num_item, data_inf_button, init_1_target):
    count = 0
    for lvl_one in root.iter('type'):
        object = etree.Element('object')
        object.attrib['access-modifier'] = 'private'
        object.attrib['name'] = 'type_uts_button_' + str(num_item)
        object.attrib['display-name'] = 'type_uts_button_' + str(num_item)
        object.attrib['uuid'] = str(uuid.uuid1())
        object.attrib['base-type'] = 'type_uts_button'
        object.attrib['base-type-id'] = 'e9a1de57-5c19-4ad3-98d9-aea8ce2813fe'
        object.attrib['ver'] = '5'

        for key, value in button_designed.items():
            designed = etree.Element("designed")
            designed.attrib['target'] = value[0]
            # Координаты по X - 1
            if (key == '1') and (num_item == 1):
                designed.attrib['value'] = value[1]
            elif (key == '1') and (num_item > 1):
                designed.attrib['value'] = str(int(value[1]) + (50 * (num_item - 1)))
            # по Y - 2
            elif (key == '2'):
                designed.attrib['value'] = str(((max_value_list_1 ) * 26) + 63)
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
                init.attrib['ref'] = 'page_' + str(num_item)
            elif key_1 != str(num_item + 2) and ((int(key_1) - 2) <= max_value_list):
                init.attrib['ref'] = 'page_' + str(int(key_1) - 2)
            elif key_1 == '11':
                init.attrib['ref'] = init_1_target
            else:
                init.attrib['ref'] = 'empty_link'
            object.append(init)
        for item in data_inf_button:
            count += 1
            init_1 = etree.Element("init")
            init_1.attrib['target'] = 'uts' + str(count) + '_path'
            init_1.attrib['ver'] = '5'
            init_1.attrib['value'] = item
            object.append(init_1)
        root.append(object)
    tree.write(path_file, pretty_print=True)
    logger.info(f'------ Страница №{num_item}заполнена! ------')
# Внесение изменения в шаблон
def modification_list_uts_upts(max_value_2, path_file, root, tree, list_active, button_bool):
    if list_active.title == 'UTS':
        name_title        = 'Управление сигнализацией'
        name_form         = 'Form_UTS'
        name_apsoure      = 'ApSource_form_UTSs'
        designed_path     = 'UTSs'
        coordinate_Width  = '870'
    elif list_active.title == 'UPTS':
        name_title        = 'Управление сигнализацией'
        name_form         = 'Form_UPTS'
        name_apsoure      = 'ApSource_form_UPTSs'
        designed_path     = 'UPTSs'
        coordinate_Width  = '870'

    for lvl_one in root.iter('type'):
        # type
        if lvl_one.attrib['name'] == 'name':
            lvl_one.attrib['name'] = name_form
        if lvl_one.attrib['display-name'] == 'name':
            lvl_one.attrib['display-name'] = name_form
        if lvl_one.attrib['uuid'] == 'uuid':
            lvl_one.attrib['uuid'] = str(uuid.uuid1())
        for lvl_two in lvl_one.iter('designed'):
            if lvl_two.attrib['value'] == 'coordinate_H':
                if (button_bool == False):
                    lvl_two.attrib['value'] = str(((max_value_2 + 1) * 26) + 61)
                else:
                    lvl_two.attrib['value'] = str(((max_value_2 + 1) * 26) + 103)

            if lvl_two.attrib['value'] == 'coordinate_W':
                lvl_two.attrib['value'] = coordinate_Width
            if lvl_two.attrib['value'] == 'name_list':
                lvl_two.attrib['value'] = name_title
        # 2 level
        for lvl_two in lvl_one.iter('object'):
            if lvl_two.attrib['name'] == 'ApTemplate':
                lvl_two.attrib['name'] = name_apsoure
            if lvl_two.attrib['display-name'] == 'ApTemplate':
                lvl_two.attrib['display-name'] = name_apsoure
            for lvl_three in lvl_two.iter('designed'):
                if lvl_three.attrib['value'] == 'designed_path':
                    lvl_three.attrib['value'] = designed_path
    tree.write(path_file, pretty_print=True)
def gen_uts_upts(path_file, file_exel, list_uts_upts, verify):
    # Соединение с Exel
    wb = openpyxl.load_workbook(file_exel, read_only=True)
    list_active = wb[list_uts_upts]
    # Максимальное количество рядов и столбцов
    rows = list_active.max_row
    # Массив с данными
    data_inf_button = []
    write_data      = []
    # Прочитаем Exel, и будем данные брать отсюда
    for row in list_active.rows:
        write_data.append(row)
    # Номера столбцов выбранной таблицы
    if list_active.title == 'UTS':
        int_active_list         = 11
        int_number_list_uts     = 12
        text_end                = 'Лист табло и сирен'
        attrib_data_1           = 'ApSource_form_UTSs'
        attrib_top_1            = 'page_'
        attrib_top_2            = 'Rectangle'
        attrib_row_1            = 'type_uts_row_'
        attrib_row_2            = 'type_uts_row'
        attrib_init_row         = attrib_row_init_UTS
        base_type_id_top        = '15726dc3-881e-4d8d-b0fa-a8f8237f08ca'
        base_type_id_row        = '70e32123-f413-4246-a6d8-6eb96bd1f953'
    elif list_active.title == 'UPTS':
        int_active_list         = 10
        int_number_list_uts     = 11
        text_end                = 'Лист пожарных табло и сирен'
        attrib_data_1           = 'ApSource_form_UPTSs'
        attrib_top_1            = 'page_'
        attrib_top_2            = 'Rectangle'
        attrib_row_1            = 'type_uts_row_'
        attrib_row_2            = 'type_uts_row'
        attrib_init_row         = attrib_row_init_UTS
        base_type_id_top        = '15726dc3-881e-4d8d-b0fa-a8f8237f08ca'
        base_type_id_row        = '70e32123-f413-4246-a6d8-6eb96bd1f953'
    # Общие для всех листов номера столбцов
    int_number       = 0
    int_uts_tag      = 2
    int_uts_desc     = 3

    # Проверим на существование файл, если есть то удалим
    if list_active.title == 'UTS':
        new_pic_path = f'{path_file}Form_UTS.omobj'
    elif list_active.title == 'UPTS':
        new_pic_path = f'{path_file}Form_UPTS.omobj'
    if os.path.isfile(new_pic_path):
        os.remove(new_pic_path)
    # В любом случае создадим новый
    shutil.copy2(f'{path_file}Form_UTS_UPTS_default.omobj', new_pic_path)

    # Счетчик всех табло и сирен в карте
    counter_uts = 0

    # Максимальное число листов, необходимость переключения страниц,
    max_value_1, button_bool, max_value_2 = read_uts_upts(write_data, list_uts_upts)

    # Начало работы с созданным файлом
    parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False)
    tree   = etree.parse(new_pic_path, parser)
    root   = tree.getroot()
    # Исправляем размеры главного листа
    # Размеры зависят от количества табло и сирен на 1 листе
    modification_list_uts_upts(max_value_2, new_pic_path, root, tree, list_active, button_bool)

    # Цикл по вкладкам табло и сирен,максимум на 240, т.е. 10 листов
    for number_list in range(max_value_1):
        # Счетчики
        count_row = 0
        count_uts_list = 0
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
            for key, value in attrib_page_top.items():
                designed = etree.Element("designed")
                designed.attrib['target'] = value[0]
                if (key == '17') and str(number_list + 1) == '1':
                    designed.attrib['value'] = 'true'
                elif (key == '17') and str(number_list + 1) != '1':
                    designed.attrib['value'] = 'false'
                else:
                    designed.attrib['value'] = value[1]
                designed.attrib['ver'] = value[2]
                object.append(designed)
            root.append(object)
            # Добавление табло и сирен на каждую вкладку
            for lvl_two in lvl_one.iter('object'):
                if lvl_two.attrib['name'] == attrib_top_1 + str(number_list + 1):

                    init_1_target = 'ApSource_form_' + list_active.title + 's'

                    if number_list == 0:
                        siren = etree.Element('object')
                        siren.attrib['access-modifier'] = 'private'
                        siren.attrib['name'] = "type_siren"
                        siren.attrib['display-name'] = "type_siren"
                        siren.attrib['uuid'] = str(uuid.uuid1())
                        siren.attrib['base-type'] = "type_uts_siren"
                        siren.attrib['base-type-id'] = "9b36c57c-7b17-4397-b329-a35cbb9d5056"
                        siren.attrib['ver'] = '5'
                        object.append(siren)
                        for key, value in attrib_uts_row_design.items():
                            siren_info = etree.Element("designed")
                            siren_info.attrib['target'] = value[0]
                            if key == '2':
                                siren_info.attrib['value'] = "0"
                            else:
                                siren_info.attrib['value'] = value[1]
                            siren_info.attrib['ver'] = value[2]
                            siren.append(siren_info)

                    # Ходим по Exel и ищем текущий активный лист
                    for item in write_data:
                        count_row += 1
                        if count_row > 3 and str(item[int_number_list_uts].value) != 'None':
                            # Считываем данные с Exel и анализируем
                            uts_tag             = str(item[int_uts_tag].value)
                            uts_tag             = translate(uts_tag)
                            active_list_defence = str(item[int_active_list].value)
                            position_on_list = int(item[int_number_list_uts].value)
                            description_uts = str(item[int_uts_desc].value)

                            # Пропускаем резервы и пустую строку, если не совпадает номер листа
                            if (not (str_find(description_uts, ('none', 'None')))) and \
                               (str(description_uts).lower() != 'резерв') and \
                               (active_list_defence == str(number_list + 1)):

                                # Массив данных для информации в кнопке переключения
                                data_inf_button.append(uts_tag + '.s_State')
                                # Увеличиваем номера табло и сирен и счетчик всех табло и сирен
                                counter_uts += 1
                                count_uts_list += 1
                                # Уровень второй, строчки - object
                                uts = etree.Element('object')
                                uts.attrib['access-modifier'] = 'private'
                                uts.attrib['name'] = attrib_row_1 + str(count_uts_list)
                                uts.attrib['display-name'] = attrib_row_1 + str(count_uts_list)
                                uts.attrib['uuid'] = str(uuid.uuid1())
                                uts.attrib['base-type'] = attrib_row_2
                                uts.attrib['base-type-id'] = base_type_id_row
                                uts.attrib['ver'] = '5'
                                object.append(uts)
                                # Информация внутри каждого модуля
                                for key, value in attrib_uts_row_design.items():
                                    uts_info = etree.Element("designed")
                                    uts_info.attrib['target'] = value[0]
                                    if key == '2':
                                        coord_Y = value[1] * (position_on_list)
                                        uts_info.attrib['value'] = str(coord_Y)
                                    else:
                                        uts_info.attrib['value'] = value[1]
                                    uts_info.attrib['ver'] = value[2]
                                    uts.append(uts_info)

                                for key, value in attrib_init_row.items():
                                    uts_init = etree.Element("init")
                                    uts_init.attrib['target'] = value[0]
                                    uts_init.attrib['ver'] = value[1]
                                    if   key == '1':
                                        uts_init.attrib['ref'] = attrib_data_1
                                    elif key == '2':
                                        uts_init.attrib['value'] = uts_tag
                                    elif key == '3':
                                        uts_init.attrib['value'] = str(verify).lower()
                                    elif key == '4':
                                        uts_init.attrib['value'] = str(verify).lower()
                                    uts.append(uts_init)

                    # Добавляем кнопку переключения
                    if button_bool == True: button_click(new_pic_path, root, tree, max_value_1, max_value_2,
                                                         number_list + 1, data_inf_button, init_1_target)
                    # Массив с данными
                    data_inf_button.clear()

    tree.write(new_pic_path, pretty_print=True)
    logger.info(f'{text_end} успешно заполнен!')