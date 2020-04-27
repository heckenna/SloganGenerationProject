import tensorflow as tf
from sloganValues import getAverageDimensions
import math
import pandas as pd
import tensorflow_hub as hub
from sklearn.model_selection import train_test_split


def lstToString(lst):
    print(lst)

def get_dataset(file_path, **kwargs):
  dataset = tf.data.experimental.make_csv_dataset(
      file_path,
      batch_size=5, # Artificially small to make examples easier to show.
    #   label_name=LABEL_COLUMN,
      na_value="?",
      num_epochs=1,
      ignore_errors=True, 
      **kwargs)
  return dataset

def encodeSlogan(slogan):
    print(slogan)
    vals = getAverageDimensions(slogan)
    for i in range(len(vals)):
        vals[i] = int(math.floor(vals[i]*(10**8)))
    return vals



df = pd.read_csv("encodedSlogans.csv", index_col=0)


# print(df.head())
# print(df.dtypes)

categories = df.loc[:,'Apparel':'Transport and Logistics']
slogans = df.drop(df.loc[:,'Apparel':'Transport and Logistics'].columns, axis=1)
slogans = slogans.drop(['EncodedValues'], axis=1)

embedding = "https://tfhub.dev/google/tf2-preview/nnlm-en-dim50/1"
hub_layer = hub.KerasLayer(embedding, input_shape=[], 
                           dtype=tf.string, trainable=True)

# 
# print(categories.head())
# print(slogans.values)

train, test = train_test_split(df, test_size=0.4, random_state=192)

categ = train.loc[:,'Apparel':'Transport and Logistics']
slog = train.drop(df.loc[:,'Apparel':'Transport and Logistics'].columns, axis=1)
slog = slog.drop(['EncodedValues'], axis=1)

test_categ = test.loc[:,'Apparel':'Transport and Logistics']
test_slog = test.drop(df.loc[:,'Apparel':'Transport and Logistics'].columns, axis=1)
test_slog = test_slog.drop(['EncodedValues'], axis=1)

traindata = tf.data.Dataset.from_tensor_slices((slog["Slogan"].values, categ.values))
testdata = tf.data.Dataset.from_tensor_slices((test_slog["Slogan"].values, test_categ.values))


# slogans = slogans.apply(lstToString)
# print(slogans)
dataset = tf.data.Dataset.from_tensor_slices((slogans['Slogan'].values, categories.values))
# dataset =  tf.data.Dataset.from_tensor_slices(slogans.values)

# print(dataset)
ex_batch, labels_batch =next(iter(traindata.batch(10)))

print(ex_batch)
print(labels_batch)

print(hub_layer(ex_batch[:3]))
# 

model = tf.keras.Sequential()
model.add(hub_layer)
model.add(tf.keras.layers.Dense(16, activation='relu'))
model.add(tf.keras.layers.Dense(16))

model.summary()

model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = model.fit(traindata.shuffle(5000).batch(512),
                    epochs=10,
                    validation_data=testdata.batch(512),
                    verbose=1)

results = model.evaluate(testdata.batch(512), verbose=2)
model.save("Model")
for name, value in zip(model.metrics_names, results):
  print("%s: %.3f" % (name, value))
  
