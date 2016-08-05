# GetShorty

"Brute force" crawler of url shortening services.

* GetShorty.py is the library;
* brute.py is a sample command line tool using GetShorty.py

# Basic crawling

To start crawling bitly two-character URLs (and storing in out.json cache file):

   $ python brute.py

If you want to crawl longer URLs, the code can be modified. I didn't bother
making it a command line argument.

Note that if you have the out.json file from this repo in the local directory,
it won't need to crawl anything, and it'll just tell you that each URL is cached
and then exit.

# TSV output

To output the cached URLs to in TSV format (like the one in sample_output
folder of this repo), use:

   $ python brute.py --csv

To output the TSV to a file:

   $ python brute.py --csv out-file.tsv

Yes, I called it --csv, but it's really in TSV format (tab-separated, not
commas). You'll get over it.

# Why?

This is just a "proof of concept" of an idea that I've read about a lot lately.
I was just curious about how difficult it would be. No real reason.