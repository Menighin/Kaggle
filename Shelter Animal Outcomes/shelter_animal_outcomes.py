# https://www.kaggle.com/c/shelter-animal-outcomes
# Highest by cross: [-0.73212213 -0.73009975 -0.72435689]
#                   [-0.73078397 -0.73066029 -0.72416817] (Excel manipulation for shedding cats)

from BREED_GROUP import BREED_GROUPS
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
import warnings

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
IS_GOOD_WITH_KIDS = 'IsGoodWithKids'
COLOR = 'Color'
COLOR1 = 'Color1'
COLOR2 = 'Color2'
IS_PURE_COLOR = 'IsPureColor'
COLOR_CHARACTERISTIC = 'ColorCharacteristic'
HAS_NAME = 'HasName'
AGE_GROUP = 'AgeGroup'
WEEK_DAY = 'WeekDay'
WEEK_YEAR = 'WeekYear'
DAY_YEAR = 'DayYear'
WORKING_DAY = 'WorkingDay'
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
ANIMAL_SIZE = 'AnimalSize'
ANIMAL_TEMPERAMENT = 'AnimalTemperament'
ANIMAL_GROOMING = 'AnimalGrooming'
ANIMAL_TRAINABILITY = 'AnimalTrainability'
ANIMAL_HYPOALLERGENIC = 'AnimalHypoallernigic'
ANIMAL_SHEDDING = 'AnimalShedding'

# Global maps
COLORS_MAP = {'last': 0, 'NaN': -1}

# Extracted Data

# Data extracted with Helper get_dog_breed_sizes.py (NOT USING!)
small_breeds = [x.upper() for x in ['Affenpinscher', 'American Eskimo', 'Australian Terrier', 'Basenji', 'Basset Hound', 'Beagle', 'Bichon Frise', 'Bolognese', 'Border Terrier', 'Boston Terrier', 'Brussels Griffon', 'Bull Terrier', 'Bulldog', 'Cairn Terrier', 'Cardigan Welsh Corgi', 'Cavalier King Charles Spaniel', 'Cesky Terrier', 'Chihuahua', 'Chinese Crested', 'Cockapoo', 'Cocker Spaniel', 'Coton de Tulear', 'Dachshund', 'Dandie Dinmont Terrier', 'English Cocker Spaniel', 'English Toy Spaniel', 'Field Spaniel', 'Fox Terrier', 'French Bulldog', 'Glen of Imaal Terrier', 'Havanese', 'Italian Greyhound', 'Jack Russell Terrier', 'Japanese Chin', 'Lakeland Terrier', 'Lancashire Heeler', 'Lhasa Apso', 'Lowchen', 'Maltese', 'Maltese Shih Tzu', 'Maltipoo', 'Manchester Terrier', 'Miniature Pinscher', 'Miniature Schnauzer', 'Norfolk Terrier', 'Norwich Terrier', 'Papillon', 'Peekapoo', 'Pekingese', 'Pembroke Welsh Corgi', 'Petit Basset Griffon Vendeen', 'Pinscher', 'Pocket Beagle', 'Pomeranian', 'Pug', 'Puggle', 'Pyrenean Shepherd', 'Rat Terrier', 'Schipperke', 'Scottish Terrier', 'Sealyham Terrier', 'Shetland Sheepdog', 'Shiba Inu', 'Shih Tzu', 'Silky Terrier', 'Skye Terrier', 'Staffordshire Bull Terrier', 'Sussex Spaniel', 'Tibetan Spaniel', 'Tibetan Terrier', 'Toy Fox Terrier', 'Welsh Terrier', 'West Highland White Terrier', 'Yorkipoo', 'Yorkshire Terrier']]

medium_breeds = [x.upper() for x in ['Airedale Terrier', 'American English Coonhound', 'American Foxhound', 'Pit Bull', 'American Water Spaniel', 'Appenzeller Sennenhunde', 'Australian Cattle', 'Australian Shepherd', 'Azawakh', 'Barbet', 'Bearded Collie', 'Bedlington Terrier', 'Black and Tan Coonhound', 'Bluetick Coonhound', 'Border Collie', 'Boxer', 'Boykin Spaniel', 'Brittany', 'Canaan', 'Chesapeake Bay Retriever', 'Chinese Shar-Pei', 'Clumber Spaniel', 'Collie', 'Curly-Coated Retriever', 'Dalmatian', 'English Foxhound', 'English Setter', 'English Springer Spaniel', 'Entlebucher Mountain', 'Finnish Lapphund', 'Finnish Spitz', 'Flat-Coated Retriever', 'German Pinscher', 'German Shorthaired Pointer', 'Golden Retriever', 'Gordon Setter', 'Harrier', 'Ibizan Hound', 'Icelandic Sheepdog', 'Irish Red and White Setter', 'Irish Terrier', 'Irish Water Spaniel', 'Keeshond', 'Kerry Blue Terrier', 'Kooikerhondje', 'Korean Jindo', 'Mutt', 'Norwegian Buhund', 'Norwegian Elkhound', 'Norwegian Lundehund', 'Nova Scotia Duck Tolling Retriever', 'Pharaoh Hound', 'Plott', 'Pointer', 'Polish Lowland Sheepdog', 'Portuguese Water', 'Puli', 'Redbone Coonhound', 'Rottweiler', 'Samoyed', 'Siberian Husky', 'Small Munsterlander Pointer', 'Soft Coated Wheaten Terrier', 'Stabyhoun', 'Standard Schnauzer', 'Swedish Vallhund', 'Treeing Tennessee Brindle', 'Vizsla', 'Welsh Springer Spaniel', 'Whippet', 'Wirehaired Pointing Griffon', 'Xoloitzcuintli']]

