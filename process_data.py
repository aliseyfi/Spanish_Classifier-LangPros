"""
Pairs Wikipedia page text and categories.

Call from command line:
    python process_data.py data_dir_path category_file_path output_file_path

data_dir_path: The folder that contains the data (in subfolders) exported by
wikiextractor (https://github.com/attardi/wikiextractor) from a wiki page dump.

category_file_path: The csv file with category data created by the included
wiki_cat_sql_dump_to_csv.py script from a dump of category link data.

output_file_path: Where you want the output file.

"""

import csv
import json
import os
import sys


def process_file(file_path):
    result = []

    with open(file_path) as f:
        for line in f:
            page = json.loads(line)
            result.append(page)

    return result


def process_data(dir_path, category_file_path, output_file_path):
    path = dir_path
    if path[-1] is not "/":
        path += "/"

    page_cursor = 0

    with open(category_file_path) as cf, open(output_file_path, "w") as of:
        cat_reader = csv.reader(cf)
        cat_cursor = next(cat_reader)
        for root, dirs, files in os.walk(path):
            for fn in sorted(files, key=lambda fn: int(fn[5:])):
                pages = process_file(root + "/" + fn)
                for page in pages:
                    if int(page["id"]) < page_cursor:
                        raise ValueError("Page ID not in order.")
                    else:
                        page_cursor = int(page["id"])
                        while cat_cursor is not None:
                            if int(cat_cursor[0]) > page_cursor:
                                break

                            if int(cat_cursor[0]) < page_cursor:
                                cat_cursor = next(cat_reader, None)
                                continue

                            if cat_cursor[1][1:5] != "Wiki":
                                to_output = {
                                    "title": page["title"],
                                    "text": page["text"],
                                    "category": cat_cursor[1][1:-1]
                                }
                                of.write(json.dumps(to_output) + "\n")

                            cat_cursor = next(cat_reader, None)


if __name__ == '__main__':
    process_data(sys.argv[1], sys.argv[2], sys.argv[3])
