import sys
for path in sys.path:
    print(path)
import PySimpleGUI as sg
import os
import re
import datetime
from loguru import logger
from function_code import *
from gen_defence_hmi import *
from gen_uts_upts_hmi import *
from gen_uso import *

# ГРАФИЧЕСКИЙ ИНТЕРФЕЙС ДЛЯ ЗАПУСКА ГЕНЕРАТОРА
# Для разработки будет использоваться более простая библиотека PySimpleGUI
# Сформировать exe: в терминале добавить: auto-py-to-exe

# Логирование в файл
def logging(path_save):
    if os.path.exists(f'{path_save}/debug.log'):

        os.remove(f'{path_save}/debug.log')
    logger.add(f'{path_save}/debug.log', level='DEBUG', format='{time} - {level} - {function} - {message}')

# Оставляем пустыми на случай отсутствия пути или значения
path_to_exel        = ''
path_to_adressmap   = ''
path_to_devstudio   = ''
path_to_filenameomx = ''
path_item           = ''
path_file_txt       = ''
path_file_signals   = ''
prefix_system       = ''
prefix_driver       = ''
path_mapai_ref      = ''
path_description    = ''
path_klk            = ''
path_kont           = ''
path_signalname     = ''
path_tagname        = ''
path_colorsheme     = ''
path_analogsformat  = ''
path_egu            = ''
path_analogtrends   = ''
tabl                = []
hat_table           = []
list_row            = {}
flag_not_click      = False

