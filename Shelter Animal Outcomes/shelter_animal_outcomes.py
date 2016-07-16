# https://www.kaggle.com/c/shelter-animal-outcomes
# Highest by cross: [-0.78491288 -0.77744353 -0.77270355]
import pandas as pd
from datetime import datetime
from sklearn import linear_model, tree, ensemble, preprocessing
from sklearn.cross_validation import train_test_split, cross_val_score
import numpy as np
import re
import math

# Data frames
train = {}
test = {}

# Constant feature names
ANIMAL_ID = 'AnimalID'
NAME = 'Name'
DATE_TIME = 'DateTime'
OUTCOME_TYPE = 'OutcomeType'
OUTCOME_SUBTYPE = 'OutcomeSubtype'
ANIMAL_TYPE = 'AnimalType'
SEX_UPON_OUTCOME = 'SexuponOutcome'
AGE_UPON_OUTCOME = 'AgeuponOutcome'
BREED = 'Breed'
BREED1 = 'Breed1'
BREED2 = 'Breed2'
COLOR = 'Color'
COLOR1 = 'Color1'
COLOR2 = 'Color2'
HAS_NAME = 'HasName'
AGE_GROUP = 'AgeGroup'
WEEK_DAY = 'WeekDay'
MONTH = 'Month'
YEAR = 'Year'
EXIT_HOUR = 'ExitHour'
IS_OPEN = 'IsOpen'
IS_PURE_BREED = 'IsPureBreed'
SEX = 'Sex'
FERTILE = 'Fertile'

# Global maps
COLORS_MAP = {'last': 0, 'NaN': -1}

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

def process_colors(color):
    global COLORS_MAP
    i = 1
    cols = {}
    for c in color.split('/'):

        # Removing colors descriptors
        c = ' '.join([w for w in c.split(' ') if len(c.split(' ')) > 1 and w not in ['Cream', 'Tabby', 'Brindle', 'Smoke', 'Tiger', 'Merle', 'Tick', 'Point']])

        if c not in COLORS_MAP:
            COLORS_MAP[c] = COLORS_MAP['last']
            COLORS_MAP['last'] += 1
        cols['Color' + str(i)] = COLORS_MAP[c]
        i += 1
    if COLOR1 not in cols: cols[COLOR1] = COLORS_MAP['NaN']
    if COLOR2 not in cols: cols[COLOR2] = COLORS_MAP['NaN']
    return pd.Series(cols)

def clean():
    global train
    global test

    # Age
    train[AGE_UPON_OUTCOME] = train[AGE_UPON_OUTCOME].apply(calculate_age) # Age to days
    train[AGE_UPON_OUTCOME] = train[AGE_UPON_OUTCOME].fillna(train[AGE_UPON_OUTCOME].median()) # Fill empty
    test[AGE_UPON_OUTCOME] = test[AGE_UPON_OUTCOME].apply(calculate_age) # Age to days
    test[AGE_UPON_OUTCOME] = test[AGE_UPON_OUTCOME].fillna(test[AGE_UPON_OUTCOME].median()) # Fill empty
    
    # Colors
    train = pd.concat([train, train[COLOR].apply(process_colors)], axis = 1)
    test = pd.concat([test, test[COLOR].apply(process_colors)], axis = 1)
    train.drop(COLOR, axis=1, inplace=True)
    test.drop(COLOR, axis=1, inplace=True)
    

    for col in [ANIMAL_TYPE, BREED]: # Labeling values
        train[col] = train[col].fillna('NaN')
        test[col] = test[col].fillna('NaN')
        le = preprocessing.LabelEncoder().fit(np.append(train[col], test[col]))
        train[col] = le.transform(train[col])
        test[col] = le.transform(test[col])

def add_has_name():
    global train
    global test

    train = pd.concat([train, train[NAME].apply(lambda n: pd.Series({HAS_NAME: 0 if pd.isnull(n) else 1}))], axis = 1)
    test = pd.concat([test, test[NAME].apply(lambda n: pd.Series({HAS_NAME: 0 if pd.isnull(n) else 1}))], axis = 1)

def map_age_group(age):
    g = 0
    if age <= 30 * 6: # New Born
        g = 0
    elif age <= 30 * 18: # Junior
        g = 1
    elif age <= 365 * 3: # Prime
        g = 2
    elif age <= 365 * 6: # Mature
        g = 3
    elif age <= 360 * 10: # Senior
        g = 4
    else: # Geriatric
        g = 5
    return pd.Series({AGE_GROUP: g})

