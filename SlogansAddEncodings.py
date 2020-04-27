from sloganValues import getAverageDimensions
import math
import pandas as pd


def encodeSlogan(slogan):
    #print(slogan)
    vals = getAverageDimensions(slogan)
    for i in range(len(vals)):
        vals[i] = int(math.floor(vals[i]*(10**8)))
    return vals



df = pd.read_csv("slogans.csv", index_col=0)

# print(df.head())
# print(df.dtypes)

#categories = df.loc[:,'Apparel':'Transport and Logistics']
slogans = df.drop(df.loc[:,'Apparel':'Transport and Logistics'].columns, axis=1)
df["EncodedValues"] = df["Slogan"].map(encodeSlogan)

df.to_csv("encodedSlogans.csv")
