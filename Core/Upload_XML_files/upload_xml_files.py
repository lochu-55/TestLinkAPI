from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from Utils.Inputs.Common_inputs import inputs


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

    def login(self):
        self.driver.get(self.url)

        self.driver.find_element(By.ID, "tl_login").send_keys(self.username)
        time.sleep(2)
        self.driver.find_element(By.ID, "tl_password").send_keys(self.password)
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//*[@id='login']/div[3]/input").click()


    def select_project(self):
        # Wait and switch to titlebar frame
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "titlebar")))

        # Wait for and select the project from dropdown
        dropdown_element = self.wait.until(
            EC.element_to_be_clickable((By.NAME, "testproject"))
        )
        select = Select(dropdown_element)
        select.select_by_visible_text(f"{inputs.PROJECT_PREFIX}:{inputs.PROJECT_NAME}")
        print("Selected project.")


        self.driver.switch_to.default_content()

    def keyword(self):
        # Switch to the mainframe now
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "mainframe")))

        print("Waiting for Keyword Management link...")
        # Locate and click the Keyword Management link inside the mainframe
        keyword_button = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Keyword Management"))
        )
        keyword_button.click()
        print("Navigated to Keyword Management.")

        self.driver.find_element(By.NAME,"do_import").click()

        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "mainframe")))

        print("Waiting to choose a keywords xml file...")
        # Locate and click the Keyword Management link inside the mainframe
        file_input = self.wait.until(
            EC.element_to_be_clickable((By.NAME, "uploadedFile"))
        )


        script_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(script_dir, "../.."))
        xml_file_path = os.path.join(project_root, 'Utils', 'XML_files', 'keywords.xml')

        # Make sure the file exists
        if os.path.exists(xml_file_path):
            file_input.send_keys(xml_file_path)
            print(f"File {xml_file_path} has been uploaded successfully.")
        else:
            print(f"File does not exist at path: {xml_file_path}")

        self.driver.find_element(By.NAME,"UploadFile").click()


    def switch_to_index(self):
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "titlebar")))
        home_button = self.driver.find_element(By.XPATH, "//a[img[@title='Desktop']]")
        home_button.click()
        print("redirected to main menu....")

    def req_spec(self):
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "mainframe")))
        print("switched to main frame....")
        home_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Requirement Specification')]"))
        )
        home_button.click()

    def import_req(self):
        self.driver.switch_to.frame("workframe")  # Replace "titlebar" with the correct frame name or ID.
        file_input=self.driver.find_element(By.NAME,"import_all")
        print("clicked import button....")
        file_input.click()


        choose_file = self.driver.find_element(By.NAME,"uploadedFile")

        script_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(script_dir, "../.."))
        xml_file_path = os.path.join(project_root, 'Utils', 'XML_files', 'Reqs.xml')

        # Make sure the file exists
        if os.path.exists(xml_file_path):
            choose_file.send_keys(xml_file_path)
            print(f"File {xml_file_path} has been uploaded successfully.")
        else:
            print(f"File does not exist at path: {xml_file_path}")

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

