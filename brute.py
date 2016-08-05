import GetShorty, sys
from BeautifulSoup import BeautifulSoup
import sys

def bitly_to_csv(url_record):
    try:
        return url_record["moved here"]
    except:
        return "ERROR"
            
def process_bitly_response(r):
    soup = BeautifulSoup(r.content)
    links = soup.findAll("a")
    obj = {}
    for l in links:
        print l["href"]
        obj[l.text] = l["href"]
    return obj

bitly = GetShorty.Shorty("http://bit.ly/", callback=process_bitly_response)

if len(sys.argv) > 1 and sys.argv[1] == "--csv":
    outfile = sys.stdout
    if len(sys.argv) > 2:
        outfile = open(sys.argv[2], "w")
    bitly.to_csv(bitly_to_csv, out=outfile)

else:
    bitly.brute_len(2)
