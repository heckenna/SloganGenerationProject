from lxml import html
import requests
import pprint
import re
import json
import time

base_url = "http://www.textart.ru/"



def parseSloganPage(url, categoryUrl, isFirstPage=True):
    global slogan_count
    page = requests.get(url)
    tree = html.fromstring(page.content)
    subpages = tree.xpath('//option[@value="#"]/text()')
    if(subpages):
        return parseSingleCategory(url)
    def removeEmsp(x): return x.replace("\u2003", "")
    def startsNewline(x): return not x[0] == "\n"
    def replaceApostrophe(x): return x.replace(u"\u2019","\'")
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
        slogan_count+=1
        if not "\n" in slogan:
            if(not companies[j] in pairs):
                pairs[companies[j]] = list()
            # print(companies[j], ">>", slogan)
            slogan = replaceApostrophe(slogan)
            slogan = re.sub('[\W_]+', ' ', slogan, flags=re.UNICODE)
            pairs[companies[j]].append(slogan)
            j += 1
        else:
            slogan = replaceApostrophe(slogan)
            slogan = re.sub('[\W_]+', ' ', slogan, flags=re.UNICODE)

            pairs[companies[j - 1]].append(slogan)
            # print(companies[j - 1], ">>", slogan)

    if(isFirstPage):
        nextPages = tree.xpath('//p[@align="center"]')
        # print(nextPages[0])
        # print(nextPages)
        if(nextPages):
            nextPages=nextPages[0].xpath('./a[@href]/@href')
            print(len(nextPages),"more pages found")
            for nextPage in nextPages:
                pairs.update(parseSloganPage(formatUrl(nextPage, categoryUrl), categoryUrl, False))
    return pairs

def formatUrl(rawUrl, categoryUrl):
    if not base_url in rawUrl:
        if "index.html" in categoryUrl:
            url = categoryUrl.replace("index.html", rawUrl)
        elif "slogans.html" in categoryUrl:
            url = categoryUrl.replace("slogans.html", rawUrl)
        # print(url)
        return url
    return rawUrl

def parseSingleCategory(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    subcategories = tree.xpath('//option[@value]/text()')
    subcategories_links = tree.xpath('//option[@value]//@value')
    categoryEntry = dict()
    for i in range(len(subcategories)):
        if(subcategories_links[i] == "#" or subcategories[i] == "Department stores"):
            continue
        
        subDict = parseSloganPage(formatUrl(subcategories_links[i], url), url)
        categoryEntry[subcategories[i]] = subDict
        time.sleep(0.05)
    
    return categoryEntry
    

def parseCategories():

    links = open('SloganLinks.json')
    data = json.load(links)
    categories = dict()
    for category in data:
        categories[category] = dict()

        categories[category] = parseSingleCategory(data[category])
        #pprint.pprint(categories[category])
        time.sleep(0.1)

    output = open('rawSlogans.json', 'w')
    json.dump(categories, output)
    output.close()
    links.close()

    f = open("rawSlogans.json", "a")
    f.write("")
    f.close()
    # print(categories)

startTime = time.time()
slogan_count = 0
parseCategories()
print(slogan_count,"Slogans Parsed in",time.time()-startTime,"seconds")
# page_url = 'http://www.textart.ru/advertising/slogans/car-rental.html'
# print(parseSloganPage(page_url))

