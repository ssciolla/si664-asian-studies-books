import csv
import json

import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

import import_functions

#
## Functions
#

def remove_puncs(given_string):
    new_string = given_string.replace(",", "").replace(";", "")
    if "." in new_string:
        new_string_split = new_string.split()
        new_words = []
        for word in new_string_split:
            if word[-1] == "." and len(word) > 2:
                new_words.append(word.replace(".", ""))
            else:
                new_words.append(word)
        new_string = " ".join(new_words)
    return new_string

def make_creator_lists(record):
    new_record_key = sorted(record['CSV'].keys())[0]
    new_record = record['CSV'][new_record_key]
    display_name = new_record["Author Display Name"]
    list_of_creators = []
    creator_fields = ['Last', 'First']
    for i in range(1,3):
        last_name = new_record["Author {} - {}".format(str(i), 'Last')].strip()
        first_name = new_record["Author {} - {}".format(str(i), 'First')].strip()
        if last_name != "" and first_name != "":
            if last_name in display_name:
                display_name_split = remove_puncs(display_name).split()
                first_index = display_name_split.index(first_name.split()[0])
                last_index = display_name_split.index(last_name)
                if first_index < last_index:
                    creator_display_name = " ".join(display_name_split[first_index:last_index + 1])
                else:
                    creator_display_name = " ".join(display_name_split[last_index:first_index + 1])
            else:
                creator_display_name = first_name + " " + last_name
            creator_list = [last_name, first_name, creator_display_name]
            list_of_creators.append(creator_list)
    return list_of_creators

def make_book_list(csv_record, html_record=None):
    csv_record = record["CSV"][new_timestamp]
    if html_record != None:
        descriptive_record = record["HTML"]
        full_title = import_functions.clean_html_title(descriptive_record["Title"])
        full_title_separated = full_title.split(": ")
        if ":" in full_title:
            subtitle = full_title_separated[1].strip()
        else:
            subtitle = ""
        title_split = full_title_separated[0].split()
        first_word = title_split[0]
        if first_word in ["The", "A", "An"]:
            prefix = first_word.strip()
            title = " ".join(title_split[1:]).strip()
        else:
            prefix = ""
            title = full_title_separated[0].strip()
        if "Keynote" in descriptive_record.keys():
            key_note = import_functions.remove_tags(descriptive_record["Keynote"], italics=True).strip()
        else:
            key_note = csv_record["Key Note"].strip()
        description = import_functions.remove_tags(descriptive_record["Book Description"], italics=True).strip()
    else:
        title = csv_record["Title"].strip()
        subtitle = csv_record["Subtitle"].strip()
        prefix = csv_record["Prefix"].strip()
        full_title = import_functions.create_full_title(csv_record).strip()
        key_note = csv_record["Key Note"].strip()
        description = csv_record["Book Description"].strip()
    pages = csv_record["Pages"].replace(',','').strip()
    publisher = csv_record["Imprint"].strip()
    series = csv_record["Series"].strip()
    if csv_record["Volume (# or N/A)"] == "N/A":
        volume = ""
    else:
        volume = csv_record["Volume (# or N/A)"].strip()
    book_list = [title, prefix, subtitle, full_title, key_note, description, pages, volume, publisher, series]
    return book_list

#
## Initializing variables
#

data_combined_file = open("output/data_combined.json", "r", encoding="utf-8")
combined_records = json.loads(data_combined_file.read())
data_combined_file.close()

new_timestamp = sorted(combined_records["1"]["CSV"].keys())[0]

worldcat_stats_file = open("input/worldcat_stats.json", "r", encoding="utf-8")
worldcat_stats = json.loads(worldcat_stats_file.read())
worldcat_stats_file.close()

#
## Preparing data for database tables
#

## publisher
print('\n')
print("/// Publisher ///")

unique_imprints = []
for combined_record_key in combined_records.keys():
    record = combined_records[combined_record_key]
    new_record_key = sorted(record['CSV'].keys())[0]
    new_record = record['CSV'][new_record_key]
    imprint = new_record["Imprint"]
    if imprint not in unique_imprints:
        unique_imprints.append(imprint)

# for unique_imprint in unique_imprints:
#     print(unique_imprint)

## series

print("\n")
print("/// Series ///")
unique_series = []
for combined_record_key in combined_records.keys():
    record = combined_records[combined_record_key]
    new_record_key = sorted(record['CSV'].keys())[0]
    new_record = record['CSV'][new_record_key]
    series = new_record["Series"]
    if series not in unique_series and series != "":
        unique_series.append(series)

