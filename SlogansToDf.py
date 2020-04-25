import pandas as pd
import numpy as np
#from pandas.io.json import json_normalize
import json


#myJson = pd.read_json("rawSlogans.json")
sloganJson = json.load(open("slogans.json"))
betterDf = pd.json_normalize(sloganJson)



parsedSlog = betterDf.T
sloganDf = pd.DataFrame(columns = ["Category", "Slogan"])

for cat in betterDf.columns:
  sloganList = betterDf[cat].loc[0]
  for slogan in sloganList:
    #newRow = pd.DataFrame(np.array([cat, slogan]), columns = ["Category", "Slogan"])
    newRow = pd.DataFrame({"Category":[cat], "Slogan":[slogan]})
    sloganDf = pd.concat([sloganDf, newRow], ignore_index=True)

#print(sloganDf)


print(sloganDf.columns)
slogansEncoded = pd.get_dummies(sloganDf["Category"])
slogansEncoded["Slogan"] = sloganDf['Slogan']
#sloganDf.drop(["Category"], inplace = True)
print(slogansEncoded)

pd.DataFrame.to_csv(slogansEncoded, "slogans.csv")


"""
categories = myJson.columns
categories = list(categories)
print(categories)

#print(myJson.columns)
print(myJson)
print((myJson.T).columns)

newDf = pd.DataFrame(columns = ["Category", "SubCat1", "SubCat2", "Company", "Slogan"])

for category in categories:
  print(((myJson[category]).dropna()))
  subCatSeries = (myJson[category]).dropna()
  print(subCatSeries.shape())
  catDf = pd.DataFrame()
  break

print(newDf)
"""

