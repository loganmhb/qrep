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
import sys

parser = argparse.ArgumentParser(description='Like sed, but indecisive.')
parser.add_argument('-r', '--recursive', action='store_true',
                    help='If FILE is a directory, process it recursively.')
parser.add_argument('-i', '--ignore', metavar='PATTERN',
                    help='Pattern of filenames to ignore during recursive operation.')
parser.add_argument('search_string')
parser.add_argument('replacement_string')
parser.add_argument('file', nargs='+')


def match_indices(match, s):
    idx = s.find(match)
    while idx != -1:
        yield idx
        idx = s.find(match, idx)


def green(text):
    return "\033[32;m" + text + "\033[37;m"

def yellow(text):
    return "\033[33;m" + text + "\033[37;m"

def red(text):
    return "\033[35;m" + text + "\033[37;m"


def query():
    choice = input(yellow("\nMake replacement? [y/n] "))
    if choice == 'y':
        return True
    elif choice == 'n':
        return False
    else:
        print(red("Please choose y or n."))
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


def display_section(current_file, match, replacement):
    """
    Print a match and replacement along with a couple lines of context.
    """
    print(yellow("".join([ "*** Match in file:", current_file, "***\n"])))
    s = match.string
    match_start, match_end = match.span()
    display_start, display_end = find_boundaries(s, match_start, match_end)
    print("".join([s[display_start:match_start],
                   red(s[match_start:match_end]),
                   green(match.expand(replacement)),
                   s[match_end:display_end]]))


def query_replace_string(current_file, search, replacement, text):
    regex = re.compile(search)
    output = ""
    search_start = 0
    match = regex.search(text)
    while match:
        display_section(current_file, match, replacement)
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


def ignored(filename, pattern):
    if pattern and re.match(pattern, filename):
        return True
    else:
        return False


def query_replace_file(search, replacement, filename, ignore_pattern, recursive=False):
    if ignored(os.path.basename(filename), ignore_pattern):
        return

    if os.path.isdir(filename):
        if recursive:
            for entry in os.scandir(filename):
                query_replace_file(search, replacement, entry.path,
                                   ignore_pattern, recursive=True)
        else:
            sys.exit('ERROR: Directory specified on non-recursive search; use --recursive.')
    else:
        with open(filename, 'r') as f:
            contents = f.read()
        new_contents = query_replace_string(filename, search, replacement, contents)
        with open(filename, 'w') as f:
            f.write(new_contents)


def main():
    args = parser.parse_args()
    for file in args.file:
        query_replace_file(args.search_string, args.replacement_string, file,
                           args.ignore, recursive=args.recursive)
