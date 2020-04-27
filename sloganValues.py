from Valence_arousal_dominance_csvParser import getValence, getArousal, getDominance, getAllDimensions
from nltk.stem import WordNetLemmatizer 

lemmatizer = WordNetLemmatizer() 


def getAverageDimensions(slogan):
    words = slogan.split()
    sum = [0,0,0]
    num = [0,0,0]
    for word in words:
        val = getAllDimensions(lemmatizer.lemmatize(word))
        if(val[0] != -1):
            for i in range(3):
                sum[i] += val[i]
                num[i] += 1
        
    avg = [0,0,0]
    for i in range(3):
        avg[i] = sum[i]/num[i]

    return avg

print(getAverageDimensions('abduction abdomen abbey'))
