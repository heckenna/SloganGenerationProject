import tensorflow as tf
import time
from sloganValues import getAverageDimensions
import Valence_arousal_dominance_csvParser as vad
import EncodeSlogansToIndicies as esti
import math
import pandas as pd
import tensorflow_hub as hub
from sklearn.model_selection import train_test_split
import numpy as np
from testPlot import confusionArrayFromInOut, plotConfusionArray, AccuracyArrayFromInOut
import matplotlib.pyplot as plt

MAX_SLOGAN_LENGTH = 16  # enc.getMaxSloganLength()
EMBEDDING_DIM = 5
VOCAB_SIZE = vad.getVocabLength()


def lstToString(lst):
    print(lst)


def get_dataset(file_path, **kwargs):
  dataset = tf.data.experimental.make_csv_dataset(
      file_path,
      batch_size=5,  # Artificially small to make examples easier to show.
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


labels_list = ["Apparel", "Automotive", "Beauty", "Beverage", "Business", "Construction", "Dining", "Education", "Financial",
    "Food", "Health and Medicine", "Household", "Shopping and Retail", "Toiletries", "Tourism and Travel", "Transport and Logistics"]


# ## HUB EMBEDDING
# embedding = "https://tfhub.dev/google/tf2-preview/nnlm-en-dim50/1"
# embedding = "https://tfhub.dev/google/tf2-preview/nnlm-en-dim128/1"
# hub_layer = hub.KerasLayer(embedding, input_shape=[],
#                            dtype=tf.string, trainable=False)

# prepare embedding matrix
num_words = VOCAB_SIZE + 2
embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
for i in range(1, num_words):
    embedding_vector = vad.getAllDimensionsIndex(i)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector

model = tf.keras.Sequential()

# load pre-trained word embeddings into an Embedding layer
# note that we set trainable = False so as to keep the embeddings fixed
model.add(tf.keras.layers.Input(shape=(MAX_SLOGAN_LENGTH,), dtype='int32'))
model.add(tf.keras.layers.Embedding(num_words,
                            EMBEDDING_DIM,
                            embeddings_initializer=tf.keras.initializers.Constant(
                                embedding_matrix),
                            input_length=MAX_SLOGAN_LENGTH,
                            trainable=False))
model.add(tf.keras.layers.Conv1D(250, 5, activation='relu'))
model.add(tf.keras.layers.GlobalMaxPooling1D())
# # model.add(tf.keras.layers.Conv1D(128,5,activation='relu'))
# # model.add(tf.keras.layers.MaxPooling1D(5))
# # # model.add(tf.keras.layers.Conv1D(128,5,activation='relu'))
# # # model.add(tf.keras.layers.GlobalMaxPooling1D())
# # # model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(200, activation='relu'))
model.add(tf.keras.layers.Dense(100, activation='relu'))
model.add(tf.keras.layers.Dense(16, activation='softmax'))

#
# model.add(hub_layer)
# model.add(tf.keras.layers.Dense(500, activation='relu'))
# model.add(tf.keras.layers.Dense(100, activation='relu'))
# model.add(tf.keras.layers.Dense(50, activation='relu'))
# model.add(tf.keras.layers.Dense(16, activation='softmax'))

model.summary()

model.compile(optimizer='Adam',
              loss=tf.keras.losses.categorical_crossentropy,
              metrics=['accuracy'])


#
# print(categories.head())
# print(slogans.values)
listConvert = lambda x: [int(z.strip()) for z in x.replace(
    "[", "").replace("]", "").split(',')]
df = pd.read_csv("encodedSlogans.csv", index_col=0)
df2 = pd.read_csv("indexEncodedSlogans.csv", index_col=0,
                  converters={'IndexEncoded': listConvert})
df["IndexEncoded"] = df2["IndexEncoded"]

# Apparel Automotive
categories = df.loc[:, 'Apparel':'Transport and Logistics']
slogans = df.drop(
    df.loc[:, 'Apparel':'Transport and Logistics'].columns, axis=1)
slogans = slogans.drop(['EncodedValues'], axis=1)

train, test = train_test_split(df, test_size=0.4, random_state=7)
print(train)
test, validate = train_test_split(test, test_size=0.25, random_state=192)


categ = train.loc[:, 'Apparel':'Transport and Logistics']

slog = train.drop(
    df.loc[:, 'Apparel':'Transport and Logistics'].columns, axis=1)
slog = slog.drop(['EncodedValues'], axis=1)

test_categ = test.loc[:, 'Apparel':'Transport and Logistics']
test_slog = test.drop(
    df.loc[:, 'Apparel':'Transport and Logistics'].columns, axis=1)
test_slog = test_slog.drop(['EncodedValues'], axis=1)

val_categ = validate.loc[:, 'Apparel':'Transport and Logistics']
val_slog = validate.drop(
    df.loc[:, 'Apparel':'Transport and Logistics'].columns, axis=1)
val_slog = val_slog.drop(['EncodedValues'], axis=1)

# print(slog["IndexEncoded"][0][0])]

# ENCODED
traindata = tf.data.Dataset.from_tensor_slices(
    (slog["IndexEncoded"], categ.values))
testdata = tf.data.Dataset.from_tensor_slices(
    (test_slog["IndexEncoded"], test_categ.values))
valdata = tf.data.Dataset.from_tensor_slices(
    (val_slog["IndexEncoded"], val_categ.values))

# #UNENCODED
# traindata = tf.data.Dataset.from_tensor_slices((slog["Slogan"], categ.values))
# testdata = tf.data.Dataset.from_tensor_slices((test_slog["Slogan"], test_categ.values))
# valdata = tf.data.Dataset.from_tensor_slices((val_slog["Slogan"], val_categ.values))
# print(valdata)

# slogans = slogans.apply(lstToString)
# print(slogans)
# dataset = tf.data.Dataset.from_tensor_slices((slogans['IndexEncoded'], categories.values))
# dataset =  tf.data.Dataset.from_tensor_slices(slogans.values)

# print(dataset)
# ex_batch, labels_batch =next(iter(traindata.batch(10)))

# print(ex_batch)
# print(labels_batch)

# print(hub_layer(ex_batch[:3]))
class_weights = {
  0: 1/163,
  1: 1/478,
  2: 1/388,
  3: 1/872,
  4: 1/1369,
  5: 1/261,
  6: 1/497,
  7: 1/358,
  8: 1/254,
  9: 1/688,
  10: 1/418,
  11: 1/656,
  12: 1/584,
  13: 1/326,
  14: 1/520,
  15: 1/660
}

es = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy',
                              min_delta=0,
                              patience=500,
                              verbose=0, mode='max')
