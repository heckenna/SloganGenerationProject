from lxml import html
import requests
import pprint
import re

def parseSloganPage(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    removeEmsp = lambda x: x.replace("\u2003", "")
    containsNewline = lambda x: not "\n" in x
    companies = list(filter(containsNewline, list(
        map(removeEmsp, tree.xpath('//p[@class="paragraf"]/text()')))))
    slogans = list(map(removeEmsp, tree.xpath('//span[@class="slogan"]/text()')))

    pairs = dict()
    j = 0
    for i, slogan in enumerate(slogans):
        if(not companies[j] in pairs):
            pairs[companies[j]] = list()
        if not "\n" in slogan:
            pairs[companies[j]].append(slogan)
            j += 1
        else:
            slogan = re.sub('[\W_]+', ' ', slogan, flags=re.UNICODE)

            pairs[companies[j - 1]].append(slogan)
    
    return pairs


furl = 'http://www.textart.ru/advertising/slogans/socks.html'
print(parseSloganPage(furl))




