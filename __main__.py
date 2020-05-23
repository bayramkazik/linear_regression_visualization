# %% REQUIRED MODULES

!pip install -U numpy
!pip install -U tensorflow
!pip install -U matplotlib
!pip install -U tensorflow_datasets


# %% MODULE IMPORTS

import numpy as np
import tensorflow as tf
import logging
from matplotlib import pyplot as plt

# %% LOGGING CONFIG

import logging
logger = tf.get_logger()
logger.setLevel(logging.ERROR)


# %% LOADING DATASET

train_data, test_data = tf.keras.datasets.mnist.load_data(path="mnist.npz")

train_input, train_output = train_data
test_input, test_output = test_data

#
