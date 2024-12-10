from testlink import TestlinkAPIClient
import logging

open('Utils/testlink_export.log', 'w').close()
# Set up logging
logging.basicConfig(filename='Utils/testlink_export.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TestLinkManager:
    def __init__(self, url, api_key):
        try:
            self.testlink = TestlinkAPIClient(url, api_key)
            logger.info("TestLink API Client initialized successfully.")
            print("TestLink API Client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize TestLink API Client: {e}")
            raise

    # API Interaction Methods
    def get_projects(self):
        try:
            projects = self.testlink.getProjects()
            logger.info(f"Fetched {len(projects)} projects.")
            return projects
        except Exception as e:
            logger.error(f"Error fetching projects: {e}")
            raise

    def get_project_test_plans(self, project_id,project_name):
        try:
            test_plans = self.testlink.getProjectTestPlans(project_id)
            logger.info(f"      Fetched {len(test_plans)} test plans for project {project_name}.")
            return test_plans
        except Exception as e:
            logger.error(f"     Error fetching test plans for project {project_name}: {e}")
            raise

    def get_test_suites_for_test_plan(self, plan_id, plan_name):
        try:
            test_suites = self.testlink.getTestSuitesForTestPlan(plan_id)
            logger.info(f"      Fetched {len(test_suites)} test suites for plan {plan_name}.")
            return test_suites
        except Exception as e:
            logger.error(f"     Error fetching test suites for test plan {plan_name}: {e}")
            raise

    def get_test_cases_for_test_plan(self, plan_id, plan_name):
        try:
            test_cases = self.testlink.getTestCasesForTestPlan(plan_id)
            logger.info(f"      Fetched {len(test_cases)} test cases for plan {plan_name}.")
            return test_cases
        except Exception as e:
            logger.error(f"     Error fetching test cases for test plan {plan_name}: {e}")
            raise

    def get_test_case_details(self, case_id):
        try:
            case_details = self.testlink.getTestCase(case_id)
            logger.info(f"      Fetched details for test case {case_id}.")
            return case_details
        except Exception as e:
            logger.error(f"     Error fetching details for test case {case_id}: {e}")
            raise


    def fetch_project_requirements(self, project_id,project_name):
        try:
            requirements = self.testlink.getRequirements(project_id)

            if requirements:
                req_doc_ids = [req['req_doc_id'] for req in requirements]
                logger.info(f"Fetched {len(req_doc_ids)} requirements for project {project_name}.\n   {', '.join(req_doc_ids)}")
                return req_doc_ids
            else:
                logger.info(f"No requirements found for project {project_name}.")
                return []
        except Exception as e:
            logger.error(f"Error fetching requirements for project {project_name}: {e}")
            raise

    def fetch_testcase_requirements(self, project_id,project_name,tcase_id):
        try:
            requirements = self.testlink.getRequirements(project_id)

            if requirements:
                l = []
                for i in requirements:
                    req_doc_id = i['req_doc_id']
                    req = self.testlink.getReqCoverage(project_id,req_doc_id)

                    if req == []:
                        continue
                    else:
                        for j in req:
                            if tcase_id == j['id']:
                                l.append(req_doc_id)
                if l == []:
                    return " "
                else:
                    return ", ".join(l)
        except Exception as e:
            logger.error(f"     Error fetching requirements for project {project_name}: {e}")
            raise

    def fetch_testcase_keywords(self, testcaseid, externalid):
        try:
            keywords = self.testlink.getTestCaseKeywords(testcaseid=testcaseid, testcaseexternalid=externalid)
            keywords = keywords.get(testcaseid, {})
            if isinstance(keywords, dict):
                val = ', '.join(keywords.values())
                logger.info(f"      Fetched keywords for test case {testcaseid}: {val}")
                return val
            else:
                logger.info(f"      No keywords found for test case {testcaseid}.")
                return " "
        except Exception as e:
            logger.error(f"     Error fetching keywords for test case {testcaseid}: {e}")
            raise

    def get_status(self, testcasedetails):
        try:
            status_dict = {'1': 'Draft', '2': 'Ready for review', '3': 'Review in progress', '4': 'Rework', '5': 'Obsolete', '6': 'Future', '7': 'Final'}
            status = status_dict.get(testcasedetails, "Unknown Status")
            logger.info(f"      Test case status: {status}")
            return status
        except Exception as e:
            logger.error(f"     Error getting status for test case {testcasedetails}: {e}")
            raise

    def get_importance(self, testcasedetails):
        try:
            imp_dict = {'1': 'High', '2': 'Medium', '3': 'Low'}
            importance = imp_dict.get(testcasedetails, "Unknown Importance")
            logger.info(f"      Test case importance: {importance}")
            return importance
        except Exception as e:
            logger.error(f"     Error getting importance for test case {testcasedetails}: {e}")
            raise

    def get_execution_type(self, testcasedetails):
        try:
            imp_dict = {'1': 'Manual', '2': 'Automated'}
            execution_type = imp_dict.get(testcasedetails, "Unknown Execution Type")
            logger.info(f"      Test case execution type: {execution_type}")
            return execution_type
        except Exception as e:
            logger.error(f"     Error getting execution type for test case {testcasedetails}: {e}")
            raise