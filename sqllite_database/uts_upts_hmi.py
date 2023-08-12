from typing import Any
from lxml import etree
from loguru import logger
import uuid
import shutil
import os
from main_base import path_hmi
from main_base import General_functions
from enum import Enum
from typing import NamedTuple


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
    # wb = openpyxl.load_workbook(file_exel, read_only=True)
    # list_active = wb[list_uts_upts]
    # # Максимальное количество рядов и столбцов
    # rows = list_active.max_row
    # # Массив с данными
    # data_inf_button = []
    # write_data      = []
    # # Прочитаем Exel, и будем данные брать отсюда
    # for row in list_active.rows:
    #     write_data.append(row)
    # # Номера столбцов выбранной таблицы
    # if list_active.title == 'UTS':
    #     int_active_list         = 11
    #     int_number_list_uts     = 12
    #     text_end                = 'Лист табло и сирен'
    #     attrib_data_1           = 'ApSource_form_UTSs'
    #     attrib_top_1            = 'page_'
    #     attrib_top_2            = 'Rectangle'
    #     attrib_row_1            = 'type_uts_row_'
    #     attrib_row_2            = 'type_uts_row'
    #     attrib_init_row         = attrib_row_init_UTS
    #     base_type_id_top        = '15726dc3-881e-4d8d-b0fa-a8f8237f08ca'
    #     base_type_id_row        = '70e32123-f413-4246-a6d8-6eb96bd1f953'
    # elif list_active.title == 'UPTS':
    #     int_active_list         = 10
    #     int_number_list_uts     = 11
    #     text_end                = 'Лист пожарных табло и сирен'
    #     attrib_data_1           = 'ApSource_form_UPTSs'
    #     attrib_top_1            = 'page_'
    #     attrib_top_2            = 'Rectangle'
    #     attrib_row_1            = 'type_uts_row_'
    #     attrib_row_2            = 'type_uts_row'
    #     attrib_init_row         = attrib_row_init_UTS
    #     base_type_id_top        = '15726dc3-881e-4d8d-b0fa-a8f8237f08ca'
    #     base_type_id_row        = '70e32123-f413-4246-a6d8-6eb96bd1f953'
    # # Общие для всех листов номера столбцов
    # int_number       = 0
    # int_uts_tag      = 2
    # int_uts_desc     = 3

    # Проверим на существование файл, если есть то удалим
    # if list_active.title == 'UTS':
    #     new_pic_path = f'{path_file}Form_UTS.omobj'
    # elif list_active.title == 'UPTS':
    #     new_pic_path = f'{path_file}Form_UPTS.omobj'
    # if os.path.isfile(new_pic_path):
    #     os.remove(new_pic_path)
    # # В любом случае создадим новый
    # shutil.copy2(f'{path_file}Form_UTS_UPTS_default.omobj', new_pic_path)

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


CONST_SIZE_TABLE_OF_FALSE = 61
CONST_SIZE_TABLE_OF_TRUE = 103


class NewRowsParams(NamedTuple):
    """Параметры для функции создания новых строк."""
    object: str
    access_modifier: str
    name: str
    display_name: str
    uuid: str
    base_type: str
    base_type_id: str
    ver: str | None


class NumberColumn(Enum):
    '''Перечисление статических столбцов таблицы.'''
    NUMBER_LIST_VU = 'number_list_VU'
    ORDER_NUMBER_FOR_VU = 'order_number_for_VU'


class DesignedParams(NamedTuple):
    target: str
    value: str
    ver: str


