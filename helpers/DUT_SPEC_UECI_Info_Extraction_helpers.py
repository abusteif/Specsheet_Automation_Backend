import csv
from itertools import zip_longest

def get_data_from_csv(csv_file_path):
    columns = []
    with open(csv_file_path, "r") as csv_file:
        reader = csv.reader(csv_file, delimiter="\t")
        for r in reader:
            columns.append(r[0].split(","))
        return [list(element) for element in zip_longest(*columns, fillvalue='')]

def insert_into_table(column_num, row_num, all_columns, value):

    for i in range(all_columns[column_num].__len__(), row_num):
        all_columns[column_num].append('')
    all_columns[column_num].append(value)


def get_list_items(ie, result):
    for e_num, e in enumerate(ie):
        if "Item" in e:
            result.append((ie[:e_num], e))
            get_list_items(ie[:e_num] + ie[e_num + 1:], result)
            return
    result.append((ie[:-1], ie[-1]))

def write_data_to_csv_file(columns, csv_file):
    csv_data_out = zip_longest(*columns, fillvalue='')
    with open(csv_file, 'w', newline='') as target_csv_file:
        wr = csv.writer(target_csv_file)
        wr.writerows(csv_data_out)

def extract_number_from_item(item):
    if "Item" in item:
        return item.split("Item ")[1]
    return item
