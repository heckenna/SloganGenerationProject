import json

def isSub(potentialSub):
    return isinstance(potentialSub, dict)

def getSlogans(cat):
    slogans = []
    for val in cat.values():
        if isSub(val):
            for slogan in getSlogans(val):
                slogans.append(reformatSlogan(slogan))
        else:
            for slogan in val:
                slogans.append(reformatSlogan(slogan))
    return slogans

def reformatSlogan(slogan):
    return slogan.strip().replace(" t ", "'t ").replace(" s ", "'s ").replace(" ll ", "'ll ").replace(" d ", "'d ").replace(" ve ", "'ve ")

def formatSlogans():
    data = open('rawSlogans.json')
    rawSlogans = json.load(data)
    categories = dict()

    for category in rawSlogans.keys():
        tempCat = getSlogans(rawSlogans[category])
        if(len(tempCat) >= 100):
            categories[category] = tempCat
            print(category, len(tempCat))

    output = open('slogans.json', 'w')
    json.dump(categories, output)
    output.close()
    data.close()

    f = open("slogans.json", "a")
    f.write("")
    f.close()

def countSlogans():
    data = open('slogans.json')
    slogans = json.load(data)
    
    for category in slogans.keys():
        print(category, len(slogans[category]))

formatSlogans()
# countSlogans()
    
            
            
            