class BaseAlarmMap():
    '''Базовый класс создания карты табло и сирен.'''
    attrib_uts_row_design = {'1': DesignedParams(target='X', value='0', ver='5'),
                             '2': DesignedParams(target='Y', value=26, ver='5'),
                             '3': DesignedParams(target='Rotation', value='0', ver='5'),
                             '4': DesignedParams(target='Width', value='854', ver='5'),
                             '5': DesignedParams(target='Height', value='26', ver='5')}
    attrib_page_top = {'1': DesignedParams(target='X', value='8', ver='5'),
                       '2': DesignedParams(target='Y', value='53', ver='5'),
                       '3': DesignedParams(target='ZValue', value='0', ver='5'),
                       '4': DesignedParams(target='Rotation', value='0', ver='5'),
                       '5': DesignedParams(target='Scale', value='1', ver='5'),
                       '6': DesignedParams(target='Width', value='854', ver='5'),
                       '7': DesignedParams(target='Height', value='26', ver='5'),
                       '8': DesignedParams(target='Opacity', value='1', ver='5'),
                       '9': DesignedParams(target='Enabled', value='true', ver='5'),
                       '10': DesignedParams(target='Tooltip', value='', ver='5'),
                       '11': DesignedParams(target='RoundingRadius', value='0', ver='5'),
                       '12': DesignedParams(target='PenColor', value='4278190080', ver='5'),
                       '13': DesignedParams(target='PenStyle', value='1', ver='5'),
                       '14': DesignedParams(target='PenWidth', value='1', ver='5'),
                       '15': DesignedParams(target='BrushColor', value='4278190080', ver='5'),
                       '16': DesignedParams(target='BrushStyle', value='0', ver='5'),
                       '17': DesignedParams(target='Visible', value='', ver='5')}
    attrib_row_init_UTS = {'1': DesignedParams(target='_link_init_ApSource_type_uts_row', ver='5'),
                           '2': DesignedParams(target='_init_uts_tag', ver='5'),
                           '3': DesignedParams(target='form_show_verify_on', ver='5'),
                           '4': DesignedParams(target='form_show_verify_off', ver='5')}
    button_designed = {'1': DesignedParams(target='X', value='8', ver='5'),
                       '2': DesignedParams(target='Y', value='687', ver='5'),
                       '3': DesignedParams(target='Rotation', value='0', ver='5'),
                       '4': DesignedParams(target='Width', value='40', ver='5'),
                       '5': DesignedParams(target='Height', value='30', ver='5')}
    button_init = {'1': DesignedParams(target='page_number', ver='5'),
                   '2': DesignedParams(target='VisibleObject', ver='5'),
                   '3': DesignedParams(target='UnVisibleObject1', ver='5'),
                   '4': DesignedParams(target='UnVisibleObject2', ver='5'),
                   '5': DesignedParams(target='UnVisibleObject3', ver='5'),
                   '6': DesignedParams(target='UnVisibleObject4', ver='5'),
                   '7': DesignedParams(target='UnVisibleObject5', ver='5'),
                   '8': DesignedParams(target='UnVisibleObject6', ver='5'),
                   '9': DesignedParams(target='UnVisibleObject7', ver='5'),
                   '10': DesignedParams(target='UnVisibleObject8', ver='5'),
                   '11': DesignedParams(target='_link_init_ApSource_type_uts_button', ver='5')}

    name_title = 'Управление сигнализацией'
    attrib_top_1 = 'page_'
    attrib_top_2 = 'Rectangle'
    attrib_row_1 = 'type_uts_row_'
    attrib_row_2 = 'type_uts_row'
    base_type_id_top = '15726dc3-881e-4d8d-b0fa-a8f8237f08ca'
    base_type_id_row = '70e32123-f413-4246-a6d8-6eb96bd1f953'
    coordinate_Width = '870'


class UTS(BaseAlarmMap):
    '''Отдельный класс для таблицы UTS.'''
    text_end = 'Лист табло и сирен'
    attrib_data_1 = 'ApSource_form_UTSs'
    name_form = 'Form_UTS'
    name_apsoure = 'ApSource_form_UTSs'
    designed_path = 'UTSs'


class UPTS(BaseAlarmMap):
    '''Отдельный класс для таблицы UPTS.'''
    text_end = 'Лист пожарных табло и сирен'
    attrib_data_1 = 'ApSource_form_UPTSs'
    name_form = 'Form_UPTS'
    name_apsoure = 'ApSource_form_UPTSs'
    designed_path = 'UPTSs'


