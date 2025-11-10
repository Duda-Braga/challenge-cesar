#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

cd "$SCRIPT_DIR"

# 1. Capture the current timestamp (Format: YYYY-MM-DD_HH-MM-SS)
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

# 2. Define the final output directory path
REPORT_DIR="reports/$TIMESTAMP"

# 3. Define the HTML report file path
HTML_FILE="$REPORT_DIR/html_report.html"

# 4. Define the raw Allure results directory path (kept static in the project root)
ALLURE_RAW_DIR="allure-results"

# --- Setup and Execution ---

# Create the timestamped output directory for this run
mkdir -p "$REPORT_DIR"

# Clean previous raw Allure data before starting a new run
rm -rf "$ALLURE_RAW_DIR"
echo "INFO: Cleaned previous raw Allure data from $ALLURE_RAW_DIR."

# Execute Pytest with reporting options
echo "INFO: Running Pytest and generating reports for $TIMESTAMP..."

# Pytest execution:
# --alluredir: Generates raw Allure data.
# --html: Generates the HTML report within the new directory.
pytest "$@" -v -s --alluredir="$ALLURE_RAW_DIR" --html="$HTML_FILE" --self-contained-html

# Check the exit status of Pytest
if [ $? -eq 0 ]; then
    echo "SUCCESS: Tests completed successfully."
    
    # --- Allure Report Generation ---
    
    echo "INFO: Generating Allure report to $REPORT_DIR/allure..."
    # Generate the final navigable Allure report and save it
    allure generate "$ALLURE_RAW_DIR" --clean --output "$REPORT_DIR/allure"

    # Option to automatically open the report
    # Uncomment the line below to open the report in the default browser:
    allure open "$REPORT_DIR/allure"
    
else
    echo "ERROR: Tests failed. Check logs and the HTML report at $HTML_FILE"
fi

# --- End of Script ---