from test_creation import TestLinkManager
import pandas as pd
import re

class ExportToExcel:
    def __init__(self, testlink_manager):
        self.testlink_manager = testlink_manager

    def collect_projects_and_test_cases(self):
        data = []
        projects = self.testlink_manager.get_projects()

        for project in projects:
            project_name = project['name']
            p1 = True  # Flag to ensure project name appears only once

            requirements = self.testlink_manager.fetch_requirements(project['id'])
            test_plans = self.testlink_manager.get_project_test_plans(project['id'])

            for plan in test_plans:
                plan_name = plan['name']
                plan_flag = True  # Flag to ensure test plan name appears only once

                test_suites = self.testlink_manager.get_test_suites_for_test_plan(plan['id'])

                for suite in test_suites:
                    suite_name = suite['name']
                    suite_flag = True  # Flag to ensure test suite name appears only once

                    test_cases = self.testlink_manager.get_test_cases_for_test_plan(plan['id'])

                    for case_id, case_data in test_cases.items():
                        if isinstance(case_data, dict):
                            for case in case_data:
                                self._process_test_case(
                                    data, project_name, plan_name, suite_name,
                                    p1, plan_flag, suite_flag,
                                    case_data[case], requirements
                                )
                                # Update flags
                                p1 = plan_flag = suite_flag = False

                        elif isinstance(case_data, list):
                            for i in case_data:
                                self._process_test_case(
                                    data, project_name, plan_name, suite_name,
                                    p1, plan_flag, suite_flag,
                                    i, requirements
                                )
                                # Update flags
                                p1 = plan_flag = suite_flag = False

        return data

    def _process_test_case(self, data, project_name, plan_name, suite_name,
                           p1, plan_flag, suite_flag, case_data, requirements):

        test_case_details = self.testlink_manager.get_test_case_details(case_data['tcase_id'])
        tc_keywords = self.testlink_manager.fetch_testcase_keywords(case_data['tcase_id'], case_data['external_id'])

        if isinstance(test_case_details, list) and len(test_case_details) > 0:
            test_case = test_case_details[0]

            preconditions = test_case.get('preconditions', '')
            summary = test_case.get('summary', '')

            steps = test_case.get('steps', [])
            if isinstance(steps, str):
                # Steps as a single string
                data.append({
                    'Project': project_name if p1 else "",
                    'Test Plan': plan_name if plan_flag else "",
                    'Test Suite': suite_name if suite_flag else "",
                    'Test Case ID': case_data['tcase_id'],
                    'Test Case Name': case_data['tcase_name'],
                    'Summary': summary,
                    'Preconditions': preconditions,
                    'Step Actions': steps,
                    'Step Expected Results': steps,
                    'Step Execution Type': steps,  # Assuming execution type is the same as steps
                    'Step Execution Status': case_data['exec_status'],
                    'Test Execution Status': test_case.get('status', " "),
                    'TC_Keywords': tc_keywords,
                    'Execution Order': case_data['execution_order'],
                    'Requirements': ", ".join(requirements),
                    'Importance': test_case.get('importance', " "),
                    'Estimated Duration': test_case.get('estimated_exec_duration', " "),
                    'Platform': case_data.get('platform_name', " ")
                })
            else:
                # Steps as a list
                self._process_steps(data, project_name, plan_name, suite_name,
                                    p1, plan_flag, suite_flag,
                                    case_data, test_case, steps,
                                    summary, preconditions, requirements, tc_keywords)

    def _process_steps(self, data, project_name, plan_name, suite_name,
                       p1, plan_flag, suite_flag, case_data, test_case, steps,
                       summary, preconditions, requirements, tc_keywords):

        steps_data = ""
        expected_result = ""
        exec_type = ""

        for step in steps:
            steps_data += f"{step['step_number']}. {step['actions']}\n"
            expected_result += step['expected_results'] + '\n'
            exec_type += step['execution_type'] + '\n'

        steps_lines = steps_data.split("\n")
        expected_result_lines = expected_result.split('\n')
        exec_type_lines = exec_type.split('\n')

        for index, step_text in enumerate(steps_lines):
            if index < len(expected_result_lines) and step_text:
                data.append({
                    'Project': project_name if (index == 0 and p1) else "",
                    'Test Plan': plan_name if (index == 0 and plan_flag) else "",
                    'Test Suite': suite_name if (index == 0 and suite_flag) else "",
                    'Test Case ID': case_data['tcase_id'] if index == 0 else "",
                    'Test Case Name': case_data['tcase_name'] if index == 0 else "",
                    'Summary': self.remove_html_tags(summary) if index == 0 else "",
                    'Preconditions': self.remove_html_tags(preconditions) if index == 0 else "",
                    'Step Actions': self.remove_html_tags(step_text),
                    'Step Expected Results': self.remove_html_tags(expected_result_lines[index]) if index < len(expected_result_lines) else "",
                    'Step Execution Type': exec_type_lines[index] if index < len(exec_type_lines) else "",
                    'Step Execution Status': case_data['exec_status'] if index == 0 else "",
                    'Test Execution Status': test_case.get('status', " ") if index == 0 else "",
                    'TC_Keywords': tc_keywords if index == 0 else "",
                    'Execution Order': case_data['execution_order'] if index == 0 else "",
                    'Requirements': ", ".join(requirements) if index == 0 else "",
                    'Importance': test_case.get('importance', " ") if index == 0 else "",
                    'Estimated Duration': test_case.get('estimated_exec_duration', " ") if index == 0 else "",
                    'Platform': case_data.get('platform_name', " ") if index == 0 else ""
                })

    def remove_html_tags(self, text):

        clean_text = re.sub(r'<.*?>', '', text)  # Regex to remove HTML tags
        return clean_text

    def export_to_excel(self, data, filename="Excelsheet/test_cases.xlsx"):
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)


if __name__ == "__main__":
    # URL and API key for TestLink
    url = "http://172.17.17.8:8085/lib/api/xmlrpc/v1/xmlrpc.php"
    api_key = "10b2132073a17c9d4a0bc700dd778f83"

    # Create an instance of TestLinkManager
    testlink_manager = TestLinkManager(url, api_key)

    # Create an instance of ExportToExcel
    exporter = ExportToExcel(testlink_manager)

    # Collect project and test case data
    data = exporter.collect_projects_and_test_cases()

    # Export data to Excel
    exporter.export_to_excel(data)
