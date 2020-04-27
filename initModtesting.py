import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


df = pd.read_csv("encodedSlogans.csv", index_col=0)

train, test = train_test_split(df, test_size=0.2, random_state=192)



history = model.fit(train, epochs=10,
                    validation_data=test, 
                    validation_steps=30)

test_loss, test_acc = model.evaluate(test)

print('Test Loss: {}'.format(test_loss))
print('Test Accuracy: {}'.format(test_acc))