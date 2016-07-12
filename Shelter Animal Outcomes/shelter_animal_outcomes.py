# https://www.kaggle.com/c/shelter-animal-outcomes
import pandas
from sklearn import linear_model, tree, ensemble
import numpy as np
import re
import math

# Constant column names
ANIMAL_ID = 'AnimalID'
NAME = 'Name'
DATE_TIME = 'DateTime'
OUTCOME_TYPE = 'OutcomeType'
OUTCOME_SUBTYPE = 'OutcomeSubtype'
ANIMAL_TYPE = 'AnimalType'
SEX_UPON_OUTCOME = 'SexuponOutcome'
AGE_UPON_OUTCOME = 'AgeuponOutcome'
BREED = 'Breed'
COLOR = 'Color'

# Maps
MAP_COLORS = {'last': 0}
MAP_BREEDS = {'last': 0}
MAP_ANIMAL_TYPE = {'Dog': 0, 'Cat': 1}
MAP_SEX = {'last': 0}

def calculate_age(age):
    try:
        w, s = age.split()
        n = int(w)
        if 'year' in s:
            return n * 365
        elif 'month' in s:
            return n * 30
        elif 'week' in s:
            return n * 7
        elif 'day' in s:
            return n
    except:
        pass

def map_colors(color):
    if color not in MAP_COLORS:
        MAP_COLORS[color] = MAP_COLORS['last']
        MAP_COLORS['last'] += 1
    return MAP_COLORS[color]

def map_breeds(breed):
    if breed not in MAP_BREEDS:
        MAP_BREEDS[breed] = MAP_BREEDS['last']
        MAP_BREEDS['last'] += 1
    return MAP_BREEDS[breed]

def map_animal_type(type):
    return MAP_ANIMAL_TYPE[type]

def map_sex(sex):
    if sex not in MAP_SEX:
        MAP_SEX[sex] = MAP_SEX['last']
        MAP_SEX['last'] += 1
    return MAP_SEX[sex]

def clean(data):
    data[AGE_UPON_OUTCOME] = data[AGE_UPON_OUTCOME].apply(calculate_age) # Age to days
    data[AGE_UPON_OUTCOME] = data[AGE_UPON_OUTCOME].fillna(data[AGE_UPON_OUTCOME].median()) # Fill empty
    data[COLOR] = data[COLOR].apply(map_colors) # Map colors to numbers
    data[BREED] = data[BREED].apply(map_breeds) # Map breeds to numbers
    data[ANIMAL_TYPE] = data[ANIMAL_TYPE].apply(map_animal_type) # Map animal types
    data[SEX_UPON_OUTCOME] = data[SEX_UPON_OUTCOME].apply(map_sex) # Map sex

def main():
    # Base for training
    train = pandas.read_csv('train.csv')
    clean(train)

    # Base for testing
    test = pandas.read_csv('test.csv')
    clean(test)

    predictors = [AGE_UPON_OUTCOME, COLOR, BREED, ANIMAL_TYPE, SEX_UPON_OUTCOME]

    #alg = linear_model.LogisticRegression(random_state=1)
    #alg = tree.DecisionTreeClassifier()
    alg = ensemble.GradientBoostingClassifier()

    alg.fit(train[predictors], train[OUTCOME_TYPE])

    predictions = alg.predict(test[predictors])

    submission = pandas.DataFrame({
        'ID': test['ID'],
        'Adoption': predictions == 'Adoption',
        'Died': predictions == 'Died',
        'Euthanasia': predictions == 'Euthanasia',
        'Return_to_owner': predictions == 'Return_to_owner',
        'Transfer': predictions == 'Transfer'
    })

    submission = submission[['ID', 'Adoption', 'Died', 'Euthanasia', 'Return_to_owner', 'Transfer']]

    submission.to_csv("kaggle.csv", header=True, index=False)

if __name__ == '__main__':
    main()