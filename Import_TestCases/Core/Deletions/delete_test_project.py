from testlink import TestlinkAPIClient
from Utils.Inputs.Common_inputs import inputs
from Core.Creations.import_TestCases import Test
from Utils.Logger.log import get_logger
import os

class TestLinkManager:
    def __init__(self):
        self.tlc = TestlinkAPIClient(inputs.API_URL, inputs.KEY)
        self.test = Test()
        self.logger = get_logger()


    def get_project_id(self, project_name):
        try:
            return self.test.get_project_id(project_name)
        except ValueError as e:
            print(f"Error: {e}")
            return None

    def delete_project(self, project_name):

        # Retrieve project ID based on project name
        project_id = self.get_project_id(project_name)

        if not project_id:
            print(f"Project '{project_name}' not found. Deletion aborted.")
            return

        try:
            response = self.tlc.deleteTestProject(inputs.PROJECT_PREFIX)
            self.logger.info(f"Project '{project_name}' deleted successfully.")
        except Exception as e:
            self.logger.info(f"Error deleting project '{project_name}': {str(e)}")

    def delete_log_file(self):
        log_file = os.path.join(inputs.LOG_PATH, "output.log")
        if os.path.exists(log_file):
            os.remove(log_file)
        print("deleted the log file....................")

if __name__ == '__main__':
    tlm = TestLinkManager()
    project_name = inputs.PROJECT_NAME
    tlm.delete_project(project_name)
    tlm.delete_log_file()