# unique_series = sorted(unique_series)
# for unique_series in unique_series:
#     print(unique_series)

## role
print("\n")
print("/// Role ///")

unique_roles = []
for combined_record_key in combined_records.keys():
    record = combined_records[combined_record_key]
    new_record_key = sorted(record['CSV'].keys())[0]
    new_record = record['CSV'][new_record_key]
    creator_role_fields = ['Author 1 - Role', 'Author 2 - Role', 'Author 3 - Role']
    for creator_field in creator_role_fields:
        role = new_record[creator_field]
        if role not in unique_roles and role != '':
            unique_roles.append(role)

# unique_roles = sorted(unique_roles)
# for unique_role in unique_roles:
#     print(unique_role)

## creator
print('\n')
print("/// Creator ///")

unique_creators = {}
for combined_record_key in combined_records.keys():
    record = combined_records[combined_record_key]
    new_creators = make_creator_lists(record)
    for new_creator in new_creators:
        full_name = new_creator[0] + ", " + new_creator[1]
        if full_name not in unique_creators:
            unique_creators[full_name] = new_creator

unique_creator_keys_sorted = sorted(unique_creators.keys())

# Creating a CSV
creators_csv_file = open("output/csvs/creators.csv", "w", newline='', encoding='utf-8')
csvwriter = csv.writer(creators_csv_file)
headers = ['last_name', 'first_name', 'display_name']
csvwriter.writerow(headers)
for key in unique_creator_keys_sorted:
    creator_row = unique_creators[key]
    csvwriter.writerow(creator_row)
creators_csv_file.close()

## book
print('\n')
print("/// Book ///")

book_lists = []
for combined_record_key in combined_records.keys():
    record = combined_records[combined_record_key]
    if "HTML" in record.keys():
        book_lists.append(make_book_list(record["CSV"][new_timestamp], record["HTML"]))
    else:
        book_lists.append(make_book_list(record["CSV"][new_timestamp]))
print(len(book_lists))

# Creating a CSV
books_csv_file = open("output/csvs/books.csv", "w", newline='', encoding='utf-8')
csvwriter = csv.writer(books_csv_file)
headers = ['title', 'prefix', 'subtitle', 'full_title', 'key_note', 'description', 'pages', 'volume', 'publisher', 'series']
csvwriter.writerow(headers)
for book_list in book_lists:
    csvwriter.writerow(book_list)
books_csv_file.close()

# versions
print('\n')
print("/// Version ///")

version_lists = []
for combined_record_key in combined_records.keys():
    record = combined_records[combined_record_key]
    new_csv_record = record["CSV"][new_timestamp]
    if "HTML" in record.keys():
        full_title = import_functions.clean_html_title(record["HTML"]["Title"])
    else:
        full_title = import_functions.create_full_title(new_csv_record)
    format_codes = ["HC", "PB", "EB", "EB (OA)"]
    for format_code in format_codes:
        year_published = new_csv_record[format_code + " Pub Year"].strip()
        isbn13 = new_csv_record[format_code + " ISBN"].strip()
        bisac_status = new_csv_record[format_code + " BISAC"].strip()
        if year_published != "" or bisac_status not in ["", "N/A"] or isbn13 not in ["", "PB Only", "Paper Only", "Not available", "See rights column"]:
            if isbn13 in ["", "See rights column", "Not available", "Not Available", "N/A"]:
                isbn13 = ""
            version_list = [full_title, format_code, isbn13, year_published, bisac_status]
            version_lists.append(version_list)

# Creating a CSV
versions_csv_file = open("output/csvs/versions.csv", "w", newline='', encoding='utf-8')
csvwriter = csv.writer(versions_csv_file)
headers = ['full_title', 'format_code', 'isbn13', 'year_published', 'bisac_status']
csvwriter.writerow(headers)
for version_list in version_lists:
    csvwriter.writerow(version_list)
versions_csv_file.close()

# countries
print('\n')
print("/// Countries ///")
unique_countries = []
for worldcat_key in worldcat_stats.keys():
    worldcat_record = worldcat_stats[worldcat_key]
    if "Complete Library Data" in worldcat_record.keys():
        holding_institutions = worldcat_record["Complete Library Data"]
        for holding_institution in holding_institutions:
            if holding_institution["country"] not in unique_countries and holding_institution["country"].strip() != "":
                unique_countries.append(holding_institution["country"])
