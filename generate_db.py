from __future__ import print_function
import sqlite3
import sys

"""
This program generates the database used for this project:

Directory Structure:
-- generate_db.py
|
-- tagged_data/
   |
   -- 1.txt
   -- 2.txt
   -- ...

Make sure the files in tagged_data/ are correctly tagged and formatted.
Make sure that no file called final_proj.db currently exists!
"""


def main(args):
    test = args.get("test", "False")
    suppress_warnings = args.get("suppress", "False")

    conn = sqlite3.connect('final_proj.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE words (word text, pos text, stress text, pron text, syllables real)''')

    for poem in range(1, 2500):
        try:
            with open("tagged_data/" + str(poem), "r") as f:
                for line in f:
                    split_line = line.split('\t')
                    if len(split_line) == 5:
                        token = str(split_line[0])
                        pos = str(split_line[1])
                        syllables = int(split_line[2])
                        stress_pattern = str(split_line[3][0])
                        full_pron = split_line[4].strip().split(" ")
                        pron = str(" ".join(full_pron[-3:]))
                        c.execute("INSERT INTO words VALUES (?,?,?,?,?)", (token, pos, stress_pattern, pron, syllables))
                        conn.commit()
        except IOError:
            if suppress_warnings == "False":
                print("Warning: Poem", poem, "not found")

    if test == "True":
        # Run a test query to make sure the database has actually been created
        for row in c.execute('SELECT * FROM words ORDER BY syllables'):
            print(row)

    conn.close()

if __name__ == "__main__":
    arg_dict = {}
    for arg in sys.argv:
        split_arg = arg.split("=")
        if len(split_arg) > 1:
            arg_dict[arg.split("=")[0]] = arg.split("=")[1]
    main(arg_dict)
