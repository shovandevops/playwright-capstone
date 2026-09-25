import json
import os

def load_json_data(filename):
    file_path = os.path.join('testdata', filename)    
    with open(file_path, 'r') as file:
        return json.load(file)

