#from accessAPI import TestLinkManager,logger
from AccessAPI import TestLinkManager,logger
import pandas as pd
from re import sub


class ExportToExcel:
    def __init__(self, testlink_manager):
        self.testlink_manager = testlink_manager


    def collect_projects_and_test_cases(self):
        data = []
        try:
            projects = self.testlink_manager.get_projects()
            logger.info("Successfully fetched projects from TestLink.")
        except Exception as e:
            logger.error(f"Failed to fetch projects: {e}")
            return []

        for project in projects:
            project_name = project.get('name')
            logger.info(f"Project  : {project_name}")
            p1 = True  # Flag to ensure project name appears only once

            try:
                requirements = self.testlink_manager.fetch_project_requirements(project['id'],project_name)
                test_plans = self.testlink_manager.get_project_test_plans(project['id'],project_name)
            except Exception as e:
                logger.error(f"     Failed to fetch requirements or test plans for project {project_name}: {e}")
                continue

            for plan in test_plans:
                plan_name = plan.get('name')
                plan_flag = True  # Flag to ensure test plan name appears only once

                try:
                    test_suites = self.testlink_manager.get_test_suites_for_test_plan(plan['id'],plan_name)
                except Exception as e:
                    logger.error(f"     Failed to fetch test suites for plan {plan_name}: {e}")
                    continue

                for suite in test_suites:
                    suite_name = suite.get('name', 'Unknown Suite')
                    suite_flag = True  # Flag to ensure test suite name appears only once

                    try:
                        test_cases = self.testlink_manager.get_test_cases_for_test_plan(plan['id'],plan_name)
                    except Exception as e:
                        logger.error(f"     Failed to fetch test cases for suite {suite_name}: {e}")
                        continue

                    for case_id, case_data in test_cases.items():
                        if isinstance(case_data, dict):
                            for case in case_data:
                                self._process_test_case(
                                    data, project_name,project['id'], plan_name, suite_name,
                                    p1, plan_flag, suite_flag,
                                    case_data[case], requirements
                                )
                                # Update flags
                                p1 = plan_flag = suite_flag = False

                        elif isinstance(case_data, list):
                            for i in case_data:
                                self._process_test_case(
                                    data, project_name,project['id'], plan_name, suite_name,
                                    p1, plan_flag, suite_flag,
                                    i, requirements
                                )
                                # Update flags
                                p1 = plan_flag = suite_flag = False

        return data

    def _process_test_case(self, data, project_name,project_id, plan_name, suite_name,
                           p1, plan_flag, suite_flag, case_data, requirements):
        try:
            test_case_details = self.testlink_manager.get_test_case_details(case_data['tcase_id'])
            test_case_req = self.testlink_manager.fetch_testcase_requirements(project_id, project_name,case_data['tcase_id'])
            tc_keywords = self.testlink_manager.fetch_testcase_keywords(case_data['tcase_id'], case_data['external_id'])
        except Exception as e:
            logger.error(f"     Failed to fetch details or keywords for test case {case_data['tcase_name']}: {e}")
            return

        if isinstance(test_case_details, list) and len(test_case_details) > 0:
            test_case = test_case_details[0]
            preconditions = test_case.get('preconditions', '')
            summary = test_case.get('summary', '')

            steps = test_case.get('steps', [])
            if isinstance(steps, str):
                # Steps as a single string
                data.append({
                    'Test Project Name': project_name if p1 else "",
                    'Project Requirements': ", ".join(requirements) if p1 else "",
                    'Platform': case_data.get('platform_name', " ") if plan_flag else "",
                    'Test Plan': plan_name if plan_flag else "",
                    'Test Suite': suite_name if suite_flag else "",
                    'Test Case Title': case_data['tcase_name'],
                    'Test Case Requirements': test_case_req,
                    'Summary': summary,
                    'Preconditions': preconditions,
                    'Step Actions': steps,
                    'Step Expected Results': steps,
                    'Step Execution Type': steps,  # Assuming execution type is the same as steps
                    'Test Execution Status': self.testlink_manager.get_status(test_case.get('status', " ")),
                    'Test Execution Type': self.testlink_manager.get_execution_type(test_case.get('execution_type')),
                    'Test Case Keywords': tc_keywords,
                    'Execution Order': case_data['execution_order'],
                    'Importance': self.testlink_manager.get_importance(test_case.get('importance', " ")),
                    'Estimated Duration': test_case.get('estimated_exec_duration', " ")
                })
            else:
                # Steps as a list
                self._process_steps(data, project_name, plan_name, suite_name,
                                    p1, plan_flag, suite_flag,
                                    case_data, test_case, steps,
                                    summary, preconditions, requirements, tc_keywords,test_case_req)

    def _process_steps(self, data, project_name, plan_name, suite_name,
                       p1, plan_flag, suite_flag, case_data, test_case, steps,
                       summary, preconditions, requirements, tc_keywords,test_case_req):
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
                    'Test Project Name': project_name if (index == 0 and p1) else "",
                    'Project Requirements': ", ".join(requirements) if (index == 0 and p1) else "",
                    'Platform': case_data.get('platform_name', " ") if (index == 0 and plan_flag) else "",
                    'Test Plan': plan_name if (index == 0 and plan_flag) else "",
                    'Test Suite': suite_name if (index == 0 and suite_flag) else "",
                    'Test Case Title': case_data['tcase_name'] if index == 0 else "",
                    'Test Case Requirements': test_case_req if index == 0 else " ",
                    'Summary': self.remove_html_tags(summary) if index == 0 else "",
                    'Preconditions': self.remove_html_tags(preconditions) if index == 0 else "",
                    'Step Actions': self.remove_html_tags(step_text),
                    'Step Expected Results': self.remove_html_tags(expected_result_lines[index]) if index < len(expected_result_lines) else "",
                    'Step Execution Type': self.testlink_manager.get_execution_type(exec_type_lines[index]) if index < len(exec_type_lines) else "",
                    'Test Execution Status': self.testlink_manager.get_status(test_case.get('status', " ")) if index == 0 else "",
                    'Test Execution Type': self.testlink_manager.get_execution_type(test_case.get('execution_type')) if index == 0 else " ",
                    'Test Case Keywords': tc_keywords if index == 0 else "",
                    'Execution Order': case_data['execution_order'] if index == 0 else "",
                    'Importance': self.testlink_manager.get_importance(test_case.get('importance', " ")) if index == 0 else "",
                    'Estimated Duration': test_case.get('estimated_exec_duration', " ") if index == 0 else ""
                })

    def remove_html_tags(self, text):
        try:
            clean_text = sub(r'<.*?>', '', text)  # Regex to remove HTML tags
            return clean_text
        except Exception as e:
            logger.error(f"     Failed to remove HTML tags from text: {e}")
            return text

    def export_to_excel(self, data, filename="Excelsheet/test_cases.xlsx"):
        try:
            df = pd.DataFrame(data)
            df.to_excel(filename, index=False)
            print(f"Data successfully exported to {filename}")
            logger.info(f"Data successfully exported to {filename}")
        except Exception as e:
            logger.error(f"Failed to export data to Excel: {e}")


if __name__ == "__main__":
    # URL and API key for TestLink
    url = "http://172.17.17.93:8085/lib/api/xmlrpc/v1/xmlrpc.php"
    api_key = "6e6ac11d3cd05d79f5d2d07e7338e0c0"
    #api_key = "10b2132073a17c9d4a0bc700dd778f83"
    # Create an instance of TestLinkManager
    testlink_manager = TestLinkManager(url, api_key)

    # Create an instance of ExportToExcel
    exporter = ExportToExcel(testlink_manager)

    # Collect project and test case data
    data = exporter.collect_projects_and_test_cases()

    # Export data to Excel
    exporter.export_to_excel(data)