# From Jeremy Singer-Vine's Data Is Plural — 2021.05.12 edition:
# "TSA screenings. In its FOIA reading room, the US Transportation
# Security Administration publishes weekly PDF files that indicate
# the number of people passing through its checkpoints, broken down
# by hour and location. IT specialist Mike Lorengo has been converting
# these PDFs into structured data files.
# https://github.com/mikelor/TsaThroughput

# The format is currently 721 columns wide, and there are only three
# that have information specifically about the Pittsburgh airport.
# This script extracts just the data of interest.

import csv, requests

new_fieldname_by_old = {'Date': 'date',
    'Hour': 'hour',
    'PIT Main Checkpoint': 'main_checkpoint',
    'PIT Alternate Checkpoint': 'alternate_checkpoint',
    "PIT Int'l Checkpoint": 'international_checkpoint'}

def write_to_csv(filename, list_of_dicts, keys):
    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys, extrasaction='ignore', lineterminator='\n')
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dicts)

def standardize_fields(fields_to_get):
    new_fieldnames = []
    for f in fields_to_get:
        if f in new_fieldname_by_old:
            new_fieldnames.append(new_fieldname_by_old[f])
        else:
            new_fieldnames.append(f.lower())
    return new_fieldnames

def cast_to_int(x, fieldname, fieldnames_to_ignore):
    if fieldname not in fieldnames_to_ignore:
        if x not in ['']:
            return int(float(x))
    return x

fields_to_get = ['Date', 'Hour',
        'PIT Main Checkpoint',
        'PIT Alternate Checkpoint',
        "PIT Int'l Checkpoint"]

url = "https://github.com/mikelor/TsaThroughput/raw/main/data/processed/tsa/throughput/TsaThroughput.All.csv"

r = requests.get(url)
reader = csv.DictReader(r.text.split('\n'))

filtered = []
for row in reader:
    new_row = {new_fieldname_by_old[f]: cast_to_int(row[f], f, ['Date', 'Hour']) for f in fields_to_get}
    filtered.append(new_row)

write_to_csv('pit-tsa-screenings.csv', filtered, standardize_fields(fields_to_get))
