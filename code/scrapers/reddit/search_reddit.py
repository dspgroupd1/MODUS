#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
from datetime import date
import pickle
import seaborn as sns
import pandas as pd

#import toolboxes
from reddit_toolbox import piecewise_lin_fit, search_mentions, search_drug_pattern, function_find_pattern, moving_average

# Getting data:
with open('objs.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
     reddit_df = pickle.load(f)
        
drug_kwrds = {'4-FA' : '4-FA|4FMP', 
              '4-MMC': '4-MMC|mephedrone | mefedron',
              '6-ABP': '6-APB| Benzofury| Benzo Fury',
              'A-PHP'  : 'alpha-PHP|α-PHP|a-php',
              'Phenibut': 'Phenibut|fenibut',

             }
reddit_df['year'] = pd.to_datetime(reddit_df['created_utc']).dt.strftime('%Y')
reddit_df['year'] = reddit_df['year'].astype('int')



def search_drug(drug_df=reddit_df, drug='', beg_year=2012, end_year=2022):
    
    search_mentions(drug_df, drug_name=function_find_pattern(drug, drug_kwrds) )
    df_no_comments = drug_df[drug_df['kind']=='t3'].reset_index()
    df_no_comments = df_no_comments[(df_no_comments['year']>=beg_year) & (df_no_comments['year']<=end_year)]

    df_no_comments = df_no_comments.drop('year', axis=1)
    agg_data = df_no_comments.groupby('year_month').sum()
    
    agg_data['moving-avg-mentions'] = moving_average(agg_data, 'contains', window=5)


    return agg_data.reset_index()
