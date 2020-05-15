import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np

cats = ["Apparel","Automotive","Beauty","Beverage","Business","Construction","Dining","Education","Financial",
    "Food","Health and Medicine","Household","Shopping and Retail","Toiletries","Tourism and Travel","Transport and Logistics"]
# rev_cats = cats[::-1]

def plotConfusionArray(array):
    df_cm = pd.DataFrame(array, index = [i for i in cats],
                    columns = [i for i in cats])
    plt.figure(figsize = (16,7))
    sn.heatmap(df_cm, annot=True)

    plt.show()

def confusionArrayFromInOut(in_vals, out_vals):
    return np.array(tf.math.confusion_matrix(in_vals, out_vals, num_classes=len(cats)))

def AccuracyArrayFromInOut(in_vals, out_vals):
    numRight = dict()
    numTot = dict()
    accuracies = dict()
    for index, inp in enumerate(in_vals):
        if not inp in numTot:
            numTot[inp] = 0
            numRight[inp] = 0
        numTot[inp] += 1
        if out_vals[index] == inp:
            numRight[inp] += 1
    
    for cat in numTot.keys():
        accuracies[cat] = numRight[cat]/numTot[cat]
    
    return accuracies

def numOccurences(vals):
    numTot = dict()
    for val in vals:
        if not val in numTot:
            numTot[val] = 0
        numTot[val] += 1
    
    return numTot

# plotConfusionArray(confusionArrayFromInOut([0,0,0,0,1,1,1,2,2,2,2,2,3,3,3,3,4,4,4,4,4,4,5,5,5,6,6,7,7,7,7,7,8,8,9,9,9,9,9], 
#                                            [0,1,2,0,3,0,3,2,4,5,4,3,2,3,4,3,6,5,6,7,9,9,4,5,6,1,8,9,9,0,3,5,5,9,8,8,6,8,9]))

# print(AccuracyArrayFromInOut([0,0,0,0,1,1,1,2,2,2,2,2,3,3,3,3,4,4,4,4,4,4,5,5,5,6,6,7,7,7,7,7,8,8,9,9,9,9,9], 
#                             [0,1,2,0,3,0,3,2,4,5,4,3,2,3,4,3,6,5,6,7,9,9,4,5,6,1,8,9,9,0,3,5,5,9,8,8,6,8,9]))

# print(numOccurences([0,0,0,0,1,1,1,2,2,2,2,2,3,3,3,3,4,4,4,4,4,4,5,5,5,6,6,7,7,7,7,7,8,8,9,9,9,9,9]))