# features/tomorrows_guess/tracker.py

import csv
from datetime import datetime

CSV_FILE = "data/tomorrow_guess_accuracy.csv"

def save_accuracy(date_str, predicted, actual):
    """
    Save the prediction and actual temperature for a date to CSV.
    """
    header = ["date", "predicted_temp", "actual_temp", "error"]
    error = abs(predicted - actual) if (predicted is not None and actual is not None) else None

    try:
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            # Write header if file is new
            if f.tell() == 0:
                writer.writerow(header)
            writer.writerow([date_str, predicted, actual, error])
    except Exception as e:
        pass
    
def read_accuracy():
    """
    Read past accuracy records.
    Returns list of dicts or empty list.
    """
    records = []
    try:
        with open(CSV_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
    except FileNotFoundError:
        pass
    return records
