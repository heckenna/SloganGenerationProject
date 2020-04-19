from Valence_arousal_dominance_csvParser import getValence, getArousal, getDominance, getAllDimensions

def getAverageDimensions(slogan):
    words = slogan.split()
    sum = [0,0,0]
    num = [0,0,0]
    for word in words:
        val = getAllDimensions(word)
        if(val[0] != -1):
            for i in range(3):
                sum[i] += val[i]
                num[i] += 1
        
    avg = [0,0,0]
    for i in range(3):
        avg[i] = sum[i]/num[i]

    return avg

print(getAverageDimensions('abduction abdomen abbey'))
