# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qgPTtGyYgHxP8fXRGR2LH2W0t7I2OLUZ
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 11:57:43 2019
TCD ML Comp. 2019/20 - Income Pred. (Group)
Goal: Predict the income.

@author: vishal
Kindly Refer to AnalyseData.py for explanation of each step.

Training Dataset: tcd-ml-1920-group-income-train.csv
Testing Dataset: tcd-ml-1920-group-income-test.csv

Regression Model: Linear
Mean Absolute Error: 26337.441347977998
Mean Squared Error: 3213609856.9474673
Root Mean Squared Error: 54895.22631266166
IDE: Pycharm
Platform: GCP Ubuntu 16.04
"""

# based on https://github.com/skarode96/kaggle-income-prediction/blob/master/IncomePredictor.py#L10

#!pip install feature_engine
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import KFold

y_column_name = 'Total_Income'

#trainDataPath = "old_data/tcd ml 2019-20 income prediction training (with labels).csv"
#testDataPath = "old_data/tcd ml 2019-20 income prediction test (without labels).csv"

#colab='/content/drive/My Drive/Kaggel_competition2/'
trainDataPath = "data/tcd-ml-1920-group-income-train.csv"
testDataPath = "data/tcd-ml-1920-group-income-test.csv"
subDataPath = "data/tcd-ml-1920-group-income-submission.csv"
subDataPath_result = "data/tcd-ml-1920-group-income-submission_result_CV.csv"

#rename_columns
def rename_column_name(dataset):
    dataset.rename(columns={'Instance':'Instance',
                            'Year of Record':'Year_of_Record',
                            'Housing Situation':'Housing',
                            'Crime Level in the City of Employement':'Crime_Level',
                            'Work Experience in Current Job [years]':'Work_Exp',
                            'Satisfation with employer':'Satisfation',
                            'Gender':'Gender', 
                            'Age':'Age', 
                            'Country':'Country',
                            'Size of City':'Size_of_City',
                            'Profession':'Profession',
                            'University Degree':'Degree',
                            'Wears Glasses':'Glasses',
                            'Hair Color':'Hair',
                            'Body Height [cm]':'Height',
                            'Yearly Income in addition to Salary (e.g. Rental Income)':'addition_salary',
                            'Total Yearly Income [EUR]':'Total_Income'},
    inplace=True)
    return dataset

selected_training_columns = [#'Instance',
                            'Year_of_Record',
                            'Housing',
                            'Crime_Level',
                            'Work_Exp',
                            'Satisfation',
                            'Gender', 
                            'Age', 
                            'Country',
                            'Size_of_City',
                            'Profession',
                            'Degree',
                            'Glasses',
                            'Hair',
                            'Height',
                            'addition_salary',
                            'Total_Income'
                            ]

    
# read_data
def read_data(trainDataPath, testDataPath):
    train_data = pd.read_csv(trainDataPath)#, nrows=50000)
    test_data = pd.read_csv(testDataPath)#, nrows=50000)
    
    train_data=rename_column_name(train_data)
    test_data=rename_column_name(test_data)

    return train_data, test_data

# remove_outliers
def remove_outliers(dataset):
    dataset = dataset[dataset['Total_Income'] > 0]
    return dataset

# preprocess_dataset
def preprocess_dataset(dataset1):
    dataset = dataset1[selected_training_columns].copy()
    process_Year_of_Record(dataset)#error
    process_Housing(dataset)######
    process_Work_Exp(dataset)###### error
    process_Satisfation(dataset)
    process_Gender(dataset)
    process_Country(dataset)
    # process_Size_of_City(dataset)
    process_Profession(dataset)
    process_Degree(dataset)
    process_Hair(dataset)
    process_addition_salary(dataset)###### error
    
  #  process_Crime_Level(dataset)####### not needed
  #  process_Age(dataset)#not needed
  #  process_Glasses(dataset)# not needMissinged
  #  process_Height(dataset)# not needed
    return dataset

def process_Year_of_Record(dataset):
    year_median = dataset['Year_of_Record'].median()
    dataset['Year_of_Record'].replace(np.nan, year_median, inplace=True)

def process_Housing(dataset):
    dataset['Housing'].replace(0, 'Missing', inplace=True)
    dataset['Housing'].replace(np.nan, 'Missing', inplace=True)

def process_Work_Exp(dataset):
    dataset['Work_Exp'].replace('#NUM!', 0, inplace=True)
    dataset['Work_Exp'] = pd.to_numeric(dataset['Work_Exp'])
    # dataset['Work_Exp'] = dataset['Work_Exp'].astype(str).astype(float)           
#    Work_Exp_median = dataset['Work_Exp'].median()
    #dataset['Work_Exp'].replace('0', 'Missing', inplace=True)

def process_Satisfation(dataset):
    dataset['Satisfation'].replace(np.nan, 'Missing', inplace=True)

def process_Gender(dataset):
    dataset['Gender'].replace('0', 'Missing', inplace=True)
    dataset['Gender'].replace('Other', 'Missing', inplace=True)
    dataset['Gender'].replace('Unknown', 'Missing', inplace=True)
    dataset['Gender'].replace(np.nan, 'Missing', inplace=True)
    dataset['Gender'].replace('f', 'female', inplace=True)

def process_Age(dataset):
    age_median = dataset['Age'].median() 
    dataset['Age'].replace(np.nan, age_median, inplace=True)
    dataset['Age'] = (dataset['Age'] * dataset['Age']) ** (0.5)## ???

def process_Country(dataset):
    dataset['Country'].replace('0', 'Missing', inplace=True)

def process_Size_of_City(dataset):
    dataset['Size_of_City'] = np.log(dataset['Size_of_City']+1)

def process_Profession(dataset):
    dataset['Profession'].replace(np.nan, 'Missing', inplace=True)
    
def process_Degree(dataset):
    dataset['Degree'].replace(np.nan, 'Missing', inplace=True)
    dataset['Degree'].replace('0', 'Missing', inplace=True)
    
def process_Hair(dataset):
    dataset['Hair'].replace('0', 'Missing', inplace=True)
    dataset['Hair'].replace('Unknown', 'Missing', inplace=True)
    dataset['Hair'].replace(np.nan, 'Missing', inplace=True)

def process_addition_salary(dataset):
    dataset['addition_salary'] = dataset['addition_salary'].str.replace('([A-Za-z]+)', '')
    dataset['addition_salary'] = pd.to_numeric(dataset['addition_salary'])
#    dataset['addition_salary'] = dataset.to_numeric(dataset['addition_salary'])
#    dataset['addition_salary'] = dataset['addition_salary'].astype(str).astype(float)
    dataset['addition_salary'].head()

#def calc_smooth_mean(df, df1, df2, cat_name, target, weight):
#    mean = df[target].mean()
#    # Compute the number of values and the mean of each group
#    agg = df.groupby(cat_name)[target].agg(['count', 'mean'])
#    counts = agg['count']
#    means = agg['mean']
#    # Compute the "smoothed" means
#    smooth = (counts * means + weight * mean) / (counts + weight)
#    # Replace each value by the according smoothed mean
#    if df2 is None:
#        return df1[cat_name].map(smooth)
#    else:
#        return df1[cat_name].map(smooth),df2[cat_name].map(smooth.to_dict())
#    
    
def smoothing_target_encoder(dataset, mean, cat_name, weight ):
    # Compute the number of values and the mean of each group
    agg = dataset.groupby(cat_name)[y_column_name].agg(['count', 'mean'])
    counts = agg['count']
    means = agg['mean']

    # Compute the 'smoothed' means
    smooth = (counts * means + weight * mean) / (counts + weight)

    # Replace each value by the according smoothed mean
    return dataset[cat_name].map(smooth)    

def encode_Cat_col(dataset, WEIGHT):
    # Compute the global mean
    target_mean = dataset[y_column_name].mean()
    
    dataset['Housing'] = smoothing_target_encoder(dataset, target_mean, cat_name='Housing', weight=WEIGHT)
    dataset['Satisfation'] = smoothing_target_encoder(dataset, target_mean, cat_name='Satisfation', weight=WEIGHT)
    dataset['Gender'] = smoothing_target_encoder(dataset, target_mean, cat_name='Gender', weight=WEIGHT)
    dataset['Country'] = smoothing_target_encoder(dataset, target_mean, cat_name='Country', weight=WEIGHT)
    dataset['Profession'] = smoothing_target_encoder(dataset, target_mean, cat_name='Profession', weight=WEIGHT)
    dataset['Degree'] = smoothing_target_encoder(dataset, target_mean, cat_name='Degree', weight=WEIGHT)
    dataset['Hair'] = smoothing_target_encoder(dataset, target_mean, cat_name='Hair', weight=WEIGHT)

#def target_encoder_Cat_col2(df, column, target='Total_Income', index=None, method='mean'):
#    index = df.index if index is None else index # Encode the entire input df if no specific indices is supplied
#    if method == 'mean':
#        encoded_column = df[column].map(df.iloc[index].groupby(column)[target].mean())
#    elif method == 'median':
#        encoded_column = df[column].map(df.iloc[index].groupby(column)[target].median())
#    elif method == 'std':
#        encoded_column = df[column].map(df.iloc[index].groupby(column)[target].std())
#    else:
#        raise ValueError("Incorrect method supplied: '{}'. Must be one of 'mean', 'median', 'std'".format(method))
#    return encoded_column
#
#def encode_Cat_col2(dataset):
#    dataset['Housing'] = target_encoder_Cat_col2(dataset, column='Housing')
#    dataset['Satisfation'] = target_encoder_Cat_col2(dataset, column='Satisfation')
#



def calculate_metrics(y_test,y_pred):
    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

def predict_prod_data(unlabelled_preprocessed_dataset, regressor):
    Y_prod_predictions = np.exp(regressor.predict(unlabelled_preprocessed_dataset))
    Y_prod_predictions = Y_prod_predictions
    df = pd.DataFrame({'Income': Y_prod_predictions})
    df.to_csv('TEST' + subDataPath, index=False)

def predict_prod_data2(X_test, clf):
    pre_test_lgb = clf.predict(X_test)
    YDataFrame = pd.DataFrame(np.exp(pre_test_lgb))

    df_test_result = pd.read_csv(subDataPath)
    df_test_result['Total Yearly Income [EUR]'] = YDataFrame.iloc[:,-1]
    df_test_result.to_csv(subDataPath_result, index = False)

def cross_val_cat(train_data, y, X_test):
    k = 2
    iter_rounds = 20000
    y_test_pred = [0] * len(X_test)
    kf = KFold(n_splits = k, random_state = 1, shuffle = True)

    cat_model = CatBoostRegressor(iterations=iter_rounds, task_type="GPU")
    for i, (train_index, val_index) in enumerate(kf.split(train_data)):
        y_train, y_val = y.iloc[train_index], y.iloc[val_index]
        X_train, X_val = train_data.iloc[train_index], train_data.iloc[val_index]
        print("Fold number ", i)

        y_train_log = np.log(y_train)
        y_val_log = np.log(y_val)
        trn_data = Pool(X_val, label=y_val_log)

        cat_model.fit(X_train, y_train_log, eval_set=trn_data, use_best_model=True)
        
        y_pred_log = cat_model.predict(X_val)
        y_pred = np.exp(y_pred_log)
        calculate_metrics(y_val,y_pred)

        y_test_pred_log = cat_model.predict(X_test)
        y_test_pred += np.exp(y_test_pred_log)

    mean_y_pred = y_test_pred/k
    YDataFrame = pd.DataFrame(mean_y_pred)

    df_test_result = pd.read_csv(subDataPath)
    df_test_result['Total Yearly Income [EUR]'] = YDataFrame.iloc[:,-1]
    df_test_result.to_csv(subDataPath_result, index = False)



#### 1. read data #######
train_data, test_data = read_data(trainDataPath, testDataPath)

#train_data=train_data.append(test_data)
train_data.info()


######################
#### 2. remove outliers########
#train_data = remove_outliers(train_data)
########################
##### 3. do preprocessing #########
train_data_preprocessed = preprocess_dataset(train_data)
test_data_preprocessed = preprocess_dataset(test_data)
#################################
train_data_preprocessed.info()
train_data_preprocessed.isnull().sum()

test_data_preprocessed.info()
test_data_preprocessed.isnull().sum()


test_data_preprocessed[y_column_name].replace(np.nan, 0, inplace=True)
train_data_preprocessed=train_data_preprocessed.append(test_data_preprocessed)
train_data_preprocessed.isnull().sum()
############################ 

######## 5. Do hot encoding #########
#encoding_column_list = ['Housing', 'Satisfation', 'Gender', 'Country', 'Profession', 'Degree', 'Hair']

encode_Cat_col(train_data_preprocessed,WEIGHT=5)

train_data_preprocessed.info()
train_data_preprocessed.isnull().sum()

######### 4. extract y column #########
test_data_preprocessed = train_data_preprocessed.loc[train_data_preprocessed[y_column_name] == 0].copy()
#test_data_preprocessed.isnull().sum()

train_data_preprocessed = train_data_preprocessed.loc[train_data_preprocessed[y_column_name] != 0].copy()
#train_data_preprocessed.isnull().sum()

y = train_data_preprocessed[y_column_name]
train_data_preprocessed.drop(y_column_name, axis=1, inplace=True)
test_data_preprocessed.drop(y_column_name, axis=1, inplace=True)


####### 6. Training the model ############
X_train, X_val, y_train, y_val = train_test_split(train_data_preprocessed, y, test_size=0.2, random_state=0)
X_test = test_data_preprocessed.copy()

##here cross_val_cat
from catboost import CatBoostRegressor, Pool
cross_val_cat(train_data_preprocessed, y, X_test)
# #regressor_Linear = LinearRegression()



# ##### 7. transform y ###############
# y_train_log = np.log(y_train)
# y_val_log = np.log(y_val)
# ###################################

# X_train.isnull().sum()
# ###### 8. fit model and predict the income ###############
# params = {
#           'max_depth': 20,
#           'learning_rate': 0.0005,
#           "boosting": "gbdt",
#           "bagging_seed": 11,
#           "metric": 'mae',
#           "verbosity": -1,
#          }
# # import lightgbm as lgb
# # trn_data = lgb.Dataset(X_train, label=y_train_log)
# # val_data = lgb.Dataset(X_val, label=y_val_log)
# #
# # clf = lgb.train(params, trn_data, 100000, valid_sets = [trn_data, val_data], verbose_eval=1000, early_stopping_rounds=500)
# #
# # y_pred_log = clf.predict(X_val)
# # y_pred = np.exp(y_pred_log)

# ###### 8.2 fit model and predict the income using Catboost ###############
# ## To run pip install catboost and tensorflow-gpu

# from catboost import CatBoostRegressor, Pool
# trn_data = Pool(X_val, label=y_val_log)

# cat_model = CatBoostRegressor(iterations=20000, task_type="GPU")
# cat_model.fit(X_train, y_train_log, eval_set=trn_data, use_best_model=True)



# y_pred_log = cat_model.predict(X_val)
# y_pred = np.exp(y_pred_log)


# #regressor_Linear.fit(X_train, y_train_log)
# #y_pred = np.exp(regressor_Linear.predict(X_test))

# ######## 9. calculate metrics ######################
# calculate_metrics(y_val,y_pred)

# #calculate_metrics(y_test,y_pred)
# #Mean Absolute Error: 13328734.232115386
# #Mean Squared Error: 1.629745039516587e+17
# #Root Mean Squared Error: 403701008.1132554
# ###########################################

# ######## 10. Predict production data ################
# # predict_prod_data2(test_data_preprocessed, clf)
# predict_prod_data2(test_data_preprocessed, cat_model)
# #predict_prod_data(test_data_preprocessed, regressor_Linear)
# ####################################################




"""
Early stopping, best iteration is:
[65153] training's l1: 0.353419 valid_1's l1: 0.390691
Mean Absolute Error: 971.1423534548443
Mean Squared Error: 9469986.618054343
Root Mean Squared Error: 3077.3343364110347

With size of city:
Did not meet early stopping. Best iteration is:
[100000]        training's l1: 0.0868621        valid_1's l1: 0.104294
Mean Absolute Error: 535.6321563052907
Mean Squared Error: 6845444.530198286
Root Mean Squared Error: 2616.380043150896



[100000]        training's l1: 0.129982 valid_1's l1: 0.130995
Mean Absolute Error: 9041.450715558276
Mean Squared Error: 525568262.7017634
Root Mean Squared Error: 22925.27562978826


Using Catboost (Caleb Teo) 19-11-2019
Iterations = 20000
Mean Absolute Error: 8409.58350966533
Mean Squared Error: 461781299.5351664
Root Mean Squared Error: 21489.0972247595

iterations = 60000
Mean Absolute Error: 8378.461673578056
Mean Squared Error: 475099853.7243708
Root Mean Squared Error: 21796.785398869502

iteration = 100000
Mean Absolute Error: 8361.410307435952
Mean Squared Error: 482027332.3600127
Root Mean Squared Error: 21955.12086871791

"""






