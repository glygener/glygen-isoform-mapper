import csv
import json


def write_log(log_file, msg, mode):    
    with open(log_file, mode) as FW:
        FW.write("%s\n" % (msg))
    
    return


def load_sheet(sheet_obj, in_file, separator):

    seen = {}
    sheet_obj["fields"] = []
    sheet_obj["data"] = []
    with open(in_file, 'r') as FR:
        csv_grid = csv.reader(FR, delimiter=separator, quotechar='"')
        row_count = 0
        for row in csv_grid:
            if json.dumps(row) in seen:
                continue
            seen[json.dumps(row)] = True
            row_count += 1
            if row_count == 1:
                for j in range(0, len(row)):
                    sheet_obj["fields"].append(row[j].strip().replace("\"", ""))
            else:
                new_row = []
                for j in range(0, len(row)):
                    new_row.append(row[j].strip())
                sheet_obj["data"].append(new_row)
    return


