#!/bin/bash

# Define the output file
OUTPUT_FILE="results1/output.xml"

# Check if the output file exists
if [[ -f "$OUTPUT_FILE" ]]; then
    # Extract total and passed tests using rebot log
    totalTests=$(rebot --report none --log none --output none --loglevel TRACE $OUTPUT_FILE | grep 'Total' | awk '{print $2}')
    passedTests=$(rebot --report none --log none --output none --loglevel TRACE $OUTPUT_FILE | grep 'PASS' | awk '{print $2}')

    if [[ "$totalTests" =~ ^[0-9]+$ ]] && [[ "$passedTests" =~ ^[0-9]+$ ]]; then
        if [[ "$totalTests" -gt 0 ]]; then
            passPercentage=$(echo "scale=2; ($passedTests / $totalTests) * 100" | bc)
            echo "Pass Percentage: $passPercentage%"
        else
            echo "No tests were run."
        fi
    else
        echo "Failed to calculate pass percentage."
    fi
else
    echo "Output file $OUTPUT_FILE not found."
fi
