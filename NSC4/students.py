import csv
import json

STUDENT_DATA_CSV = './students_data.csv'
STUDENT_DATA_COLS = ['Name','Roll Number','Aadhar','Subject 1','Subject 2','Subject 3','Subject 4','Subject 5']

# Read the CSV data to a dictionary
def read_csv_data(csv_file_path):
    data = []
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        # Create a CSV reader
        csv_reader = csv.DictReader(csv_file)
        for record in csv_reader:
            # Append each record to the data list
            data.append(record)
    return data

# Return the data for the student matching the input data, else return a blank dictionary
def get_student_data(name, rollNum, aadharLast4Digits):
    dataDict = read_csv_data(STUDENT_DATA_CSV)
    for record in dataDict:
        if record['Name']==name and record['Roll Number']==rollNum and record['Aadhar']==aadharLast4Digits:
            return record
    return {}

if __name__ == '__main__':
    name = input("Enter the name of the student: ")
    rollNum = input("Enter the roll number: ")
    aadharLast4Digits = input("Enter the last 4 digits of the Aadhar number: ")
    print(get_student_data(name, rollNum, aadharLast4Digits))
