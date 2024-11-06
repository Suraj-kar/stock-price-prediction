# data_reader.py
import csv

def read_csv(filename):
    """Read a CSV file and return the header and data."""
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        data = [row for row in reader]  # Read the data into a list
    return header, data
