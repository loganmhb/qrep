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


def red(text):
    return "\033[35;m" + text + "\033[37;m"


def query():
    choice = input("Make replacement? [y/n]")
    if choice == 'y':
        return True
    elif choice == 'n':
        return False
    else:
        print("Please choose y or n.")
        return query()


def find_boundaries(s, match_start, match_end):
    while s[match_start] != '\n' and match_start > 0:
        match_start -= 1
    while s[match_end] != '\n' and match_end < len(s):
        match_end += 1
    return match_start, match_end


def display_section(match, replacement):
    s = match.string
    match_start, match_end = match.span()
    display_start, display_end = find_boundaries(s, match_start, match_end)
    print("disp start: ", display_start, ", match_start: ", match_start, ", match_end: ", match_end, ", disp end:", display_end)
    print("".join([s[display_start:match_start],
                   red(s[match_start:match_end]),
                   green(replacement),
                   s[match_end:display_end]]))


def query_replace(search, replacement, f):
    regex = re.compile(search)
    file_str = open(f).read()
    print("length:", len(file_str))
    output = ""
    search_start = 0
    match = regex.search(file_str)
    print("first match:", match)
    while match:
        print("start:", search_start)
        display_section(match, replacement)
        match_start, match_end = match.span()
        if query():
            output += match.string[search_start:match_start]
            output += replacement
        else:
            output += match.string[search_start:match_end]

        _, search_start = match.span()
        match = regex.search(file_str, search_start)
    output += file_str[search_start:]
    print("output:")
    print(output)


def main():
    args = parser.parse_args()
    print(args)
    query_replace(args.search_string, args.replacement_string, args.file)

if __name__ == "__main__":
    main()
