import json #strips string from dictionary
import numpy as np
import pandas as pd
import time
import datetime
import ast
import os
#random.seed(4612)

def random_shuffle_file(location):
    return np.genfromtxt(location, dtype =None, delimiter=',')

def read_csv_file(location, user_num):
    return  location + str(user_num) + '.csv' 

def create_df(location, user_num):
    if not os.path.isfile(read_csv_file(location, user_num)):
        return None
    else:
        return pd.read_csv(read_csv_file(location, user_num))
    return df.drop('Unnamed: 0', axis=1)

def combine_dataframes(location, random_list, start_num=0, end_num=1):
    beginning_num = start_num
    for num in range(beginning_num, end_num):
        if os.path.isfile(read_csv_file(location, random_list[num])) == False:
            beginning_num += 1
        else:
            break
    combined_df = create_df(location, random_list[beginning_num])
    for num in range(beginning_num+1, end_num+1):
        combined_df = pd.concat([combined_df, create_df(location, random_list[num])], axis=0, sort=False)
    return combined_df.drop(labels=['Unnamed: 0'],axis=1)

def transform_dataframe(dataframe):
    df = dataframe
    df['day_week_name'] = pd.to_datetime(df.date).dt.weekday_name
    df['day_week_number'] = pd.to_datetime(df.date).dt.weekday
    df['day_month'] = pd.to_datetime(df.date).dt.day
    df = pd.concat([df, pd.get_dummies(df.day_week_name)],axis=1)
    #df = pd.concat([df, pd.get_dummies(df.day_month,prefix='day')], axis=1)
    #0-> Monday; 5->Saturday; 6->Sunday
    #df['weekday'] = pd.Series(np.where(pd.to_datetime(df.date).dt.weekday >= 5, 1, 0))
    df['amount_tens'] = pd.Series(np.where(df.amount % 10.00 == 0, 1, 0))
    df['amount_hundreds'] = pd.Series(np.where(df.amount % 100.00 == 0, 1, 0))
    df['amount_thousands'] = pd.Series(np.where(df.amount % 1000.00 == 0, 1, 0))
    
    #Drop Columns
    df = df.drop(labels=['day_week_name',
                        'day_month',
                        'date',
                        #'name',
                        #'category',
                        'day_week_number',
                        #'day_31',
                        'Sunday'], 
                        axis=1)
    return df

def split_categories(overall_dataframe, dataframe_column):
    new_list = []
    for i in dataframe_column:
        if ('[' in i) and (']' in i):
            new_list.append(ast.literal_eval(i))
        elif type(i) is list:
            new_list.append(i)
        else:
            new_list.append([])
    categories = pd.DataFrame(np.array(new_list).tolist(), 
                              columns=['category_%s' % i for i in list(range(1,np.max([len(x) for x in new_list])+1))])
    #categories.fillna(value=0, inplace=True)
    overall_dataframe = pd.concat([overall_dataframe.reset_index(drop=True),categories], axis=1).drop(labels=['category'],axis=1)

    return overall_dataframe

