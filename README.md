# TestLink API Framework

This framework automates the process of importing test cases into TestLink.

---
# TestLink v1.9.19 Setup and Test Case Import

The configuration and Docker files have been pushed to the following repository:  
[https://github.com/lochu-55/testlink_1.9.19](https://github.com/lochu-55/testlink_1.9.19)

## Installing TestLink v1.9.19 Using Docker

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lochu-55/testlink_1.9.19.git
   cd testlink_1.9.19

2. **Build and install TestLink using Docker Compose**
   Run the following commands in your terminal:
   ```bash
   docker-compose --env-file ./envs/testlink-1.9.19.env -f docker-compose.yml -f docker-compose.build.yml build tl_code
   docker-compose --env-file ./envs/testlink-1.9.19.env -f docker-compose.yml -f docker-compose.build.yml build tl_pg tl_apache
   docker-compose --env-file ./envs/testlink-1.9.19.env -f docker-compose.yml up -d

3. **Access Testlink**
   Open the following URL in your browser:
   ```bash
   https://localhost:8085
   
4. **Login Credentials:**
    - **Username:** admin
    - **Password:** admin


## Prerequisites

- Python 3.x installed.
- `pip` for managing Python packages.
- Docker installed and running to manage TestLink and database services.

---

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd TestLinkAPI
    ```

2. Install the required dependencies:
    ```bash
    pip install -r Import_TestCases/Utils/Libraries/requirements.txt
    ```

---

## Usage


### **Preparing Test Case File for TestLink Import**

Here is the structure of the Excel file to ensure compatibility with TestLink’s import functionality.

---

#### **File Requirements**
1. **File Format**: The file must be in `.xlsx` format (e.g., `NVME.xlsx`).
2. **Sheet Structure**: The Excel sheet must include the following columns **in the exact order**:

---

#### **Column Description**
| **Column Name**          | **Description**                                                                                 | **Example Data**                      |
|--------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------|
| **Test Suite**           | The category or module of the test case.                                                       | Basic Functionality Tests             |
| **Test Case Title**      | A descriptive title for the test case.                                                         | Device Detection and Initialization   |
| **Requirements**         | The associated requirement IDs or references.                                                  | use-case-01, feature-01               |
| **Summary**              | A brief description of the test case objective.                                                | Verify NVMe device initialization.    |
| **Preconditions**        | Any prerequisites required before executing the test case.                                      | Power on the system.                  |
| **Steps_actions**        | Step-by-step instructions for performing the test.                                              | 1. Launch VM; 2. Check dmesg output.  |
| **Keywords**             | Tags or labels for categorizing the test (e.g., regression, performance, smoke).                | Smoke, Sanity                         |
| **Status**               | The current state of the test case (e.g., Draft, Future, Rework, Obsolete).                     | Draft                                 |
| **Importance**           | The priority of the test case (e.g., High, Medium, Low).                                        | High                                  |
| **TestCase_execution_type** | The type of execution (e.g., Automated, Manual).                                               | Automated                             |
| **Exec time**            | Estimated time to complete the test case (in seconds).                                          | 100                                   |
| **Expected_results**     | The expected outcome or behavior for each step.                                                 | The VM should launch without errors.  |
| **Step_execution_type**  | Specifies whether each step is Manual or Automated.                                             | Manual/Automated                      |

---

#### **Example of Correct Format**

| **Test Suite**            | **Test Case Title**              | **Requirements**        | **Summary**                                                     | **Preconditions**         | **Steps_actions**                                | **Keywords**        | **Status**   | **Importance** | **TestCase_execution_type** | **Exec time** | **Expected_results**                         | **Step_execution_type** |
|---------------------------|----------------------------------|-------------------------|-----------------------------------------------------------------|---------------------------|------------------------------------------------|---------------------|--------------|----------------|-----------------------------|---------------|-----------------------------------------------|-------------------------|
| Basic Functionality Tests | Device Detection and Initialization | use-case-01             | Verify that the NVMe device initializes correctly.              | Power on system           | 1. Launch VM; 2. Check dmesg output.           | Smoke, Sanity       | Draft        | High           | Automated                   | 100           | The VM should launch without errors.         | Automated              |
| Performance Tests         | Random Read Operation           | use-case-01, feature-01 | Verify that driver handles random read operations.              | Power on system           | 1. Perform random read operation using fio.    | Performance         | Future       | Medium         | Manual                      | 180           | The code should run without errors.          | Manual                 |

---



### Configure the Framework

Update the configuration file `Import_TestCases/Utils/Inputs/Common_inputs.py` with your required values and paths:

- `API_URL`: The TestLink API URL.
- `LOGIN`: The TestLink login URL.
- `KEY`: Your TestLink API key.
- `PROJECT_NAME`: The name of the test project in TestLink.
- `PROJECT_PREFIX`: Prefix for the test project in TestLink.
- `PLAN_NAME`: Name of the test plan in TestLink.
- `PLATFORM_NAME`: Name of the platform being tested.
- `SUITE_NAME`: Name of the test suite in TestLink.
- `BUILD_NAME`: Name of the build being used.
- `MANUAL`: Value indicating manual execution type (1 for manual).
- `EXCEL_PATH`: Path to the Excel file containing the test case data.
- `LOG_PATH`: Path to the log file directory.
- `keywords_excel_file`: Path to the Excel file containing keywords.
- `req_xml_file`: Path to the XML file containing requirements.

### Run the Framework

1. Grant execute permissions to the shell script:
    ```bash
    chmod 777 testlink_import.sh
    ```

2. Execute the script to start importing test cases:
    ```bash
    ./testlink_import.sh
    ```

---

## Database Access

To access the database used by TestLink:

1. **Access the IP Address of postgresql Container:**
   ```bash
   docker inspect testlink_pg_1.9.19 | grep IPAddress
   ``` 
    
    Example output:
    ```json
    "IPAddress": "172.21.0.2",
    ```

2. Replace the value of variable named **host** in class **DB** present in **"Utils/Inputs/Common_inputs"** with above retreived IPAddress
   

---
### Exporting the Test Cases
Follow these steps to export test cases from TestLink:
1. **Navigate to the TestLinkAPI/Export directory:**
   ```bash
   cd TestLinkAPI/Export

2. **Run the export script using Python 3:**
   ```bash
   python3 Core/Creation/export_excel.py
   
3. The exported Excel file, `test_cases.xlsx`, will be saved in the `Excelsheet` folder.

---
## Notes

- Ensure Docker containers for TestLink and its database are running before executing the framework.
- Verify the Excel file structure matches the required format as specified in the framework documentation.
