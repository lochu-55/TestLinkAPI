from testlink import TestlinkAPIClient

from Utils.Inputs.Common_inputs import inputs
from Utils.Logger.log import get_logger


class Create:
    tlc = TestlinkAPIClient(inputs.API_URL, inputs.KEY)
    

    def __init__(self):
        self.newProjectID = 0
        self.newTestPlanID_A = 0
        self.newTestSuiteID_A = 0
        self.logger = get_logger()

    def create_test_project(self):
        newpro = self.tlc.createTestProject(inputs.PROJECT_NAME,inputs.PROJECT_PREFIX,active=1,public=1,notes="pcie based nvme project",options={'requirementsEnabled' : 1, 'testPriorityEnabled' : 1,'automationEnabled' : 1, 'inventoryEnabled' : 1})
        self.logger.info("Successfully created Test project: %s", newpro)
        self.newProjectID = newpro[0]['id']
        self.logger.info("project ID ---> %s",self.newProjectID)
        return self.newProjectID


    def create_test_plan(self):
        newTestPlan = self.tlc.createTestPlan(inputs.PLAN_NAME, testprojectname=inputs.PROJECT_NAME,
                    notes='New TestPlan created with the PCI',active=1, public=1)
        self.logger.info("Successfully created Test Plan and linked to project:  %s", newTestPlan)
        self.newTestPlanID_A = newTestPlan[0]['id']
        self.logger.info("New Test Plan '%s' - id ---> %s" % (inputs.PLAN_NAME,self.newTestPlanID_A))
        return self.newTestPlanID_A

    def create_build(self):
        newBuild = self.tlc.createBuild(self.newTestPlanID_A, inputs.BUILD_NAME,
                                    'Notes for the Build', releasedate="2016-12-31")
        self.logger.info("Successfully created Build %s", newBuild)
        newBuildID_A = newBuild[0]['id']
        self.logger.info("New Build '%s' - id ---> %s" % (inputs.BUILD_NAME, newBuildID_A))
        return newBuildID_A

    def create_platform(self):
        newPlatForm = self.tlc.createPlatform(inputs.PROJECT_NAME, inputs.PLATFORM_NAME,
                notes='Platform for ubuntu, unique name, only used in this project',
                platformondesign=True, platformonexecution=True)
        self.logger.info("Successfully created Platform %s", newPlatForm)
        newPlatFormID_A = newPlatForm['id']
        response = self.tlc.addPlatformToTestPlan(self.newTestPlanID_A, inputs.PLATFORM_NAME)
        self.logger.info("Successfully added platform to test plan...%s", response )
        return newPlatFormID_A

    def create_suite(self):
        newTestSuite = self.tlc.createTestSuite(self.newProjectID, inputs.SUITE_NAME,
                    "Details of the Test Suite A")
        self.logger.info("Successfully created Test Suite %s", newTestSuite)
        self.newTestSuiteID_A = newTestSuite[0]['id']
        self.logger.info("New Test Suite '%s' - id ---> %s" % (inputs.SUITE_NAME, self.newTestSuiteID_A))
        return self.newTestSuiteID_A



if __name__ == "__main__":
    create_instance = Create()

    create_instance.create_test_project()
    create_instance.create_test_plan()
    create_instance.create_build()
    create_instance.create_platform()
    create_instance.create_suite()
    print("created test project,plan,build,platform and suite successfully...")
