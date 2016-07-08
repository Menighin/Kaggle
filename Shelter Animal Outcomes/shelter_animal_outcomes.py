# https://www.kaggle.com/c/shelter-animal-outcomes
import pandas
from sklearn import linear_model
import numpy as np

animals = pandas.read_csv('train.csv')

print(animals.describe())