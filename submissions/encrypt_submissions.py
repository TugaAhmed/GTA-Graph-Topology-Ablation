import os
from encryption.encrypt import encrypt_file

SUBMISSION_DIR = os.path.dirname(os.path.abspath(__file__))

csv_files = [
    f for f in os.listdir(SUBMISSION_DIR)
    if f.endswith(".csv") and f != "sample_submission.csv"
]

for csv_file in csv_files:
    input_path = os.path.join(SUBMISSION_DIR, csv_file)
    encrypt_file(input_path)
