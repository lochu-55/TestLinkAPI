import pandas as pd
import xml.etree.ElementTree as ET
import re


class XMLToExcelConverter:
    def __init__(self, xml_file, excel_file):
        self.xml_file = xml_file
        self.excel_file = excel_file
        self.processed_specs = set()

    @staticmethod
    def remove_html_tags(text):
        if text:
            return re.sub(r"<[^>]*>", "", text)
        return text

    @staticmethod
    def map_req_spec_type(req_type):
        type_mapping = {
            "1": "Section",
            "2": "User Requirement Specification",
            "3": "System Requirement Specification",
        }
        return type_mapping.get(req_type, "Unknown Type")

    @staticmethod
    def map_requirement_type(req_type):
        type_mapping = {
            "1": "Informational",
            "2": "Feature",
            "3": "Use Case",
            "4": "User Interface",
            "5": "Non-Functional",
            "6": "Constraint",
            "7": "System Function",
        }
        return type_mapping.get(req_type, "Unknown Type")

    def parse_requirements(self, req_spec, parent_data, data):
        for requirement in req_spec.findall(".//requirement"):
            req_data = {
                **parent_data,
                #"Req Spec Doc ID": "",
                "Spec Revision": "",
                "Spec Type": "",
                "Scope": "",
                "Requirement Doc ID": requirement.find("docid").text,
                "Requirement Title": requirement.find("title").text,
                "Requirement Version": requirement.find("version").text,
                "Requirement Revision": requirement.find("revision").text,
                "Requirement Description": self.remove_html_tags(
                    requirement.find("description").text
                ),
                "Requirement Type": self.map_requirement_type(
                    requirement.find("type").text
                ),
                "Expected Coverage": requirement.find("expected_coverage").text,
            }
            data.append(req_data)

    def parse_specifications(self, req_spec, parent_data, data, level=1):
        doc_id = req_spec.get("doc_id")
        if doc_id in self.processed_specs:
            return
        self.processed_specs.add(doc_id)

        # Extract additional fields
        revision = req_spec.find("revision").text if req_spec.find("revision") is not None else None
        scope = self.remove_html_tags(req_spec.find("scope").text) if req_spec.find("scope") is not None else None
        spec_type = self.map_req_spec_type(req_spec.find("type").text)

        parent_data[f"Sub Spec Level {level} Title"] = req_spec.get("title")
        parent_data[f"Sub Spec Level {level} Doc ID"] = doc_id
        #parent_data[f"Sub Spec Level {level} Revision"] = revision
        #parent_data[f"Sub Spec Level {level} Scope"] = scope
        #parent_data[f"Sub Spec Level {level} Spec Type"] = spec_type

        spec_data = {
            **parent_data,
            #"Req Spec Doc ID": doc_id,
            "Spec Revision": revision,
            "Spec Type": spec_type,
            "Scope": scope,
            "Requirement Doc ID": None,
            "Requirement Title": None,
            "Requirement Version": None,
            "Requirement Revision": None,
            "Requirement Description": None,
            "Requirement Type": None,
            "Expected Coverage": None,
        }

        data.append(spec_data)

        self.parse_requirements(req_spec, parent_data, data)

        nested_specs = req_spec.findall("req_spec")
        for nested_spec in nested_specs:
            self.parse_specifications(nested_spec, parent_data.copy(), data, level + 1)

    def parse_and_convert(self):
        tree = ET.parse(self.xml_file)
        root = tree.getroot()

        data = []

        top_level_specs = root.findall(".//req_spec")
        for req_spec in top_level_specs:
            self.parse_specifications(req_spec, {}, data)

        df = pd.DataFrame(data)

        sub_spec_columns = [col for col in df.columns if col.startswith("Sub Spec Level")]
        sub_spec_columns.sort(key=lambda x: (int(re.search(r"\d+", x).group()), x))  # Sort by level

        fixed_columns = [
            "Spec Revision",
            "Spec Type",
            "Scope",
        ]
        requirement_columns = [
            "Requirement Doc ID",
            "Requirement Title",
            "Requirement Version",
            "Requirement Revision",
            "Requirement Description",
            "Requirement Type",
            "Expected Coverage",
        ]

        df = df[sub_spec_columns + fixed_columns + requirement_columns]

        for col in sub_spec_columns:
            df[col] = df[col].mask(df[col].duplicated(), "")

        df.to_excel(self.excel_file, index=False)
        print(f"XML data is converted to Excel and saved to {self.excel_file}")


if __name__ == "__main__":
    xml_file = "Input.xml"
    excel_file = "Output_Req.xlsx"  
    converter = XMLToExcelConverter(xml_file, excel_file)
    converter.parse_and_convert()
