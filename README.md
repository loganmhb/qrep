# ([q]uery [rep]lace)

`qrep` is a command line tool for search-and-replace. It's kind of like `sed`, but indecisive -- it won't replace anything until you tell it to.

## Usage

You invoke it like this:

    qrep term replacement file.txt

It will search through `file.txt` looking for `term`. When it finds a match, it will ask you if you want to replace `term` with `replacement`, highlighting them with fancy magical terminal escape codes. If you say yes, it will make the replacement.

`term` is interpreted as a Python regular expression, directly. In `replacement`, capture groups from the regex are available using backslash notation. So for example,

    qrep 'def ([a-z]+)(\(.*\)):' 'def \2\1:' qrep.py

will switch the name and arguments of each function definition in the file qrep.py.

If the file argument is a directory and you specify `-r` or `--recursive`, `qrep` will recursively perform the search through each file and subdirectory. You can exclude files or subdirectories by pattern with the `--ignore` flag:

    qrep -r --ignore node_modules myVar myRenamedVar .

## Installation

Coming soon: a homebrew recipe!

For now, this does the trick:

    cp qrep.py ~/bin/qrep
