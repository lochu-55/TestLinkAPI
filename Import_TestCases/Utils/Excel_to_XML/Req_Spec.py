import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom

from Utils.Inputs.DropDown_options import Options

df = pd.read_excel('Utils/Excel_to_XML/xlsx_files/req_spec.xlsx')


root = ET.Element("requirement-specification")

for _, row in df.iterrows():
    req_spec = ET.SubElement(root, "req_spec", title=row['Req-Title'], doc_id=row['Document ID'])

    type_ = ET.SubElement(req_spec, "type")
    type_value = Options.req_Op_Type.get(str(row["Type"]), "0")
    type_.text = str(type_value)


    total_req = ET.SubElement(req_spec, "total_req")
    total_req.text = str(0)

    scope = ET.SubElement(req_spec, "scope")
    scope_text = row['Scope']
    scope.text = f"<![CDATA[<p>{scope_text}</p>"



    requirement = ET.SubElement(req_spec, "requirement")

    docid = ET.SubElement(requirement, "docid")
    docid.text = str(row['Sub-requirement Doc ID'])

    title = ET.SubElement(requirement, "title")
    title.text = str(row['Sub-requirement Title'])


    status = ET.SubElement(requirement, "status")
    status_value = Options.req_status_mapping.get(row['Status'], "D")
    status.text = status_value


    req_type_sub = ET.SubElement(requirement, "type")
    req_type_value = Options.req_type_mapping.get(row['Sub-type'], "0")
    req_type_sub.text = str(req_type_value)


    description = ET.SubElement(requirement, "description")
    description_text = row['Scope']
    description.text = f"<![CDATA[<p>{description_text}</p>"

    expected_coverage = ET.SubElement(requirement, "expected_coverage")
    expected_coverage.text = str(row['Expected-coverage'])


print("requirements converted from xlsx to xml successfully.......")
# Create an ElementTree object
tree = ET.ElementTree(root)
xml_str = minidom.parseString(ET.tostring(root, 'utf-8')).toprettyxml(indent="    ")


with open("Utils/Excel_to_XML/xml_files/Reqs.xml", "w", encoding="UTF-8") as f:
    f.write(xml_str)
