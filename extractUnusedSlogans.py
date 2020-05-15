import pandas as pd
from sloganValues import getTotalWords, getValidWords, getRating

def extractSlogans():
    df = pd.read_csv("uncategorizedSloganList.csv")
    s_df = pd.read_csv("slogans.csv", index_col=0)
    usedSlogans = s_df["Slogan"]
    foundSlogans = set()
    # print(usedSlogans)

    for i in df["Slogan"]:
        if not (i in usedSlogans.values or i[:-1] in usedSlogans.values):
            foundSlogans.add(i)

    for i in foundSlogans:
        company = df.loc[df['Slogan'] == i]['Company'].values
        print(company[0]+",", i)

def rateSlogans():
    df = pd.read_csv("testSlogans.csv", index_col=0)
    df["numWords"] = df["Slogan"].map(getValidWords)
    df["rating"] = df["Slogan"].map(getRating)
    df.to_csv("testSlogans.csv")

rateSlogans()