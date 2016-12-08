from __future__ import print_function
import random
import sqlite3
import sys

"""
Note: In order to run this file,
you must have a sqlite3 db named final_proj.db (obtained by running the generate_db.py file)
in your working directory that contains all possible words that can be used in your poem
"""

conn = sqlite3.connect('final_proj.db')
c = conn.cursor()


def convert_grammar(grammar):
    """
    Converts grammar into a dictionary structure
    :param grammar: string form of grammar
    :type grammar: String
    :return: dictionary form of grammar
    :rtype: Dictionary
    """
    grammar = grammar.strip()
    grammar = grammar.split("\n")
    split_grammar = []
    for i in range(len(grammar)):
        split_grammar.append(grammar[i].strip().split(" -> "))
    new_grammar = {}
    for e in split_grammar:
        if e[0] in new_grammar.keys():
            new_grammar[e[0]].append(e[1].split(" "))
        else:
            new_grammar[e[0]] = [e[1].split(" ")]
    return new_grammar


def generate_random_pos(initial_stack, grammar):
    """
    Randomly generates a sequence of terminal nodes given an initial stack and a CFG
    :param initial_stack: list containing elements that form the initial stack
    :type initial_stack: List
    :param grammar: dictionary representation of a CFG
    :type grammar: Dictionary
    :return: list of terminal nodes
    :rtype: List
    """
    if type(initial_stack) is str:
        stack = [initial_stack]
    else:
        stack = initial_stack
    sentence = []
    while stack:
        last = stack.pop()
        if last in grammar.keys():
            stack.extend(grammar[last][random.randint(0, len(grammar[last])-1)])
        else:
            sentence.append(last)
    sentence.reverse()
    return sentence


def get_random_word(pos, stress, rhyme, syllables):
    """
    Retrieves a random word from a database
    :param pos: part of speech
    :type pos: String
    :param stress: stress pattern (either 0 - unstressed, 1 - primary stress, 2 - secondary stress)
    :type stress: String
    :param rhyme: pronunciation of the word
    :type rhyme: String
    :param syllables: number of syllables
    :type syllables: Integer
    :return: a word fitting the specified criteria
    :rtype: String
    """
    s = '%'
    if stress:
        s = stress
    r = '%'
    if rhyme:
        r = rhyme
    sy = '%'
    if syllables:
        sy = syllables
    c.execute("SELECT * FROM words WHERE pos LIKE ? AND stress LIKE ? AND pron LIKE ? AND syllables LIKE ?",
              (pos, s, r, sy))
    data = c.fetchall()
    if len(data) == 0:
        return False
    else:
        return data[random.randint(0, len(data) - 1)]


def generate_word_from_pos(pos_sentence, rhyme_scheme):
    """
    Given a sequence of terminal nodes (pos tags), converts them to a sequence of words
    :param pos_sentence: list containing part-of-speech tags
    :type pos_sentence: List
    :param rhyme_scheme: rhyme scheme of the poem e.g. "ABAB", "AABB", etc.
    :type rhyme_scheme: String
    :return: list of words
    :rtype: List
    """
    rhyme_dict = {}
    for char in rhyme_scheme:
        if char not in rhyme_dict:
            rhyme_dict[char] = ""
    split_by_line = " ".join(pos_sentence).split(" EOL ")
    word_sentence = []
    for i in range(len(split_by_line)):
        new_line = []
        split_by_pos = split_by_line[i].split(" ")
        prev_stress = ""
        for j in range(len(split_by_pos)):
            pos = split_by_pos[j]
            if pos == "EOS" or pos == "EOP":
                continue
            elif j == 0:
                word_entry = get_random_word(pos, False, False, False)
            else:
                if prev_stress == "1" or prev_stress == "2":
                    if j == len(split_by_pos) - 1:
                        if rhyme_dict[rhyme_scheme[i]] == "":
                            word_entry = get_random_word(pos, "0", False, False)
                            if word_entry:
                                rhyme_dict[rhyme_scheme[i]] = " ".join(word_entry[3].split(" ")[-3:])
                        else:
                            word_entry = get_random_word(pos, "0", rhyme_dict[rhyme_scheme[i]], False)
                    else:
                        word_entry = get_random_word(pos, "0", False, False)
                else:
                    choice = str(random.randint(1, 2))
                    if j == len(split_by_pos) - 1:
                        if rhyme_dict[rhyme_scheme[i]] == "":
                            word_entry = get_random_word(pos, choice, False, False)
                            if word_entry:
                                rhyme_dict[rhyme_scheme[i]] = " ".join(word_entry[3].split(" ")[-3:])
                        else:
                            word_entry = get_random_word(pos, choice, rhyme_dict[rhyme_scheme[i]], False)
                    else:
                        word_entry = get_random_word(pos, choice, False, False)
            if word_entry:
                word = word_entry[0]
                stress = word_entry[2]
                prev_stress = stress.split(" ")[-1]
            else:
                return word_sentence, True
            new_line.append(word)
        word_sentence.append(new_line)
    return word_sentence, False


def convert_list_to_poem(sentence_list):
    """
    Converts a list of words to a poem
    :param sentence_list: list of words
    :type sentence_list: List
    :return: list of words converted into a human-readable format
    :rtype: String
    """
    s = ""
    for l in sentence_list:
        if l:
            s += " ".join(l) + "\n"
    return s


def main(args):
    """
    Main program, outputs a randomly generated poem depending on commandline arguments
    :param args: list possibly containing grammar for the poem and its rhyme scheme
    :type args: List
    :return: random poem
    :rtype: String
    """
    grammar_file = args.get("grammar", "grammar")
    rhyme_scheme = args.get("rhyme", "ABAB")

    try:
        f = open(grammar_file, "r")
    except IOError:
        print("Grammar file does not exist!")
    else:
        grammar = f.read()
        f.close()

        grammar = convert_grammar(grammar)
        pos_sentence = generate_random_pos(["POEM"], grammar)
        word_sentence = ""
        while True:
            word_sentence, redo = generate_word_from_pos(pos_sentence, rhyme_scheme)
            if redo:
                continue
            else:
                break
        return convert_list_to_poem(word_sentence)

if __name__ == "__main__":
    arg_dict = {}
    for arg in sys.argv:
        split_arg = arg.split("=")
        if len(split_arg) > 1:
            arg_dict[arg.split("=")[0]] = arg.split("=")[1]
    poem = main(arg_dict)
    print(poem)

conn.close()