class ParserFile():
    '''Парсер файла картинки'''
    def __init__(self, new_pic_path: str) -> None:
        parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False)
        self.tree = etree.parse(new_pic_path, parser)
        self.root = self.tree.getroot()

    def __call__(self, *args: Any, **kwds: Any) -> tuple:
        return self.root, self.tree, self

    def modification_list_uts_upts(self, max_value_2: int, path_file: str, active_tabl: str, button_bool: bool) -> None:
        """Модификация шаблока карты сигнализаций

        Args:
            max_value_2 (int): максимальное кол-во защит на листе
            path_file (str): путь новой картинки
            active_tabl (str): активный лист таблицы
            button_bool (bool): флаг показа кнопок
        """
        def update_string(object: dict, key: str, value: str, new_value: str) -> None:
            '''Поиск и обновление строки'''
            if object[key] == value:
                object[key] = new_value

        table = UTS() if active_tabl == 'UTS' else UPTS()

        for lvl_one in self.root.iter('type'):
            # type
            update_string(lvl_one.attrib, 'name', 'name', table.name_form)
            update_string(lvl_one.attrib, 'display-name', 'name', table.name_form)
            update_string(lvl_one.attrib, 'uuid', 'uuid', str(uuid.uuid1()))

            for lvl_two in lvl_one.iter('designed'):
                if lvl_two.attrib['value'] == 'coordinate_H':
                    if button_bool:
                        lvl_two.attrib['value'] = str(((max_value_2 + 1) * 26) + CONST_SIZE_TABLE_OF_TRUE)
                    else:
                        lvl_two.attrib['value'] = str(((max_value_2 + 1) * 26) + CONST_SIZE_TABLE_OF_FALSE)

                update_string(lvl_two.attrib, 'value', 'coordinate_W', table.coordinate_Width)
                update_string(lvl_two.attrib, 'value', 'name_list', table.name_title)

            # 2 level
            for lvl_two in lvl_one.iter('object'):
                update_string(lvl_two.attrib, 'name', 'ApTemplate', table.name_apsoure)
                update_string(lvl_two.attrib, 'display-name', 'ApTemplate', table.name_apsoure)

                for lvl_three in lvl_two.iter('designed'):
                    update_string(lvl_three.attrib, 'value', 'designed_path', table.designed_path)

                    if lvl_three.attrib['value'] == 'designed_path':
                        lvl_three.attrib['value'] = table.designed_path
        self.tree.write(path_file, pretty_print=True)

    def new_rows(self, params: NewRowsParams):
        """Создаем новые строки."""
        object = etree.Element(params.object)
        object.attrib['access-modifier'] = params.access_modifier
        object.attrib['name'] = params.name
        object.attrib['display-name'] = params.display_name
        object.attrib['uuid'] = params.uuid
        object.attrib['base-type'] = params.base_type
        object.attrib['base-type-id'] = params.base_type_id
        
        if params.ver:
            object.attrib['ver'] = params.ver

        return object

    def parser_lvl_one(self, table: UTS | UPTS, number_list: int, root):
        """Парсим первый уровень."""
        object = self.new_rows(NewRowsParams(
            object='object',
            access_modifier='private',
            name=f'{table.attrib_top_1}{str(number_list + 1)}',
            display_name=f'{table.attrib_top_1}{str(number_list + 1)}',
            uuid=str(uuid.uuid1()),
            base_type=table.attrib_top_2,
            base_type_id=table.base_type_id_top))

        for key, value in table.attrib_page_top.items():
            designed = etree.Element("designed")
            designed.attrib['target'] = value.target
            if (key == '17') and str(number_list + 1) == '1':
                designed.attrib['value'] = 'true'
            elif (key == '17') and str(number_list + 1) != '1':
                designed.attrib['value'] = 'false'
            else:
                designed.attrib['value'] = value.value
            designed.attrib['ver'] = value.ver
            object.append(designed)
        root.append(object)
        return object
    
    def parser_lvl_two(self, table: UTS | UPTS, object):
        """Парсинг сирены."""
        siren = self.new_rows(NewRowsParams(
            object='object',
            access_modifier='private',
            name='type_siren',
            display_name='type_siren',
            uuid=str(uuid.uuid1()),
            base_type='type_uts_siren',
            base_type_id='9b36c57c-7b17-4397-b329-a35cbb9d5056',
            ver='5'))
        object.append(siren)

        for key, value in table.attrib_uts_row_design.items():
            siren_info = etree.Element("designed")
            siren_info.attrib['target'] = value[0]
            if key == '2':
                siren_info.attrib['value'] = "0"
            else:
                siren_info.attrib['value'] = value[1]
            siren_info.attrib['ver'] = value[2]
            siren.append(siren_info)
        return siren

    def parser_uts_signal(self, table: UTS | UPTS, object):
        uts = self.new_rows(NewRowsParams(
            object='object',
            access_modifier='private',
            name=f'{table.attrib_row_1}{str(count_uts_list)}',
            display_name=f'{table.attrib_row_1}{str(count_uts_list)}',
            uuid=str(uuid.uuid1()),
            base_type=f'{table.attrib_row_2}',
            base_type_id=f'{table.base_type_id_row}',
            ver='5'))
        
        object.append(uts)
        # Информация внутри каждого модуля
        for key, value in table.attrib_uts_row_design.items():
            uts_info = etree.Element("designed")
            uts_info.attrib['target'] = value[0]
            if key == '2':
                coord_Y = value[1] * (position_on_list)
                uts_info.attrib['value'] = str(coord_Y)
            else:
                uts_info.attrib['value'] = value[1]
            uts_info.attrib['ver'] = value[2]
            uts.append(uts_info)

        for key, value in table.attrib_row_init_UTS.items():
            uts_init = etree.Element("init")
            uts_init.attrib['target'] = value[0]
            uts_init.attrib['ver'] = value[1]
            if   key == '1':
                uts_init.attrib['ref'] = table.attrib_data_1
            elif key == '2':
                uts_init.attrib['value'] = uts_tag
            elif key == '3':
                uts_init.attrib['value'] = 'false'
            elif key == '4':
                uts_init.attrib['value'] = 'false'
            uts.append(uts_init)
