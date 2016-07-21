# https://www.kaggle.com/c/shelter-animal-outcomes
# Highest by cross: [-0.77862342 -0.76835471 -0.76439125]
import pandas as pd
from datetime import datetime
from sklearn import linear_model, tree, ensemble, preprocessing
from sklearn.cross_validation import train_test_split, cross_val_score
import xgboost as xgb
import numpy as np
import re
import math
import sys
import time

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
IS_POPULAR_BREED = 'IsPopularBreed'
COLOR = 'Color'
COLOR1 = 'Color1'
COLOR2 = 'Color2'
HAS_NAME = 'HasName'
AGE_GROUP = 'AgeGroup'
WEEK_DAY = 'WeekDay'
MONTH = 'Month'
QUARTER = 'Quarter'
YEAR = 'Year'
HOLIDAY = 'Holiday'
EXIT_HOUR = 'ExitHour'
EXIT_MINUTE = 'ExitMinute'
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
    

    for col in [ANIMAL_TYPE, BREED1, BREED2]: # Labeling values
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

def map_holidays(d):
    date = datetime.strptime(d, '%Y-%m-%d %H:%M:%S')

    # confederate Heroes
    if date.month == 1 and date.day == 19:
        return pd.Series({HOLIDAY: 1})
    # Texas Independance
    if date.month == 3 and date.day == 2:
        return pd.Series({HOLIDAY: 2})
    # San Jacinto Day        
    if date.month == 4 and date.day == 21:
        return pd.Series({HOLIDAY: 3})                       
    # Mothers Day        
    if date.month == 5 and date.day == 10:
        return pd.Series({HOLIDAY: 4})                       
    # Emancipation Day        
    if date.month == 6 and date.day == 19:
        return pd.Series({HOLIDAY: 5})
    # Fathers Day        
    if date.month == 6 and 18 <= date.day <= 22:
        return pd.Series({HOLIDAY: 6})
    # 4th July
    if date.month == 7 and date.day == 4:
        return pd.Series({HOLIDAY: 11})
    # Lyndon day       
    if date.month == 8 and date.day == 27:
        return pd.Series({HOLIDAY: 7})                       
    # Veterans day       
    if date.month == 11 and date.day == 11:
        return pd.Series({HOLIDAY: 8}) 
    # ThanksGiving                    
    if date.month == 11 and 25<=date.day <= 27:
        return pd.Series({HOLIDAY: 9})
    # Christmas                    
    if date.month == 12 and 23<=date.day <= 27:
        return pd.Series({HOLIDAY: 10})

    return pd.Series({HOLIDAY: 0}) 


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

    # Quarter
    quarter = lambda d: pd.Series({QUARTER: int(datetime.strptime(d, date_format).month / 4)})
    train = pd.concat([train, train[DATE_TIME].apply(quarter)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(quarter)], axis = 1)

    # Year
    year = lambda d: pd.Series({YEAR: datetime.strptime(d, date_format).year})
    train = pd.concat([train, train[DATE_TIME].apply(year)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(year)], axis = 1)

    # ExitHour
    exit_hour = lambda d: pd.Series({EXIT_HOUR: datetime.strptime(d, date_format).hour})
    train = pd.concat([train, train[DATE_TIME].apply(exit_hour)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(exit_hour)], axis = 1)

    # ExitMinute
    exit_minute = lambda d: pd.Series({EXIT_MINUTE: datetime.strptime(d, date_format).minute})
    train = pd.concat([train, train[DATE_TIME].apply(exit_minute)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(exit_minute)], axis = 1)

    # IsOpen
    is_open = lambda d: pd.Series({IS_OPEN: 1 if datetime.strptime(d, date_format).hour >= 11 and datetime.strptime(d, date_format).hour <= 19 else 0})
    train = pd.concat([train, train[DATE_TIME].apply(is_open)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(is_open)], axis = 1)

    # Holidays
    train = pd.concat([train, train[DATE_TIME].apply(map_holidays)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(map_holidays)], axis = 1)

def split_breed(b):
    bds = b.split('/')
    return pd.Series({BREED1: bds[0], BREED2: bds[1] if len(bds) > 1 else 'NaN'})

