from __future__ import print_function
import sys
import nltk
import string

"""
This program tags the corpora used for this project:

Directory Structure:
-- tag_data.py
|
-- tagged_data/ (empty)
|
-- data/
   |
   -- 1
   -- 2
   -- ...

Make sure the files in data/ are the poems and are numbered numerically.
Note that this program reads only files numbered 1 to 2500
"""


def word_tokenize(data):
    """
    Given a string, split the string into words and add special tags
    :param data: poem in form of a string
    :type data: String
    :return: poem converted into a list
    :rtype: List
    """
    ret = []
    strip_data = data.strip().split("\n")
    for line in strip_data:
        strip_line = line.strip()
        if strip_line == "":
            ret.append("EOS")
        else:
            if strip_line[0] == "_" and strip_line[-1] == "_" or strip_line.isupper():
                continue
            else:
                for element in strip_line.split(" "):
                    if element != "":
                        ret.append(element)
                ret.append("EOL")
    ret.append("EOP")
    return ret


def main(args):
    """
    Goes through a corpora of poems and tags them
    :return: nothing
    :rtype: None
    """
    cmu_dict = nltk.corpus.cmudict.dict()
    suppress_warnings = args.get("suppress", "False")

    for poem in range(1, 2500):
        try:
            with open("data/" + str(poem), "r") as f:
                """
                For each word, we tag its:
                part-of-speech
                number of syllables
                stress-pattern
                pronunciation
                """
                data = f.read()
                text = word_tokenize(data)
                tagged_text = nltk.pos_tag(text)
                with open("tagged_data/" + str(poem), "w") as o:
                    for item in tagged_text:
                        if item[0] not in ["EOL", "EOS", "EOP"]:
                            normalized = item[0].translate(None, string.punctuation).lower()
                            pron = cmu_dict.get(normalized, [])
                            if pron:
                                num_syllable = 0
                                stress_pattern = ""
                                for phon in pron[0]:
                                    if phon[-1].isdigit():
                                        num_syllable += 1
                                        stress_pattern += phon[-1]
                                o.write("\t".join([normalized, item[1], str(num_syllable), stress_pattern,
                                                   " ".join(pron[0])]) + "\n")
                            else:
                                o.write("\t".join([normalized, item[1]]) + "\n")
                        else:
                            o.write("\t".join([item[0], item[0]]) + "\n")
        except IOError:
            if suppress_warnings != "True":
                print("Warning: Poem", poem, "not found.")


if __name__ == "__main__":
    arg_dict = {}
    for arg in sys.argv:
        split_arg = arg.split("=")
        if len(split_arg) > 1:
            arg_dict[arg.split("=")[0]] = arg.split("=")[1]
    main(arg_dict)
