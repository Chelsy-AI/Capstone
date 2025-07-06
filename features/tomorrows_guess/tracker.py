import csv
from datetime import datetime

CSV_FILE = "data/tomorrow_guess_accuracy.csv"

def save_accuracy(date_str, predicted, actual):
    """
    Saves a prediction record to CSV file for tracking accuracy over time.
    Takes the date, what we predicted, and what actually happened.

    """
    
    header = ["date", "predicted_temp", "actual_temp", "error"]
    
    # Calculate how far off our prediction was (prediction error)
    error = abs(predicted - actual) if (predicted is not None and actual is not None) else None

    try:
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            
            if f.tell() == 0:
                writer.writerow(header)
                
            writer.writerow([date_str, predicted, actual, error])
            
    except Exception as e:
        pass
    
def read_accuracy():
    """
    Reads all previous prediction records from the CSV file.
    Returns a list of dictionaries, each containing one prediction record.

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