large_breeds = [x.upper() for x in ['Afghan Hound', 'Akita', 'Alaskan Malamute', 'Anatolian Shepherd', 'Belgian Malinois', 'Belgian Sheepdog', 'Belgian Tervuren', 'Berger Picard', 'Bernese Mountain', 'Black Russian Terrier', 'Bloodhound', 'Borzoi', 'Bouvier des Flandres', 'Bracco Italiano', 'Briard', 'Bullmastiff', 'Cane Corso', 'Catahoula Leopard', 'Chinook', 'Chow Chow', 'Doberman Pinscher', 'Dogue de Bordeaux', 'German Shepherd', 'German Wirehaired Pointer', 'Giant Schnauzer', 'Goldador', 'Goldendoodle', 'Great Dane', 'Great Pyrenees', 'Greater Swiss Mountain', 'Greyhound', 'Irish Setter', 'Irish Wolfhound', 'Komondor', 'Kuvasz', 'Labradoodle', 'Labrador Retriever', 'Leonberger', 'Mastiff', 'Neapolitan Mastiff', 'Newfoundland', 'Old English Sheepdog', 'Otterhound', 'Poodle', 'Rhodesian Ridgeback', 'Saint Bernard', 'Saluki', 'Schnoodle', 'Scottish Deerhound', 'Sloughi', 'Tibetan Mastiff', 'Treeing Walker Coonhound', 'Weimaraner']]

def calculate_age(age):
    try:
        w, s = age.split()
        n = int(w)
        if 'year' in s:
            return int(n * 365)
        elif 'month' in s:
            return int(n * 30)
        elif 'week' in s:
            return int(n * 7)
        elif 'day' in s:
            return int(n)
    except:
        pass

def process_colors(color):
    global COLORS_MAP
    
    # Splitting colors
    i = 1
    cols = {}
    mix_colors = color.split('/')
    for c in mix_colors:

        # Color characteristic
        if len(c.split()) > 1:
            cols[COLOR_CHARACTERISTIC] = c.split()[1]

        # Removing colors characteristics
        c = c.split()[0]

        if c not in COLORS_MAP:
            COLORS_MAP[c] = COLORS_MAP['last']
            COLORS_MAP['last'] += 1
        cols['Color' + str(i)] = COLORS_MAP[c]
        i += 1

    if COLOR1 not in cols: cols[COLOR1] = COLORS_MAP['NaN']
    if COLOR2 not in cols: cols[COLOR2] = COLORS_MAP['NaN']
    if COLOR_CHARACTERISTIC not in cols: cols[COLOR_CHARACTERISTIC] = 'Pure'

    # IsPureColor
    if len(color.split('/')) == 1 and len(color.split()) == 1:
        cols[IS_PURE_COLOR] = 1
    else:
        cols[IS_PURE_COLOR] = 0

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
    
    for col in [ANIMAL_TYPE, BREED1, BREED2, COLOR_CHARACTERISTIC, COLOR]: # Labeling values
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

    # Week of the year
    week_year = lambda d: pd.Series({WEEK_YEAR: datetime.strptime(d, date_format).isocalendar()[1]})
    train = pd.concat([train, train[DATE_TIME].apply(week_year)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(week_year)], axis = 1)

    # WeekDay
    week_day = lambda d: pd.Series({WEEK_DAY: datetime.strptime(d, date_format).weekday()})
    train = pd.concat([train, train[DATE_TIME].apply(week_day)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(week_day)], axis = 1)

    # WorkingDay
    working_day = lambda d: pd.Series({WORKING_DAY: 0 if datetime.strptime(d, date_format).weekday == 5 or datetime.strptime(d, date_format).weekday == 6 else 1})
    train = pd.concat([train, train[DATE_TIME].apply(working_day)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(working_day)], axis = 1)

    # Day of the year
    day_year = lambda d: pd.Series({DAY_YEAR: datetime.strptime(d, date_format).timetuple().tm_yday})
    train = pd.concat([train, train[DATE_TIME].apply(day_year)], axis = 1)
    test  = pd.concat([test , test [DATE_TIME].apply(day_year)], axis = 1)

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
    popular_dogs_cats = ('Pit Bull Mix,Chihuahua Shorthair Mix,Labrador Retriever Mix,German Shepherd Mix,Australian Cattle Mix,Dachshund Mix,Boxer Mix,Miniature Poodle Mix,Border Collie Mix'.upper().split(',') + 
        'Domestic Shorthair Mix,Domestic Medium Hair Mix,Domestic Longhair Mix,Siamese Mix,Domestic Shorthair'.upper().split(','))
    is_it = 0
    for bd in popular_dogs_cats:
        if bd in b.upper():
            is_it = 1
            break

    return pd.Series({IS_POPULAR_BREED: is_it})

