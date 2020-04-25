import tensorflow as tf
from sloganValues import getAverageDimensions
import math


def get_dataset(file_path, **kwargs):
  dataset = tf.data.experimental.make_csv_dataset(
      file_path,
      batch_size=5, # Artificially small to make examples easier to show.
      label_name=LABEL_COLUMN,
      na_value="?",
      num_epochs=1,
      ignore_errors=True, 
      **kwargs)
  return dataset

def encodeSlogan(slogan):
    vals = getAverageDimensions(slogan)
    for i in range(len(vals)):
        vals[i] = math.floor(vals[i]*(10**8))
    return vals

raw_train_data = get_dataset("slogans.csv")