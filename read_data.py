from __future__ import print_function

"""
Note:
You most likely will not use this file,
this file contains a helper function used to convert a collection of poems
into several separate files, each containing exactly one poem
"""

f = open("data/pg12759.txt", "r")

poem_number = 2500

is_part_of_poem = False
poem_text = ""
for line in f:
    if line.strip() != "" and line.strip().isupper():
        is_part_of_poem = False
        o = open(str(poem_number), "w")
        o.write(poem_text)
        poem_text = ""
        poem_number += 1
        continue
    poem_text += line
