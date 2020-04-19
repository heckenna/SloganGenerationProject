import pandas as pd
import numpy as np

myCsv = pd.read_csv("Valence_Arousal_Dominance_WarrinerEtAl.csv", usecols =["Word", "Valence", "Arousal", "Dominance"])

def getValence(word):
    if(len(myCsv.loc[myCsv['Word'] == word]) == 0):
        return -1
    return myCsv.loc[myCsv['Word'] == word]['Valence'].values[0]

def getArousal(word):
    if(len(myCsv.loc[myCsv['Word'] == word]) == 0):
        return -1
    return myCsv.loc[myCsv['Word'] == word]['Arousal'].values[0]

def getDominance(word):
    if(len(myCsv.loc[myCsv['Word'] == word]) == 0):
        return -1
    return myCsv.loc[myCsv['Word'] == word]['Dominance'].values[0]

def getAllDimensions(word):
    values = []
    values.append(getValence(word))
    values.append(getArousal(word))
    values.append(getDominance(word))
    return values

#testLine = myCsv.loc[myCsv['Word'] == 'abalone']

# values = ["abalone"]

# values.append(getAllDimensions(values[0]))

# print(values)