# ******************************************************************************
# GetShorty
# by Jake Kara
# jake@jakekara.com
# 
# Proof of concept for "brute force" crawling URL shortening services to see
# 
# ******************************************************************************

import requests, random, math, json, time, sys
from BeautifulSoup import BeautifulSoup

class Charsets:
    def ascii_range(self, a, b):
        return map(lambda x: chr(x), range(a, b + 1))
    def uppers(self):
        return self.ascii_range(65,90)
    def lowers(self):
        return self.ascii_range(97,122)
    def numerals(self):
        return self.ascii_range(48,57)

class Brute:
    def __init__(self, characters=(Charsets()).numerals(), length=8):
        self.chars = characters
        self.blength = length
        
    def shift(self, n):
        return self.chars[n]

    def max_permutations(self, length):
        if length == 0:
            return 0
        return len(self.chars) ** length
    
    def infinite_nth(self, n):
        return self.chars[ n % len(self.chars)]

    def nth_char(self, n):
        print "nth_char", n, n % len(self.chars)
        return self.chars[n % len(self.chars)]
    
    def nth(self, n):
        carry = n
        offsets = [0] * self.blength
        ranges = map(lambda x: (self.max_permutations(x),
                                self.max_permutations(x + 1) - 1),
                     range(0,self.blength))
        ret = ""
        for i in range(0, self.blength):
            max_val = ranges[i][1]
            min_val = ranges[i][0]
            if n < min_val:
                ret = self.chars[0] + ret
                continue

            part = carry % (max_val + 1)
            new_char = self.infinite_nth(part / max(min_val, 1))
            carry -= part
            ret =  new_char + ret
        return ret

    def for_all(self, f):
        for i in range(self.max_permutations(self.blength)):
            f(self.nth(i))

class Shorty:
    def __init__(self, base_url, cache_file="out.json", callback=(lambda x: x)):
        self.b_url = base_url
        self.filename = cache_file
        self.load_cache()
        self.page_processor = callback

    def get_long_url(self, x):
        url = self.b_url + x
        if x in self.url_map.keys():
            print x, "CACHED"
            return
        try:
            r = requests.get(url, allow_redirects=False)
        except:
            return
        obj = self.page_processor(r)
        print obj
        self.url_map[x] = obj
        self.update_cache()
        time.sleep(1)

    # Brute urls with length x 
    def brute_len(self, x,
                  characters=(Charsets()).lowers()\
                  + (Charsets()).uppers()\
                  + (Charsets()).numerals()):
        (Brute(length=2, characters=characters))\
            .for_all(self.get_long_url)

    def load_cache(self):
        try:
            self.url_map = json.loads(open(self.filename,"r").read())
        except:
            self.url_map = {}

    def update_cache(self):
        outfile = open (self.filename, "w")
        outfile.write(json.dumps(self.url_map, indent=2))
        outfile.close()

    def to_csv(self, f, out=sys.stdout):
        # outfile = open(out, "a")
        out.write("short\tlong")
        for k in sorted(self.url_map):
            # print self.b_url + k + "\t" + f(self.url_map[k])
            try:
                out.write(self.b_url + k + "\t" + f(self.url_map[k]) + "\n")
            except:
                # For now I'm not bothering with non-unicode character errors
                out.write(self.b_url + k + "\t" + "[INVALID CHARACTER ERROR]" + "\n")
                continue