sg.theme('NeutralBlue')
tab1_layout = [
    [sg.Text('В проекте DevStudio в дереве Root: НЕ ДОЛЖНО БЫТЬ ОДИНАКОВЫХ НАЗВАНИЙ ПАПОК!', text_color='red', size=('93','0'))],
    [sg.Text('Укажите путь к файлу с сохранёнными путями если имеется, если нет, то заполните вручную, и сохраните данные в файл', text_color='Yellow', size=('93','0'))],
    [sg.Text('Файл с сохранениями: ', size=('27','0')), sg.InputText(key='-file2-', size=(68)), sg.FileBrowse('Обзор'), sg.Button('Открыть файл', size=(15,0))],
    [sg.Text('Где сохранить файл:  ', size=('27','0')),sg.InputText(key='-file1_9-', size=(68)), sg.FolderBrowse('Обзор'), sg.Button('Сохранить в файл', size=(15, 0))],
    [sg.Text('Заполнение атрибутов и карты адресов  --------------------------------------------------------------------------------------------------'
             '------------------------------------------------------------------', text_color='Yellow')],
    [sg.Text('Путь к файлу конфигурации (.xlsx):  ',size=('27','0')), sg.InputText(key='-file1_1-', size=(88)), sg.FileBrowse('Обзор')],
    [sg.Text('Путь к папке с файлами DevStudio:   ',size=('27','0')), sg.InputText(key='-file1_2-', size=(88)), sg.FolderBrowse('Обзор')],
    [sg.Text('Префикс системы:                    ',size=('27','0')), sg.InputText(key='-file1_7-', size=(31)),
     sg.Text('Драйвер системы(OFS!,SAR!...):      ',size=('25','0')), sg.InputText(key='-file1_8-', size=(32))],
    [sg.Text('Дополнительные данные для генерации  --------------------------------------------------------------------------------------------------------------------'
             '------------------------------------------------', text_color='Yellow')],
    [sg.Text('Название станции для трендов:       ',size=('27', '0')),sg.InputText(key='-file2_2-', size=(96))],
    [sg.Text('Файл для трендов item (.xlsx):'      ,size=('27','0')), sg.InputText(key='-file1_4-', size=(88)), sg.FileBrowse('Обзор')],
    [sg.Text('Папка хранения трендов:             ',size=('27','0')), sg.InputText(key='-file1_5-', size=(88)), sg.FolderBrowse('Обзор')],
    [sg.Text('Папка скрипта поиска сигналов:      ',size=('27','0')), sg.InputText(key='-file1_6-', size=(88)), sg.FolderBrowse('Обзор')],
]
tab2_layout = [
    [sg.Text('Выбор карты адресов:                ',size=('20','0')),
     sg.Checkbox('OPC DA', default=False, key='-OPCDA-'), sg.Checkbox('OPC UA', default=False, key='-OPCUA-'), sg.Checkbox('Modbus', default=True, key='-MODBUS-'),
     sg.Checkbox('Если необходимо заполнить AI в карту адресов ModBus503.xml', default=False, key='AN_503')],
    [sg.Text('Аналоговые сигналы:'     , size=('21','0')), sg.Button('Объекты',  key='-AI_DEV-',    size=(8,0)), sg.Button('Карта адресов', key='-AI_MAP-',    size=(11,0)),
                                                         sg.Button('Clear All',  key='-AI_CLEAR-',    size=(7,0)),
     sg.Text('Дискретные вх.сигналы:'  , size=('21','0')), sg.Button('Объекты',  key='-DI_DEV-',    size=(8,0)), sg.Button('Карта адресов', key='-DI_MAP-',    size=(11,0)),
                                                         sg.Button('Clear All',  key='-DI_CLEAR-',    size=(7,0))],
    [sg.Text('МПНА:'                   , size=('21','0')), sg.Button('Объекты',  key='-PUMPS_DEV-', size=(8,0)), sg.Button('Карта адресов', key='-PUMPS_MAP-', size=(11,0)),
                                                         sg.Button('Clear All',  key='-PUMPS_CLEAR-', size=(7,0)),
     sg.Text('Задвижки:'               , size=('21','0')), sg.Button('Объекты',  key='-ZD_DEV-',    size=(8,0)), sg.Button('Карта адресов', key='-ZD_MAP-',    size=(11,0)),
                                                         sg.Button('Clear All',  key='-ZD_CLEAR-',    size=(7,0))],
    [sg.Text('Вспомсистемы:'           , size=('21','0')), sg.Button('Объекты',  key='-VS_DEV-',    size=(8,0)), sg.Button('Карта адресов', key='-VS_MAP-',    size=(11,0)),
                                                         sg.Button('Clear All',  key='-VS_CLEAR-',    size=(7,0)),
     sg.Text('Индикаторы событий(Pic):', size=('21','0')), sg.Button('Объекты',  key='-PIC_DEV-',   size=(8,0)), sg.Button('Карта адресов', key='-PIC_MAP-',   size=(11,0)),
                                                         sg.Button('Clear All',  key='-PIC_CLEAR-',   size=(7,0))],
    [sg.Text('Смежные системы:'        , size=('21','0')), sg.Button('Объекты',  key='-SS_DEV-',    size=(8,0)), sg.Button('Карта адресов', key='-SS_MAP-',    size=(11,0)),
                                                         sg.Button('Clear All',  key='-SS_CLEAR-',    size=(7,0)),
     sg.Text('Табло и сирены(UTS):'    , size=('21','0')), sg.Button('Объекты',  key='-UTS_DEV-',   size=(8,0)), sg.Button('Карта адресов', key='-UTS_MAP-',    size=(11,0)),
                                                         sg.Button('Clear All',  key='-UTS_CLEAR-',   size=(7,0))],
    [sg.Text('Табло и сирены(UPTS):'   , size=('21', '0')), sg.Button('Объекты', key='-UPTS_DEV-',   size=(8, 0)),sg.Button('Карта адресов', key='-UPTS_MAP-', size=(11, 0)),
                                                         sg.Button('Clear All',  key='-UPTS_CLEAR-',   size=(7, 0)),
     sg.Text('Агрегатные защиты:'      , size=('21', '0')), sg.Button('Объекты', key='-KTPRA_DEV-', size=(8, 0)), sg.Button('Карта адресов', key='-KTPRA_MAP-', size=(11, 0)),
                                                         sg.Button('Clear All',  key='-KTPRA_CLEAR-', size=(7, 0))],
    [sg.Text('Агрегатные готовности:'  , size=('21', '0')), sg.Button('Объекты', key='-GMPNA_DEV-', size=(8, 0)), sg.Button('Карта адресов', key='-GMPNA_MAP-', size=(11, 0)),
                                                         sg.Button('Clear All',  key='-GMPNA_CLEAR-', size=(7, 0)),
     sg.Text('Станционные защиты(МНС):', size=('21', '0')), sg.Button('Объекты', key='-KTPR_DEV-',   size=(8, 0)),sg.Button('Карта адресов', key='-KTPR_MAP-', size=(11, 0)),
                                                         sg.Button('Clear All',  key='-KTPR_CLEAR-',   size=(7, 0))],
    [sg.Text('Пожарные извещатели:'    , size=('21', '0')), sg.Button('Объекты', key='-PI_DEV-', size=(8, 0)),    sg.Button('Карта адресов', key='-PI_MAP-', size=(11, 0)),
                                                         sg.Button('Clear All',  key='-PI_CLEAR-', size=(7, 0)),
     sg.Text('Пожарные зоны:'          , size=('21', '0')), sg.Button('Объекты', key='-PZ_DEV-', size=(8, 0)),    sg.Button('Карта адресов', key='-PZ_MAP-', size=(11, 0)),
                                                         sg.Button('Clear All',  key='-PZ_CLEAR-', size=(7, 0))],
    [sg.Text('Станционные защиты(ПТ):', size=('21', '0')), sg.Button('Объекты', key='-KTPRP_DEV-',   size=(8, 0)),sg.Button('Карта адресов', key='-KTPRP_MAP-', size=(11, 0)),
                                                         sg.Button('Clear All',  key='-KTPRP_CLEAR-',   size=(7, 0))]
]
tab3_layout = [
    [sg.Text('AttributesMapColorScheme.xml:', size=('23', '0')), sg.Button('Карта атрибутов',  key='-COLOR_MAP-',  size=(16, 0)), sg.Button('Clear', key='-COLOR_CLEAR-',  size=(6, 0))],
    [sg.Text('AttributesAnalogsFormats.xml:', size=('23', '0')), sg.Button('Карта атрибутов',  key='-FORMAT_MAP-', size=(16, 0)), sg.Button('Clear', key='-FORMAT_CLEAR-', size=(6, 0))],
    [sg.Text('AttributesMapEGU.xml:'        , size=('23', '0')), sg.Button('Карта атрибутов',  key='-EGU_MAP-',    size=(16, 0)), sg.Button('Clear', key='-EGU_CLEAR-',    size=(6, 0))],
    [sg.Text('AttributesAnalogTrends.xml:'  , size=('23', '0')), sg.Button('Карта атрибутов',  key='-TREND_MAP-',  size=(16, 0)), sg.Button('Clear', key='-TREND_CLEAR-',  size=(6, 0))],
    [sg.Text('Готовности пожарных зон:'     , size=('23', '0')), sg.Button('Карта атрибутов',  key='-DESC_MAP-',   size=(16, 0)), sg.Button('Clear', key='-DESC_CLEAR-',   size=(6, 0))],
    [sg.Text('Тренды(Windows):', size=('23', '0')), sg.Button('Сформировать файл', key='-TREND-', size=(16, 0))],
    [sg.Text('Тренды(Linux + ModBus):'      , size=('23', '0')), sg.Button('Сформировать файл', key='TREND_Lin_MB', size=(16, 0))],
    [sg.Text('SQL запрос поиска сигналов:'  , size=('23', '0')), sg.Button('SQL запрос', key='-SQL-', size=(16, 0))],
]
tab4_layout = [
    [sg.Text('Выбор карты адресов:',size=('20','0')), sg.Checkbox('OPC DA', default=False, key='SE_OPCDA'),
     sg.Checkbox('OPC UA', default=False, key='SE_OPCUA'), sg.Checkbox('Modbus', default=True, key='SE_MODBUS')],
    [sg.Button('Заполнить: AI',      key='-AI_DIAG-',      size=(17,0)), sg.Button('Очистить: AI',      key='-AI_DIAG_CLEAR-',    size=(17,0))],
    [sg.Button('Заполнить: AO',      key='-AO_DIAG-',      size=(17,0)), sg.Button('Очистить: AO',      key='-AO_DIAG_CLEAR-',    size=(17,0))],
    [sg.Button('Заполнить: DI',      key='-DI_DIAG-',      size=(17,0)), sg.Button('Очистить: DI',      key='-DI_DIAG_CLEAR-',    size=(17,0))],
    [sg.Button('Заполнить: DO',      key='-DO_DIAG-',      size=(17,0)), sg.Button('Очистить: DO',      key='-DO_DIAG_CLEAR-',    size=(17,0))],
    [sg.Button('Заполнить: CPS',     key='-CPS_DIAG-',     size=(17,0)), sg.Button('Очистить: CPS',     key='-CPS_DIAG_CLEAR-',   size=(17,0))],
    [sg.Button('Заполнить: CPUKC',   key='-CPUKC_DIAG-',   size=(17,0)), sg.Button('Очистить: CPUKC',   key='-CPUKC_DIAG_CLEAR-', size=(17,0))],
    [sg.Button('Заполнить: CPU',     key='-CPU_DIAG-',     size=(17,0)), sg.Button('Очистить: CPU',     key='-CPU_DIAG_CLEAR-',   size=(17,0))],
    [sg.Button('Заполнить: NOC_NOE', key='-NOC_NOE_DIAG-', size=(17,0)), sg.Button('Очистить: NOC_NOE', key='-NOC_DIAG_CLEAR-',   size=(17,0))],
    [sg.Button('Заполнить: CRA',     key='-CRA_DIAG-',     size=(17,0)), sg.Button('Очистить: CRA',     key='-CRA_DIAG_CLEAR-',   size=(17,0))],
    [sg.Button('Заполнить: NOR',     key='-NOR_DIAG-',     size=(17,0)), sg.Button('Очистить: NOR',     key='-NOR_DIAG_CLEAR-',   size=(17,0))],
    [sg.Button('Заполнить: NOM',     key='-NOM_DIAG-',     size=(17,0)), sg.Button('Очистить: NOM',     key='-NOM_DIAG_CLEAR-',   size=(17,0))]
]
tab5_layout = [
    [sg.Text('Выбор карты адресов:',size=('20','0')), sg.Checkbox('OPC DA', default=False, key='MK_OPCDA'),
     sg.Checkbox('OPC UA', default=False, key='MK_OPCUA'), sg.Checkbox('Modbus', default=True, key='MK_MODBUS')],
    [sg.Button('Заполнить: AI8',     key='MK_AI8',      size=(17,0)), sg.Button('Очистить: AI8',     key='MK_AI8_CLEAR',   size=(17,0)),
     sg.Text('Проверь соответствие в таблице HW (Тип): МК-516-008A',size=('60','0'))],
    [sg.Button('Заполнить: AO',      key='MK_AO',       size=(17,0)), sg.Button('Очистить: AO',      key='MK_AO_CLEAR',    size=(17,0)),
     sg.Text('Проверь соответствие в таблице HW (Тип): MK-514-008',size=('60','0'))],
    [sg.Button('Заполнить: DI',      key='MK_DI',       size=(17,0)), sg.Button('Очистить: DI',      key='MK_DI_CLEAR',    size=(17,0)),
     sg.Text('Проверь соответствие в таблице HW (Тип): MK-521-032',size=('60','0'))],
    [sg.Button('Заполнить: DO',      key='MK_DO',       size=(17,0)), sg.Button('Очистить: DO',      key='MK_DO_CLEAR',    size=(17,0)),
     sg.Text('Проверь соответствие в таблице HW (Тип): MK-531-032',size=('60','0'))],
    [sg.Button('Заполнить: MN',      key='MK_MN',       size=(17,0)), sg.Button('Очистить: MN',      key='MK_MN_CLEAR',    size=(17,0)),
     sg.Text('Проверь соответствие в таблице HW (Тип): MK-546-010',size=('60','0'))],
    [sg.Button('Заполнить: CN',      key='MK_CN',       size=(17,0)), sg.Button('Очистить: CN',      key='MK_CN_CLEAR',    size=(17,0)),
     sg.Text('Проверь соответствие в таблице HW (Тип): MK-545-010',size=('60','0'))],
    [sg.Button('Заполнить: CPU',     key='MK_CPU',      size=(17,0)), sg.Button('Очистить: CPU',     key='MK_CPU_CLEAR',   size=(17,0)),
     sg.Text('Проверь соответствие в таблице HW (Тип): MK-504-120',size=('60','0'))],
    [sg.Button('Заполнить: PSU',     key='MK_PSU',      size=(17,0)), sg.Button('Очистить: PSU',     key='MK_PSU_CLEAR',   size=(17,0)),
     sg.Text('Проверь соответствие в таблице HW (Тип): MK-550-024',size=('60','0'))],
    [sg.Button('Заполнить: RS',      key='MK_RS',       size=(17,0)), sg.Button('Очистить: RS',      key='MK_RS_CLEAR',    size=(17,0)),
     sg.Text('Проверь соответствие в таблице HW (Тип): MK-541-002',size=('60','0'))],
    [sg.Button('Заполнить: RackStates', key='RackS', size=(17, 0)),   sg.Button('Очистить: RackStates', key='RackS_CLEAR', size=(17, 0))],
]
tab6_layout = [
    [sg.Text('Где разместить файлы:  ',size=('27','0')), sg.InputText(key='SAMPLE', size=(88)), sg.FolderBrowse('Обзор')],

    [sg.Text('Генерация кадров защит и готовностей:',size=('30','0')),
     sg.Checkbox('Агрегатные защиты', default=False, key='DEFENC'), sg.Checkbox('Агрегатные готовности', default=False, key='READIF'),
     sg.Checkbox('Станционные защиты', default=False, key='STATDEF'), sg.Checkbox('Пожарные защиты', default=False, key='PTDEF')],
    [sg.Button('Создать шаблон', key='NEW_SAMPLE_DEF', size=(25,0)), sg.Button('Запустить генерацию', key='START_DEFENCE', size=(25,0))],
    [sg.Text('Генерация кадров UTS или UPTS:',size=('30','0')),
     sg.Checkbox('UTS', default=False, key='UTS_GEN'), sg.Checkbox('UPTS', default=False, key='UPTS_GEN'),
     sg.Checkbox('Окно управление', default=False, key='Verify')],
    [sg.Button('Создать шаблон', key='NEW_SAMPLE_UTS', size=(25,0)), sg.Button('Запустить генерацию', key='START_UTS', size=(25,0))],
    [sg.Text('Генерация только служебных сигналов', size=('30', '0')),
     sg.Checkbox('МНС', default=False, key='DIAG_MNS_SRV'), sg.Checkbox('ПТ', default=False, key='DIAG_PT_SRV')],
    [sg.Button('Создать шаблон', key='NEW_SAMPLE_DIAG_SRV', size=(25, 0)),
     sg.Button('Запустить генерацию', key='START_GEN_DIAG_SRV', size=(25, 0))],
    [sg.Text('Генерация кадров диагностики', size=('30', '0')),
     sg.Checkbox('МНС', default=False, key='DIAG_MNS'), sg.Checkbox('ПТ', default=False, key='DIAG_PT')],
    [sg.Button('Создать шаблон', key='NEW_SAMPLE_DIAG', size=(25, 0)),
     sg.Button('Запустить генерацию', key='START_GEN_DIAG', size=(25, 0))],
    [sg.Text('Для примера смотри Exel НПС Аксинино-2. '
             'Для генерации диагностики должны быть заполнены 3 таблицы: HW, Net, USO:\n'
             '-- HW должна содержать типы модулей.\n'
             '-- Net должна содержать уходящие и входящие линки корзин.\n'
             '-- USO должна содержать служебные сигналы', size=('100', '0'))],
]
tab7_layout = [
    [sg.Text('Папка с шаблонами:              ',size=('27','0')), sg.InputText(key='MSG_PATH_SAMPLE', size=(88)), sg.FolderBrowse('Обзор')],
    [sg.Text('Где разместить файлы запросов:  ',size=('27','0')), sg.InputText(key='MSG_PATH_REQ', size=(88)), sg.FolderBrowse('Обзор')],
    [sg.Button('Диагностика', key='DIAG_MSG', size=(20,0)),
     sg.Text('В таблице MSG должны быть добавлены адреса: '
             'TblD_Racks, TblD_ModulesPSU, TblD_ModulesCPU, TblD_ModulesMN, TblD_ModulesCN, TblD_ModulesRS',size=('90','0'))],
    [sg.Button('DO', key='DO_MSG', size=(20,0)),
     sg.Text('В таблице MSG должны быть добавлены адреса: '
             'TblDO',size=('90','0'))],
]
tab8_layout = [
    [sg.Text('Где разместить файлы:  ',size=('27','0')), sg.InputText(key='SU_PATH', size=(88)), sg.FolderBrowse('Обзор')],
    [sg.Checkbox('МНС', default=False, key='ChB_MNS'), sg.Checkbox('ПТ', default=False, key='ChB_PT'),
     sg.Checkbox('РП', default=False, key='ChB_RP'), sg.Checkbox('САР', default=False, key='ChB_SAR')],
    [sg.Button('Cfg_KTPRS', key='CFG_KTPRS', size=(20,0)),  sg.Button('Cfg_ktpra', key='CFG_KTPRA', size=(20,0)),
     sg.Button('Cfg_KTPR',  key='CFG_KTPR',  size=(20,0)),  sg.Button('Cfg_NA',    key='CFG_NA',    size=(20,0))],
    [sg.Button('Cfg_AI',    key='CFG_AI',    size=(20, 0)), sg.Button('Cfg_AO',    key='CFG_AO',    size=(20, 0)),
     sg.Button('Cfg_DI',    key='CFG_DI',    size=(20, 0)), sg.Button('Cfg_DO',    key='CFG_DO',    size=(20, 0))],
    [sg.Button('Cfg_ZD',    key='CFG_ZD',    size=(20, 0)), sg.Button('Cfg_VS',    key='CFG_VS',    size=(20, 0)),
     sg.Button('Cfg_VSGRP', key='CFG_VSGRP', size=(20, 0)), sg.Button('Cfg_NPS',   key='CFG_NPS',   size=(20, 0))],
    [sg.Button('gv_DIAG',   key='CFG_DIAG',  size=(20, 0)), sg.Button('Cfg_UTS',   key='CFG_UTS',   size=(20, 0)),
     sg.Button('Cfg_VV',    key='CFG_VV',    size=(20, 0)), sg.Button('Cfg_DPS',   key='CFG_DPS',   size=(20, 0))],
    [sg.Button('Cfg_RSREQ', key='CFG_RSREQ', size=(20, 0)), sg.Button('Cfg_AI_sim',key='CFG_AI_SIM',size=(20, 0)),
     sg.Button('Cfg_PIC',   key='CFG_PIC',   size=(20, 0)), sg.Button('Cfg_DI_sim',key='CFG_DI_sim',size=(20, 0)),
     sg.Button('Cfg_DO_sim',key='CFG_DO_sim',size=(20, 0))],

    [sg.Button('Cfg_TM_TS', key='CFG_TM_TS', size=(20, 0)), sg.Button('Cfg_TM_TU', key='CFG_TM_TU', size=(20, 0)),
     sg.Button('Cfg_TM_TI2',key='CFG_TM_TI2',size=(20, 0)), sg.Button('Cfg_TM_TI4',key='CFG_TM_TI4',size=(20, 0))],
    [sg.Button('Cfg_TM_TII',key='CFG_TM_TII',size=(20, 0)), sg.Button('Cfg_TM_TR2',key='CFG_TM_TR2',size=(20, 0)),
     sg.Button('Cfg_TM_TR4',key='CFG_TM_TR4',size=(20, 0))],
]
tab9_layout = [
    [sg.Text('Где разместить файл:  ',size=('27','0')), sg.InputText(key='IMIT_PATH', size=(88)), sg.FolderBrowse('Обзор')],
    [sg.Text('Стартовый ModBus адрес', size=('22','0')),
     sg.Text('AI: ', size=('3','0')), sg.InputText(key='Start_AI', size=(24)),
     sg.Text('DI: ', size=('3','0')), sg.InputText(key='Start_DI', size=(24)),
     sg.Text('DO: ', size=('3','0')), sg.InputText(key='Start_DO', size=(24))],
    [sg.Button('Cfg_DI_Imit',  key='CFG_DI_IMIT',  size=(20,0)), sg.Button('Cfg_AI_Imit',  key='CFG_AI_IMIT',  size=(20,0))],
    [sg.Button('Заполнить конфигурацию', key='Click_imit_xml', size=(20, 0))]
]
tab10_layout = [
    [sg.Text('Укажи путь до КЗФКП:',size=('18','0')), sg.InputText(key='PATH_KZFKP', size=(75)), sg.FileBrowse('Обзор'),
     sg.Button('Открыть файл', key='READ_KZFKP', size=(15, 0))],
    [sg.Text('Выбери шкаф:',size=('18','0')), sg.Combo(tabl, default_value='КЗФКП не загружено', key='PICK_USO', size=(30, 0)),
     sg.Text('Укажи номер строки шапки таблицы:  ',size=('30','0')), sg.InputText(key='NUM_SHEET', size=(5)),
     sg.Button('Прочитать таблицу', key='READ_TABL', size=(15, 0))],
    [sg.Text('Укажи название столбцов на листе выбранной таблицы КЗФКП:',size=('50','0'))],
    [sg.Combo(tabl, default_value='Тэг',          key='TAG',     size=(29, 0)),
     sg.Combo(tabl, default_value='Наименование', key='NAME',    size=(29, 0)),
     sg.Combo(tabl, default_value='Схема',        key='SCHEME',  size=(29, 0)),
     sg.Combo(tabl, default_value='КлК',          key='KLK',     size=(29, 0))],
    [sg.Combo(tabl, default_value='Контакт',      key='CONTACT', size=(29, 0)),
     sg.Combo(tabl, default_value='Корзина',      key='RACK',    size=(29, 0)),
     sg.Combo(tabl, default_value='Модуль',       key='MODUL',   size=(29, 0)),
     sg.Combo(tabl, default_value='Канал',        key='CHANNEL', size=(29, 0))],
    [sg.Text('Укажи базу SQL:',size=('18','0')), sg.InputText(key='PATH_SQL', size=(94)), sg.FolderBrowse('Обзор')],
    [sg.Button('Заполнить выбранную таблицу', key='LOAD_KZFKP',  size=(25, 0)),
     sg.Button('Очистить всю таблицу KD',     key='CLEAR_KZFKP', size=(25, 0))],

]

layout = [[sg.TabGroup
           ([[sg.Tab('Настройки', tab1_layout),
              sg.Tab('Объекты и карта адресов', tab2_layout),
              sg.Tab('Карты атрибутов', tab3_layout),
              sg.Tab('Диагностика SE', tab4_layout),
              sg.Tab('Диагностика MK', tab5_layout),
              sg.Tab('Кадры ВУ', tab6_layout),
              sg.Tab('Сообщения', tab7_layout),
              sg.Tab('СУ', tab8_layout),
              sg.Tab('Имитатор', tab9_layout),
              #sg.Tab('Тест', tab10_layout),
              ]])]], [sg.Multiline(f'Сборка генератора запущена\n', key='logger', size=('128', '5'), autoscroll=True)]

