# ([q]uery [rep]lace)

`qrep` is kind of like `sed`, but indecisive. You invoke it like this:

    ./qrep.py term replacement file.txt

It will search through `file.txt` looking for `term`. When it finds a match, it will ask you if you want to replace `term` with `replacement`, highlighting them with fancy magical terminal escape codes. When it's done searching, it will print the whole file.

`term` is interpreted as a Python regular expression, directly. Use at your own risk.

# Coming soon
- Update files in place
- Recursive searches of directories
