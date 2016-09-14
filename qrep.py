#!/usr/bin/env python3

import argparse
import re

parser = argparse.ArgumentParser(description='Like sed, but indecisive.')
parser.add_argument('search_string')
parser.add_argument('replacement_string')
parser.add_argument('file')

def match_indices(match, s):
    idx = s.find(match)
    while idx != -1:
        yield idx
        idx = s.find(match, idx)


def green(text):
    return "\033[32;m" + text + "\033[37;m"


def yellow(text):
    return "\033[33;m" + text + "\033[37;m"


def highlight_replacement(text, match, replacement):
    start, end = match.span()
    pre, post = text[:start], text[end:] # non-highlighted section
    return pre + yellow(text[start:end]) + green(replacement) + post


def query():
    choice = input("Make replacement? [y/n]")
    if choice == 'y':
        return True
    elif choice == 'n':
        return False
    else:
        "Please choose y or n."
        return query()


def query_replace(search, replacement, file):
    regex = re.compile(search)
    f = open(file, 'r')
    output = ""
    for line in f:
        m = re.match(search, line)
        if m:
            print(highlight_replacement(line, m, replacement))
            if query():
                start, end = m.span()
                output += line[:start]
                output += replacement
                output += line[end:]
            else:
                output += line
        else:
            output += line

    print("output:")
    print(output)


def main():
    args = parser.parse_args()
    print(args)
    query_replace(args.search_string, args.replacement_string, args.file)

if __name__ == "__main__":
    main()
