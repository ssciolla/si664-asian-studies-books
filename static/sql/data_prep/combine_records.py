import json
import csv

import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

import import_functions

# Functions

def pull_isbns(record_dictionary):
    isbns = []
    for key in ["HC ISBN", "PB ISBN", "EB ISBN", "EB (OA) ISBN"]:
        value = record_dictionary[key]
        if value not in ["", "PB Only", "Paper Only", "N/A", "See rights column", "Not Available"]:
            isbns.append(value)
    return isbns


def remove_prefixes(title_string):
    title_without_prefix = title_string
    title_string_split = title_string.split()
    for prefix in ['The', "A", "An"]:
        if title_string_split[0] == prefix:
            title_without_prefix = " ".join(title_string_split[1:])
            return title_without_prefix
    return title_without_prefix

def replace_dashes_with_hyphen(given_string):
    bits_of_dashes = ['—', '–', '\u2013']
    string_cleaned = given_string
    for bit in bits_of_dashes:
        string_cleaned = string_cleaned.replace(bit, '-')
    return string_cleaned

# Importing new records file
new_data_file = open('input/neh_title_records.json', "r", encoding='utf-8')
new_data = json.loads(new_data_file.read())
new_data_file.close()
new_records = new_data["Title Records"]

# Importing old records file
old_data_file = open('input/neh_title_records_old.json', "r", encoding='utf-8')
old_data = json.loads(old_data_file.read())
old_data_file.close()
old_records = old_data["Title Records"]

# Setting timestamps
new_timestamp = new_data['Last Updated']
old_timestamp = old_data['Last Updated']

## Matching New and Old Records
print("\n*** CSV ***")

                                # '259': '', # Materials for the Study of Local History in Japan
manual_matches = {'262': '262', # Occasional Papers No. 3
                  '265': '265', # Production Materials from The Effects of the Atomic Bomb on Hiroshima and Nagasaki
                  '310': '310', # Compound Verb in Hindi
                  '312': '312', # Introduction to Old Javanese Language and Literature
                  '313': '313', # Reaction to World News Events and the Influence of Mass Media in an Indian Village
                  '314': '314'} # Change and the Persistence of Tradition in India

records_matched = {}
records_not_matched = {}
new_records_matched = []
for old_record_key in old_records.keys():
    old_record = old_records[old_record_key]
    old_isbns = pull_isbns(old_record)
    unique_identifier = old_record_key
    if old_record_key in manual_matches.keys():
        records_combined = {}
        new_record_key = manual_matches[old_record_key]
        new_record = new_records[new_record_key]
        records_combined[new_timestamp] = new_record
        records_combined[old_timestamp] = old_record
        records_matched[unique_identifier] = {}
        records_matched[unique_identifier]["CSV"] = records_combined
        new_records_matched.append(new_record_key)
    else:
        accum = 0
        for new_record_key in new_records.keys():
            accum += 1
            new_record = new_records[new_record_key]
            new_isbns = pull_isbns(new_record)
            if pull_isbns(new_record) == pull_isbns(old_record) and len(new_isbns) != 0:
                if new_record_key in new_records_matched:
                    print("New Record {} was already matched; second match found with {}".format(new_record_key, old_record_key))
                else:
                    records_combined = {}
                    records_combined[new_timestamp] = new_record
                    records_combined[old_timestamp] = old_record
                    records_matched[unique_identifier] = {}
                    records_matched[unique_identifier]["CSV"] = records_combined
                    new_records_matched.append(new_record_key)
                    break
            if accum == len(new_records.keys()):
                records_not_matched[old_record_key] = old_record
                print("No match found for {}: {}".format(old_record_key, import_functions.create_full_title(old_record)))

# Adding one new record
last_record_key = sorted(records_matched.keys())[-1]
brand_new_record = new_records["120"]
brand_new_record_key = str(int(last_record_key) + 1)
records_matched[brand_new_record_key] = {}
records_matched[brand_new_record_key]["CSV"] = {}
records_matched[brand_new_record_key]["CSV"][new_timestamp] = brand_new_record

print("Records matched: " + str(len(records_matched)))
print("Total new records: " + str(len(new_records)))
print("Total old records: " + str(len(old_records)))

### Matching New Descriptive Records
print("\n*** HTML ***")

# Opening descriptive records file
descript_metadata_file = open("input/descript_records.json", "r", encoding="utf-8")
new_descriptive_records = json.loads(descript_metadata_file.read())
descript_metadata_file.close()

# Opening descriptive matches file
descriptive_manual_matches_file = open("input/descriptive_matches.csv", "r", newline='', encoding="utf-8-sig")
csvreader = csv.reader(descriptive_manual_matches_file)
rows = []
for line in csvreader:
    rows.append(line)
descriptive_manual_matches_file.close()

descriptive_manual_matches = {}
for row in rows:
    descriptive_manual_matches[row[0]] = row[1]

# Incorporating new descriptive metadata with HTML tags

matched_record_indexes = []
descript_records_matched = 0

for descript_dict in new_descriptive_records[1:]: # Ignoring sample entry
    full_html_title = descript_dict["Title"]
    cleaned_html_title = import_functions.clean_html_title(full_html_title)
    cleaned_html_title = replace_dashes_with_hyphen(cleaned_html_title)
    if cleaned_html_title in descriptive_manual_matches.keys():
        record_index = descriptive_manual_matches[cleaned_html_title]
        # print(record_index)
        records_matched[record_index]["HTML"] = descript_dict
        descript_records_matched += 1
        matched_record_indexes.append(int(record_index))
        continue
    else:
        accum = 0
        for record_matched_key in records_matched.keys():
            accum += 1
            new_record = records_matched[record_matched_key]["CSV"][new_timestamp]
            new_record_title_for_comparison = replace_dashes_with_hyphen(import_functions.create_full_title(new_record))
            if (new_record_title_for_comparison == cleaned_html_title) or (new_record_title_for_comparison == remove_prefixes(cleaned_html_title)): # or
               # (new_record_title_for_comparison in cleaned_html_title and len(new_record_title_for_comparison.split()) >= len(cleaned_html_title.split()) - 2):
                if record_matched_key in matched_record_indexes and cleaned_html_title != "Studies in the Literature of the Great Vehicle: Three Mahayana Buddhist Texts":
                    print("** Record matched already!! **")
                    print(record_matched_key)
                    print(cleaned_html_title)
                else:
                    records_matched[record_matched_key]["HTML"] = descript_dict
                    matched_record_indexes.append(record_matched_key)
                    descript_records_matched += 1
                break
            if accum == len(records_matched.keys()):
                print("*** No match found: {} ***".format(cleaned_html_title))

print("Total descriptive records: " + str(len(new_descriptive_records[1:])))
print("Records matched: " + str(descript_records_matched))
print(sorted(matched_record_indexes, key=lambda x: int(x)))

# Storing data so far
combined_data_file = open("output/data_combined.json", "w", encoding="utf-8")
combined_data_file.write(json.dumps(records_matched, indent=4))
combined_data_file.close()
