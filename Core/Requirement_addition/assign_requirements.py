import pandas as pd
from testlink import TestlinkAPIClient
from Core.Creations.DB_access import get_ids_and_srs_ids_by_req_doc_names
from Core.Creations.import_TestCases import Test
from Utils.Inputs.Common_inputs import inputs
from Utils.Logger.log import get_logger
logger = get_logger()


tlc = TestlinkAPIClient(inputs.API_URL, inputs.KEY)
test = Test()

if __name__ == "__main__":
    try:
        excel_file = inputs.EXCEL_PATH
        df = pd.read_excel(excel_file)
        df = df.dropna(subset=['Test Suite', 'Test Case Title', 'Requirements'])


        # Fetch all existing projects in TestLink
        existing_projects = tlc.getProjects()
        project_names = [project['name'] for project in existing_projects]
        print("Project Names:\n", project_names)

        # Get the project name from inputs
        enter_project_name = inputs.PROJECT_NAME
        project_id = test.get_project_id(enter_project_name)


        # Fetch existing test plans for the project
        plans = tlc.getProjectTestPlans(project_id)
        plan_ids = [plan['id'] for plan in plans]

        for _, row in df.iterrows():
            test_suite = row['Test Suite']
            test_case_title = str(row['Test Case Title'])
            requirements = row['Requirements']

            test_case_details = tlc.getTestCaseIDByName(
                testcasename=test_case_title
            )
            if not test_case_details:
                print(f"Test case '{test_case_title}' not found. Skipping.")
                continue

            test_case_id = test_case_details[0]['id']
            ext_id = tlc.getTestCase(testcaseid=test_case_id)[0]['full_tc_external_id']

            req_ids = [req.strip() for req in requirements.split(',') if req.strip()]
            srs_results = get_ids_and_srs_ids_by_req_doc_names(req_ids)

            if not srs_results:
                print(f"No matching SRS names found for requirements: {req_ids}. Skipping.")
                continue


            assignment_payload = [
                {'req_spec': srs_id, 'requirements': [req_id]}
                for req_id, srs_id in srs_results
            ]
            logger.info(f"Assigning requirements to Test Case ID {test_case_id}: {assignment_payload}")



            response = tlc.assignRequirements(ext_id, project_id, assignment_payload)

            logger.info(f"Response from TestLink for Test Case %s'{test_case_title}':", response)
        print("requirements assigned successfully..........")
    except Exception as e:
        print("Error:", str(e))
