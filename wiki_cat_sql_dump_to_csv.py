import re
import sys

with open(sys.argv[1]) as sql_f, open(sys.argv[2], 'w') as output_f:
    past_header_info = False

    for l in sql_f:
        cat_links = re.findall(r"\(\d+,'[^']+',", l)

        for cat_link in cat_links:
            # Example cat_link: "(110655,'Premios_Nobel_de_Estados_Unidos',"
            output_f.write(cat_link[1:-1] + "\n")
