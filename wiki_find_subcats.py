import re
import sys

with open(sys.argv[1]) as sql_f, open(sys.argv[2], 'w') as output_f:

    for l in sql_f:
        cat_links = re.findall(r"\(\d+,'[^']+',[^)]+'subcat'\)", l)
        cat_links = re.findall(r"\(\d+,'[^']+',", " ".join(cat_links))

        for cat_link in cat_links:
            # Example cat_link: "(110655,'Premios_Nobel_de_Estados_Unidos',"
            output_f.write(cat_link[1:-1] + "\n")