def add_age_group():
    global test, train
    train = pd.concat([train, train[AGE_UPON_OUTCOME].apply(map_age_group)], axis = 1)
    test  = pd.concat([test , test [AGE_UPON_OUTCOME].apply(map_age_group)], axis = 1)

def add_datetime_features():
    global test, train

    date_format = '%Y-%m-%d %H:%M:%S'

    # WeekDay
    week_day = lambda d: pd.Series({WEEK_DAY: datetime.strptime(d, date_format).weekday()})
    train = pd.concat([train, train[DATE_TIME].apply(week_day)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(week_day)], axis = 1)

    # Month
    month = lambda d: pd.Series({MONTH: datetime.strptime(d, date_format).month})
    train = pd.concat([train, train[DATE_TIME].apply(month)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(month)], axis = 1)

    # Year
    year = lambda d: pd.Series({YEAR: datetime.strptime(d, date_format).year})
    train = pd.concat([train, train[DATE_TIME].apply(year)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(year)], axis = 1)

    # ExitHour
    exit_hour = lambda d: pd.Series({EXIT_HOUR: datetime.strptime(d, date_format).hour})
    train = pd.concat([train, train[DATE_TIME].apply(exit_hour)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(exit_hour)], axis = 1)

    # IsOpen
    is_open = lambda d: pd.Series({IS_OPEN: 1 if datetime.strptime(d, date_format).hour >= 11 and datetime.strptime(d, date_format).hour <= 19 else 0})
    train = pd.concat([train, train[DATE_TIME].apply(is_open)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(is_open)], axis = 1)


def add_is_pure_breed():
    global test, train

    is_pure = lambda b: pd.Series({IS_PURE_BREED: 1 if 'Mix' not in b else 0})
    train = pd.concat([train, train[DATE_TIME].apply(is_pure)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(is_pure)], axis = 1)

def add_sex_and_fertile():
    global test, train
    
    train[SEX_UPON_OUTCOME] = train[SEX_UPON_OUTCOME].fillna('Unknown')
    test[SEX_UPON_OUTCOME] = test[SEX_UPON_OUTCOME].fillna('Unknown')

    define_sex = lambda s: pd.Series({SEX: 0 if 'Male' in s else 1})
    train = pd.concat([train, train[SEX_UPON_OUTCOME].apply(define_sex)], axis = 1)
    test  = pd.concat([test , test[SEX_UPON_OUTCOME].apply(define_sex)], axis = 1)

    is_fertile = lambda s: pd.Series({FERTILE: 0 if 'Spayed' in s or 'Neutered' in s else 1})
    train = pd.concat([train, train[SEX_UPON_OUTCOME].apply(is_fertile)], axis = 1)
    test  = pd.concat([test , test[SEX_UPON_OUTCOME].apply(is_fertile)], axis = 1)

def main():
    global train
    global test

    # Base for training
    train = pd.read_csv('train.csv')

    # Base for testing
    test = pd.read_csv('test.csv')

    # Feature IsPureBreed
    add_is_pure_breed()

    # Cleaning data
    clean()

    # Feature HasName
    add_has_name()

    # Feature AgeGroup
    add_age_group()

    # Feature WeekDay, ExitHour, WorkingDay and Holiday
    add_datetime_features()

    # Feature of Sex and Fertile
    add_sex_and_fertile()

    predictors = [AGE_UPON_OUTCOME, COLOR1, COLOR2, BREED, ANIMAL_TYPE, HAS_NAME, AGE_GROUP, WEEK_DAY, MONTH, YEAR, EXIT_HOUR, IS_OPEN, IS_PURE_BREED, SEX, FERTILE]

    #alg = linear_model.LogisticRegression(random_state=1)
    #alg = tree.DecisionTreeClassifier()
    alg = ensemble.GradientBoostingClassifier()

    fit = alg.fit(train[predictors], train[OUTCOME_TYPE])

    # Testing with cross validation
    print("LogLoss:")
    print(cross_val_score(alg, train[predictors], train[OUTCOME_TYPE], cv=3, scoring='log_loss', verbose=0))

    predictions = alg.predict_proba(test[predictors])

    submission = pd.DataFrame(predictions, index = test.index, columns = fit.classes_)
    submission.sort_index(inplace = True)
    submission.to_csv("kaggle.csv", index_label="ID")   

if __name__ == '__main__':
    main()