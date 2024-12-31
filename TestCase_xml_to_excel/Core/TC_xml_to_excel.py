import xml.etree.ElementTree as ET
import pandas as pd
import re

def clean_html(raw_html):
    """Remove HTML tags from a string."""
    raw_html = raw_html.replace("&nbsp;", " ")
    clean = re.compile('<.*?>')
    return re.sub(clean, '', raw_html).strip()

def get_status(val):
    status_dict = {'1': 'Draft', '2': 'Ready for review', '3': 'Review in progress',
                       '4': 'Rework', '5': 'Obsolete', '6': 'Future', '7': 'Final'}
    status = status_dict.get(val," ")
    return status


def get_importance(val):
    imp_dict = {'1': 'High', '2': 'Medium', '3': 'Low'}
    importance = imp_dict.get(val, " ")
    return importance

def get_execution_type(val):
    exec_dict = {'1': 'Manual', '2': 'Automated'}
    execution_type = exec_dict.get(val, " ")
    return execution_type

def parse_test_suite(xml_node, parent_names=[]):
    data = []
    suite_name = xml_node.attrib.get("name", "")
    current_names = parent_names + [suite_name]

    for child in xml_node:
        if child.tag == "testsuite":
            data.extend(parse_test_suite(child, current_names))
        elif child.tag == "testcase":
            testcase_name = child.attrib.get("name", "")
            testcase_id = child.attrib.get("internalid", "")
            summary = clean_html(child.findtext("summary", ""))
            preconditions = clean_html(child.findtext("preconditions", ""))
            status_raw = child.findtext("status", "")
            importance_raw = child.findtext("importance", "")
            execution_type_raw = child.findtext("execution_type", "")
            estimated_duration = child.findtext("estimated_exec_duration", "")

            status = get_status(status_raw)
            importance = get_importance(importance_raw)
            execution_type = get_execution_type(execution_type_raw)

            keywords = ", ".join([kw.attrib.get("name", "") for kw in child.findall("keywords/keyword")])

            steps = []
            for step in child.findall("steps/step"):
                step_number = step.findtext("step_number", "")
                actions = clean_html(step.findtext("actions", ""))
                expected_results = clean_html(step.findtext("expectedresults", ""))
                step_execution_type = get_execution_type(step.findtext("execution_type", execution_type))
                steps.append({
                    "Step Number": step_number,
                    "Step Actions": actions,
                    "Step Expected Results": expected_results,
                    "Step Execution Type": step_execution_type
                })

            suite_columns = {f"Suite Level {i+1}": name for i, name in enumerate(current_names[1:])}  

            if steps:
                for idx, step in enumerate(steps):
                    data.append({
                        **({key: value if idx == 0 else "" for key, value in suite_columns.items()}),
                        "Test Case Name": testcase_name if idx == 0 else "",
                        "Test Case ID": testcase_id if idx == 0 else "",
                        "Status": status if idx == 0 else "",
                        "Execution Type": execution_type if idx == 0 else "",
                        "Importance": importance if idx == 0 else "",
                        "Preconditions": preconditions if idx == 0 else "",
                        "Summary": summary if idx == 0 else "",
                        "Estimated Duration": estimated_duration if idx == 0 else "",
                        "Keywords": keywords if idx == 0 else "",
                        **step
                    })
            else:
                data.append({
                    **suite_columns,
                    "Test Case Name": testcase_name,
                    "Test Case ID": testcase_id,
                    "Status": status,
                    "Execution Type": execution_type,
                    "Importance": importance,
                    "Preconditions": preconditions,
                    "Summary": summary,
                    "Estimated Duration": estimated_duration,
                    "Keywords": keywords,
                    "Step Number": "",
                    "Step Actions": "",
                    "Step Expected Results": "",
                    "Step Execution Type": ""
                })

    return data

def xml_to_excel(xml_file, excel_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    data = parse_test_suite(root)

    df = pd.DataFrame(data)

    df.to_excel(excel_file, index=False, sheet_name="Test Cases")

xml_file = "PCI.xml"
excel_file = "out.xlsx"

xml_to_excel(xml_file, excel_file)
print("Converting xml to excel done")