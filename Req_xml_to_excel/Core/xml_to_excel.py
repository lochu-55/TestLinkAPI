import pandas as pd
import xml.etree.ElementTree as ET
import re


class XMLToExcelConverter:
    def __init__(self, xml_file, excel_file):
        self.xml_file = xml_file
        self.excel_file = excel_file

    @staticmethod
    def remove_html_tags(text):
        if text:
            return re.sub(r'<[^>]*>', '', text)
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
    def map_requirement_status(status):
        status_mapping = {
            "D": "Draft",
            "R": "Review",
            "W": "Rework",
            "F": "Finished",
            "I": "Implemented",
            "V": "Valid",
            "N": "Not Testable",
            "O": "Obsolete",
        }
        return status_mapping.get(status, "Unknown Status")

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

    def parse_and_convert(self):
        # Parse the XML file
        tree = ET.parse(self.xml_file)
        root = tree.getroot()

        data = []

        for req_spec in root.findall(".//req_spec"):
            req_spec_data = {
                "req_spec_title": req_spec.get("title"),
                "req_spec_doc_id": req_spec.get("doc_id"),
                "req_spec_revision": req_spec.find("revision").text,
                "req_spec_type": self.map_req_spec_type(req_spec.find("type").text),
                "req_spec_scope": self.remove_html_tags(req_spec.find("scope").text)
                if req_spec.find("scope") is not None
                else None,
            }

            first_requirement = True

            for requirement in req_spec.findall(".//requirement"):
                req_data = req_spec_data.copy() if first_requirement else {
                    "req_spec_title": None,
                    "req_spec_doc_id": None,
                    "req_spec_revision": None,
                    "req_spec_type": None,
                    "req_spec_scope": None,
                }
                req_data.update(
                    {
                        "requirement_docid": requirement.find("docid").text,
                        "requirement_title": requirement.find("title").text,
                        "requirement_version": requirement.find("version").text,
                        "requirement_revision": requirement.find("revision").text,
                        "requirement_description": self.remove_html_tags(
                            requirement.find("description").text
                        ),
                        "requirement_status": self.map_requirement_status(
                            requirement.find("status").text
                        ),
                        "requirement_type": self.map_requirement_type(
                            requirement.find("type").text
                        ),
                        "requirement_expected_coverage": requirement.find(
                            "expected_coverage"
                        ).text,
                    }
                )
                data.append(req_data)
                first_requirement = False

        df = pd.DataFrame(data)

        df.to_excel(self.excel_file, index=False)
        print(f"XML data is Converted to Excel and  data saved to {self.excel_file}")


if __name__ == "__main__":
    xml_file = 'Input_Req.xml'
    excel_file = 'Output_Req.xlsx'
    converter = XMLToExcelConverter(xml_file, excel_file)
    converter.parse_and_convert()
