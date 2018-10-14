#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib.request

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def element_to_sort(el):
    match = re.search(r'\w(-\w*)+\.jpg', el)
    if match:
        filename = match.group()
        slices = filename.split('-')
        return slices[-1]
    else:
        return el

def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    file = open(filename, 'r')
    urls_info = re.findall(r'GET\s+(/.*?puzzle.*?jpg)', file.read())
    match = re.search(r'[^_]+(\.\w+)+', filename)
    if match:
        host = 'http://' + match.group()
        urls = set(map(lambda x: host + x, urls_info))
        return sorted(urls, key=element_to_sort)
    else:
        print('Could not get hostname')
        sys.exit(1)

def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    for i, url in enumerate(img_urls):
        filename = dest_dir + '/img%d' % i
        urllib.request.urlretrieve(url, filename)

    html_images = map(lambda x: '<img src="%s"/>' % x, img_urls)
    html_content = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Images</title>
        <style>
            body {
                display: flex;
            }
        </style>
    </head>
    <body>
        %s
    <body>
    </html>
    ''' % '\n        '.join(html_images)
    file = open('images/index.html', 'w')
    file.write(html_content)
    file.close()

def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--todir dir] logfile ')
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main()