window = sg.Window('Генератор объектов', layout)

while True:
    event, values = window.read()
    if event == 'Закрыть окно' or event == sg.WIN_CLOSED: break
    # Сохраняем все пути в один файл .xml
    if event == 'Сохранить в файл':
        # Исключаем случайное нажатие по кнопке
        if values['-file1_9-'] == '': continue
        flag_not_click = True
        path_to_exel        = values['-file1_1-']
        path_to_devstudio   = values['-file1_2-']
        path_to_filenameomx = f'{path_to_devstudio}/typical_prj.omx'
        path_to_adressmap   = f'{path_to_devstudio}/ODA.xml'
        path_item           = values['-file1_4-']
        path_sample         = values['SAMPLE']
        path_sample_msg     = values['MSG_PATH_SAMPLE']
        path_sample_req     = values['MSG_PATH_REQ']
        path_su             = values['SU_PATH']
        path_imit           = values['IMIT_PATH']
        mb_adrr_AI          = values['Start_AI']
        mb_adrr_DI          = values['Start_DI']
        mb_adrr_DO          = values['Start_DO']
        path_file_txt       = values['-file1_5-']
        path_file_signals   = values['-file1_6-']
        prefix_system       = values['-file1_7-']
        prefix_driver       = values['-file1_8-']
        path_save           = values['-file1_9-'] + '/generator_path_save.txt'
        path_map_modbus     = f'{path_to_devstudio}/ModBus.xml'
        path_map_modbus503  = f'{path_to_devstudio}/ModBus503.xml'
        name_station        = values['-file2_2-']
        path_mapai_ref      = f'{path_to_devstudio}/AttributesMapAI_Ref.xml'
        path_description    = f'{path_to_devstudio}/AttributesMapDescription.xml'
        path_klk            = f'{path_to_devstudio}/AttributesMapKlk.xml'
        path_kont           = f'{path_to_devstudio}/AttributesMapKont.xml'
        path_signalname     = f'{path_to_devstudio}/AttributesMapSignalName.xml'
        path_tagname        = f'{path_to_devstudio}/AttributesMapTagName.xml'
        path_colorsheme     = f'{path_to_devstudio}/AttributesMapColorScheme.xml'
        path_analogsformat  = f'{path_to_devstudio}/AttributesAnalogsFormats.xml'
        path_egu            = f'{path_to_devstudio}/AttributesMapEGU.xml'
        path_analogtrends   = f'{path_to_devstudio}/AttributesAnalogsFormats.xml'

        save_string = (f'path_to_exel: {path_to_exel}\npath_to_devstudio: {path_to_devstudio}\n'
                       f'path_item: {path_item}\nНазвание станции: {name_station}\n'
                       f'path_file_txt: {path_file_txt}\npath_file_signals: {path_file_signals}\n'
                       f'prefix_system: {prefix_system}\nprefix_driver: {prefix_driver}\n'
                       f'path_sample: {path_sample}\npath_sample_msg: {path_sample_msg}\n'
                       f'path_sample_req: {path_sample_req}\npath_su: {path_su}\n'
                       f'path_imit: {path_imit}\nmb_adrr_AI: {mb_adrr_AI}\n'
                       f'mb_adrr_DI: {mb_adrr_DI}\nmb_adrr_DO: {mb_adrr_DO}\n'
                       f'Дата сформированного файла : {datetime.date.today()}\n'
                       f'Время сформированного файла: {datetime.datetime.now().time()}')
        if not os.path.exists(path_save):
            text_file = open(path_save, 'w')
            text_file.write(save_string)
            text_file.close()
        else:
            os.remove(path_save)
            text_file = open(path_save, 'w')
            text_file.write(save_string)
            text_file.close()
        # Запуск обработки экземпляра класса
        New_copy = Equipment(path_to_exel, path_to_adressmap, path_map_modbus, path_map_modbus503,
                             path_to_filenameomx, prefix_system, prefix_driver)
        # Передадим путь для логирования в отдельную функцию
        #logging(values['-file1_9-'])
        logger.info(f'Пути к файлам добавлены в новый документ: {path_save}')
        window['logger'].update(f'Открыт файл с сохранениями' + '\n', append=True)
    # Открываем файл и считываем сохраненные пути
    if event == 'Открыть файл':
        # Исключаем случайное нажатие по кнопке
        if values['-file2-'] == '': continue
        flag_not_click = True
        # Передадим путь для логирования в отдельную функцию
        #logging(re.split('/generator_path_save.txt', values['-file2-'])[0])
        window['logger'].update(f'Открыт файл с сохранениями' + '\n', append=True)
        logger.info(f'Открыт файл с сохранениями')
        try:
            with open(values['-file2-']) as paths:
                for string in paths:
                    split_str = string.strip().split(': ')
                    if split_str[0] == 'path_to_exel'       :
                        path_to_exel        = split_str[1]
                        window['-file1_1-'].update(path_to_exel)
                        logger.info(f'Путь к файлу конфигурации (.xlsx) найден')
                        window['logger'].update(f'Путь к файлу конфигурации (.xlsx) найден\n', append=True)
                    if split_str[0] == 'path_to_devstudio'  :
                        path_to_devstudio = split_str[1]
                        window['-file1_2-'].update(path_to_devstudio)
                        logger.info(f'Путь к папке с файлами DevStudio найден')
                        window['logger'].update(f'Путь к папке с файлами DevStudio найден\n', append=True)
                    if split_str[0] == 'path_item'          :
                        path_item           = split_str[1]
                        window['-file1_4-'].update(path_item)
                        logger.info(f'Файл для трендов item (.xlsx) найден')
                        window['logger'].update(f'Файл для трендов item (.xlsx) найден\n', append=True)
                    if split_str[0] == 'path_file_txt'      :
                        path_file_txt       = split_str[1]
                        window['-file1_5-'].update(path_file_txt)
                        logger.info(f'Папка хранения трендов найдена')
                        window['logger'].update(f'Папка хранения трендов найдена\n', append=True)
                    if split_str[0] == 'path_file_signals'  :
                        path_file_signals   = split_str[1]
                        window['-file1_6-'].update(path_file_signals)
                        logger.info(f'Папка SQL скрипта поиска сигналов найдена')
                        window['logger'].update(f'Папка SQL скрипта поиска сигналов найдена\n', append=True)
                    if split_str[0] == 'prefix_system'      :
                        prefix_system       = split_str[1]
                        window['-file1_7-'].update(prefix_system)
                        logger.info(f'Префикс системы: {prefix_system}')
                        window['logger'].update(f'Префикс системы: {prefix_system}\n', append=True)
                    if split_str[0] == 'prefix_driver'      :
                        prefix_driver       = split_str[1]
                        window['-file1_8-'].update(prefix_driver)
                        logger.info(f'Драйвер системы: {prefix_driver} ')
                        window['logger'].update(f'Драйвер системы: {prefix_driver}\n', append=True)
                    if split_str[0] == 'Название станции'   :
                        name_station       = split_str[1]
                        window['-file2_2-'].update(name_station)
                        logger.info(f'Название станции: {name_station}')
                        window['logger'].update(f'Название станции: {name_station}\n', append=True)
                    if split_str[0] == 'path_sample'        :
                        sample       = split_str[1]
                        window['SAMPLE'].update(sample)
                        logger.info(f'Путь генерации защит: {sample}')
                        window['logger'].update(f'Путь генерации защит: {sample}\n', append=True)
                    if split_str[0] == 'path_sample_msg'        :
                        path_sample_msg = split_str[1]
                        window['MSG_PATH_SAMPLE'].update(path_sample_msg)
                        logger.info(f'Путь хранения шаблонов сообщений: {path_sample_msg}')
                        window['logger'].update(f'Путь хранения шаблонов сообщений: {path_sample_msg}\n', append=True)
                    if split_str[0] == 'path_sample_req'        :
                        path_sample_req = split_str[1]
                        window['MSG_PATH_REQ'].update(path_sample_req)
                        logger.info(f'Путь хранения запросов сообщений: {path_sample_req}')
                        window['logger'].update(f'Путь хранения запросов сообщений: {path_sample_req}\n', append=True)
                    if split_str[0] == 'path_su':
                        path_su = split_str[1]
                        window['SU_PATH'].update(path_su)
                        logger.info(f'Путь хранения файлов СУ: {path_su}')
                        window['logger'].update(f'Путь хранения файлов СУ: {path_su}\n', append=True)
                    if split_str[0] == 'path_imit':
                        path_imit = split_str[1]
                        window['IMIT_PATH'].update(path_imit)
                        logger.info(f'Путь хранения файла xml имитатора: {path_imit}')
                        window['logger'].update(f'Путь хранения файла xml имитатора: {path_imit}\n', append=True)
                    if split_str[0] == 'mb_adrr_AI':
                        mb_adrr_AI = split_str[1]
                        window['Start_AI'].update(mb_adrr_AI)
                        logger.info(f'ModBus адрес AI: {mb_adrr_AI}')
                        window['logger'].update(f'ModBus адрес AI: {mb_adrr_AI}\n', append=True)
                    if split_str[0] == 'mb_adrr_DI':
                        mb_adrr_DI = split_str[1]
                        window['Start_DI'].update(mb_adrr_DI)
                        logger.info(f'ModBus адрес DI: {mb_adrr_DI}')
                        window['logger'].update(f'ModBus адрес DI: {mb_adrr_DI}\n', append=True)
                    if split_str[0] == 'mb_adrr_DO':
                        mb_adrr_DO = split_str[1]
                        window['Start_DO'].update(mb_adrr_DO)
                        logger.info(f'ModBus адрес DO: {mb_adrr_DO}')
                        window['logger'].update(f'ModBus адрес DO: {mb_adrr_DO}\n', append=True)

            if path_to_devstudio != '':
                path_to_adressmap   = f'{path_to_devstudio}/ODA.xml'
                path_map_modbus     = f'{path_to_devstudio}/ModBus.xml'
                path_map_modbus503  = f'{path_to_devstudio}/ModBus503.xml'
                path_to_filenameomx = f'{path_to_devstudio}/typical_prj.omx'

                New_copy = Equipment(path_to_exel, path_to_adressmap, path_map_modbus, path_map_modbus503,
                                     path_to_filenameomx, prefix_system, prefix_driver)
                logger.info('Экземпляр класса определен')
                paths.closed
            else:
                window['logger'].update(f'Отсутствует путь до папки с файлами проекта DevStudio. Работа генератора прекращена!\n', append=True)
                logger.info('Отсутствует путь до папки с файлами проекта DevStudio. Работа генератора прекращена!н')
        except:
            window['logger'].update('Отсутствует файл сохранений.  ' + '\n', append=True)
            logger.error(f'Отсутствует файл сохранений')

    # Экспорт КЗФКП
    # if event == 'READ_KZFKP':
    #     if values['PATH_KZFKP'] == '':
    #         logger.info(f'Не найден путь к файлy КЗФКП')
    #         window['logger'].update(f'Не найден путь к файлy КЗФКП\n', append=True)
    #         continue
    #     tabl = export_kzfkp(values['PATH_KZFKP'], values['PICK_USO'], values['NUM_SHEET'], True, False, False, list_row)
    #     window['PICK_USO'].update(value='Загружено. Выбери таблицу', values=tabl)
    # if event == 'READ_TABL':
    #     if values['PICK_USO'] == 'Загружено. Выбери таблицу':
    #         logger.info(f'Таблица не выбрана!')
    #         window['logger'].update(f'Таблица не выбрана!\n', append=True)
    #         continue
    #     if values['NUM_SHEET'] == '':
    #         logger.info(f'Не указан ряд с заголовком таблицы!')
    #         window['logger'].update(f'Не указан ряд с заголовком таблицы!\n', append=True)
    #         continue
    #     hat_tabl = export_kzfkp(values['PATH_KZFKP'], values['PICK_USO'], values['NUM_SHEET'], False, True, False, list_row)
    #     window['TAG'].    update(value='Выбери столбец: Тэг',          values=hat_tabl)
    #     window['NAME'].   update(value='Выбери столбец: Наименование', values=hat_tabl)
    #     window['SCHEME']. update(value='Выбери столбец: Схема',        values=hat_tabl)
    #     window['KLK'].    update(value='Выбери столбец: КлК',          values=hat_tabl)
    #     window['CONTACT'].update(value='Выбери столбец: Контакт',      values=hat_tabl)
    #     window['RACK'].   update(value='Выбери столбец: Корзина',      values=hat_tabl)
    #     window['MODUL'].  update(value='Выбери столбец: Модуль',       values=hat_tabl)
    #     window['CHANNEL'].update(value='Выбери столбец: Канал',        values=hat_tabl)
    # if event == 'LOAD_KZFKP':
    #     if values['TAG']     == 'Выбери столбец: Тэг'     or values['NAME']    == 'Выбери столбец: Наименование' or \
    #        values['SCHEME']  == 'Выбери столбец: Схема'   or values['KLK']     == 'Выбери столбец: КлК'          or \
    #        values['CONTACT'] == 'Выбери столбец: Контакт' or values['RACK']    == 'Выбери столбец: Корзина'      or \
    #        values['MODUL']   == 'Выбери столбец: Модуль'  or values['CHANNEL'] == 'Выбери столбец: Канал':
    #         logger.info(f'Один или несколько столбцов не выбраны!')
    #         window['logger'].update(f'Один или несколько столбцов не выбраны!\n', append=True)
    #         continue
    #     list_row = {'Тэг'          : values['TAG'],
    #                 'Наименование' : values['NAME'],
    #                 'Схема'        : values['SCHEME'],
    #                 'КлК'          : values['KLK'],
    #                 'Контакт'      : values['CONTACT'],
    #                 'Корзина'      : values['RACK'],
    #                 'Модуль'       : values['MODUL'],
    #                 'Канал'        : values['CHANNEL']}
    #     export_kzfkp(values['PATH_KZFKP'], values['PICK_USO'], values['NUM_SHEET'], False, False, True, list_row)
    # if event == 'CLEAR_KZFKP':
    #     remove_tabl()

    # Генерация аналоговых сигналов
    if event == '-AI_DEV-' and flag_not_click:
        logger.info(f'Analogs: генерация объектов DevStudio')
        function_state = New_copy.analogs_omx()
        window['logger'].update(f'{function_state}\n', append=True)
    if event == '-AI_MAP-' and flag_not_click:
        if values['-MODBUS-'] is True and values['AN_503'] is True:
            logger.info(f'Analogs: Внимание! Заполнится 2 типа карты адресов!')
        if values['-OPCDA-'] is True:
            logger.info(f'Analogs: заполнение карты адресов для {"OPCDA"}')
            function_state = New_copy.analogs_map()
            window['logger'].update(f'{function_state}\n', append=True)
        if values['-MODBUS-'] is True:
            logger.info(f'Analogs: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.analogs_map_modbus(False)
            window['logger'].update(f'{function_state}\n', append=True)
        if values['AN_503'] is True:
            logger.info(f'Analogs: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.analogs_map_modbus(True)
            window['logger'].update(f'{function_state}\n', append=True)
    if event == '-AI_CLEAR-' and flag_not_click:
        logger.info(f'Analogs: очистка объектов и карты адресов')
        function_state = New_copy.clear_objects('Analogs', values['-MODBUS-'], values['-OPCDA-'], values['-OPCUA-'])
        window['logger'].update(f'{function_state}\n', append=True)
    # Генерация входных дискретных сигналов
    if event == '-DI_DEV-' and flag_not_click:
        logger.info(f'Diskrets: генерация объектов DevStudio')
        function_state = New_copy.diskret_in_omx()
        window['logger'].update(f'{function_state}\n', append=True)
    if event == '-DI_MAP-' and flag_not_click:
        if values['-OPCDA-'] is True:
            logger.info(f'Diskrets: заполнение карты адресов для {"OPCDA"}')
            function_state = New_copy.diskret_in_map()
            window['logger'].update(f'{function_state}\n', append=True)
        if values['-MODBUS-'] is True:
            logger.info(f'Diskrets: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.diskret_in_map_modbus()
            window['logger'].update(f'{function_state}\n', append=True)
    if event == '-DI_CLEAR-' and flag_not_click:
        logger.info(f'Diskrets: очистка объектов и карты адресов')
        function_state = New_copy.clear_objects('Diskrets', values['-MODBUS-'], values['-OPCDA-'], values['-OPCUA-'])
        window['logger'].update(f'{function_state}\n', append=True)
    # Генерация МПНА
    if event == '-PUMPS_DEV-' and flag_not_click:
        logger.info(f'NAs: генерация объектов DevStudio')
        function_state = New_copy.pumps_omx()
        window['logger'].update(f'{function_state}\n', append=True)
    if event == '-PUMPS_MAP-' and flag_not_click:
        if values['-OPCDA-'] is True:
            logger.info(f'NAs: заполнение карты адресов для {"OPCDA"}')
            function_state = New_copy.pumps_map()
            window['logger'].update(f'{function_state}\n', append=True)
        if values['-MODBUS-'] is True:
            logger.info(f'NAs: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.pumps_map_modbus()
            window['logger'].update(f'{function_state}\n', append=True)
    if event == '-PUMPS_CLEAR-' and flag_not_click:
        logger.info(f'NAs: очистка объектов и карты адресов')
        function_state = New_copy.clear_objects('NAs', values['-MODBUS-'], values['-OPCDA-'], values['-OPCUA-'])
        window['logger'].update(f'{function_state}\n', append=True)
    # Генерация вспомсистем
    if event == '-VS_DEV-' and flag_not_click:
        logger.info(f'AuxSystems: генерация объектов DevStudio')
        function_state = New_copy.auxsystem_omx()
        window['logger'].update(f'{function_state}\n', append=True)
    if event == '-VS_MAP-' and flag_not_click:
        if values['-OPCDA-'] is True:
            logger.info(f'AuxSystems: заполнение карты адресов для {"OPCDA"}')
            function_state = New_copy.auxsystem_map()
            window['logger'].update(f'{function_state}\n', append=True)
        if values['-MODBUS-'] is True:
            logger.info(f'AuxSystems: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.auxsystem_map_modbus()
            window['logger'].update(f'{function_state}\n', append=True)
    if event == '-VS_CLEAR-' and flag_not_click:
        logger.info(f'AuxSystems: очистка объектов и карты адресов')
        function_state = New_copy.clear_objects('AuxSystems', values['-MODBUS-'], values['-OPCDA-'], values['-OPCUA-'])
        window['logger'].update(f'{function_state}\n', append=True)
    # Генерация задвижек
    if event == '-ZD_DEV-' and flag_not_click:
        logger.info(f'Valves: генерация объектов DevStudio')
        function_state = New_copy.valves_omx()
        window['logger'].update(f'{function_state}\n', append=True)
    if event == '-ZD_MAP-' and flag_not_click:
        if values['-OPCDA-'] is True:
            logger.info(f'Valves: заполнение карты адресов для {"OPCDA"}')
            function_state = New_copy.valves_map()
            window['logger'].update(f'{function_state}\n', append=True)
        if values['-MODBUS-'] is True:
            logger.info(f'Valves: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.valves_map_modbus()
            window['logger'].update(f'{function_state}\n', append=True)
    if event == '-ZD_CLEAR-' and flag_not_click:
        logger.info(f'Valves: очистка объектов и карты адресов')
        function_state = New_copy.clear_objects('Valves', values['-MODBUS-'], values['-OPCDA-'], values['-OPCUA-'])
        window['logger'].update(f'{function_state}\n', append=True)
    # Генерация смежных систем
    if event == '-SS_DEV-' and flag_not_click:
        logger.info(f'SS: генерация объектов DevStudio')
        function_state = New_copy.relayted_system_omx()
        window['logger'].update(f'{function_state}\n', append=True)
    if event == '-SS_MAP-' and flag_not_click:
        if values['-OPCDA-'] is True:
            logger.info(f'SS: заполнение карты адресов для {"OPCDA"}')
            function_state = New_copy.relayted_system_map()
            window['logger'].update(f'{function_state}\n', append=True)
        if values['-MODBUS-'] is True:
            logger.info(f'SS: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.relayted_system_map_modbus()
            window['logger'].update(f'{function_state}\n', append=True)
    if event == '-SS_CLEAR-' and flag_not_click:
        logger.info(f'SS: очистка объектов и карты адресов')
        function_state = New_copy.clear_objects('SSs', values['-MODBUS-'], values['-OPCDA-'], values['-OPCUA-'])
        window['logger'].update(f'{function_state}\n', append=True)
    # Индикаторы событий Picture
    if event == '-PIC_DEV-' and flag_not_click:
        logger.info(f'Pictures: генерация объектов DevStudio')
        function_state = New_copy.picture_omx()
        window['logger'].update(f'{function_state}\n', append=True)
    if event == '-PIC_MAP-' and flag_not_click:
        if values['-OPCDA-'] is True:
            logger.info(f'Pictures: заполнение карты адресов для {"OPCDA"}')
            function_state = New_copy.picture_map()
            window['logger'].update(f'{function_state}\n', append=True)
        if values['-MODBUS-'] is True:
            logger.info(f'Pictures: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.picture_map_modbus()
            window['logger'].update(f'{function_state}\n', append=True)
    if event == '-PIC_CLEAR-' and flag_not_click:
        logger.info(f'Pictures: очистка объектов и карты адресов')
        function_state = New_copy.clear_objects('Pictures', values['-MODBUS-'], values['-OPCDA-'], values['-OPCUA-'])
        window['logger'].update(f'{function_state}\n', append=True)
    # UTS
    if event == '-UTS_DEV-' and flag_not_click:
        logger.info(f'UTSs: генерация объектов DevStudio')
        function_state = New_copy.uts_omx()
        window['logger'].update(f'{function_state}\n', append=True)
    if event == '-UTS_MAP-' and flag_not_click:
        if values['-OPCDA-'] is True:
            logger.info(f'UTSs: заполнение карты адресов для {"OPCDA"}')
            function_state = New_copy.uts_map()
            window['logger'].update(f'{function_state}\n', append=True)
        if values['-MODBUS-'] is True:
            logger.info(f'UTSs: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.uts_map_modbus()
            window['logger'].update(f'{function_state}\n', append=True)
    if event == '-UTS_CLEAR-' and flag_not_click:
        logger.info(f'UTSs: очистка объектов и карты адресов')
        function_state = New_copy.clear_objects('UTSs', values['-MODBUS-'], values['-OPCDA-'], values['-OPCUA-'])
        window['logger'].update(f'{function_state}\n', append=True)
    # UPTS
    if event == '-UPTS_DEV-' and flag_not_click:
        logger.info(f'UPTSs: генерация объектов DevStudio')
        function_state = New_copy.upts_omx()
        window['logger'].update(f'{function_state}\n', append=True)
    if event == '-UPTS_MAP-' and flag_not_click:
        if values['-OPCDA-'] is True:
            logger.info(f'UPTSs: заполнение карты адресов для {"OPCDA"}')
            function_state = New_copy.upts_map()
            window['logger'].update(f'{function_state}\n', append=True)
        if values['-MODBUS-'] is True:
            logger.info(f'UPTSs: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.upts_map_modbus()
            window['logger'].update(f'{function_state}\n', append=True)
    if event == '-UPTS_CLEAR-' and flag_not_click:
        logger.info(f'UPTSs: очистка объектов и карты адресов')
        function_state = New_copy.clear_objects('UPTSs', values['-MODBUS-'], values['-OPCDA-'], values['-OPCUA-'])
        window['logger'].update(f'{function_state}\n', append=True)
    # KTPR(МНС)
    if event == '-KTPR_DEV-' and flag_not_click:
        logger.info(f'KTPRs: генерация объектов DevStudio')
        function_state = New_copy.ktpr_omx()
        window['logger'].update(f'{function_state}\n', append=True)
    if event == '-KTPR_MAP-' and flag_not_click:
        if values['-OPCDA-'] is True:
            logger.info(f'KTPRs: заполнение карты адресов для {"OPCDA"}')
            function_state = New_copy.ktpr_map()
            window['logger'].update(f'{function_state}\n', append=True)
        if values['-MODBUS-'] is True:
            logger.info(f'KTPRs: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.ktpr_map_modbus()
            window['logger'].update(f'{function_state}\n', append=True)
    if event == '-KTPR_CLEAR-' and flag_not_click:
        logger.info(f'KTPRs: очистка объектов и карты адресов')
        function_state = New_copy.clear_objects('KTPRs', values['-MODBUS-'], values['-OPCDA-'], values['-OPCUA-'])
        window['logger'].update(f'{function_state}\n', append=True)
    # KTPRP(ПТ)
    if event == '-KTPRP_DEV-' and flag_not_click:
        logger.info(f'KTPRs: генерация объектов DevStudio')
        function_state = New_copy.ktprp_omx()
        window['logger'].update(f'{function_state}\n', append=True)
    if event == '-KTPRP_MAP-' and flag_not_click:
        if values['-OPCDA-'] is True:
            logger.info(f'KTPRs: заполнение карты адресов для {"OPCDA"}')
            function_state = New_copy.ktprp_map()
            window['logger'].update(f'{function_state}\n', append=True)
        if values['-MODBUS-'] is True:
            logger.info(f'KTPRs: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.ktprp_map_modbus()
            window['logger'].update(f'{function_state}\n', append=True)
    if event == '-KTPRP_CLEAR-' and flag_not_click:
        logger.info(f'KTPRs: очистка объектов и карты адресов')
        function_state = New_copy.clear_objects('KTPRs', values['-MODBUS-'], values['-OPCDA-'], values['-OPCUA-'])
        window['logger'].update(f'{function_state}\n', append=True)
    # KTPRA
    if event == '-KTPRA_DEV-' and flag_not_click:
        logger.info(f'KTPRAs: генерация объектов DevStudio')
        function_state = New_copy.ktpra_omx()
        window['logger'].update(f'{function_state}\n', append=True)
    if event == '-KTPRA_MAP-' and flag_not_click:
        if values['-OPCDA-'] is True:
            logger.info(f'KTPRAs: заполнение карты адресов для {"OPCDA"}')
            function_state = New_copy.ktpra_map()
            window['logger'].update(f'{function_state}\n', append=True)
        if values['-MODBUS-'] is True:
            logger.info(f'KTPRAs: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.ktpra_map_modbus()
            window['logger'].update(f'{function_state}\n', append=True)
    if event == '-KTPRA_CLEAR-' and flag_not_click:
        logger.info(f'KTPRAs: очистка объектов и карты адресов')
        function_state = New_copy.clear_objects('KTPRAs', values['-MODBUS-'], values['-OPCDA-'], values['-OPCUA-'])
        window['logger'].update(f'{function_state}\n', append=True)
    # GMPNA
    if event == '-GMPNA_DEV-' and flag_not_click:
        logger.info(f'GMPNAs: генерация объектов DevStudio')
        function_state = New_copy.gmpna_omx()
        window['logger'].update(f'{function_state}\n', append=True)
    if event == '-GMPNA_MAP-' and flag_not_click:
        if values['-OPCDA-'] is True:
            logger.info(f'GMPNAs: заполнение карты адресов для {"OPCDA"}')
            function_state = New_copy.gmpna_map()
            window['logger'].update(f'{function_state}\n', append=True)
        if values['-MODBUS-'] is True:
            logger.info(f'GMPNAs: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.gmpna_map_modbus()
            window['logger'].update(f'{function_state}\n', append=True)
    if event == '-GMPNA_CLEAR-' and flag_not_click:
        logger.info(f'GMPNAs: очистка объектов и карты адресов')
        function_state = New_copy.clear_objects('GMPNAs', values['-MODBUS-'], values['-OPCDA-'], values['-OPCUA-'])
        window['logger'].update(f'{function_state}\n', append=True)
    # Пожарные извещатели
    if event == '-PI_DEV-' and flag_not_click:
        logger.info(f'PIs: генерация объектов DevStudio')
        function_state = New_copy.pi_omx()
        window['logger'].update(f'{function_state}\n', append=True)
    if event == '-PI_MAP-' and flag_not_click:
        if values['-OPCDA-'] is True:
            logger.info(f'PIs: заполнение карты адресов для {"OPCDA"}')
            function_state = New_copy.pi_map()
            window['logger'].update(f'{function_state}\n', append=True)
        if values['-MODBUS-'] is True:
            logger.info(f'PIs: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.pi_map_modbus()
            window['logger'].update(f'{function_state}\n', append=True)
    if event == '-PI_CLEAR-' and flag_not_click:
        logger.info(f'PIs: очистка объектов и карты адресов')
        function_state = New_copy.clear_objects('PIs', values['-MODBUS-'], values['-OPCDA-'], values['-OPCUA-'])
        window['logger'].update(f'{function_state}\n', append=True)
    # Пожарные зоны
    if event == '-PZ_DEV-' and flag_not_click:
        logger.info(f'PZs: генерация объектов DevStudio')
        function_state = New_copy.pz_omx()
        window['logger'].update(f'{function_state}\n', append=True)
    if event == '-PZ_MAP-' and flag_not_click:
        if values['-OPCDA-'] is True:
            logger.info(f'PZs: заполнение карты адресов для {"OPCDA"}')
            function_state = New_copy.pz_map()
            window['logger'].update(f'{function_state}\n', append=True)
        if values['-MODBUS-'] is True:
            logger.info(f'PZs: заполнение карты адресов для {"MODBUS"}')
            function_state = New_copy.pz_map_modbus()
            window['logger'].update(f'{function_state}\n', append=True)
    if event == '-PZ_CLEAR-' and flag_not_click:
        logger.info(f'PZs: очистка объектов и карты адресов')
        function_state = New_copy.clear_objects('PZs', values['-MODBUS-'], values['-OPCDA-'], values['-OPCUA-'])
        window['logger'].update(f'{function_state}\n', append=True)

    # Карта атрибутов
    # AttributesMapColorScheme.xml
    if event == '-COLOR_MAP-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        logger.info(f'AttributesMapColorScheme.xml: генерация началась')
        function_state = New_copy.color_diskrets(f'{values["-file1_2-"]}/AttributesMapColorScheme.xml')
        window['logger'].update(f'{function_state}\n', append=True)
        logger.info(f'AttributesMapColorScheme.xml: генерация закончена')
    if event == '-COLOR_CLEAR-' and flag_not_click:
        logger.info(f'AttributesMapColorScheme.xml: очистка карты атрубутов')
        function_state = New_copy.clear_map('AttributesMapColorScheme.xml', '.Diskrets.', f'{values["-file1_2-"]}/AttributesMapColorScheme.xml')
        window['logger'].update(f'{function_state}\n', append=True)
    # AttributesAnalogsFormats.xml
    if event == '-FORMAT_MAP-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'AttributesAnalogsFormats.xml: генерация началась')
        function_state = New_copy.analogformat_map(f"{values['-file1_2-']}/AttributesAnalogsFormats.xml")
        window['logger'].update(f'{function_state}\n', append=True)
        logger.info(f'AttributesAnalogsFormats.xml: генерация закончена')
    if event == '-FORMAT_CLEAR-' and flag_not_click:
        logger.info(f'AttributesAnalogsFormats.xml: очистка карты атрубутов')
        function_state = New_copy.clear_map('AttributesAnalogsFormats.xml', '.Analogs.', f"{values['-file1_2-']}/AttributesAnalogsFormats.xml")
        window['logger'].update(f'{function_state}\n', append=True)
    # AttributesMapEGU.xml
    if event == '-EGU_MAP-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'AttributesMapEGU.xml: генерация началась')
        function_state = New_copy.egu_map(f"{values['-file1_2-']}/AttributesMapEGU.xml")
        window['logger'].update(f'{function_state}\n', append=True)
        logger.info(f'AttributesMapEGU.xml: генерация закончена')
    if event == '-EGU_CLEAR-' and flag_not_click:
        logger.info(f'AttributesMapEGU.xml: очистка карты атрубутов')
        function_state = New_copy.clear_map('AttributesMapEGU.xml', '.Analogs.', f"{values['-file1_2-']}/AttributesMapEGU.xml")
        window['logger'].update(f'{function_state}\n', append=True)
    # AttributesAnalogTrends.xml
    if event == '-TREND_MAP-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'AttributesAnalogTrends.xml: генерация началась')
        function_state = New_copy.analogs_trend(f"{values['-file1_2-']}/AttributesAnalogTrends.xml")
        window['logger'].update(f'{function_state}\n', append=True)
        logger.info(f'AttributesAnalogTrends.xml: генерация закончена')
    if event == '-TREND_CLEAR-' and flag_not_click:
        logger.info(f'AttributesAnalogTrends.xml: очистка карты атрубутов')
        function_state = New_copy.clear_map('AttributesAnalogTrends.xml', '.Analogs.', f"{values['-file1_2-']}/AttributesAnalogTrends.xml")
        window['logger'].update(f'{function_state}\n', append=True)
    # Готовность пожарных зон
    if event == '-DESC_MAP-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'Готовность пожарных зон: генерация началась')
        function_state = New_copy.pzs_ready_map(f"{values['-file1_2-']}/AttributesMapDescription.xml")
        window['logger'].update(f'{function_state}\n', append=True)
        logger.info(f'Готовность пожарных зон: генерация закончена')
    if event == '-DESC_CLEAR-' and flag_not_click:
        logger.info(f'Готовность пожарных зон: очистка карты атрубутов')
        function_state = New_copy.clear_map('Готовность пожарных зон', '.PZs.', f"{values['-file1_2-']}/AttributesMapDescription.xml")
        window['logger'].update(f'{function_state}\n', append=True)
    # SQL запрос поиска сигналов
    if event == '-SQL-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if values['-file1_6-'] == '':
            logger.info(f'Не найдена конечная папка для сохранения')
            window['logger'].update(f'Не найдена конечная папка для сохранения\n', append=True)
            continue

        logger.info(f'Генерация SQL запроса началась')
        function_state = New_copy.sql_script_search(values['-file1_6-'])
        window['logger'].update(f'{function_state}\n', append=True)
        logger.info(f'Генерация SQL запроса завершена')
    # Тренды
    if event == '-TREND-' and flag_not_click:
        if values['-file1_4-'] != '':
            logger.info(f'Файл items.xml найден')
        else:
            logger.info(f'Файл items.xml не найден\nГенерация завершена! Проверь пути!')
            window['logger'].update(f'Файл items.xml не найден\nГенерация завершена! Проверь пути!',append=True)
            continue
        if values['-file1_5-'] != '':
            logger.info(f'Конечная папка для файла тренда выбрана: {values["-file1_6-"]}\SQLSearch.xml')
        else:
            logger.info(f'Конечная папка для файла тренда не выбрана\nГенерация завершена! Проверь пути!')
            window['logger'].update(f'Конечная папка для файла тренда не выбрана\nГенерация завершена! Проверь пути!', append=True)
            continue
        if values['-file2_2-'] == '':
            logger.info(f'Отсутствует название станции для трендов\nГенерация завершена!')
            window['logger'].update(f'Отсутствует название станции для трендов\nГенерация завершена!', append=True)
            continue

        logger.info(f'Генерация файла тренда началась')
        function_state = New_copy.trends_xml(values['-file1_4-'], values['-file1_5-'], values['-file2_2-'])
        window['logger'].update(f'{function_state}\n', append=True)
        logger.info(f'Генерация файла завершена')
    if event == 'TREND_Lin_MB' and flag_not_click:

        if values['-file1_5-'] != '':
            logger.info(f'Конечная папка для файла тренда выбрана: {values["-file1_6-"]}\SQLSearch.xml')
        else:
            logger.info(f'Конечная папка для файла тренда не выбрана\nГенерация завершена! Проверь пути!')
            window['logger'].update(f'Конечная папка для файла тренда не выбрана\nГенерация завершена! Проверь пути!', append=True)
            continue
        if values['-file2_2-'] == '':
            logger.info(f'Отсутствует название станции для трендов\nГенерация завершена!')
            window['logger'].update(f'Отсутствует название станции для трендов\nГенерация завершена!', append=True)
            continue

        logger.info(f'Генерация файла тренда началась')
        function_state = New_copy.trends_linux_xml(values['-file1_5-'], values['-file2_2-'])
        window['logger'].update(f'{function_state}\n', append=True)
        logger.info(f'Генерация файла завершена')

    # Генерация кадров ВУ
    # Создадим шаблон по команде
    if event == 'NEW_SAMPLE_DEF':
        if values['SAMPLE'] == '':
            logger.error(f'Отсутствует папка для размещения шаблона')
            window['logger'].update(f'Отсутствует папка для размещения шаблона\n', append=True)
            continue
        defence_gen(values['SAMPLE'])
        logger.info(f'Шаблон для генерации защит и готовностей создан')
        window['logger'].update(f'Шаблон для генерации защит и готовностей создан\n', append=True)
    if event == 'NEW_SAMPLE_UTS':
        if values['SAMPLE'] == '':
            logger.error(f'Отсутствует папка для размещения шаблона')
            window['logger'].update(f'Отсутствует папка для размещения шаблона\n', append=True)
            continue
        uts_upts_gen(values['SAMPLE'])
        logger.info(f'Шаблон для генерации формы табло и сирен создан')
        window['logger'].update(f'Шаблон для генерации формы табло и сирен создан\n', append=True)
    if event == 'NEW_SAMPLE_DIAG':
        if values['SAMPLE'] == '':
            logger.error(f'Отсутствует папка для размещения шаблона')
            window['logger'].update(f'Отсутствует папка для размещения шаблона\n', append=True)
            continue
        diag_gen(values['SAMPLE'])
        logger.info(f'Шаблон для генерации форм диагностики создан')
        window['logger'].update(f'Шаблон для генерации форм диагностики создан\n', append=True)
    if event == 'NEW_SAMPLE_DIAG_SRV':
        if values['SAMPLE'] == '':
            logger.error(f'Отсутствует папка для размещения шаблона')
            window['logger'].update(f'Отсутствует папка для размещения шаблона\n', append=True)
            continue
        diag_gen(values['SAMPLE'])
        logger.info(f'Шаблон для генерации форм диагностики создан')
        window['logger'].update(f'Шаблон для генерации форм диагностики создан\n', append=True)

    # Готовности и защиты
    if event == 'START_DEFENCE' and flag_not_click:
        if values['SAMPLE'] == '':
            logger.error(f'Отсутствует папка для размещения кадров')
            window['logger'].update(f'Отсутствует папка для размещения кадров\n', append=True)
            continue
        if values['DEFENC'] is False and values['READIF'] is False and \
           values['STATDEF']is False and values['PTDEF'] is False:
            logger.error(f'Не выбрано что генерить')
            window['logger'].update(f'Не выбрано что генерить\n', append=True)
            continue
        if not os.path.exists(f"{values['SAMPLE']}\Form_Defences_default.omobj"):
            logger.error(f'Отсутствует шаблон. Нажми кнопку создать шаблон')
            window['logger'].update(f'Отсутствует шаблон. Нажми кнопку создать шаблон\n', append=True)
            continue
        if values['DEFENC'] is True:
            logger.info(f'Генерация агрегатных защит начата')
            window['logger'].update(f'Генерация агрегатных защит начата\n', append=True)
            gen_station_defence(f"{values['SAMPLE']}\\", values['-file1_1-'], 'KTPRA')
            logger.info(f'Генерация агрегатных защит завершена')
            window['logger'].update(f'Генерация агрегатных защит завершена\n', append=True)
        if values['READIF'] is True:
            logger.info(f'Генерация агрегатных готовностей начата')
            window['logger'].update(f'Генерация агрегатных готовностей начата\n', append=True)
            gen_station_defence(f"{values['SAMPLE']}\\", values['-file1_1-'], 'GMPNA')
            logger.info(f'Генерация агрегатных готовностей завершена')
            window['logger'].update(f'Генерация агрегатных готовностей завершена\n', append=True)
        if values['STATDEF'] is True:
            logger.info(f'Генерация общестанционных защит начата')
            window['logger'].update(f'Генерация общестанционных защит начата\n', append=True)
            gen_station_defence(f"{values['SAMPLE']}\\", values['-file1_1-'], 'KTPR')
            logger.info(f'Генерация общестанционных защит завершена')
            window['logger'].update(f'Генерация общестанционных защит завершена\n', append=True)
        if values['PTDEF'] is True:
            logger.info(f'Генерация противопожарных защит начата')
            window['logger'].update(f'Генерация противопожарных защит начата\n', append=True)
            gen_station_defence(f"{values['SAMPLE']}\\", values['-file1_1-'], 'KTPRP')
            logger.info(f'Генерация противопожарных защит завершена')
            window['logger'].update(f'Генерация противопожарных защит завершена\n', append=True)
    # UTS and UPTS
    if event == 'START_UTS' and flag_not_click:
        if values['SAMPLE'] == '':
            logger.error(f'Отсутствует папка для размещения кадров')
            window['logger'].update(f'Отсутствует папка для размещения кадров\n', append=True)
            continue
        if values['UTS_GEN'] is False and values['UPTS_GEN'] is False:
            logger.error(f'Не выбрано что генерить')
            window['logger'].update(f'Не выбрано что генерить\n', append=True)
            continue
        if not os.path.exists(f"{values['SAMPLE']}\Form_UTS_UPTS_default.omobj"):
            logger.error(f'Отсутствует шаблон. Нажми кнопку создать шаблон')
            window['logger'].update(f'Отсутствует шаблон. Нажми кнопку создать шаблон\n', append=True)
            continue
        if values['UTS_GEN'] is True:
            logger.info(f'Генерация табло и сирен для МНС начата')
            window['logger'].update(f'Генерация табло и сирен для МНС начата\n', append=True)
            gen_uts_upts(f"{values['SAMPLE']}/", values['-file1_1-'], 'UTS', values['Verify'])
            logger.info(f'Генерация табло и сирен для МНС завершена')
            window['logger'].update(f'Генерация табло и сирен для МНС завершена\n', append=True)

        if values['UPTS_GEN'] is True:
            logger.info(f'Генерация табло и сирен для ПТ начата')
            window['logger'].update(f'Генерация табло и сирен для ПТ начата\n', append=True)
            gen_uts_upts(f"{values['SAMPLE']}/", values['-file1_1-'], 'UPTS', values['Verify'])
            logger.info(f'Генерация табло и сирен для ПТ завершена')
            window['logger'].update(f'Генерация табло и сирен для ПТ завершена\n', append=True)
    # Diag
    if event == 'START_GEN_DIAG' and flag_not_click:
        if values['SAMPLE'] == '':
            logger.error(f'Отсутствует папка для размещения кадров')
            window['logger'].update(f'Отсутствует папка для размещения кадров\n', append=True)
            continue
        if values['DIAG_MNS'] is False and values['DIAG_PT'] is False:
            logger.error(f'Не выбрано что генерить')
            window['logger'].update(f'Не выбрано что генерить\n', append=True)
            continue
        if not os.path.exists(f"{values['SAMPLE']}\D_USO_Template.omobj"):
            logger.error(f'Отсутствует шаблон. Нажми кнопку создать шаблон')
            window['logger'].update(f'Отсутствует шаблон. Нажми кнопку создать шаблон\n', append=True)
            continue
        if values['DIAG_MNS'] is True:
            logger.info(f'Генерация кадров диагностики для МНС начата')
            window['logger'].update(f'Генерация кадров диагностики для МНС начата\n', append=True)
            generate_uso(f"{values['SAMPLE']}/", values['-file1_1-'], False, 'MNS_')
            logger.info(f'Генерация кадров диагностики для МНС завершена')
            window['logger'].update(f'Генерация кадров диагностики для МНС завершена\n', append=True)
        if values['DIAG_PT'] is True:
            logger.info(f'Генерация кадров диагностики для ПТ начата')
            window['logger'].update(f'Генерация кадров диагностики для ПТ начата\n', append=True)
            generate_uso(f"{values['SAMPLE']}/", values['-file1_1-'], True, 'PT_')
            logger.info(f'Генерация кадров диагностики для ПТ завершена')
            window['logger'].update(f'Генерация кадров диагностики для ПТ завершена\n', append=True)
    # Служебные сигналы
    if event == 'START_GEN_DIAG_SRV' and flag_not_click:
        if values['SAMPLE'] == '':
            logger.error(f'Отсутствует папка для размещения кадров')
            window['logger'].update(f'Отсутствует папка для размещения кадров\n', append=True)
            continue
        if values['DIAG_MNS_SRV'] is False and values['DIAG_PT_SRV'] is False:
            logger.error(f'Не выбрано что генерить')
            window['logger'].update(f'Не выбрано что генерить\n', append=True)
            continue
        if not os.path.exists(f"{values['SAMPLE']}\D_USO_Template.omobj"):
            logger.error(f'Отсутствует шаблон. Нажми кнопку создать шаблон')
            window['logger'].update(f'Отсутствует шаблон. Нажми кнопку создать шаблон\n', append=True)
            continue
        if values['DIAG_MNS_SRV'] is True:
            logger.info(f'Генерация служебных сигналов для МНС начата')
            window['logger'].update(f'Генерация служебных сигналов для МНС начата\n', append=True)
            generate_uso(f"{values['SAMPLE']}/", values['-file1_1-'], False, 'MNS_')
            logger.info(f'Генерация служебных сигналов для МНС завершена')
            window['logger'].update(f'Генерация служебных сигналов для МНС завершена\n', append=True)
        if values['DIAG_PT_SRV'] is True:
            logger.info(f'Генерация служебных сигналов для ПТ начата')
            window['logger'].update(f'Генерация служебных сигналов для ПТ начата\n', append=True)
            generate_uso(f"{values['SAMPLE']}/", values['-file1_1-'], True, 'PT_')
            logger.info(f'Генерация служебных сигналов для ПТ завершена')
            window['logger'].update(f'Генерация служебных сигналов для ПТ завершена\n', append=True)

    # Сообщения
    # Диагностика
    if event == 'DIAG_MSG' and flag_not_click:
        if values['MSG_PATH_SAMPLE'] == '':
            logger.error(f'Отсутствует папка для размещения шаблонов')
            window['logger'].update(f'Отсутствует папка для размещения шаблонов\n', append=True)
            continue
        if values['MSG_PATH_REQ'] == '':
            logger.error(f'Отсутствует папка для размещения запросов')
            window['logger'].update(f'Отсутствует папка для размещения запросов\n', append=True)
            continue
        logger.info(f'Генерация сообщений для диагностики начата')
        window['logger'].update(f'Генерация сообщений для диагностики начата\n', append=True)
        # Генерация сообщений
        msg_report = New_copy.msg_racks(f"{values['MSG_PATH_SAMPLE']}/", (f"{values['MSG_PATH_REQ']}/"))
        window['logger'].update(f'{msg_report}\n', append=True)

        msg_report = New_copy.msg_modules(f"{values['MSG_PATH_SAMPLE']}/", (f"{values['MSG_PATH_REQ']}/"))
        window['logger'].update(f'{msg_report}\n', append=True)

        msg_report = New_copy.msg_modules_rs(f"{values['MSG_PATH_SAMPLE']}/", (f"{values['MSG_PATH_REQ']}/"))
        window['logger'].update(f'{msg_report}\n', append=True)

        logger.info(f'Генерация сообщений для диагностики завершена')
        window['logger'].update(f'Генерация сообщений для диагностики завершена\n', append=True)
    # DO
    if event == 'DO_MSG' and flag_not_click:
        if values['MSG_PATH_SAMPLE'] == '':
            logger.error(f'Отсутствует папка для размещения шаблонов')
            window['logger'].update(f'Отсутствует папка для размещения шаблонов\n', append=True)
            continue
        if values['MSG_PATH_REQ'] == '':
            logger.error(f'Отсутствует папка для размещения запросов')
            window['logger'].update(f'Отсутствует папка для размещения запросов\n', append=True)
            continue
        logger.info(f'Генерация сообщений DO начата')
        window['logger'].update(f'Генерация сообщений DO начата\n', append=True)
        # Генерация сообщений
        msg_report = New_copy.msg_do(f"{values['MSG_PATH_SAMPLE']}/", (f"{values['MSG_PATH_REQ']}/"))
        window['logger'].update(f'{msg_report}\n', append=True)

        logger.info(f'Генерация сообщений DO завершена')
        window['logger'].update(f'Генерация сообщений DO завершена\n', append=True)

    # Диагностика
    # SE
    # AI
    if event == '-AI_DIAG-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapAI_Ref.xml")     and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml")        and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml")       and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(f'Diag.AIs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(f'Diag.AIs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.AIs: генерация началась')
        function_state = New_copy.diag_analogs_in(f"{values['-file1_2-']}/AttributesMapAI_Ref.xml", f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                                  f"{values['-file1_2-']}/AttributesMapKont.xml", f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                                  f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.AIs: генерация закончена\n', append=True)
        logger.info(f'Diag.AIs: генерация закончена')
    if event == '-AI_DIAG_CLEAR-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapAI_Ref.xml")     and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml")        and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml")       and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(f'Diag.AIs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(f'Diag.AIs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n', append=True)
            continue
        if values['SE_OPCDA'] is False and values['SE_OPCUA'] is False and values['SE_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки', append=True)
            continue
        logger.info(f'Diag.AIs: очистка объектов, карты адресов и атрубутов')
        function_state = New_copy.diag_clear('AIs', True, values['SE_OPCDA'], values['SE_OPCUA'], values['SE_MODBUS'],
                                             f"{values['-file1_2-']}/AttributesMapAI_Ref.xml",
                                             f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                             f"{values['-file1_2-']}/AttributesMapKont.xml",
                                             f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                             f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
    # AO
    if event == '-AO_DIAG-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapAI_Ref.xml")     and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml")        and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml")       and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(f'Diag.AOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(f'Diag.AOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.AOs: генерация началась')
        function_state = New_copy.diag_analogs_out(f"{values['-file1_2-']}/AttributesMapAI_Ref.xml", f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                                  f"{values['-file1_2-']}/AttributesMapKont.xml", f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                                  f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.AOs: генерация закончена\n', append=True)
        logger.info(f'Diag.AOs: генерация закончена')
    if event == '-AO_DIAG_CLEAR-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapAI_Ref.xml")     and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml")        and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml")       and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(f'Diag.AOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(f'Diag.AOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n', append=True)
            continue
        if values['SE_OPCDA'] is False and values['SE_OPCUA'] is False and values['SE_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки', append=True)
            continue

        logger.info(f'Diag.AOs: очистка объектов, карты адресов и атрубутов')
        function_state = New_copy.diag_clear('AOs', True, values['SE_OPCDA'], values['SE_OPCUA'], values['SE_MODBUS'],
                                             f"{values['-file1_2-']}/AttributesMapAI_Ref.xml",
                                             f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                             f"{values['-file1_2-']}/AttributesMapKont.xml",
                                             f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                             f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
    # DI
    if event == '-DI_DIAG-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml")        and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml")       and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(f'Diag.DIs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(f'Diag.DIs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.DIs: генерация началась')
        function_state = New_copy.diag_diskrets_in(f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                                   f"{values['-file1_2-']}/AttributesMapKont.xml",
                                                   f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                                   f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.DIs: генерация закончена\n', append=True)
        logger.info(f'Diag.DIs: генерация закончена')
    if event == '-DI_DIAG_CLEAR-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml")        and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml")       and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(f'Diag.AOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(f'Diag.AOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n', append=True)
            continue
        if values['SE_OPCDA'] is False and values['SE_OPCUA'] is False and values['SE_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки', append=True)
            continue

        logger.info(f'Diag.DIs: очистка объектов, карты адресов и атрубутов')
        function_state = New_copy.diag_clear('DIs', True, values['SE_OPCDA'], values['SE_OPCUA'], values['SE_MODBUS'],
                                             f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                             f"{values['-file1_2-']}/AttributesMapKont.xml",
                                             f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                             f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
    # DO
    if event == '-DO_DIAG-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml") and \
                not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml") and \
                not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
                not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(
                f'Diag.DOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(
                f'Diag.DOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n',
                append=True)
            continue

        logger.info(f'Diag.DOs: генерация началась')
        function_state = New_copy.diag_diskrets_out(f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                                    f"{values['-file1_2-']}/AttributesMapKont.xml",
                                                    f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                                    f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.DOs: генерация закончена\n', append=True)
        logger.info(f'Diag.DOs: генерация закончена')
    if event == '-DO_DIAG_CLEAR-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml")        and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml")       and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(f'Diag.DOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(f'Diag.DOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n', append=True)
            continue
        if values['SE_OPCDA'] is False and values['SE_OPCUA'] is False and values['SE_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки', append=True)
            continue

        logger.info(f'Diag.DOs: очистка объектов, карты адресов и атрубутов')
        function_state = New_copy.diag_clear('DOs', True, values['SE_OPCDA'], values['SE_OPCUA'], values['SE_MODBUS'],
                                             f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                             f"{values['-file1_2-']}/AttributesMapKont.xml",
                                             f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                             f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
    # CPUKC
    if event == '-CPUKC_DIAG-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.CPUKCs: генерация началась')
        function_state = New_copy.diag_cpukcs()
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.CPUKCs: генерация закончена\n', append=True)
        logger.info(f'Diag.CPUKCs: генерация закончена')
    if event == '-CPUKC_DIAG_CLEAR-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if values['SE_OPCDA'] is False and values['SE_OPCUA'] is False and values['SE_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.CPUKCs: очистка объектов, карты адресов')
        function_state = New_copy.diag_clear('CPUKCs', False, values['SE_OPCDA'], values['SE_OPCUA'], values['SE_MODBUS'],)
        window['logger'].update(f'{function_state}\n', append=True)
    # CPU
    if event == '-CPU_DIAG-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.CPUs: генерация началась')
        function_state = New_copy.diag_cpus()
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.CPUs: генерация закончена\n', append=True)
        logger.info(f'Diag.CPUs: генерация закончена')
    if event == '-CPU_DIAG_CLEAR-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if values['SE_OPCDA'] is False and values['SE_OPCUA'] is False and values['SE_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.CPUs: очистка объектов, карты адресов')
        function_state = New_copy.diag_clear('CPUs', False, values['SE_OPCDA'], values['SE_OPCUA'], values['SE_MODBUS'],)
        window['logger'].update(f'{function_state}\n', append=True)
    # NOC_NOE
    if event == '-NOC_NOE_DIAG-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.NOC_NOEs: генерация началась')
        function_state = New_copy.diag_noc_noe()
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.NOC_NOEs: генерация закончена\n', append=True)
        logger.info(f'Diag.NOC_NOEs: генерация закончена')
    if event == '-NOC_DIAG_CLEAR-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if values['SE_OPCDA'] is False and values['SE_OPCUA'] is False and values['SE_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.NOC_NOEs: очистка объектов, карты адресов')
        function_state = New_copy.diag_clear('NOC_NOEs', False, values['SE_OPCDA'], values['SE_OPCUA'], values['SE_MODBUS'],)
        window['logger'].update(f'{function_state}\n', append=True)
    # CRA
    if event == '-CRA_DIAG-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.CRAs: генерация началась')
        function_state = New_copy.diag_cras()
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.CRAs: генерация закончена\n', append=True)
        logger.info(f'Diag.CRAs: генерация закончена')
    if event == '-CRA_DIAG_CLEAR-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if values['SE_OPCDA'] is False and values['SE_OPCUA'] is False and values['SE_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.CRAs: очистка объектов, карты адресов')
        function_state = New_copy.diag_clear('CRAs', False, values['SE_OPCDA'], values['SE_OPCUA'], values['SE_MODBUS'],)
        window['logger'].update(f'{function_state}\n', append=True)
    # NOR
    if event == '-NOR_DIAG-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.NORs: генерация началась')
        function_state = New_copy.diag_nors()
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.NORs: генерация закончена\n', append=True)
        logger.info(f'Diag.NORs: генерация закончена')
    if event == '-NOR_DIAG_CLEAR-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if values['SE_OPCDA'] is False and values['SE_OPCUA'] is False and values['SE_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.NORs: очистка объектов, карты адресов')
        function_state = New_copy.diag_clear('NORs', False, values['SE_OPCDA'], values['SE_OPCUA'], values['SE_MODBUS'],)
        window['logger'].update(f'{function_state}\n', append=True)
    # NOM
    if event == '-NOM_DIAG-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.NOMs: генерация началась')
        function_state = New_copy.diag_noms()
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.NOMs: генерация закончена\n', append=True)
        logger.info(f'Diag.NOMs: генерация закончена')
    if event == '-NOM_DIAG_CLEAR-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if values['SE_OPCDA'] is False and values['SE_OPCUA'] is False and values['SE_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.NOMs: очистка объектов, карты адресов')
        function_state = New_copy.diag_clear('NOMs', False, values['SE_OPCDA'], values['SE_OPCUA'], values['SE_MODBUS'],)
        window['logger'].update(f'{function_state}\n', append=True)
    # CPS
    if event == '-CPS_DIAG-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.CPSs: генерация началась')
        function_state = New_copy.diag_cps()
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.CPSs: генерация закончена\n', append=True)
        logger.info(f'Diag.CPSs: генерация закончена')
    if event == '-CPS_DIAG_CLEAR-' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if values['SE_OPCDA'] is False and values['SE_OPCUA'] is False and values['SE_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.CPSs: очистка объектов, карты адресов')
        function_state = New_copy.diag_clear('CPSs', False, values['SE_OPCDA'], values['SE_OPCUA'], values['SE_MODBUS'],)
        window['logger'].update(f'{function_state}\n', append=True)

    # MK
    # Rackstate
    if event == 'RackS' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.RackStates: генерация началась')
        function_state = New_copy.diag_rackstates()
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.RackStates: генерация закончена\n', append=True)
        logger.info(f'Diag.RackStates: генерация закончена')
    if event == 'RackS_CLEAR' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if values['MK_OPCDA'] is False and values['MK_OPCUA'] is False and values['MK_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.RackStates: очистка объектов, карты адресов и атрубутов')
        function_state = New_copy.diag_clear('RackStates', False, values['MK_OPCDA'], values['MK_OPCUA'], values['MK_MODBUS'],)
        window['logger'].update(f'{function_state}\n', append=True)
    #AI8
    if event == 'MK_AI8' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapAI_Ref.xml")     and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml")        and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml")       and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(f'Diag.AIs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(f'Diag.AIs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.AIs: генерация началась')
        function_state = New_copy.diag_mk_analogs_in(f"{values['-file1_2-']}/AttributesMapAI_Ref.xml", f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                                     f"{values['-file1_2-']}/AttributesMapKont.xml", f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                                     f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.AIs: генерация закончена\n', append=True)
        logger.info(f'Diag.AIs: генерация закончена')
    if event == 'MK_AI8_CLEAR' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapAI_Ref.xml")     and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml")        and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml")       and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(f'Diag.AIs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(f'Diag.AIs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n', append=True)
            continue
        if values['MK_OPCDA'] is False and values['MK_OPCUA'] is False and values['MK_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.AIs: очистка объектов, карты адресов и атрубутов')
        function_state = New_copy.diag_clear('AIs', True, values['MK_OPCDA'], values['MK_OPCUA'], values['MK_MODBUS'],
                                             f"{values['-file1_2-']}/AttributesMapAI_Ref.xml",
                                             f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                             f"{values['-file1_2-']}/AttributesMapKont.xml",
                                             f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                             f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
    # AO
    if event == 'MK_AO' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapAI_Ref.xml")     and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml")        and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml")       and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(f'Diag.AOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(f'Diag.AOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.AOs: генерация началась')
        function_state = New_copy.diag_mk_analogs_out(f"{values['-file1_2-']}/AttributesMapAI_Ref.xml", f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                                      f"{values['-file1_2-']}/AttributesMapKont.xml", f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                                      f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.AOs: генерация закончена\n', append=True)
        logger.info(f'Diag.AOs: генерация закончена')
    if event == 'MK_AO_CLEAR' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapAI_Ref.xml")     and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml")        and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml")       and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(f'Diag.AOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(f'Diag.AOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n', append=True)
            continue
        if values['MK_OPCDA'] is False and values['MK_OPCUA'] is False and values['MK_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.AOs: очистка объектов, карты адресов и атрубутов')
        function_state = New_copy.diag_clear('AOs', True, values['MK_OPCDA'], values['MK_OPCUA'], values['MK_MODBUS'],
                                             f"{values['-file1_2-']}/AttributesMapAI_Ref.xml",
                                             f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                             f"{values['-file1_2-']}/AttributesMapKont.xml",
                                             f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                             f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
    # DI
    if event == 'MK_DI' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml")        and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml")       and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(f'Diag.DIs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(f'Diag.DIs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.DIs: генерация началась')
        function_state = New_copy.diag_mk_diskrets_in(f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                                      f"{values['-file1_2-']}/AttributesMapKont.xml",
                                                      f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                                      f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.DIs: генерация закончена\n', append=True)
        logger.info(f'Diag.DIs: генерация закончена')
    if event == 'MK_DI_CLEAR' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml")        and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml")       and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(f'Diag.AOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(f'Diag.AOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n', append=True)
            continue
        if values['MK_OPCDA'] is False and values['MK_OPCUA'] is False and values['MK_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.DIs: очистка объектов, карты адресов и атрубутов')
        function_state = New_copy.diag_clear('DIs', True, values['MK_OPCDA'], values['MK_OPCUA'], values['MK_MODBUS'],
                                             f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                             f"{values['-file1_2-']}/AttributesMapKont.xml",
                                             f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                             f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
    # DO
    if event == 'MK_DO' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml") and \
                not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml") and \
                not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
                not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(
                f'Diag.DOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(
                f'Diag.DOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n',
                append=True)
            continue

        logger.info(f'Diag.DOs: генерация началась')
        function_state = New_copy.diag_mk_diskrets_out(f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                                    f"{values['-file1_2-']}/AttributesMapKont.xml",
                                                    f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                                    f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.DOs: генерация закончена\n', append=True)
        logger.info(f'Diag.DOs: генерация закончена')
    if event == 'MK_DO_CLEAR' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKlk.xml")        and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapKont.xml")       and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapSignalName.xml") and \
           not os.path.isfile(f"{values['-file1_2-']}/AttributesMapTagName.xml"):
            logger.info(f'Diag.DOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!')
            window['logger'].update(f'Diag.DOs: путь до папки с файлами не найден.\nГенерация завершена! Один или несколько путей отсутствуют. Проверь пути!\n', append=True)
            continue
        if values['MK_OPCDA'] is False and values['MK_OPCUA'] is False and values['MK_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.DOs: очистка объектов, карты адресов и атрубутов')
        function_state = New_copy.diag_clear('DOs', True, values['MK_OPCDA'], values['MK_OPCUA'], values['MK_MODBUS'],
                                             f"{values['-file1_2-']}/AttributesMapKlk.xml",
                                             f"{values['-file1_2-']}/AttributesMapKont.xml",
                                             f"{values['-file1_2-']}/AttributesMapSignalName.xml",
                                             f"{values['-file1_2-']}/AttributesMapTagName.xml")
        window['logger'].update(f'{function_state}\n', append=True)
    #MN
    if event == 'MK_MN' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.MNs: генерация началась')
        function_state = New_copy.diag_mk_mns()
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.MNs: генерация закончена\n', append=True)
        logger.info(f'Diag.MNs: генерация закончена')
    if event == 'MK_MN_CLEAR' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if values['MK_OPCDA'] is False and values['MK_OPCUA'] is False and values['MK_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.MNs: очистка объектов, карты адресов и атрубутов')
        function_state = New_copy.diag_clear('MNs', False, values['MK_OPCDA'], values['MK_OPCUA'], values['MK_MODBUS'],)
        window['logger'].update(f'{function_state}\n', append=True)
    # CN
    if event == 'MK_CN' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.CNs: генерация началась')
        function_state = New_copy.diag_mk_cns()
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.CNs: генерация закончена\n', append=True)
        logger.info(f'Diag.CNs: генерация закончена')
    if event == 'MK_CN_CLEAR' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if values['MK_OPCDA'] is False and values['MK_OPCUA'] is False and values['MK_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.CNs: очистка объектов, карты адресов и атрубутов')
        function_state = New_copy.diag_clear('CNs', False, values['MK_OPCDA'], values['MK_OPCUA'], values['MK_MODBUS'],)
        window['logger'].update(f'{function_state}\n', append=True)
    # CPU
    if event == 'MK_CPU' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.CPUs: генерация началась')
        function_state = New_copy.diag_mk_cpus()
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.CPUs: генерация закончена\n', append=True)
        logger.info(f'Diag.CPUs: генерация закончена')
    if event == 'MK_CPU_CLEAR' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if values['MK_OPCDA'] is False and values['MK_OPCUA'] is False and values['MK_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.CPUs: очистка объектов, карты адресов и атрубутов')
        function_state = New_copy.diag_clear('CPUs', False, values['MK_OPCDA'], values['MK_OPCUA'], values['MK_MODBUS'],)
        window['logger'].update(f'{function_state}\n', append=True)
    # PSU
    if event == 'MK_PSU' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.PSUs: генерация началась')
        function_state = New_copy.diag_mk_psus()
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.PSUs: генерация закончена\n', append=True)
        logger.info(f'Diag.PSUs: генерация закончена')
    if event == 'MK_PSU_CLEAR' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if values['MK_OPCDA'] is False and values['MK_OPCUA'] is False and values['MK_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.PSUs: очистка объектов, карты адресов и атрубутов')
        function_state = New_copy.diag_clear('PSUs', False, values['MK_OPCDA'], values['MK_OPCUA'], values['MK_MODBUS'],)
        window['logger'].update(f'{function_state}\n', append=True)
    # RS
    if event == 'MK_RS' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(
                f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue

        logger.info(f'Diag.RSs: генерация началась')
        function_state = New_copy.diag_mk_rs()
        window['logger'].update(f'{function_state}\n', append=True)
        window['logger'].update(f'Diag.RSs: генерация закончена\n', append=True)
        logger.info(f'Diag.RSs: генерация закончена')
    if event == 'MK_RS_CLEAR' and flag_not_click:
        if values['-file1_2-'] == '':
            logger.info(f'Не найден путь к папке с файлами DevStudio')
            window['logger'].update(
                f'Не найден путь к папке с файлами DevStudio.Генерация завершена! Проверь пути!\n', append=True)
            continue
        if values['MK_OPCDA'] is False and values['MK_OPCUA'] is False and values['MK_MODBUS'] is False:
            logger.info(f'Не выбрана карта для очистки')
            window['logger'].update(f'Не выбрана карта для очистки\n', append=True)
            continue

        logger.info(f'Diag.RSs: очистка объектов, карты адресов и атрубутов')
        function_state = New_copy.diag_clear('RSs', False, values['MK_OPCDA'], values['MK_OPCUA'],
                                             values['MK_MODBUS'], )
        window['logger'].update(f'{function_state}\n', append=True)
    # СУ
    if event == 'CFG_KTPRS' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_KTPRS начата')
        window['logger'].update(f'Генерация cfg_KTPRS начата\n', append=True)
        New_copy.gen_cfg_ktprs(values['SU_PATH'])
        logger.info(f'Генерация cfg_KTPRS завершена')
        window['logger'].update(f'Генерация cfg_KTPRS завершена\n', append=True)
    if event == 'CFG_KTPRA' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_KTPRA начата')
        window['logger'].update(f'Генерация cfg_KTPRA начата\n', append=True)
        New_copy.gen_cfg_ktpra(values['SU_PATH'])
        logger.info(f'Генерация cfg_KTPRA завершена')
        window['logger'].update(f'Генерация cfg_KTPRA завершена\n', append=True)
    if event == 'CFG_KTPR' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_KTPR начата')
        window['logger'].update(f'Генерация cfg_KTPR начата\n', append=True)
        New_copy.gen_cfg_ktpr(values['SU_PATH'])
        logger.info(f'Генерация cfg_KTPR завершена')
        window['logger'].update(f'Генерация cfg_KTPR завершена\n', append=True)
    if event == 'CFG_NA' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_NA начата')
        window['logger'].update(f'Генерация cfg_NA начата\n', append=True)
        New_copy.gen_cfg_na(values['SU_PATH'])
        logger.info(f'Генерация cfg_NA завершена')
        window['logger'].update(f'Генерация cfg_NA завершена\n', append=True)
    if event == 'CFG_AI' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_AI начата')
        window['logger'].update(f'Генерация cfg_AI начата\n', append=True)
        New_copy.gen_cfg_AI(values['SU_PATH'])
        logger.info(f'Генерация cfg_AI завершена')
        window['logger'].update(f'Генерация cfg_AI завершена\n', append=True)
    if event == 'CFG_AO' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_AO начата')
        window['logger'].update(f'Генерация cfg_AO начата\n', append=True)
        New_copy.gen_cfg_AO(values['SU_PATH'])
        logger.info(f'Генерация cfg_AO завершена')
        window['logger'].update(f'Генерация cfg_AO завершена\n', append=True)
    if event == 'CFG_DI' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_DI начата')
        window['logger'].update(f'Генерация cfg_DI начата\n', append=True)
        New_copy.gen_cfg_DI(values['SU_PATH'])
        logger.info(f'Генерация cfg_DI завершена')
        window['logger'].update(f'Генерация cfg_DI завершена\n', append=True)
    if event == 'CFG_DO' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_DO начата')
        window['logger'].update(f'Генерация cfg_DO начата\n', append=True)
        New_copy.gen_cfg_DO(values['SU_PATH'])
        logger.info(f'Генерация cfg_DO завершена')
        window['logger'].update(f'Генерация cfg_DO завершена\n', append=True)
    if event == 'CFG_DI_sim' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_DI_sim начата')
        window['logger'].update(f'Генерация cfg_DI_sim начата\n', append=True)
        New_copy.gen_cfg_DI_sim(values['SU_PATH'])
        logger.info(f'Генерация cfg_DI_sim завершена')
        window['logger'].update(f'Генерация cfg_DI_sim завершена\n', append=True)
    if event == 'CFG_DO_sim' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_DO_sim начата')
        window['logger'].update(f'Генерация cfg_DO_sim начата\n', append=True)
        New_copy.gen_cfg_DO_sim(values['SU_PATH'])
        logger.info(f'Генерация cfg_DO_sim завершена')
        window['logger'].update(f'Генерация cfg_DO_sim завершена\n', append=True)
    if event == 'CFG_ZD' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_ZD начата')
        window['logger'].update(f'Генерация cfg_ZD начата\n', append=True)
        New_copy.gen_cfg_ZD(values['SU_PATH'])
        logger.info(f'Генерация cfg_ZD завершена')
        window['logger'].update(f'Генерация cfg_ZD завершена\n', append=True)
    if event == 'CFG_VS' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_VS начата')
        window['logger'].update(f'Генерация cfg_VS начата\n', append=True)
        New_copy.gen_cfg_VS(values['SU_PATH'])
        logger.info(f'Генерация cfg_VS завершена')
        window['logger'].update(f'Генерация cfg_VS завершена\n', append=True)
    if event == 'CFG_VSGRP' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_VSGRP начата')
        window['logger'].update(f'Генерация cfg_VSGRP начата\n', append=True)
        New_copy.gen_cfg_VSGRP(values['SU_PATH'])
        logger.info(f'Генерация cfg_VSGRP завершена')
        window['logger'].update(f'Генерация cfg_VSGRP завершена\n', append=True)
    if event == 'CFG_NPS' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_NPS начата')
        window['logger'].update(f'Генерация cfg_NPS начата\n', append=True)
        New_copy.gen_cfg_nps(values['SU_PATH'])
        logger.info(f'Генерация cfg_NPS завершена')
        window['logger'].update(f'Генерация cfg_NPS завершена\n', append=True)
    if event == 'CFG_PIC' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue
        if values['ChB_MNS'] is False and values['ChB_PT'] is False and \
                values['ChB_RP'] is False and values['ChB_SAR'] is False:
            logger.error(f'Не выбрано что генерить')
            window['logger'].update(f'Не выбрано что генерить\n', append=True)
            continue

        logger.info(f'Генерация cfg_PIC начата')
        window['logger'].update(f'Генерация cfg_PIC начата\n', append=True)
        if values['ChB_MNS'] is True: New_copy.gen_cfg_pic(values['SU_PATH'], 'MNS')
        if values['ChB_PT']  is True: New_copy.gen_cfg_pic(values['SU_PATH'], 'ASPT')
        if values['ChB_RP']  is True: New_copy.gen_cfg_pic(values['SU_PATH'], 'RP')
        if values['ChB_SAR'] is True: New_copy.gen_cfg_pic(values['SU_PATH'], 'SAR')
        logger.info(f'Генерация cfg_PIC завершена')
        window['logger'].update(f'Генерация cfg_PIC завершена\n', append=True)
    if event == 'CFG_UTS' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_UTS начата')
        window['logger'].update(f'Генерация cfg_UTS начата\n', append=True)
        New_copy.gen_cfg_uts(values['SU_PATH'])
        logger.info(f'Генерация cfg_UTS завершена')
        window['logger'].update(f'Генерация cfg_UTS завершена\n', append=True)
    if event == 'CFG_VV' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_VV начата')
        window['logger'].update(f'Генерация cfg_VV начата\n', append=True)
        New_copy.gen_cfg_VV(values['SU_PATH'])
        logger.info(f'Генерация cfg_VV завершена')
        window['logger'].update(f'Генерация cfg_VV завершена\n', append=True)
    if event == 'CFG_DPS' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_DPS начата')
        window['logger'].update(f'Генерация cfg_DPS начата\n', append=True)
        New_copy.gen_cfg_DPS(values['SU_PATH'])
        logger.info(f'Генерация cfg_DPS завершена')
        window['logger'].update(f'Генерация cfg_DPS завершена\n', append=True)
    if event == 'CFG_RSREQ' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_RSREQ начата')
        window['logger'].update(f'Генерация cfg_RSREQ начата\n', append=True)
        New_copy.gen_cfg_rsreq(values['SU_PATH'])
        logger.info(f'Генерация cfg_RSREQ завершена')
        window['logger'].update(f'Генерация cfg_RSREQ завершена\n', append=True)
    if event == 'CFG_AI_SIM' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация cfg_AI_sim начата')
        window['logger'].update(f'Генерация cfg_AI_sim начата\n', append=True)
        New_copy.gen_cfg_AI_sim(values['SU_PATH'])
        logger.info(f'Генерация cfg_AI_sim завершена')
        window['logger'].update(f'Генерация cfg_AI_sim завершена\n', append=True)
    if event == 'CFG_DIAG' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация gv_DIAG начата')
        window['logger'].update(f'Генерация gv_DIAG начата\n', append=True)
        New_copy.gen_gv_diag(values['SU_PATH'])
        logger.info(f'Генерация gv_DIAG завершена')
        window['logger'].update(f'Генерация gv_DIAG завершена\n', append=True)
    # TM
    if event == 'CFG_TM_TS' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация Cfg_TM_TS начата')
        window['logger'].update(f'Генерация Cfg_TM_TS начата\n', append=True)
        New_copy.gen_cfg_TS(values['SU_PATH'])
        logger.info(f'Генерация Cfg_TM_TS завершена')
        window['logger'].update(f'Генерация Cfg_TM_TS завершена\n', append=True)
    if event == 'CFG_TM_TU' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация Cfg_TM_TU начата')
        window['logger'].update(f'Генерация Cfg_TM_TU начата\n', append=True)
        New_copy.gen_cfg_TU(values['SU_PATH'])
        logger.info(f'Генерация Cfg_TM_TU завершена')
        window['logger'].update(f'Генерация Cfg_TM_TU завершена\n', append=True)
    if event == 'CFG_TM_TII' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация Cfg_TM_TII начата')
        window['logger'].update(f'Генерация Cfg_TM_TII начата\n', append=True)
        New_copy.gen_cfg_TII(values['SU_PATH'])
        logger.info(f'Генерация Cfg_TM_TII завершена')
        window['logger'].update(f'Генерация Cfg_TM_TII завершена\n', append=True)
    if event == 'CFG_TM_TI2' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация Cfg_TM_TI2 начата')
        window['logger'].update(f'Генерация Cfg_TM_TI2 начата\n', append=True)
        New_copy.gen_cfg_TI2(values['SU_PATH'])
        logger.info(f'Генерация Cfg_TM_TI2 завершена')
        window['logger'].update(f'Генерация Cfg_TM_TI2 завершена\n', append=True)
    if event == 'CFG_TM_TI4' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация Cfg_TM_TI4 начата')
        window['logger'].update(f'Генерация Cfg_TM_TI4 начата\n', append=True)
        New_copy.gen_cfg_TI4(values['SU_PATH'])
        logger.info(f'Генерация Cfg_TM_TI4 завершена')
        window['logger'].update(f'Генерация Cfg_TM_TI4 завершена\n', append=True)
    if event == 'CFG_TM_TR2' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация Cfg_TM_TR2 начата')
        window['logger'].update(f'Генерация Cfg_TM_TR2 начата\n', append=True)
        New_copy.gen_cfg_TR2(values['SU_PATH'])
        logger.info(f'Генерация Cfg_TM_TR2 завершена')
        window['logger'].update(f'Генерация Cfg_TM_TR2 завершена\n', append=True)
    if event == 'CFG_TM_TR4' and flag_not_click:
        if values['SU_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация Cfg_TM_TR4 начата')
        window['logger'].update(f'Генерация Cfg_TM_TR4 начата\n', append=True)
        New_copy.gen_cfg_TR4(values['SU_PATH'])
        logger.info(f'Генерация Cfg_TM_TR4 завершена')
        window['logger'].update(f'Генерация Cfg_TM_TR4 завершена\n', append=True)
    # Imitator
    if event == 'Click_imit_xml' and flag_not_click:
        if values['IMIT_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue
        if values['Start_AI'] == '' or values['Start_DI'] == '' or values['Start_DO'] == '':
            logger.error(f'Отсутствует один или несколько стартовых ModBus адресов')
            window['logger'].update(f'Отсутствует один или несколько стартовых ModBus адресов\n', append=True)
            continue

        logger.info(f'Генерация файла имитатора xml начата')
        window['logger'].update(f'Генерация файла имитатора xml начата\n', append=True)
        New_copy.file_xml_imitator(values['IMIT_PATH'], values['Start_AI'], values['Start_DI'], values['Start_DO'])
        logger.info(f'Генерация файла имитатора xml завершена')
        window['logger'].update(f'Генерация файла имитатора xml завершена\n', append=True)
    # CFG_DI_IMIT
    if event == 'CFG_DI_IMIT' and flag_not_click:
        if values['IMIT_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация файла СУ: gen_cfg_DI_imit начата')
        window['logger'].update(f'Генерация файла СУ: gen_cfg_DI_imit начата\n', append=True)
        New_copy.gen_cfg_DI_imit(values['IMIT_PATH'])
        logger.info(f'Генерация файла СУ: gen_cfg_DI_imit завершена')
        window['logger'].update(f'Генерация файла СУ: gen_cfg_DI_imit завершена\n', append=True)
    # CFG_AI_IMIT
    if event == 'CFG_AI_IMIT' and flag_not_click:
        if values['IMIT_PATH'] == '':
            logger.error(f'Отсутствует папка для размещения файлов')
            window['logger'].update(f'Отсутствует папка для размещения файлов\n', append=True)
            continue

        logger.info(f'Генерация файла СУ: gen_cfg_AI_imit начата')
        window['logger'].update(f'Генерация файла СУ: gen_cfg_AI_imit начата\n', append=True)
        New_copy.gen_cfg_AI_imit(values['IMIT_PATH'])
        logger.info(f'Генерация файла СУ: gen_cfg_AI_imit завершена')
        window['logger'].update(f'Генерация файла СУ: gen_cfg_AI_imit завершена\n', append=True)
window.close()