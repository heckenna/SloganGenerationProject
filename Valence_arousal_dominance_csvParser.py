import pandas as pd
import numpy as np
import random

random.seed(145)
myCsv = pd.read_csv("Valence_Arousal_Dominance_WarrinerEtAl.csv", usecols =["Word", "Valence", "Arousal", "Dominance"])

def getVAD():
    return pd.read_csv("Valence_Arousal_Dominance_WarrinerEtAl.csv", usecols =["Word", "Valence", "Arousal", "Dominance"])

def getIndex(word):
    if(len(myCsv.loc[myCsv['Word'] == word.lower()]) == 0):
        return getVocabLength() + 1
    return myCsv.index[myCsv['Word'] == word.lower()][0] + 1

def getValence(word):
    if(len(myCsv.loc[myCsv['Word'] == word.lower()]) == 0):
        return -1
    return myCsv.loc[myCsv['Word'] == word.lower()]['Valence'].values[0]

def getArousal(word):
    if(len(myCsv.loc[myCsv['Word'] == word.lower()]) == 0):
        return -1
    return myCsv.loc[myCsv['Word'] == word.lower()]['Arousal'].values[0]

def getDominance(word):
    if(len(myCsv.loc[myCsv['Word'] == word.lower()]) == 0):
        return -1
    return myCsv.loc[myCsv['Word'] == word.lower()]['Dominance'].values[0]

def getAllDimensions(word):
    values = []
    values.append(getValence(word))
    values.append(getArousal(word))
    values.append(getDominance(word))
    return values

# Dimensions: [IsWord, UseVad, Valence, Arousal, Dominance]
def getAllDimensionsIndex(index):
    if(index == 0):
        return None #[0, 0, 0]
    elif(index == getVocabLength() + 1):
        # retVal = [1, 0, 1, 1, 1]
        retVal = [random.random()]*5
        # retVal.extend([random.random()]*245)
        return retVal
    index -= 1
    # values.append(myCsv.iloc[index]['Valence'][0])
    # values.append(myCsv.iloc[index]['Arousal'][0])
    # values.append(myCsv.iloc[index][0])
    #return myCsv.iloc[index][['Valence','Arousal','Dominance']].to_numpy().tolist()
    ans = [1, 1] 
    ans.extend(myCsv.iloc[index][['Valence', 'Arousal', 'Dominance']].to_numpy().tolist())
    # ans.extend([random.random()]*245)
    ans = [random.random()]*5
    return ans

def getVocabLength():
    return len(myCsv)

#testLine = myCsv.loc[myCsv['Word'] == 'abalone']

# values = ["abalone"]

# values.append(getAllDimensions(values[0]))

# print(values)

# print(getIndex('friend'))
# print(getVocabLength())
# print(getAllDimensionsIndex(1))