startTime = time.time()
history = model.fit(traindata.shuffle(10000).batch(512),
                     epochs=500,
                     validation_data=valdata.batch(512),
                     verbose=1,
                     callbacks=[es])
                      # , class_weight = class_weights)
endtime=time.time()
print("Training time taken:", - startTime + endtime)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc = 'upper left')
# plt.show()

# model = tf.keras.models.load_model('saved_models/hubModel')
model.save("saved_models\hubModel")
# model.save("saved_models\convModel")
# prediction_input = esti.stringToList("Melts in Your Mouth, Not in Your Hands")
# prediction_input = esti.sloganToIndicies(prediction_input)
# output = model.predict([prediction_input])

# temp = output[0].argsort()
# ranks = np.empty_like(temp)
# ranks[temp] = np.arange(len(output[0]))
# for i in range(len(labels_list)):
#   print(ranks[i],"\t:",labels_list[i])

predictInput=testdata.batch(len(train))
print(predictInput)

# categ = train.loc[:,'Apparel':'Transport and Logistics']

actual=test.loc[:, 'Apparel':'Transport and Logistics'].apply(
    esti.lster, axis = 1)
actual=actual.map(np.argmax)

results=model.evaluate(predictInput, verbose = 2)
predictions= np.argmax(model.predict(predictInput, verbose=2), axis = 1)
print(max(actual))
print(max(predictions))
print("accuracy: ", AccuracyArrayFromInOut(actual, predictions))
confArr=confusionArrayFromInOut(actual, predictions)
print(confArr)
#plotConfusionArray(confArr)
for name, value in zip(model.metrics_names, results):
  print("%s: %.3f" % (name, value))
# """
