#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    # define list for urls
    urls = []
    # getting all urls from file name
    with open(filename) as file:
        urls_with_all_extenstions = re.findall('(?<=GET.)\S*', file.read())
    # finding only .jpg files
    for url in urls_with_all_extenstions:
        if ".jpg" in url:
            urls.append(f"http://code.google.com{url}")
    sorted_urls = sorted(urls)

    return sorted_urls


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    # checking if dir already exist then creat dir
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    # fetching each of image form img_ruls list
    for i in range(len(img_urls)):
        try:
            print(f"downloading image number {i} please wait......")
            urllib.request.urlretrieve(img_urls[i], f"{dest_dir}/img{i}.jpg")
        except:
            print(
                "Can't downloads images please make sure you are connected to interetn and retry")
    # writing  html file
    with open('index.html', 'w') as html_file:
        html_file.write('<html>')
        html_file.write('<body>')
        html_file.write('<table>')
        for i in range(len(img_urls)):
            if i % 2 == 0:
                html_file.write(f'<img src="./images/img{i}.jpg">')
        html_file.write('</tr>')
        html_file.write('</table>')
        html_file.write('</body>')
        html_file.write('</html>')


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)
    img_urls = read_urls(parsed_args.logfile)
    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