def is_breed_in(breed, breeds):
    for b in breeds:
        if b in breed:
            return True
    return False

def animal_size(b):
    if b.upper() in small_breeds or is_breed_in(b.upper(), small_breeds):       # Small
        return pd.Series({ANIMAL_SIZE: 1})
    elif b.upper() in medium_breeds or is_breed_in(b.upper(), medium_breeds):   # Medium
        return pd.Series({ANIMAL_SIZE: 2})
    elif b.upper() in large_breeds or is_breed_in(b.upper(), large_breeds):     # Large
        return pd.Series({ANIMAL_SIZE: 3})
    else:                                                                       # Unknown
        return pd.Series({ANIMAL_SIZE: 0})        

def is_good_with_kids(br):
    for b in br.upper().replace(' MIX', '').split('/'):
        if b in ' '.join(BREED_GROUPS['KIDS']['good']):
            return pd.Series({IS_GOOD_WITH_KIDS: 1})
        if b in ' '.join(BREED_GROUPS['KIDS']['not_good']):
            return pd.Series({IS_GOOD_WITH_KIDS: 0})
    return pd.Series({IS_GOOD_WITH_KIDS: 2})           

def animal_size_2(br):
    for b in br.upper().replace(' MIX', '').split('/'):
        if b in ' '.join(BREED_GROUPS['SIZE']['toy']):
            return pd.Series({ANIMAL_SIZE: 1})
        if b in ' '.join(BREED_GROUPS['SIZE']['small']):
            return pd.Series({ANIMAL_SIZE: 2})
        if b in ' '.join(BREED_GROUPS['SIZE']['medium']):
            return pd.Series({ANIMAL_SIZE: 3})
        if b in ' '.join(BREED_GROUPS['SIZE']['large']):
            return pd.Series({ANIMAL_SIZE: 4})
        if b in ' '.join(BREED_GROUPS['SIZE']['giant']):
            return pd.Series({ANIMAL_SIZE: 5})
    return pd.Series({ANIMAL_SIZE: 0}) 

def animal_temperament(br):
    for b in br.upper().replace(' MIX', '').split('/'):
        if b in ' '.join(BREED_GROUPS['TEMPERAMENT']['friendly']):
            return pd.Series({ANIMAL_TEMPERAMENT: 1})
        if b in ' '.join(BREED_GROUPS['TEMPERAMENT']['agressive']):
            return pd.Series({ANIMAL_TEMPERAMENT: 2})
    return pd.Series({ANIMAL_TEMPERAMENT: 0}) 

def animal_trainability(br):
    for b in br.upper().replace(' MIX', '').split('/'):
        if b in ' '.join(BREED_GROUPS['TRAINABILITY']['easy']):
            return pd.Series({ANIMAL_TRAINABILITY: 1})
        if b in ' '.join(BREED_GROUPS['TRAINABILITY']['medium']):
            return pd.Series({ANIMAL_TRAINABILITY: 2})
        if b in ' '.join(BREED_GROUPS['TRAINABILITY']['hard']):
            return pd.Series({ANIMAL_TRAINABILITY: 3})
    return pd.Series({ANIMAL_TRAINABILITY: 0}) 

def animal_grooming(br):
    for b in br.upper().replace(' MIX', '').split('/'):
        if b in ' '.join(BREED_GROUPS['GROOMING']['low']):
            return pd.Series({ANIMAL_GROOMING: 1})
        if b in ' '.join(BREED_GROUPS['GROOMING']['medium']):
            return pd.Series({ANIMAL_GROOMING: 2})
        if b in ' '.join(BREED_GROUPS['GROOMING']['high']):
            return pd.Series({ANIMAL_GROOMING: 3})
    return pd.Series({ANIMAL_GROOMING: 0}) 

def animal_hypoallergenic(br):
    for b in br.upper().replace(' MIX', '').split('/'):
        if b in ' '.join(BREED_GROUPS['HYPOALLERGENIC']['hypo']):
            return pd.Series({ANIMAL_HYPOALLERGENIC: 1})
    return pd.Series({ANIMAL_HYPOALLERGENIC: 0}) 

