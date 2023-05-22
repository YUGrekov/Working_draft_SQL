from function_code import *
from gen_defence_hmi import *
from gen_uts_upts_hmi import *
from gen_uso import *
from lxml import etree
import codecs

# Пути до файлов неисповедимы
#path_to_exel        = 'D:\Проекты\ЛПДС_Каракатеевы\KarkateevoIO_PT.xlsx'
#path_to_exel        = 'D:\Проекты\НПС-Аксинино_2\HMI\_Docs\НПС Аксинино-2 IO МК-500 v1.78.xlsx'
#path_to_exel        = 'D:\Проекты\НПС-Аксинино_2\HMI\_Docs\KarkateevoIO.xlsx'
#path_to_exel        = 'D:\Проекты\LPDS_Salim\HMI\_Docs\ИО_ПТ_Салым_v2.56.xlsx'
#path_to_exel        = 'D:\Проекты\НПС-Аксинино_2\HMI\_Docs\АСУ ПТ Аксинино-2 IO_v3.72.xlsx'
path_to_exel        = 'D:\Проекты\LPDS_Salim\HMI\_Docs\НПС Салым-4 IO v0.38.xlsx'
#path_to_exel        = 'D:\Проекты\LPDS_Salim\HMI_KARKAR\_Docs\KarkateevoIO.xlsx'

# path_to_adressmap       = 'D:\Проекты\НПС-Аксинино_2\HMI\project\\typical_prj\ODA.xml'
# path_to_adressmap_mb    = 'D:\Проекты\НПС-Аксинино_2\HMI\project\\typical_prj\ModBus.xml'
# path_to_adressmap_mb503 = 'D:\Проекты\НПС-Аксинино_2\HMI\project\\typical_prj\ModBus503.xml'
# path_to_filenameomx     = 'D:\Проекты\НПС-Аксинино_2\HMI\project\\typical_prj\\typical_prj.omx'

path_to_adressmap       = 'D:\Проекты\LPDS_Salim\HMI\project\\typical_prj\ODA.xml'
path_to_adressmap_mb    = 'D:\Проекты\LPDS_Salim\HMI\project\\typical_prj\ModBus.xml'
path_to_adressmap_mb503 = 'D:\Проекты\LPDS_Salim\HMI\project\\typical_prj\MModBus503.xml'
path_to_filenameomx     = 'D:\Проекты\LPDS_Salim\HMI\project\\typical_prj\\typical_prj.omx'

# Карты для заполнения атрибутов
diag_file_MapAI_Ref         = 'D:\Проекты\LPDS_Salim\HMI\project\\typical_prj\\AttributesMapAI_Ref.xml'
diag_file_MapDescription    = 'D:\Проекты\LPDS_Salim\HMI\project\\typical_prj\\AttributesMapDescription.xml'
diag_file_MapKlk            = 'D:\Проекты\LPDS_Salim\HMI\project\\typical_prj\\AttributesMapKlk.xml'
diag_file_MapKont           = 'D:\Проекты\LPDS_Salim\HMI\project\\typical_prj\\AttributesMapKont.xml'
diag_file_MapSignalName     = 'D:\Проекты\LPDS_Salim\HMI\project\\typical_prj\\AttributesMapSignalName.xml'
diag_file_MapTagName        = 'D:\Проекты\LPDS_Salim\HMI\project\\typical_prj\\AttributesMapTagName.xml'
diag_file_MapColorScheme    = 'D:\Проекты\LPDS_Salim\HMI\project\\typical_prj\\AttributesMapColorScheme.xml'
diag_file_MapAnalogsFormats = 'D:\Проекты\LPDS_Salim\HMI\project\\typical_prj\\AttributesAnalogsFormats.xml'
diag_file_MapEgu            = 'D:\Проекты\LPDS_Salim\HMI\project\\typical_prj\\AttributesMapEGU.xml'
file_AnalogTrends           = 'D:\Проекты\LPDS_Salim\HMI\project\\typical_prj\\AttributesAnalogTrends.xml'

# Тренды
path_item     = 'D:\Проекты\LPDS_Salim\HMI\_Docs\Trends\items.xlsx'
#path_file_txt = 'D:\Проекты\НПС-Аксинино_2\HMI\_Docs\Trends\\'
path_file_txt = 'D:\Проекты\LPDS_Salim\HMI\_Docs\Trends\\'

