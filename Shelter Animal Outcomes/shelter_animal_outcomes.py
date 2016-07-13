# https://www.kaggle.com/c/shelter-animal-outcomes
import pandas
from sklearn import linear_model, tree, ensemble, preprocessing
from sklearn.cross_validation import train_test_split, cross_val_score
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

def clean(train, test):
    train[AGE_UPON_OUTCOME] = train[AGE_UPON_OUTCOME].apply(calculate_age) # Age to days
    train[AGE_UPON_OUTCOME] = train[AGE_UPON_OUTCOME].fillna(train[AGE_UPON_OUTCOME].median()) # Fill empty
    test[AGE_UPON_OUTCOME] = test[AGE_UPON_OUTCOME].apply(calculate_age) # Age to days
    test[AGE_UPON_OUTCOME] = test[AGE_UPON_OUTCOME].fillna(test[AGE_UPON_OUTCOME].median()) # Fill empty
    
    for col in [ANIMAL_TYPE, SEX_UPON_OUTCOME, BREED, COLOR]: # Labeling values
        train[col] = train[col].fillna('NaN')
        test[col] = test[col].fillna('NaN')
        le = preprocessing.LabelEncoder().fit(np.append(train[col], test[col]))
        train[col] = le.transform(train[col])
        test[col] = le.transform(test[col])

def main():
    # Base for training
    train = pandas.read_csv('train.csv')

    # Base for testing
    test = pandas.read_csv('test.csv')

    # Cleaning data
    clean(train, test)

    predictors = [AGE_UPON_OUTCOME, COLOR, BREED, ANIMAL_TYPE, SEX_UPON_OUTCOME]

    #alg = linear_model.LogisticRegression(random_state=1)
    #alg = tree.DecisionTreeClassifier()
    alg = ensemble.GradientBoostingClassifier()

    fit = alg.fit(train[predictors], train[OUTCOME_TYPE])

    # Testing with cross validation
    #print("LogLoss:")
    #print(cross_val_score(alg, train[predictors], train[OUTCOME_TYPE], cv=3, scoring='log_loss', verbose=0))

    predictions = alg.predict_proba(test[predictors])

    submission = pandas.DataFrame(predictions, index = test.index, columns = fit.classes_)
    submission.sort_index(inplace = True)
    submission.to_csv("kaggle.csv", index_label="ID")   

if __name__ == '__main__':
    main()