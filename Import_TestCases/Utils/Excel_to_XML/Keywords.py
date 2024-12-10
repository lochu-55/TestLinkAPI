import pandas as pd
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom as minidom
from Utils.Inputs.Common_inputs import inputs

def convert_excel_to_xml(input_file, output_file):
    df = pd.read_excel(input_file)
    keywords_root = Element('keywords')

    for _, row in df.iterrows():
        keyword_name = row['Keywords']
        description = row['Description'] if pd.notna(row['Description']) else 'na'

        keyword_element = SubElement(keywords_root, 'keyword', name=keyword_name)
        notes_element = SubElement(keyword_element, 'notes')

        notes_element.text = description

    rough_string = tostring(keywords_root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(pretty_xml)

    print("keywords converted from xlsx to xml.....")


convert_excel_to_xml(inputs.keywords_excel_file, inputs.req_xml_file)

