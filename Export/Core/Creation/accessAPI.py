from testlink import TestlinkAPIClient
from bs4 import BeautifulSoup


class TestLinkManager:
    def __init__(self, url, api_key):
        self.testlink = TestlinkAPIClient(url, api_key)

    # API Interaction Methods
    def get_projects(self):
        return self.testlink.getProjects()

    def get_project_test_plans(self, project_id):
        return self.testlink.getProjectTestPlans(project_id)

    def get_test_suites_for_test_plan(self, plan_id):
        return self.testlink.getTestSuitesForTestPlan(plan_id)

    def get_test_cases_for_test_plan(self, plan_id):
        return self.testlink.getTestCasesForTestPlan(plan_id)

    def get_test_case_details(self, case_id):
        return self.testlink.getTestCase(case_id)

    def fetch_requirements(self,project_id):
        requirements = self.testlink.getRequirements(project_id)
        if requirements:
            req_doc_ids = []
            for req in requirements:
                req_doc_ids.append(req['req_doc_id'])
            return req_doc_ids

        else:
            return []

    def fetch_testcase_keywords(self, testcaseid, externalid):
        keywords = self.testlink.getTestCaseKeywords(testcaseid=testcaseid, testcaseexternalid=externalid)
        keywords = keywords[testcaseid]
        if isinstance(keywords,dict):
            val = keywords.values()
            val = ', '.join(val)
            return val
        else:
            return " "






