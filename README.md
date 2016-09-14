# ([q]uery [rep]lace)

`qrep` is a command line tool for search-and-replace. It's kind of like `sed`, but indecisive -- it won't replace anything until you tell it to. You invoke it like this:

    ./qrep.py term replacement file.txt

It will search through `file.txt` looking for `term`. When it finds a match, it will ask you if you want to replace `term` with `replacement`, highlighting them with fancy magical terminal escape codes. When it's done searching, it will print the whole file.

`term` is interpreted as a Python regular expression, directly. In `replacement`, backslash groups from the regex are available. So for example,

    ./qrep.py 'def ([a-z_]+)(\(.\)):' 'def \2\1:' qrep.py

will switch the name and arguments of each function definition in the file qrep.py.

# Coming soon
- Update files in place
- Recursive searches of directories
