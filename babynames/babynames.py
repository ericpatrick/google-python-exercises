#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""


def extract_names(filename):
    """
    Given a file name for baby.html, returns a list starting with the year string
    followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    with open(filename, 'r') as file:
        data = file.read()

    year_index_last = data.find('</h3')
    year_index_first = year_index_last - 4
    year = data[year_index_first:year_index_last]

    year_list = [year]
    table_line_seek = year_index_last

    while True:
        row_index_first = data.find('<tr align="right"', table_line_seek)
        if row_index_first == -1:
            break
        row_index_last = data.find('\n', row_index_first)
        row = data[row_index_first:row_index_last]
        row_info = []
        row_seek = 0
        while len(row_info) < 3:
            row_pos_first = row.find('d>', row_seek) + 2
            row_pos_last = row.find('</td', row_seek)
            row_info.append(row[row_pos_first:row_pos_last])
            row_seek = row_pos_last + 4

        row_info.reverse()
        year_list.append(' '.join(row_info[::2]))
        year_list.append(' '.join(row_info[1:3]))

        table_line_seek = row_index_last

    year_list.sort()

    return year_list


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
        print('usage: [--summaryfile] file [file ...]')
        sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    summary = False
    if args[0] == '--summaryfile':
        summary = True
        del args[0]

        for arg in args:
            print(extract_names(arg))
        # For each filename, get the names, then either print the text output
        # or write it to a summary file


if __name__ == '__main__':
    main()
