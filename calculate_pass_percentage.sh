# Change to the results directory
cd results || { echo "Failed to navigate to 'results' directory. Exiting."; exit 1; }

#!/bin/bash

# Path to the Robot Framework output XML file
OUTPUT_XML="output.xml"

# Đếm tổng số testcase
TOTAL_TCS=$(xmllint --xpath "count(//test)" "$OUTPUT_XML")

# Đếm số testcase thành công
PASSED_TCS=$(xmllint --xpath "count(//test/status[@status='PASS'])" "$OUTPUT_XML")

# Calculate pass percentage
if [[ "$TOTAL_TCS" =~ ^[0-9]+$ && "$PASSED_TCS" =~ ^[0-9]+$ ]]; then
    passPercentage=$(echo "scale=2; ($PASSED_TCS / $TOTAL_TCS) * 100" | bc)
    echo ${passPercentage}
else
    echo "Failed to calculate pass percentage."
    exit 1
fi