def is_popular_breed(b):
    # PivotTable on training data
    popular_dogs_cats = ('Pit Bull Mix,Chihuahua Shorthair Mix,Labrador Retriever Mix,German Shepherd Mix,Australian Cattle Dog Mix,Dachshund Mix,Boxer Mix,Miniature Poodle Mix,Border Collie Mix'.upper().split(',') + 
        'Domestic Shorthair Mix,Domestic Medium Hair Mix,Domestic Longhair Mix,Siamese Mix,Domestic Shorthair'.upper().split(','))
    is_it = 0
    for bd in popular_dogs_cats:
        if bd in b.upper():
            is_it = 1
            break

    return pd.Series({IS_POPULAR_BREED: is_it})

def add_breed_features():
    global test, train

    # IsPureBreed
    is_pure = lambda b: pd.Series({IS_PURE_BREED: 1 if 'Mix' not in b and '/' not in b else 0})
    train = pd.concat([train, train[BREED].apply(is_pure)], axis = 1)
    test  = pd.concat([test , test [BREED].apply(is_pure)], axis = 1)
   
    # Splitting breeds
    train = pd.concat([train, train[BREED].apply(split_breed)], axis = 1)
    test  = pd.concat([test , test [BREED].apply(split_breed)], axis = 1)

    # IsPopularBreed
    train = pd.concat([train, train[BREED].apply(is_popular_breed)], axis = 1)
    test  = pd.concat([test , test [BREED].apply(is_popular_breed)], axis = 1)

def add_sex_and_fertile():
    global test, train
    
    train[SEX_UPON_OUTCOME] = train[SEX_UPON_OUTCOME].fillna('Unknown')
    test[SEX_UPON_OUTCOME] = test[SEX_UPON_OUTCOME].fillna('Unknown')

    define_sex = lambda s: pd.Series({SEX: 0 if 'Male' in s else 1 if 'Female' in s else 2})
    train = pd.concat([train, train[SEX_UPON_OUTCOME].apply(define_sex)], axis = 1)
    test  = pd.concat([test , test[SEX_UPON_OUTCOME].apply(define_sex)], axis = 1)

    is_fertile = lambda s: pd.Series({FERTILE: 0 if 'Spayed' in s or 'Neutered' in s else 1 if 'Intact' in s else 2})
    train = pd.concat([train, train[SEX_UPON_OUTCOME].apply(is_fertile)], axis = 1)
    test  = pd.concat([test , test[SEX_UPON_OUTCOME].apply(is_fertile)], axis = 1)

