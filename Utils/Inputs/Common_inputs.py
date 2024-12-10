# Constants

class inputs:
    API_URL = "http://localhost:8085/lib/api/xmlrpc/v1/xmlrpc.php"
    LOGIN = "http://localhost:8085/login.php?note=logout&viewer="
    KEY = "10b2132073a17c9d4a0bc700dd778f83"
    PROJECT_NAME = "PCI"
    PROJECT_PREFIX ="pcie"
    PLAN_NAME= "PCIE-planA"
    PLATFORM_NAME = "ubuntu"
    SUITE_NAME = "suite-nvme"
    BUILD_NAME = "v0.0.1"
    MANUAL = 1
    EXCEL_PATH = "TC_Excel_sheet/NVME.xlsx"
    LOG_PATH = "Utils/Logger"
    keywords_excel_file = 'Utils/Excel_to_XML/xlsx_files/keywords.xlsx'
    req_xml_file = 'Utils/Excel_to_XML/xml_files/keywords.xml'

class DB:
    host = "172.28.0.3"
    database = "testlink-1.9.19"
    user = "tlink"
    password = "tlink"