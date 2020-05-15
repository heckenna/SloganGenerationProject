import pandas as pd 
import numpy as np
import Valence_arousal_dominance_csvParser as val
from nltk.stem import WordNetLemmatizer 

lemmatizer = WordNetLemmatizer() 


def stringToList(word):
  return word.split()

def getMaxSloganLength():
  slogansFromCSV = pd.read_csv("encodedSlogans.csv", usecols = ["Slogan"])
  slogansFromCSV["SlogansToList"] = pd.DataFrame.applymap(slogansFromCSV, stringToList)
  return np.max(np.vectorize(len)(slogansFromCSV["SlogansToList"]))

def sloganToIndicies(sloglist):
  #lst = np.zeros(16)
  lst = [0]*16
  for i in range(len(sloglist)):
    lst[i] = val.getIndex(lemmatizer.lemmatize(sloglist[i]))
  return lst

def lster(arg):
  lst = []
  for col in range(len(arg)):
    lst.append(arg[col])
  return lst

'''
df = pd.read_csv("encodedSlogans.csv", index_col = 0)
df = df.sum(axis = 0)
print(df)
#'''
'''
def lster(arg):
  return [arg["Apparel"], arg["Automotive"]]


df = pd.read_csv("encodedSlogans.csv", index_col = 0)
smol = df[['Apparel', 'Automotive']]
df["Target"] = smol.apply(lster, axis = 1)
print(df)
#'''
"""
valArDom = pd.read_csv("Valence_Arousal_Dominance_WarrinerEtAl.csv", usecols =["Word", "Valence", "Arousal", "Dominance"])
slogansFromCSV = pd.read_csv("encodedSlogans.csv", usecols = ["Slogan"])

#print(stringToList(slogansFromCSV["Slogan"][1]))

slogansFromCSV["SlogansToList"] = pd.DataFrame.applymap(slogansFromCSV, stringToList)

#Max length is 16!!!
#print(np.max(np.vectorize(len)(slogansFromCSV["SlogansToList"])))

#slogansFromCSV["IndexEncoded"] = np.vectorize(sloganToIndicies)(slogansFromCSV["SlogansToList"])

#print(slogansFromCSV["IndexEncoded"])
#print(np.vectorize(sloganToIndicies)(["eat", "Some", "Chocolate"]))
slogansFromCSV["IndexEncoded"] = pd.Series.map(slogansFromCSV["SlogansToList"], sloganToIndicies)
pd.DataFrame.to_csv(slogansFromCSV, "indexEncodedSlogans.csv")
print(slogansFromCSV["IndexEncoded"])
#"""