unique_countries = sorted(unique_countries) + ["Unknown"]

# Creating CSV
countries_file = open('output/csvs/countries.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(countries_file)
header = "country_name"
csv_writer.writerow([header])
for unique_country in unique_countries:
    csv_writer.writerow([unique_country])
countries_file.close()

# institutions
print('\n')
print("/// Institution ///")

unique_institutions = {}
for worldcat_key in worldcat_stats.keys():
    worldcat_record = worldcat_stats[worldcat_key]
    if "Complete Library Data" in worldcat_record.keys():
        holding_institutions = worldcat_record["Complete Library Data"]
        for holding_institution in holding_institutions:
            if holding_institution["oclcSymbol"] not in unique_institutions:
                institution_name = holding_institution["institutionName"]
                oclc_symbol = holding_institution["oclcSymbol"]
                street_address = holding_institution["streetAddress1"]
                for key in ['streetAddress2', 'city', 'state']:
                    if holding_institution[key].strip() != "":
                        street_address += ", " + holding_institution[key].strip()
                if holding_institution["postalCode"].strip() != "":
                    street_address == " " + holding_institution["postalCode"].strip()
                country_name = holding_institution["country"].strip()
                if country_name == "":
                    country_name = "Unknown"
                opac_url = holding_institution["opacUrl"]
                institution_list = [institution_name, oclc_symbol, street_address, country_name, opac_url]
                unique_institutions[oclc_symbol] = institution_list

# Creating CSV
institutions_file = open("output/csvs/institutions.csv", "w", newline='', encoding="utf-8")
csvwriter = csv.writer(institutions_file)
headers = ['institution_name', 'oclc_symbol', 'street_address', 'country_name', 'opac_url']
csvwriter.writerow(headers)
institution_codes_sorted = sorted(unique_institutions.keys())
for institution_code in institution_codes_sorted:
    csvwriter.writerow(unique_institutions[institution_code])
institutions_file.close()

# Attribution
print('\n')
print("/// Attribution ///")

attribution_lists = []
for combined_record_key in combined_records.keys():
    record = combined_records[combined_record_key]
    new_csv_record = record["CSV"][new_timestamp]
    if "HTML" in record.keys():
        full_title = import_functions.clean_html_title(record["HTML"]["Title"])
    else:
        full_title = import_functions.create_full_title(new_csv_record)
    creator_fields = ['Last', 'First']
    for i in range(1,3):
        last_name = new_csv_record["Author {} - {}".format(str(i), 'Last')].strip()
        first_name = new_csv_record["Author {} - {}".format(str(i), 'First')].strip()
        role = new_csv_record["Author {} - {}".format(str(i), 'Role')].strip()
        if last_name != "" and first_name != "":
            attribution_list = [full_title, last_name, first_name, role]
            attribution_lists.append(attribution_list)

# Creating CSV
attributions_file = open("output/csvs/attributions.csv", "w", newline='', encoding="utf-8")
csvwriter = csv.writer(attributions_file)
headers = ['full_title', 'last_name', 'first_name', 'role']
csvwriter.writerow(headers)
for attribution_list in attribution_lists:
    csvwriter.writerow(attribution_list)
attributions_file.close()

# holding
print('\n')
print("/// Holding ///")

holding_lists = []
for worldcat_key in worldcat_stats.keys():
    if worldcat_key not in ['259', '365']:
        worldcat_record = worldcat_stats[worldcat_key]
        associated_combined_record = combined_records[worldcat_key]
        # try:
        #     print(worldcat_record["Response Metadata"][sorted(worldcat_record["Response Metadata"].keys())[0]]["Title"])
        # except:
        #      print("No query made")
        if "HTML" in associated_combined_record.keys():
            full_title = import_functions.clean_html_title(associated_combined_record["HTML"]["Title"])
        else:
            full_title = import_functions.create_full_title(associated_combined_record["CSV"][new_timestamp])
        if "Complete Library Data" in worldcat_record.keys():
            holding_institutions = worldcat_record["Complete Library Data"]
            for holding_institution in holding_institutions:
                holding_list = [full_title, holding_institution["oclcSymbol"]]
                holding_lists.append(holding_list)

# Creating CSV
holdings_file = open("output/csvs/holdings.csv", "w", newline='', encoding="utf-8")
csvwriter = csv.writer(holdings_file)
headers = ['full_title', 'oclc_symbol']
csvwriter.writerow(headers)
for holding_list in holding_lists:
    csvwriter.writerow(holding_list)
holdings_file.close()
