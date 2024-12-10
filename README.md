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
    cd TestLink_API
    ```

2. Install the required dependencies:
    ```bash
    pip install -r Utils/Libraries/requirements.txt
    ```

---

## Usage

### Configure the Framework

Update the configuration file `Utils/Inputs/Common_inputs.py` with:

- `API_URL`: The TestLink API URL.
- `KEY`: Your TestLink API Key.
- `PROJECT_NAME`: Test project name in TestLink.
- `EXCEL_PATH`: Path to the Excel file containing the test case data.

### Run the Framework

1. Grant execute permissions to the shell script:
    ```bash
    chmod +x testlink_total.sh
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

3. **Connect to the Database Using the IP Address:**
    ```bash
    psql -h 172.21.0.2 -U tlink -d testlink-1.9.19
    ```

---

## Notes

- Ensure Docker containers for TestLink and its database are running before executing the framework.
- Verify the Excel file structure matches the required format as specified in the framework documentation.