def main(reprocess):
    global train, test
    
    if reprocess:
        # Base for training
        train = pd.read_csv('train.csv')

        # Base for testing
        test = pd.read_csv('test.csv')
        
        print('Cleaning and adding features...')
        start_add_and_clean = time.time()

        # Feature IsPureBreed
        add_breed_features()

        # Cleaning data
        clean()

        # Feature HasName
        add_has_name()

        # Feature AgeGroup
        add_age_group()

        # Feature of Datetime
        add_datetime_features()

        # Feature of Sex and Fertile
        add_sex_and_fertile()

        print('Cleaned and added: ' + str(int(time.time() - start_add_and_clean)) + 's')

    else:
        # Base for training
        train = pd.read_csv('train++.csv')

        # Base for testing
        test = pd.read_csv('test++.csv')

    # Not using: HOLIDAY, QUARTER
    predictors = [AGE_UPON_OUTCOME, COLOR1, COLOR2, ANIMAL_TYPE, HAS_NAME, AGE_GROUP, WEEK_DAY, MONTH, YEAR, EXIT_HOUR, IS_OPEN, IS_PURE_BREED, SEX, FERTILE, BREED1, BREED2, IS_POPULAR_BREED, EXIT_MINUTE]

    # alg = ensemble.GradientBoostingClassifier()
    # alg = xgb.XGBClassifier(max_depth = 7, n_estimators = 300, learning_rate = 0.05, silent = 1, objective='multi:softprob', subsample=0.85, colsample_bytree=0.75)


    #############################################################################
    train.ix[train.OutcomeType == 'Adoption', OUTCOME_TYPE] = 0
    train.ix[train.OutcomeType == 'Died', OUTCOME_TYPE] = 1
    train.ix[train.OutcomeType == 'Euthanasia', OUTCOME_TYPE] = 2
    train.ix[train.OutcomeType == 'Return_to_owner', OUTCOME_TYPE] = 3
    train.ix[train.OutcomeType == 'Transfer', OUTCOME_TYPE] = 4

    ids_test = test['ID']
    print('ids_test: ' + str(len(ids_test)))
    target = train[OUTCOME_TYPE]

    train.drop(OUTCOME_TYPE, axis=1, inplace=True)
    train.drop(ANIMAL_ID, axis=1, inplace=True)
    train.drop(BREED, axis=1, inplace=True)
    train.drop(OUTCOME_SUBTYPE, axis=1, inplace=True)
    train.drop(NAME, axis=1, inplace=True)
    train.drop(SEX_UPON_OUTCOME, axis=1, inplace=True)
    train.drop(DATE_TIME, axis=1, inplace=True)

    test.drop(BREED, axis=1, inplace=True)
    test.drop(NAME, axis=1, inplace=True)
    test.drop(DATE_TIME, axis=1, inplace=True)
    test.drop(SEX_UPON_OUTCOME, axis=1, inplace=True)
    test.drop('ID', axis=1, inplace=True)

    dtrain = xgb.DMatrix(train,target,missing = -9999) 
    dtest = xgb.DMatrix(test,missing = -9999)

    param1 = {'max_depth':7, 'eta':0.1, 'silent':1, 'objective':'multi:softprob','num_class':5,'eval_metric':'mlogloss','subsample':0.75,'colsample_bytree':0.85} 
    param2 = {'max_depth':6, 'eta':0.1, 'silent':1, 'objective':'multi:softprob','num_class':5,'eval_metric':'mlogloss','subsample':0.85,'colsample_bytree':0.75} 
    param3 = {'max_depth':8, 'eta':0.1, 'silent':1, 'objective':'multi:softprob','num_class':5,'eval_metric':'mlogloss','subsample':0.65,'colsample_bytree':0.75} 
    param4 = {'max_depth':9, 'eta':0.1, 'silent':1, 'objective':'multi:softprob','num_class':5,'eval_metric':'mlogloss','subsample':0.55,'colsample_bytree':0.65} 
    param5 = {'max_depth':10, 'eta':0.1, 'silent':1, 'objective':'multi:softprob','num_class':5,'eval_metric':'mlogloss','subsample':0.55,'colsample_bytree':0.55} 
    num_round = 125

    bst1 = xgb.train(param1, dtrain, num_round)
    bst2 = xgb.train(param2, dtrain, num_round) 
    bst3 = xgb.train(param3, dtrain, num_round) 
    bst4 = xgb.train(param3, dtrain, num_round) 
    bst5 = xgb.train(param3, dtrain, num_round)

    pred1 = bst1.predict(dtest)
    pred2 = bst2.predict(dtest) 
    pred3 = bst3.predict(dtest) 
    pred4 = bst4.predict(dtest) 
    pred5 = bst5.predict(dtest)

    print('pred1: ' + str(len(pred1['0'])))    
    

    ypred_submit = pd.DataFrame((pred1 + pred2 + pred3 + pred4 + pred5) / 5)

    print('ypred: ' + str(len(ypred_submit[0])))    

    #ypred_submit.to_csv('ypred.csv', index=False)
    #ids_test.to_csv('ids_test.csv', index=False)

    submission = pd.DataFrame() 
    submission["ID"] = ids_test.values 
    submission["Adoption"]= ypred_submit[0] 
    submission["Died"]= ypred_submit[1] 
    submission["Euthanasia"]= ypred_submit[2] 
    submission["Return_to_owner"]= ypred_submit[3] 
    submission["Transfer"]= ypred_submit[4] 
    submission.to_csv('submission.csv',index=False)


    ##############################################################################

    '''print('Training...')
    start_training = time.time()

    fit = alg.fit(train[predictors], train[OUTCOME_TYPE])

    print('Trained: ' + str(int(time.time() - start_training)) + 's')

    # Testing with cross validation
    print("LogLoss:")
    print(cross_val_score(alg, train[predictors], train[OUTCOME_TYPE], cv=3, scoring='log_loss', verbose=0))

    print('Predicting...')
    start_predictions = time.time()

    predictions = alg.predict_proba(test[predictors])

    print('Predicted: ' + str(int(time.time() - start_predictions)) + 's')

    submission = pd.DataFrame(predictions, index = test.index, columns = fit.classes_)
    submission.sort_index(inplace = True)
    submission.to_csv('kaggle.csv', index_label='ID')  

    # Saving train and test CSV to not reprocess it again
    train.to_csv('train++.csv')
    test.to_csv('test++.csv')'''

if __name__ == '__main__':
    main('-r' in sys.argv)