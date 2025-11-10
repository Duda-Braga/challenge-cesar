# Automation Project — API, Web, and Mobile

This project brings together three automation fronts:

- **API** — Testing via `pytest` and `.sh` scripts
- **Web** — Testing with **Selenium**

- **Mobile** — Testing with **Appium**

---

## Installation and Requirements

1. **Clone the repository:**

   ```bash
   git clone https://github.com/seuusuario/nome-do-repo.git
   cd nome-do-repo


cd repository-name

2. **Create and activate the virtual environment:**
   ```bash
    python -m venv myproject
    source myproject/bin/activate

3. **Install Dependencies:**

Make sure you have Python installed. Next, install the necessary dependencies listed in your `requirements.txt` file:

    
    
    pip install -r requirements.txt
    

4. **Run the Tests (Pytest)**

To run the tests, use the `pytest` command specifying the path to the desired test directory.

| Flow  |  Pytest |
| :---  | :--- |
| **Web** | `pytest web-flow/tests` |
| **Mobile**  | `pytest mobile-flow/tests` |
| **API**  | `pytest api-test/tests` |

NOTE: Remember to run Appium for the mobile test and the API being tested.

### API test script

The API test has an automated script to run the tests:

    
    chmod +x api-test/run_tests.sh
    ./api-test/run_tests.sh

### Generate Allure report
```bash
pytest web-flow/tests --alluredir=reports/web
allure generate reports/web --clean
allure open
