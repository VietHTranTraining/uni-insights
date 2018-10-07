import json
import os

# Get all files at directory
def get_all_files(data_dir):
    file_names = [os.path.join(data_dir, fl)
                  for fl in os.listdir(data_dir)
                  if os.path.isfile(os.path.join(data_dir, fl))]
    return file_names

# Get all directories at directory
def get_all_dirs(data_dir):
    dir_names = [os.path.join(data_dir, fl)
                  for fl in os.listdir(data_dir)
                  if os.path.isdir(os.path.join(data_dir, fl))]
    return dir_names 

# Write json object to file
def write_json(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=2)

# Read json from file
def read_json(file_name):
    data = None
    with open(file_name) as f:
        data = json.load(f)
    return data

def read_text_file(file_name):
    content = ''
    with open(file_name) as f:
        for line in f:
            content += line
    return content
