from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from Utils.Inputs.Common_inputs import inputs
from Utils.Logger.log import get_logger


class TestLinkAutomation:

    def __init__(self, url, username, password):
        self.url = url
        self.opts = Options()
        self.opts.add_argument("--headless")
        self.opts.add_experimental_option("detach", True)
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(options=self.opts)
        self.wait = WebDriverWait(self.driver, 10)
        self.logger = get_logger()

    def login(self):
        self.driver.get(self.url)

        self.driver.find_element(By.ID, "tl_login").send_keys(self.username)
        time.sleep(2)
        self.driver.find_element(By.ID, "tl_password").send_keys(self.password)
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//*[@id='login']/div[3]/input").click()


    def select_project(self):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "titlebar")))

        dropdown_element = self.wait.until(
            EC.element_to_be_clickable((By.NAME, "testproject"))
        )
        select = Select(dropdown_element)
        select.select_by_visible_text(f"{inputs.PROJECT_PREFIX}:{inputs.PROJECT_NAME}")
        self.logger.info("Selected the project..........")


        self.driver.switch_to.default_content()

    def keyword(self):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "mainframe")))

        self.logger.info("Waiting for Keyword Management link....")
        keyword_button = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Keyword Management"))
        )
        keyword_button.click()
        self.logger.info("Navigated to Keyword Management.........")

        self.driver.find_element(By.NAME,"do_import").click()

        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "mainframe")))

        self.logger.info("Waiting to choose a keywords xml file...")
        file_input = self.wait.until(
            EC.element_to_be_clickable((By.NAME, "uploadedFile"))
        )


        script_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(script_dir, "../.."))
        xml_file_path = os.path.join(project_root, 'Utils', 'Excel_to_XML','xml_files', 'keywords.xml')

        if os.path.exists(xml_file_path):
            file_input.send_keys(xml_file_path)
            self.logger.info(f"File {xml_file_path} has been uploaded successfully.....")
        else:
            self.logger.info(f"File does not exist at path: {xml_file_path}")

        self.driver.find_element(By.NAME,"UploadFile").click()


    def switch_to_index(self):
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "titlebar")))
        home_button = self.driver.find_element(By.XPATH, "//a[img[@title='Desktop']]")
        home_button.click()
        self.logger.info("redirected to main menu....")

    def req_spec(self):
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "mainframe")))
        self.logger.info("switched to main frame....")
        home_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Requirement Specification')]"))
        )
        home_button.click()

    def import_req(self):
        self.driver.switch_to.frame("workframe")  # Replace "titlebar" with the correct frame name or ID.
        file_input=self.driver.find_element(By.NAME,"import_all")
        self.logger.info("clicked import button....")
        file_input.click()


        choose_file = self.driver.find_element(By.NAME,"uploadedFile")

        script_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(script_dir, "../.."))
        xml_file_path = os.path.join(project_root, 'Utils', 'Excel_to_XML', 'xml_files','Reqs.xml')

        # Make sure the file exists
        if os.path.exists(xml_file_path):
            choose_file.send_keys(xml_file_path)
            self.logger.info(f"File {xml_file_path} has been uploaded successfully.")
        else:
            self.logger.info(f"File does not exist at path: {xml_file_path}")

        self.driver.find_element(By.NAME, "uploadFile").click()


if __name__ == "__main__":
    testlink_url = inputs.LOGIN
    username = "admin"
    password = "admin"
    ts = TestLinkAutomation(testlink_url, username, password)
    ts.login()
    ts.select_project()
    ts.keyword()
    ts.switch_to_index()
    ts.req_spec()
    ts.import_req()
    print("imported both keywords and requirements xml successfully............")
