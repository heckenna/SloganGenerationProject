import NRCemotionParser as nrc
import Valence_arousal_dominance_csvParser as vad
import pandas as pd


def getMergedwords():
  emotionData = nrc.getNRCemotions()
  vadData = vad.getVAD()

  result = pd.merge(emotionData, vadData, how="outer",on="Word")
  return result

def getFeature(word, feature):
  myCsv = getMergedwords()
  if(len(myCsv.loc[myCsv['Word'] == word]) == 0):
    return -1
  return myCsv.loc[myCsv['Word'] == word][feature].values[0]

def getValence(word):
  getFeature(word, "Valence")

def getArousal(word):
  getFeature(word, "Arousal")

def getDominance(word):
  getFeature(word, "Dominance")

def getPositve(word):
  getFeature(word, "Positive")

def getNegative(word):
  getFeature(word, "Negative")

def getAnger(word):
  getFeature(word, "Anger")

def getAnticipation(word):
  getFeature(word, "Anticipation")

def getDisgust(word):
  getFeature(word, "Disgust")

def getFear(word):
  getFeature(word, "Fear")

def getJoy(word):
  getFeature(word, "Joy")

def getSadness(word):
  getFeature(word, "Sadness")

def getSurprise(word):
  getFeature(word, "Surprise")

def getTrust(word):
  getFeature(word, "Trust")

def getAllDimensions(word):
    values = []
    dimensions = ["Valence", "Arousal", "Dominance",  "Positive", "Negative", "Anger", "Anticipation", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust"]
    for feature in dimensions:
      values.append(getFeature(word, feature))
    return values