class Alarm_map():
   
    def __init__(self, work_tabl: str) -> None:
        self._work_tabl = work_tabl

        dop_function = General_functions()
        table = UTS() if self._work_tabl == 'UTS' else UPTS()
        # Проверим на существование файл, если есть то удалим
        new_pic_path = f'{path_hmi}\\Form_UTS.omobj' if work_tabl == 'uts' else f'{path_hmi}\\Form_UPTS.omobj'

        if os.path.isfile(new_pic_path):
            os.remove(new_pic_path)
        # В любом случае создадим новый      
        shutil.copy2(f'{path_hmi}\\Form_UTS_UPTS_default.omobj', new_pic_path)
        # Счетчик всех табло и сирен в карте
        counter_uts = 0

        # Максимальное число листов, необходимость переключения страниц
        max_value_1 = dop_function.max_value_column(work_tabl, NumberColumn.NUMBER_LIST_VU.value, False)
        max_value_2 = dop_function.max_value_column(work_tabl, NumberColumn.ORDER_NUMBER_FOR_VU.value, False)
        button_bool = True if max_value_1 > 1 else False

        # Начало работы с созданным файлом
        parser = ParserFile(new_pic_path)
        tree, root = parser()

        # Исправляем размеры главного листа
        # Размеры зависят от количества табло и сирен на 1 листе
        parser.modification_list_uts_upts(max_value_2, new_pic_path, work_tabl, button_bool)

        data_value = dop_function.connect_by_sql_order(work_tabl, f'"id", "name", "number_list_VU", "number_protect_VU"', '''"number_list_VU", "number_protect_VU"''')
        # Цикл по вкладкам табло и сирен,максимум на 240, т.е. 10 листов
        for number_list in range(max_value_1):
            # Счетчики
            count_row = 0
            count_uts_list = 0
            # Уровень первой строчки - type
            for lvl_one in root.iter('type'):

                # Уровень второй, добавляем уровень TOP
                object = parser.parser_lvl_one(table, number_list, root)

                # Добавление табло и сирен на каждую вкладку
                for lvl_two in lvl_one.iter('object'):
                    if lvl_two.attrib['name'] == f'{table.attrib_top_1}{str(number_list + 1)}':

                        init_1_target = f'ApSource_form_{self._work_tabl}s'

                        if not number_list:
                            siren = parser.parser_lvl_two(table, object)
                    
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
                                    table.data_inf_button.append(uts_tag + '.s_State')
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
                                    uts = parser.new_rows(NewRowsParams(
                                        object='object',
                                        access_modifier='private',
                                        name=f'{table.attrib_row_1}{str(count_uts_list)}',
                                        display_name=f'{table.attrib_row_1}{str(count_uts_list)}',
                                        uuid=str(uuid.uuid1()),
                                        base_type=f'{table.attrib_row_2}',
                                        base_type_id=f'{table.base_type_id_row}',
                                        ver='5'))
                                    
                                    object.append(uts)
                                    # Информация внутри каждого модуля
                                    for key, value in table.attrib_uts_row_design.items():
                                        uts_info = etree.Element("designed")
                                        uts_info.attrib['target'] = value[0]
                                        if key == '2':
                                            coord_Y = value[1] * (position_on_list)
                                            uts_info.attrib['value'] = str(coord_Y)
                                        else:
                                            uts_info.attrib['value'] = value[1]
                                        uts_info.attrib['ver'] = value[2]
                                        uts.append(uts_info)

                                    for key, value in table.attrib_row_init_UTS.items():
                                        uts_init = etree.Element("init")
                                        uts_init.attrib['target'] = value[0]
                                        uts_init.attrib['ver'] = value[1]
                                        if   key == '1':
                                            uts_init.attrib['ref'] = table.attrib_data_1
                                        elif key == '2':
                                            uts_init.attrib['value'] = uts_tag
                                        elif key == '3':
                                            uts_init.attrib['value'] = 'false'
                                        elif key == '4':
                                            uts_init.attrib['value'] = 'false'
                                        uts.append(uts_init)

                        # Добавляем кнопку переключения
                        if button_bool == True: button_click(new_pic_path, root, tree, max_value_1, max_value_2,
                                                            number_list + 1, data_inf_button, init_1_target)
                        # Массив с данными
                        data_inf_button.clear()

        tree.write(new_pic_path, pretty_print=True)
        logger.info(f'{text_end} успешно заполнен!')

