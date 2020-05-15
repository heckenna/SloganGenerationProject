import pandas as pd



def getNRCemotions():
  myCsv = pd.read_csv("NRC-Emotion-Lexicon-v0.92\\NRC-Emotion-Lexicon-v0.92-In105Languages-Nov2017Translations.csv", sep = '|' ,usecols = ["English (en)", "Positive", "Negative", "Anger", "Anticipation", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust"])
  myCsv = myCsv.rename(columns={"English (en)":"Word"})
  return myCsv


print(getNRCemotions())













