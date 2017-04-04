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


def process_data(
        dir_path, category_file_path, output_file_path,
        cat_count=500, pages_per_cat=30):
    path = dir_path
    if path[-1] is not "/":
        path += "/"

    page_cursor = 0     # The id of the current page.

    with open(category_file_path) as cf, open(output_file_path, "w") as of:
        cat_reader = csv.reader(cf)

        # Build dict of category counts
        categories = {}
        for cat in cat_reader:
            if cat[1][1:5] == "Wiki":
                continue
            elif cat[1][1:-1] not in categories:
                categories[cat[1][1:-1]] = 1
            else:
                categories[cat[1][1:-1]] += 1

        cats = [k for k, v in sorted(
            categories.items(), key=lambda x: x[1], reverse=True)]
        cats = cats[:cat_count]

        cat_used_pages = {}
        for cat in cats:
            cat_used_pages[cat] = 0

        cf.seek(0)
        cat_cursor = next(cat_reader)   # Current category, page id pair

        # For each file (including those in subfolders)
        for root, dirs, files in os.walk(path):
            # Go through all files in each subfolder in numerical order
            for fn in sorted(files, key=lambda fn: int(fn[5:])):
                if cat_cursor is None:
                    break
                pages = process_file(root + "/" + fn)
                for page in pages:
                    if cat_cursor is None:
                        break

                    if int(page["id"]) < page_cursor:
                        raise ValueError("Page ID not in order.")
                    else:
                        page_cursor = int(page["id"])

                        # Page in category/page pair missing
                        while int(cat_cursor[0]) < page_cursor:
                            cat_cursor = next(cat_reader, None)

                            if int(cat_cursor[0]) > page_cursor:
                                break

                        # Current page has no categories, move on.
                        if int(cat_cursor[0]) > page_cursor:
                            continue

                        page_cats = []
                        while int(cat_cursor[0]) == page_cursor:
                            page_cats.append(cat_cursor[1][1:-1])
                            cat_cursor = next(cat_reader, None)

                        # Take most popular category from page
                        if len(page_cats) is 0:
                            continue
                        top_cat = None
                        for cat in page_cats:
                            if cat not in cats:
                                continue
                            elif top_cat is None:
                                top_cat = cat
                            else:
                                if cats.index(cat) < cats.index(top_cat):
                                    top_cat = cat

                        if (top_cat is not None and
                                cat_used_pages[top_cat] < pages_per_cat):

                            to_output = {
                                "title": page["title"],
                                "text": page["text"][:1100],
                                "category": top_cat
                            }
                            of.write(json.dumps(to_output) + "\n")
                            cat_used_pages[top_cat] += 1

                        cat_cursor = next(cat_reader, None)


if __name__ == '__main__':
    process_data(sys.argv[1], sys.argv[2], sys.argv[3])
