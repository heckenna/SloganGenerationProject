from lxml import html
import requests
import pprint
import re
import json
import time

base_url = "http://www.textart.ru/"

def parseSloganPage(url):

    page = requests.get(url)
    tree = html.fromstring(page.content)
    def removeEmsp(x): return x.replace("\u2003", "")
    def startsNewline(x): return not x[0] == "\n"
    def removeNonAlpha(x): return re.sub('[\W_]+', ' ', x, flags=re.UNICODE)
    # print(list(map(removeEmsp, tree.xpath('//p[@class="paragraf"]/text()'))))
    companies = list(map(removeNonAlpha, list(filter(startsNewline, list(
        map(removeEmsp, tree.xpath('//p[@class="paragraf"]/text()')))))))
    slogans = list(map(removeEmsp, tree.xpath(
        '//span[@class="slogan"]/text()')))
    pairs = dict()
    print(url)
    # print(companies, len(slogans))
    j = 0
    for i, slogan in enumerate(slogans):

        if not "\n" in slogan:
            if(not companies[j] in pairs):
                pairs[companies[j]] = list()
            # print(companies[j], ">>", slogan)
            pairs[companies[j]].append(slogan)
            j += 1
        else:
            slogan = re.sub('[\W_]+', ' ', slogan, flags=re.UNICODE)

            pairs[companies[j - 1]].append(slogan)
            # print(companies[j - 1], ">>", slogan)

    return pairs

def formatUrl(rawUrl, categoryUrl):
    if not base_url in rawUrl:
        url = categoryUrl.replace("index.html", rawUrl)
        # print(url)
        return url
    return rawUrl

def parseCategories():

    links = open('SloganLinks.json')
    data = json.load(links)
    categories = dict()
    for category in data:
        categories[category] = dict()

        page = requests.get(data[category])
        tree = html.fromstring(page.content)
        subcategories = tree.xpath('//option[@value]/text()')
        subcategories_links = tree.xpath('//option[@value]//@value')
        for i in range(len(subcategories)):
            if(subcategories_links[i] == "#" or subcategories[i] == "Alcoholic drinks"):
                continue
            
            subDict = parseSloganPage(formatUrl(subcategories_links[i], data[category]))
            categories[category][subcategories[i]] = subDict
            time.sleep(0.05)
        time.sleep(0.1)
        #pprint.pprint(categories[category])

    output = open('rawSlogans.json', 'w')
    json.dump(categories, output)
    output.close()
    links.close()

    f = open("rawSlogans.json", "a")
    f.write("")
    f.close()
    # print(categories)


parseCategories()
page_url = 'http://www.textart.ru/database/english-advertising-slogans/restaurant-advertising-slogans.html'
# print(parseSloganPage(page_url))

