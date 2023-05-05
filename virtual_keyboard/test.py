import openpyxl
from lxml import etree

def str_find(str1, arr):
    i = 0
    for el in arr:
        if str(str1).find(el) > -1:
            return True

path_gen_pic = 'D:\Проекты\LPDS_Salim\HMI\_Docs\Gen\\D_MNS_SAR_VV.omobj'

parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False)
tree   = etree.parse(path_gen_pic, parser)
root   = tree.getroot()

# Редактируем шаблон под нужное УСО
for lvl_one in root.iter('type'):

    for lvl_two in lvl_one.iter('object'):

        if str_find(lvl_two.attrib['name'], {'r_basket'}):

            

            for lvl_three in lvl_two.iter('object'):


                if str_find(lvl_three.attrib['name'], {'Module_AMI0810'}) or str_find(lvl_three.attrib['name'], {'Module_AMO0410'}) or\
                   str_find(lvl_three.attrib['name'], {'Module_DDI3202K'}) or str_find(lvl_three.attrib['name'], {'Module_NOM'}) or\
                   str_find(lvl_three.attrib['name'], {'Module_DDO3202K'}):


                    for lvl_four in lvl_three.iter('init'):
                        if lvl_four.attrib['target'] == '_init_path':
                            lvl_four.attrib['target'] = '_init_path_type'

tree.write(path_gen_pic, pretty_print=True,encoding='utf-8')
print('Go')





     