import pandas as pd
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom as minidom

def convert_xml_to_excel(input_file, output_file):
    # Parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Extract data from XML
    data = []
    for keyword_element in root.findall('keyword'):
        keyword_name = keyword_element.get('name')
        notes_element = keyword_element.find('notes')
        description = notes_element.text.strip() if notes_element is not None else "na"

        # Remove CDATA wrapper
        description = description.replace("<![CDATA[", "").replace("]]>", "").strip()

        # Append to data list
        data.append({'Keywords': keyword_name, 'Description': description})

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Write to Excel file
    df.to_excel(output_file, index=False)


def convert_excel_to_xml(input_file, output_file):
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Create the root element
    keywords_root = Element('keywords')

    # Iterate through the DataFrame and create XML structure
    for _, row in df.iterrows():
        keyword_name = row['Keywords']
        description = row['Description'] if pd.notna(row['Description']) else 'na'

        # Create a 'keyword' element
        keyword_element = SubElement(keywords_root, 'keyword', name=keyword_name)
        notes_element = SubElement(keyword_element, 'notes')

        # Add CDATA section
        notes_element.text = description

    # Beautify and write to file
    rough_string = tostring(keywords_root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(pretty_xml)


# Example usage
input_excel_file = 'keywords.xlsx'  # Replace with your input .xlsx file
output_xml_file = 'keywords_import03.xml'  # Replace with your desired output .xml file
convert_excel_to_xml(input_excel_file, output_xml_file)

# Example usage
# input_xml_file = 'keywords.xml'  # Replace with your input .xml file
# output_excel_file = 'keywords_01.xlsx'  # Replace with your desired output .xlsx file
# convert_xml_to_excel(input_xml_file, output_excel_file)
