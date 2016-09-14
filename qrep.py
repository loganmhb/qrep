#!/usr/bin/env python3

# Copyright 2016 Logan Buckley

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import re
import os


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
    choice = input("Make replacement? [y/n] ")
    if choice == 'y':
        return True
    elif choice == 'n':
        return False
    else:
        print("Please choose y or n.")
        return query()


def find_boundaries(s, match_start, match_end, extra_lines=2):
    start = match_start
    end = match_end
    for i in range(extra_lines):
        boundary = s.rfind('\n', 0, start-1)
        if boundary == -1:
            break
        start = boundary

    for i in range(extra_lines):
        boundary = s.find('\n', end+1)
        if boundary == -1:
            break
        end = boundary

    return start, end


def display_section(match, replacement):
    """
    Print a match and replacement along with a couple lines of context.
    """
    s = match.string
    match_start, match_end = match.span()
    display_start, display_end = find_boundaries(s, match_start, match_end)
    print("".join([s[display_start:match_start],
                   red(s[match_start:match_end]),
                   green(match.expand(replacement)),
                   s[match_end:display_end]]))


def query_replace_string(search, replacement, text):
    regex = re.compile(search)
    output = ""
    search_start = 0
    match = regex.search(text)
    while match:
        display_section(match, replacement)
        match_start, match_end = match.span()
        if query():
            output += match.string[search_start:match_start]
            output += match.expand(replacement)
        else:
            output += match.string[search_start:match_end]

        _, search_start = match.span()
        match = regex.search(text, search_start)
    output += text[search_start:]
    return output

def query_replace_file(search, replacement, filename):
    if os.path.isdir(filename):
        for entry in os.scandir(filename):
            query_replace_file(search, replacement, entry.path)
    else:
        with open(filename, 'r') as f:
            contents = f.read()
        new_contents = query_replace_string(search, replacement, contents)
        with open(filename, 'w') as f:
            f.write(new_contents)


def main():
    args = parser.parse_args()
    print(args)
    query_replace_file(args.search_string, args.replacement_string, args.file)

if __name__ == "__main__":
    main()
