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

from contextlib import ExitStack
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
        dir_path, category_file_path, subcat_file_path, catinfo_file_path,
        output_file_path, cat_count=500, pages_per_cat=30):
    path = dir_path
    if path[-1] is not "/":
        path += "/"

    page_cursor = 0     # The id of the current page.

    with ExitStack() as stack:
        cf = stack.enter_context(open(category_file_path))
        subcf = stack.enter_context(open(subcat_file_path))
        catinfo = stack.enter_context(open(catinfo_file_path))
        of = stack.enter_context(open(output_file_path + ".json", "w"))
        csvof = stack.enter_context(
            open(output_file_path + ".csv", "w", newline=""))

        cat_reader = csv.reader(cf)
        subcat_reader = csv.reader(subcf)
        catinfo_reader = csv.reader(catinfo)
        csv_writer = csv.writer(csvof)

        subcats = {}
        for subcat in subcat_reader:
            parent = subcat[1][1:-1]
            subcat_id = int(subcat[0])
            if subcat_id in subcats:
                subcats[subcat_id].append(parent)
            else:
                subcats[subcat_id] = [parent]
        print("SUBCATS " + str(len(subcats)))

        children = {}
        for info in catinfo_reader:
            if int(info[0]) in subcats:
                for parent in subcats[int(info[0])]:
                    if parent in children:
                        children[parent].append(info[1][1:-1])
                    else:
                        children[parent] = [info[1][1:-1]]
        print("PARENTS " + str(len(children)))
        for _ in range(3):
            for k, values in dict(children).items():
                is_sub = False
                for parent, v in dict(children).items():
                    if k in v:
                        is_sub = True
                        children[parent].extend(values)
                if is_sub and k in children:
                    del children[k]

            print("LENGTH: " + str(len(children)))

        # Build dict of category counts
        categories = {}
        for cat in cat_reader:
            if cat[1][1:5] == "Wiki" or ("_" in cat[1]):
                continue
            elif cat[1][1:-1] not in categories:
                categories[cat[1][1:-1]] = 1
            else:
                categories[cat[1][1:-1]] += 1

        for cat in dict(categories):
            if cat in children:
                for child in children[cat]:
                    print(child + " is a subcat of " + cat)
                    if child in categories:
                        categories[cat] += categories[child]

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

                            page_text = page["text"][:1000]
                            to_output = {
                                "title": page["title"],
                                "text": page_text,
                                "category": top_cat
                            }
                            of.write(json.dumps(to_output) + "\n")

                            page_text = page_text.replace("\n", " ")
                            page_text = page_text.replace("\t", " ")
                            csv_writer.writerow([page_text, top_cat])

                            cat_used_pages[top_cat] += 1

                        cat_cursor = next(cat_reader, None)


if __name__ == '__main__':
    cat_count = int(sys.argv[6]) if len(sys.argv) >= 6 else 500
    pages_per_cat = int(sys.argv[7]) if len(sys.argv) >= 7 else 30

    process_data(
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
        cat_count, pages_per_cat)