# Поиск сигналов
path_file_signals = 'D:\Проекты\LPDS_Salim\HMI\_Docs\Trends\SQLSearch.xml'

# Диавгностика
path_gen_hmi_USO = 'D:\Проекты\LPDS_Salim\HMI\HMI_NPS\gen_pic\\'
prefix_sys_HMI   = 'MNS_'

# Карта защит
# Путь расположения файлов .omobj для генерации защит, здесь должен быть шаблон: Form_Defences_default.omobj
path_gen_station_defence   = 'D:\Проекты\LPDS_Salim\HMI\_Docs\Defence\\'
# GMPNA или KTPRA или KTPR иди KTPRP
list_defence = 'KTPR'


# DevStudio
prefix_system = ''
prefix_driver = 'OFS!'

New_copy = Equipment(path_to_exel, path_to_adressmap, path_to_adressmap_mb,
                    path_to_adressmap_mb503, path_to_filenameomx, prefix_system, prefix_driver)

# DevStudio_omx
#New_copy.clear_objects()
#New_copy.analogs_omx()
#New_copy.diskret_in_omx()
#New_copy.picture_omx()
#New_copy.auxsystem_omx()
#New_copy.valves_omx()
#New_copy.pumps_omx()
#New_copy.relayted_system_omx()
#New_copy.uts_omx()
#New_copy.ktpr_omx()
#New_copy.ktprp_omx()
#New_copy.ktpra_omx()
#New_copy.gmpna_omx()
#New_copy.upts_omx()
#New_copy.ktprp_omx()
#New_copy.pi_omx()
#New_copy.pz_omx()

# DevStudio_map
#New_copy.analogs_map()
#New_copy.analogs_map_modbus()
#New_copy.diskret_in_map()
#New_copy.diskret_in_map_modbus()
#New_copy.picture_map()
#New_copy.auxsystem_map()
#New_copy.auxsystem_map_modbus()
#New_copy.valves_map()
#New_copy.pumps_map()
#New_copy.pumps_map_modbus()
#New_copy.relayted_system_map()
#New_copy.relayted_system_map_modbus()
#New_copy.uts_map()
#New_copy.ktpr_map()
#New_copy.ktprp_map()
#New_copy.ktprp_map_modbus()
#New_copy.ktpra_map()
#New_copy.ktpra_map_modbus()
#New_copy.gmpna_map()
#New_copy.upts_map()
#New_copy.upts_map_modbus()
#New_copy.pi_map()
#New_copy.pi_map_modbus()
#New_copy.pz_map()
#New_copy.pz_map_modbus()


# Диагностика
#New_copy.analogformat_map(diag_file_MapAnalogsFormats)
#New_copy.map_egu(diag_file_MapEgu)
#New_copy.diag_analogs_in(diag_file_MapAI_Ref, diag_file_MapKlk, diag_file_MapKont, diag_file_MapSignalName, diag_file_MapTagName)
#New_copy.diag_clear('AIs', True, diag_file_MapAI_Ref, diag_file_MapKlk, diag_file_MapKont, diag_file_MapSignalName, diag_file_MapTagName)
#New_copy.diag_analogs_out(diag_file_MapAI_Ref, diag_file_MapKlk, diag_file_MapKont, diag_file_MapSignalName, diag_file_MapTagName)
New_copy.diag_diskrets_in(diag_file_MapKlk, diag_file_MapKont, diag_file_MapSignalName, diag_file_MapTagName)
New_copy.diag_diskrets_out(diag_file_MapKlk, diag_file_MapKont, diag_file_MapSignalName, diag_file_MapTagName)
#New_copy.diag_cpukcs()
#New_copy.diag_cpus()
#New_copy.diag_noc_noe()
#New_copy.diag_cras()
#New_copy.color_diskrets(diag_file_MapColorScheme)
#New_copy.pzs_ready_map('D:\project\\typical_prj\AttributesMapDescription.xml')
#MK
#New_copy.diag_mk_analogs_in(diag_file_MapAI_Ref, diag_file_MapKlk, diag_file_MapKont, diag_file_MapSignalName, diag_file_MapTagName)
#New_copy.diag_mk_analogs_out(diag_file_MapAI_Ref, diag_file_MapKlk, diag_file_MapKont, diag_file_MapSignalName, diag_file_MapTagName)
#New_copy.diag_mk_diskrets_in(diag_file_MapKlk, diag_file_MapKont, diag_file_MapSignalName, diag_file_MapTagName)
#New_copy.diag_mk_diskrets_out(diag_file_MapKlk, diag_file_MapKont, diag_file_MapSignalName, diag_file_MapTagName)
#New_copy.diag_mk_cpus()
#New_copy.diag_mk_cns()
#New_copy.diag_mk_mns()
#New_copy.diag_mk_psus()
#New_copy.diag_mk_rs()
# CLEAR
# New_copy.diag_clear('AIs', True, False, False, True,
#                     diag_file_MapAI_Ref,
#                     diag_file_MapKlk,
#                     diag_file_MapKont,
#                     diag_file_MapSignalName,
#                     diag_file_MapTagName)


