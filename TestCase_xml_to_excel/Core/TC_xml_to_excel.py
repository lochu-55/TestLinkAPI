import xml.etree.ElementTree as ET
from openpyxl import Workbook
import re

# Function to remove HTML tags from a string
def clean_html(raw_html):
    """Remove HTML tags from a string."""
    raw_html = raw_html.replace("&nbsp;", " ")
    clean = re.compile('<.*?>')
    return re.sub(clean, '', raw_html).strip()

# Function to map status values to their meanings
def get_status(val):
    status_dict = {
        '1': 'Draft', '2': 'Ready for review', '3': 'Review in progress',
        '4': 'Rework', '5': 'Obsolete', '6': 'Future', '7': 'Final'
    }
    return status_dict.get(val, " ")

# Function to map importance values to their meanings
def get_importance(val):
    imp_dict = {'1': 'High', '2': 'Medium', '3': 'Low'}
    return imp_dict.get(val, " ")

# Function to map execution type values to their meanings
def get_execution_type(val):
    exec_dict = {'1': 'Manual', '2': 'Automated'}
    return exec_dict.get(val, " ")

def process_testsuite(testsuite, worksheet, suite_hierarchy, printed_hierarchy, row_counter=[1]):
    suite_name = testsuite.get("name")
    suite_hierarchy.append(suite_name)

    for testcase in testsuite.findall("testcase"):
        # Get the test case name
        case_name = testcase.get("name", " ")

        summary = (testcase.find("summary").text.strip() if testcase.find("summary") is not None else " ")
        preconditions_element = testcase.find("preconditions")
        preconditions = preconditions_element.text.strip() if preconditions_element is not None and preconditions_element.text else " "
        clean_summary = clean_html(summary)  # Remove HTML tags from the summary
        clean_preconditions = clean_html(preconditions)
        t_execution_type_ele = testcase.find("execution_type")
        t_execution_type = get_execution_type(t_execution_type_ele.text.strip()) if t_execution_type_ele is not None and t_execution_type_ele.text else " "
        importance_ele = testcase.find("importance")
        importance = get_importance(importance_ele.text.strip()) if importance_ele is not None and importance_ele.text else " "
        estimated_exec_duration_ele = testcase.find("estimated_exec_duration")
        estimated_exec_duration = estimated_exec_duration_ele.text.strip() if estimated_exec_duration_ele is not None and estimated_exec_duration_ele.text else " "
        status_ele = testcase.find("status")
        status = get_status(status_ele.text.strip()) if status_ele is not None and status_ele.text else " "

        test_case_row_added = False
        # Check if steps exist, and create rows for each step
        steps_found = False  # Flag to check if steps are found
        for step in testcase.findall("steps/step"):
            steps_found = True
            step_number = step.find("step_number").text if step.find("step_number") is not None else ""
            actions = step.find("actions").text.strip() if step.find("actions") is not None else ""
            expectedresults_ele = step.find("expectedresults")
            expectedresults = expectedresults_ele.text.strip() if expectedresults_ele is not None and expectedresults_ele.text else ""
            execution_type_ele = step.find("execution_type")
            execution_type = get_execution_type(execution_type_ele.text.strip()) if execution_type_ele is not None and execution_type_ele.text else ""

            # Clean the HTML tags for actions and expected results
            clean_actions = clean_html(actions)
            clean_expectedresults = clean_html(expectedresults)

            # Create a new row for each step
            step_row = ["" for _ in range(max_level)] + ["", "", "", ""]
            step_row[max_level + 3:max_level + 6] = [step_number, clean_actions, clean_expectedresults, execution_type]

            # Add test case details (name, summary, preconditions) only once
            if not test_case_row_added:
                step_row[max_level:max_level + 3] = [case_name, clean_summary, clean_preconditions, t_execution_type, importance, estimated_exec_duration, status]
                test_case_row_added = True
            else:
                step_row[max_level:max_level + 3] = ["", "", "", "", "", "", ""]

            # Fill suite levels only if not already printed for this row
            for i, suite in enumerate(suite_hierarchy):
                if not printed_hierarchy[i]:
                    step_row[i] = suite
                    printed_hierarchy[i] = True

            # Append the step row
            worksheet.append(step_row)
            row_counter[0] += 1

        # If no steps are found, add a row with empty columns for steps
        if not steps_found:
            empty_step_row = ["" for _ in range(max_level)] + ["", "", "", "", "", "", ""]
            empty_step_row[max_level:max_level + 3] = [case_name, clean_summary, clean_preconditions, t_execution_type, importance, estimated_exec_duration, status]
            for i, suite in enumerate(suite_hierarchy):
                if not printed_hierarchy[i]:
                    empty_step_row[i] = suite
                    printed_hierarchy[i] = True
            worksheet.append(empty_step_row)
            row_counter[0] += 1

    # Process nested suites (sub-suites)
    for nested_suite in testsuite.findall("testsuite"):
        process_testsuite(nested_suite, worksheet, suite_hierarchy.copy(), printed_hierarchy.copy(), row_counter)

    # Remove the current suite from the hierarchy after processing
    suite_hierarchy.pop()

def find_max_depth(testsuite, current_depth=1):
    max_depth = current_depth
    for nested_suite in testsuite.findall("testsuite"):
        nested_depth = find_max_depth(nested_suite, current_depth + 1)
        max_depth = max(max_depth, nested_depth)
    return max_depth

def xml_to_excel(xml_file, excel_file):
    global max_level

    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Calculate the actual maximum depth of the suite hierarchy
    max_level = max(find_max_depth(suite) for suite in root.findall("testsuite"))

    # Create a new Excel workbook and worksheet
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Test Cases"

    # Add headers to the worksheet, dynamically adjusting for actual depth
    headers = [f"Suite Level {i+1}" for i in range(max_level)] + ["Test Case Name", "Summary", "Preconditions", "Test Execution Type", "Importance", "Estimated Exec Duration", "Status", "Step Number", "Actions", "Step Expected Results", "Step Execution Type"]
    worksheet.append(headers)

    # Process the top-level test suites
    for testsuite in root.findall("testsuite"):
        process_testsuite(testsuite, worksheet, [], [False] * max_level)

    # Save the Excel file
    workbook.save(excel_file)
    print(f"Excel file saved as {excel_file}")

if __name__ == "__main__":
    # Input XML file and output Excel file
    xml_file = "PCI.xml"  # Replace with your XML file path
    excel_file = "out.xlsx"  # Replace with your desired Excel output file path

    # Call the conversion function
    xml_to_excel(xml_file, excel_file)
