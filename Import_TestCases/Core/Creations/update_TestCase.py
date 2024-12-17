from Utils.Inputs.Common_inputs import inputs
from Core.Creations.create_test_pro import Create
from Core.Creations.import_TestCases import Test
from testlink.testlinkerrors import TLResponseError
from Utils.Logger.log import get_logger

class Update:
    def __init__(self):
        self.test = Test()
        self.create = Create()
        self.logger = get_logger()

    def func(self):
        # Retrieve all test suites for the project
        res = Create.tlc.getFirstLevelTestSuitesForTestProject(self.test.get_project_id(inputs.PROJECT_NAME))
        suite_ids = [suite['id'] for suite in res]

        for suite_id in suite_ids:
            r = Create.tlc.getTestCasesForTestSuite(testsuiteid=suite_id, deep=False, details="simple")

            for test_case in r:
                tc_id = test_case["id"]
                tc_full_ext_id = Create.tlc.getTestCase(testcaseid=tc_id)[0]["full_tc_external_id"]
                tc_name = Create.tlc.getTestCase(testcaseid=tc_id)[0]["name"]
                print(tc_id, tc_full_ext_id, tc_name)

    def update_tc(self):
        testcase_id = input("Enter the test case ID you want to update: ").strip()
        #new_summary = input("Enter the new summary for the test case: ").strip()

        try:
            # Update only the summary field
            response = Create.tlc.updateTestCase(
                testcase_id,
                version=1,  # Optional, leave empty if not needed
                testcasename="Device_testing",  # Must be provided compulsory
                summary="testing a device",
                preconditions=None,  # Optional, leave empty if not needed
                steps=None,  # Optional, leave empty if not needed
                importance=None,  # Optional, leave empty if not needed
                executiontype=None,  # Optional, leave empty if not needed
                status=None,  # Optional, leave empty if not needed
                estimatedexecduration=None  # Optional, leave empty if not needed
            )
            print(f"Test case {testcase_id} updated successfully!")
            print("API Response:", response)  # Add this line to check the raw response
        except TLResponseError as e:
            print(f"Error occurred: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


# Initialize and run the update
u = Update()
print("TestCaseID TestCase_ExternalID TestCaseName\n")
u.func()
u.update_tc()