#New_copy.clear_map('AttributesMapColorScheme.xml', '.Diskrets.', diag_file_MapColorScheme)
#New_copy.diag_rackstates()

# Imitator
#New_copy.file_xml_imitator(path_file_txt, 50200, 50000)

#New_copy.gen_cfg_pic('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\SU\\', 'MNS')
#New_copy.gen_cfg_ktprs('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\SU\\')
#New_copy.gen_cfg_ktpr('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\SU\\')
#New_copy.gen_cfg_ZD('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\SU\\')
#New_copy.gen_gv_diag('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\SU\\')
#New_copy.gen_cfg_na('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\SU\\')
#New_copy.gen_cfg_TS('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\SU\\')
#New_copy.gen_cfg_TU('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\SU\\')
#New_copy.gen_cfg_TI2('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\SU\\')
#New_copy.gen_cfg_TI4('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\SU\\')
#New_copy.gen_cfg_TII('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\SU\\')
#New_copy.gen_cfg_TR2('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\SU\\')
#New_copy.gen_cfg_TR4('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\SU\\')
#New_copy.gen_cfg_DI_imit('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\SU\\')
#New_copy.gen_cfg_AI_imit('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\SU\\')

# Тренды
#New_copy.trends1_xml()
#New_copy.trends_xml(path_item, path_file_txt, 'АСУТП НПС-4 ЛПДС Салым')
#New_copy.trends_snmp_xml()
#New_copy.analogs_trend(file_AnalogTrends)
#New_copy.trends_linux_xml(path_file_txt, 'АСУПТ НПС-2 Аксинино')

# SQL скрипт для поиска сигналов
# Название таблицы: SearchSignal -> signals -> allSignals
#New_copy.sql_script_search('D:\Проекты\LPDS_Salim\HMI\_Docs\Trends\\')

# Сообщения MSG
#New_copy.msg_racks('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\MSG\\', 'D:\Проекты\НПС-Аксинино_2\HMI\_Docs\MSG\\')
#New_copy.msg_modules('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\MSG\\', 'D:\Проекты\НПС-Аксинино_2\HMI\_Docs\MSG\\')
#New_copy.msg_modules_rs('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\MSG\\', 'D:\Проекты\НПС-Аксинино_2\HMI\_Docs\MSG\\')
#New_copy.msg_do('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\MSG\\', 'D:\Проекты\НПС-Аксинино_2\HMI\_Docs\MSG\\')

# HMI
# Экранные формы диагностики
#gen_HMI_USO(path_gen_hmi_USO, path_to_exel, prefix_sys_HMI)
#generate_serv_signal('D:\Проекты\НПС-Аксинино_2\HMI\_Docs\Defence\\', path_to_exel, False, 'MNS_')

# Карты защит и готовностей
#gen_station_defence(path_gen_station_defence, path_to_exel, list_defence)

# Табло и сирены
#gen_uts_upts('D:\Проекты\LPDS_Salim\HMI\_Docs\Defence\\', path_to_exel, 'UTS', 'false')

# Поиск сигналов
#gen_signals_viewer(path_to_exel, 'D:\Проекты\LPDS_Salim\HMI\_Docs\\')

# Сводки
#path_to_lrxml        = 'D:\Проекты\LPDS_Salim\HMI\_Docs\Reports\\report_mns_salym.lrxml'
#path_to_exel_reports = 'D:\Проекты\LPDS_Salim\HMI\_Docs\Reports\\reports_mns.xlsx'
#gen_report_table(path_to_lrxml,path_to_exel_reports,path_to_exel,['AI','VS','ZD','UMPNA'])

#New_copy.search_ts_id('D:\Проекты\LPDS_Salim\HMI\_Docs\Trends\\')
#New_copy.dmz_trends_tree('D:\Проекты\ЛПДС_Каракатеевы')








