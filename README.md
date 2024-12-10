# TestLink API Framework

This framework automates the process of importing test cases into TestLink.

---

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
    pip install -r Utils/Libraries/requirements.txt
    ```

---

## Usage

### Configure the Framework

Update the configuration file `Utils/Inputs/Common_inputs.py` with your required values and paths:

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
    chmod 777 testlink_total.sh
    ```

2. Execute the script to start importing test cases:
    ```bash
    ./testlink_total.sh
    ```

---

## Database Access

To access the database used by TestLink:

1. **Access the PostgreSQL Container:**
    ```bash
    docker exec -it testlink_pg_1.9.19 bash
    ```
    Inside the container, use the following command to connect:
    ```bash
    psql -h tl_pg -U tlink -d testlink-1.9.19
    ```

2. **Find the Container's IP Address:**
    Run the following command:
    ```bash
    docker inspect testlink_pg_1.9.19 | grep -i ipaddress
    ```
    Example output:
    ```json
    "IPAddress": "172.21.0.2",
    ```

3. Replace the value of variable named host in class DB present in Utils/Inputs/Common_inputs with above retreived IPAddress
   

---

## Notes

- Ensure Docker containers for TestLink and its database are running before executing the framework.
- Verify the Excel file structure matches the required format as specified in the framework documentation.