def animal_shedding(br):
    for b in br.upper().replace(' MIX', '').split('/'):
        if b in ' '.join(BREED_GROUPS['SHEDDING']['constant']):
            return pd.Series({ANIMAL_SHEDDING: 1})
        if b in ' '.join(BREED_GROUPS['SHEDDING']['minimal']):
            return pd.Series({ANIMAL_SHEDDING: 2})
    return pd.Series({ANIMAL_SHEDDING: 0}) 

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

    # AnimalSize
    train = pd.concat([train, train[BREED].apply(animal_size_2)], axis = 1)
    test  = pd.concat([test , test [BREED].apply(animal_size_2)], axis = 1)

    # IsGoodWithKids
    train = pd.concat([train, train[BREED].apply(is_good_with_kids)], axis = 1)
    test  = pd.concat([test , test [BREED].apply(is_good_with_kids)], axis = 1)

    # AnimalTemperament
    train = pd.concat([train, train[BREED].apply(animal_temperament)], axis = 1)
    test  = pd.concat([test , test [BREED].apply(animal_temperament)], axis = 1)

    # AnimalTrainability
    train = pd.concat([train, train[BREED].apply(animal_trainability)], axis = 1)
    test  = pd.concat([test , test [BREED].apply(animal_trainability)], axis = 1)

    # AnimalGrooming
    train = pd.concat([train, train[BREED].apply(animal_grooming)], axis = 1)
    test  = pd.concat([test , test [BREED].apply(animal_grooming)], axis = 1)

    # AnimalHypoallergenic
    train = pd.concat([train, train[BREED].apply(animal_hypoallergenic)], axis = 1)
    test  = pd.concat([test , test [BREED].apply(animal_hypoallergenic)], axis = 1)

    # AnimalShedding
    train = pd.concat([train, train[BREED].apply(animal_shedding)], axis = 1)
    test  = pd.concat([test , test [BREED].apply(animal_shedding)], axis = 1)
    
    # Labeling breeds
    for col in [BREED]: # Labeling values
        train[col] = train[col].fillna('NaN')
        test[col] = test[col].fillna('NaN')
        le = preprocessing.LabelEncoder().fit(np.append(train[col], test[col]))
        train[col] = le.transform(train[col])
        test[col] = le.transform(test[col])

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

    # Saving train and test CSV to not reprocess it again
    train.to_csv('train++.csv')
    test.to_csv('test++.csv')

    # Supressing warnings
    warnings.simplefilter('ignore')    

    # Not using: COLOR_CHARACTERISTIC
    predictors = [AGE_UPON_OUTCOME, COLOR1, COLOR2, IS_PURE_COLOR, ANIMAL_TYPE, HAS_NAME, AGE_GROUP, WEEK_DAY, WEEK_YEAR, DAY_YEAR, WORKING_DAY, MONTH, YEAR, EXIT_HOUR, IS_OPEN, IS_PURE_BREED, SEX, 
                  FERTILE, BREED, BREED1, BREED2, ANIMAL_SIZE, EXIT_MINUTE, HOLIDAY, QUARTER, IS_GOOD_WITH_KIDS, ANIMAL_TEMPERAMENT, ANIMAL_TRAINABILITY, ANIMAL_GROOMING,
                  ANIMAL_HYPOALLERGENIC, ANIMAL_SHEDDING]

    # alg = ensemble.GradientBoostingClassifier()
    # alg = xgb.XGBClassifier(max_depth = 7, n_estimators = 300, learning_rate = 0.05, silent = 1, objective='multi:softprob', subsample=0.85, colsample_bytree=0.75)
    alg = xgb.XGBClassifier(max_depth = 8, n_estimators = 200, learning_rate = 0.05, silent = 1, objective='multi:softprob', subsample=0.8, colsample_bytree=0.6)

    print('Training...')
    start_training = time.time()

    fit = alg.fit(train[predictors], train[OUTCOME_TYPE])

    print('Trained: ' + str(int(time.time() - start_training)) + 's')

    # Testing with cross validation
    logloss = cross_val_score(alg, train[predictors], train[OUTCOME_TYPE], cv=3, scoring='log_loss', verbose=0)
    print("LogLoss: " + str(logloss))
                    
    print('Predicting...')
    start_predictions = time.time()

    predictions = alg.predict_proba(test[predictors])

    print('Predicted: ' + str(int(time.time() - start_predictions)) + 's')

    submission = pd.DataFrame(predictions, index = test.index, columns = fit.classes_)
    submission.sort_index(inplace = True)
    submission.to_csv('kaggle.csv', index_label='ID') 

    

if __name__ == '__main__':
    main('-r' in sys.argv)