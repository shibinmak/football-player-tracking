"""

** coded by shibinmak on 6/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""


import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from config import config



def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):

        split = xml_file.split('/')
        basename = split[-1]
        filebase = basename[:basename.rfind('.') + 1]
        imgbase = filebase + 'png'
        split[-1] = imgbase
        filename = os.path.sep.join(split)

        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (filename,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     'players',
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['imagepath', 'width', 'height', 'label', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def xml2csv():
    image_path = os.path.join(config.parent, 'Dataset','players')
    xml_df = xml_to_csv(image_path)
    csvf = os.path.join(config.ANNOT_PATH)
    xml_df.to_csv(csvf, index=None)
    print('Successfully converted xml to csv.')


xml2csv()