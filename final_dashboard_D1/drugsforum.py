#!/usr/bin/env python
# coding: utf-8

# In[271]:


import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
import pwlf

import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
plt.rcParams["figure.figsize"] = (16, 8)


# In[4]:


def get_nps_list():
    nps_list = ['1B-LSD', '1D-LSD', '1P-LSD', '1V-LSD', '1CP-AL-LAD', '1CP-LSD', '1CP-MIPLA', 
                   '2+3-FEA', '2-CB', '2-FA', '2-FDCK', '2-FEA', '2-FMA', '2-FPM', '2-MMC', 
                   '2/3-FEA', '2C-B-FLY', '2C-C', '2C-D', '2C-E', '2C-E-NBOME', '2F-DCK', '2F-KETAMINE', 
                   '3-CEC', '3-CMC', '3-CPM', '3-FA', '3-FEA', '3-FMA', '3-FPM', '3-HO-PCE', '3-HO-PCP', 
                   '3-MEC', '3-MEO-PCE', '3-MMA', '3-MMC', '3-ME-PCE', '3-ME-PCP', '3-ME-PCPY', 
                   '3-MEO-PCP', '3.4-DMMC', '3D-MXE', '4-ACO-MET', '4-ACO-DET', '4-ACO-DPT', 
                   '4-ACO-MIPT', '4-CDC', '4-CEC', '4-CL-PVP', '4-CMC', '4-EMC', '4-FMA', '4-FMPH', 
                   '4-HO-DET', '4-HO-DPT', '4-HO-EPT', '4-HO-MALT', '4-HO-MET', '4-HO-MIPT', 
                   '4-HO-MCPT', '4-ME-MABP', '4-MEC', '4-MPD', '4-MPM', '4B-MAR', '4C-MAR', 
                   '4F-MAR', '4F-MPH', '4F-METHYLFENIDAAT', '4F-RITALIN', '4FMA', '5-APB', 
                   '5-BR-DMT', '5-BROMO-DMT', '5-DBFPV', '5-EAPB', '5-HTP', '5-MAPB', '5-MEO-DALT', 
                   '5-MEO-DIPT', '5-MEO-MIPT', '5-MMPA', '5-MEO-DMT', '5-MEO-MET', '5-METHYLETHYLONE', 
                   '5BR-ADB-INACA', '5F-ADB', '5F-PCN', '5F-SGT-151', '6-APB', '6-CL-ADB-A', '6-CL-ADBA', 
                   '7-ABF', '7-ADD', 'A-PCYP', 'A-PHP', 'A-PIHP', 'ADB', 'ADB-BUTINACA', 'AL-LAD', 'ALD-52', 
                   'AMT', 'BB-8', 'BK-2C-B', 'BK-BBDP', 'BK-EBDP', 'BOH-2C-B', 'BROMAZOLAM', 'BROMONORDIAZEPAM', 
                   'CBD', 'CLONAZOLAM', 'DC-C', 'DC-TROPA-MIX', 'DCK', 'DESOXY-MDA', 'DESOXY-MDMA', 'DHM', 'DMC', 
                   'DMXE', 'DOC', 'DPT', 'DESCHCLOROKETAMINE', 'DESCHLOROKETAMINE', 'DESCHLOROETIZOLAM', 
                   'DICLAZEPAM', 'ED-DB', 'EPT', 'ETH-LAD', 'ETHYL-HEX', 'ETHYL-PENTEDRONE', 'ETIZOLAM', 
                   'FLUALPRAZOLAM', 'FLUBROMAZEPAM', 'FLUBROMAZOLAM', 'FLUBROTIZOLAM', 'FLUETIZOLAM', 
                   'FLUNITRAZOLAM', 'FLUOREXETAMINE', 'GW-0742', 'GW-501516', 'GIDAZEPAM', 'HEP', 'HEX-EN', 
                   'HXE', 'IDRA-21', 'JWH-210', 'L-THEANINE', 'LGD-4033', 'LSD', 'LSZ', 'MD-PHP', 'MDPHP', 
                   'MEAI', 'MET', 'MF-PVP', 'MK-2866', 'MK-677', 'MXPR', 'MXIPR', 'MEPHEDRENE', 
                   'METHALLYLESCALINE', 'N-ETHYL-HEXEDRONE', 'N-ETHYLHEXEDRONE', 'NB-5-MEO-DALT', 
                   'NB-5-MEO-MIPT', 'NDH', 'NEP', 'NORFLURAZEPAM', 'O-DSMT', 'O-PCE', 'PHENIBUT', 
                   'PHOSPHATIDYLSERINE', 'PYRAZOLAM', 'RAD-140', 'RAD-150', 'RIBOFLAVINE', 'S-23', 
                   'S-4', 'SGT-152', 'SR-9009', 'SR-9011', 'SULBUTIAMINE', 'SYNTHACAINE', 'THC-C4', 
                   'TRYPTAMINE', 'VINPOCETINE', 'YK-11', 'A-D2PV', 'BK-MDDMA', 'Α-PIHP', 'ΒOH-2C-B']
    return nps_list



def search_drug_pattern(search_word):
    '''creates regex search pattern from a search word 
    for example 3mmc search will look for 
    3mmc 3-mmc 3 mmc and 3MMC 3 MMC 3-MMC
    '''
    search_word = search_word.strip() # remove leadning and trailing white spaces
    pattern = r'\s+' # one white space or more
    search_word=re.sub(pattern,"-", search_word)    
    pattern = r'([0-9]+)' # one dash or more
    search_word = re.sub(pattern, r"\1-", search_word)
    pattern = r'-+' # one dash or more
    search_word = re.sub(pattern,"-", search_word)
 
    pattern = search_word.replace("-","\s*\-*")
    pattern = '\\b'+pattern+'\\b'
    pattern = re.compile(pattern, flags=re.IGNORECASE)  
    return pattern


# combine three sources of drugsforum.nl and return df
def get_nl_df():
    df1 = pd.read_csv('nl_corpus/drugs_generaldrugsforumnl_threads.csv',
                     lineterminator='\n')
    df2 = pd.read_csv('nl_corpus/research_chemicalsdrugsforumnl_threads.csv')
    df3 = pd.read_csv('nl_corpus/trip_reportsdrugsforumnl_threads.csv',
                     lineterminator='\n')
    return pd.concat([df1, df2, df3], axis=0)    



def fill_missing_months(drug_df, beg_year, end_year):
#    beg_year, end_year = 2008, 2022
    beg_month, end_month = 1, 12
    for year in range(beg_year, end_year+1):
        for month in range(beg_month, end_month+1):
            if month<10:
                month_str = '0'+str(month)
            else:
                month_str = str(month)
            month_year = str(year) + '-' + month_str
            if month_year in drug_df['month-year'].unique():
                #print(month_year)
                continue
            new_row = pd.DataFrame({
                'month' : [month_str],
                'year' : [str(year)],
                'month-year' : [month_year],
                'comments' : [0],
                'views' : [0],
                'url' : [''],
                'title' : ['something'],
                'username' : ['something]'],
                'user_url' : [''],
                'thread_id' : [0],
                'forum' : [''],
            }, index = [len(drug_df)])
            drug_df = drug_df.append(new_row)
    return drug_df



def search_drug_drugsforum(drug, beg_year, end_year):
    df = get_nl_df()
    drug_df = pd.DataFrame(columns=df.columns)
    df = df[df['date']!='something']
    df['title'] = df['title'].str.lower()
    df['content'] = df['content'].str.lower()

    drug_name = drug.lower()
    drug_pattern = search_drug_pattern(drug_name)
    t_df = df[df['title'].str.contains(pat=drug_pattern)]
    c_df = df[df['title'].str.contains(pat=drug_pattern)]
    tc_df = pd.concat([t_df,c_df]).drop_duplicates().reset_index(drop=True)
    drug_df = pd.concat([drug_df, tc_df]).drop_duplicates().reset_index(drop=True)

    drug_df['month'] = drug_df['date'].apply(lambda x: int(x.split('-')[1]))
    drug_df['year'] = drug_df['date'].apply(lambda x: int(x.split('-')[0]))
    drug_df['month-year'] = drug_df['date'].apply(lambda x: x.split('-')[0] + '-' + x.split('-')[1])
    
    # filter by year given through dashboard
    drug_df = drug_df[(drug_df['year']>=beg_year) & (drug_df['year']<=end_year)]
    
    drug_df = fill_missing_months(drug_df, beg_year, end_year)
    
    data=drug_df.sort_values(by=['month-year'], ascending=True)

    data['views'] = data['views'].astype('int')
    data['comments'] = data['comments'].astype('int')

    data['month-year'] = data['month-year'].apply(lambda x: datetime.strptime(x, "%Y-%m"))
    data['freq'] = data['views'].map(lambda x: 0 if x == 0 else 1)
    
    data = data.drop(['thread_id','forum','title','content','url','username','user_id','user_url','date']
              ,axis=1)
    
    
    agg_data = pd.DataFrame()
    agg_data['views'] = data.groupby(['month-year'])['views'].sum().reset_index()['views']
#    agg_data['comments'] = data.groupby(['month-year'])['comments'].sum().reset_index()['comments']
#    agg_data['freq'] = data.groupby(['month-year'])['freq'].sum().reset_index()['freq']
    agg_data['month-year'] = data.groupby(['month-year'])['freq'].sum().reset_index()['month-year']
    data = agg_data
    
    data['moving-avg-views'] = data['views'].rolling(5).mean()
    data['moving-avg-views'] = data['moving-avg-views'].fillna(0)


    return data

# In[41]:


# return dataframe with all nps metrics as columns, with a column for month-year
def get_all_nps_metrics(beg_year=2012, end_year=2023, metric='views'):
    nps_df = pd.DataFrame()
    nps_list = get_nps_list()
    for nps in nps_list:
        try:
            df = search_drug_drugsforum(nps, beg_year, end_year)
            nps_df[nps] = df[metric]
        except:
            print(nps)
    nps_df['month-year'] = df['month-year']  
    return nps_df



nps_df = get_all_nps_metrics()

 # return list of nps with the highest views (number returned=count)
def get_current_max_nps(nps_df, count=5, days=90, metric='views'):
    today = datetime.today()
    threshold_date = datetime.today() - timedelta(days=days)
    df = nps_df[nps_df['month-year']>=threshold_date]
    df = df.drop(['month-year'], axis=1)
    sum_df = df.sum(axis='rows').reset_index(name=metric)
    max_df = sum_df.sort_values(by=metric, ascending=False).head(count)
    max_nps = list(max_df['index'])
    return max_nps

# return the list of nps with the highest views, in string format for the front-end
def get_current_max_nps_string(nps_df, count=5, days=90, metric='views'):
    max_nps = get_current_max_nps(nps_df, count=count, days=days, metric=metric)
    max_nps = [str(i+1)+'. '+x for i,x in enumerate(max_nps)]
    # max_nps = "\n".join(max_nps)
    max_nps = "<br/>".join(max_nps)
    return max_nps


# In[264]:


# get % of views for given nps
def get_fraction_nps(nps, nps_df, days=90, metric='views'):
    # search vendor list to get nps in the format of df
    pattern = search_drug_pattern(nps)
    nps_list = get_nps_list()
    df = pd.DataFrame(columns=['month-year',metric])
    
    # if nps is in vendor website, use the info available
    #try:
    if not nps in nps_list:
        nps = list(filter(pattern.match, nps_list))[0]
    df['month-year'] = nps_df['month-year']
    df[metric] = nps_df[nps]
    nps_df = nps_df.drop(nps, axis=1)
#     except:  # if nps not in vendor website, run search for it
#         print("are we searching")
#         df = search_drug(nps)
        
    today = datetime.today()
    threshold_date = datetime.today() - timedelta(days=days)
    
    # take the recent values and drop month-year column
    nps_df = nps_df[nps_df['month-year']>=threshold_date]
    nps_df = nps_df.drop(['month-year'], axis=1)
    
    df = df[df['month-year']>=threshold_date]
    df = df.drop(['month-year'],axis=1)
    nps_views = df[metric].sum()
    sum_df = nps_df.sum(axis='rows').reset_index(name=metric)
    all_views = sum_df[metric].sum()
    return round(nps_views*100/all_views,2)



# return total views summed for all nps 
def get_total_views_nps(nps_df, metric='views'):
    today = datetime.today()
    threshold_date = today - timedelta(days=90+today.day)
    # take the recent values and drop month-year column
    nps_df = nps_df[nps_df['month-year']>=threshold_date]
    nps_df = nps_df.drop(['month-year'], axis=1)
    sum_df = nps_df.sum(axis='rows').reset_index(name=metric)
    all_views = sum_df[metric].sum()
    return all_views


def is_increasing_nps(views, threshold=1):
    months = 6
    views = list(views)[-months:]
    if sum(views) < 500:
        return False
    decrease = 0
    increase = 0
    total_views = sum(views)
    for i,view in enumerate(views[1:]):
        if view <= views[i-1]:
            decrease += 1
        increase += view - views[i-1]
    
    if decrease <= threshold:
        return total_views
    else:
        return False

def get_nps_piecewise_df(nps_df):
    today = datetime.today()
    days = 12*31 + today.day
    nps_list = list(get_current_max_nps(nps_df, count=75, days=days))
    threshold_date = datetime.today() - timedelta(days=days)
    # take the recent values and drop month-year column
    nps_df = nps_df[nps_df['month-year']>=threshold_date]
    nps_df = nps_df[nps_df['month-year']<=today-timedelta(today.day)]
    
    df = pd.DataFrame(columns=nps_list)
    df['month-year'] = nps_df['month-year']

    for nps in tqdm(nps_list):
#        try:
            # apply piecewise on rolling avg
        df[nps] = nps_df[nps].rolling(4).mean()
        df[nps] = df[nps].fillna(0)
        model = pwlf.PiecewiseLinFit(np.arange(0,len(df.index)), list(df[nps]))
        breakpoints = model.fit(5)
        y_pred = model.predict(np.arange(0,len(df.index)))
        df[nps] = y_pred
#         except:
#             print(nps)
    df = df.drop(['month-year'], axis=1)
    return df



def get_increasing_nps(nps_df, piecewise_df):
    df = piecewise_df
    nps_list = piecewise_df.columns.values
    increasing_df = pd.DataFrame()
    increasing_nps = {}
    for nps in nps_list:
        is_increase = is_increasing_nps(df[nps])
        if is_increase:
            increasing_df[nps] = df[nps]
            increasing_nps[nps] = round(df[nps].tail(6).sum())
    increasing_nps = {k: v for k, v in sorted(increasing_nps.items(), key=lambda item: item[1], reverse=True)}
    increasing_nps = list(increasing_nps.keys())[0:5]
    increasing_nps = [str(i+1) + '. ' + x for i,x in enumerate(increasing_nps)]
    increasing_nps = "<br/>".join(increasing_nps)
    return increasing_nps


def get_newly_occurring_nps(nps_df, count, days, metric='views'):
    today = datetime.today()
    threshold_date = today - timedelta(days=days + today.day)
    # take the recent values and drop month-year column
    cur_df = nps_df[nps_df['month-year'] >= threshold_date]
    cur_df = cur_df[cur_df['month-year'] < today]
    cur_df = cur_df.drop(['month-year'], axis=1)
    cur_sum_df = cur_df.sum(axis='rows').reset_index(name=metric)

    # get list of nps where total views before 90 days was zero
    nps_df = nps_df[nps_df['month-year'] < threshold_date]
    nps_df = nps_df.drop(['month-year'], axis=1)
    sum_df = nps_df.sum(axis='rows').reset_index(name=metric)
    sum_df = sum_df[sum_df['views'] == 0]
    new_nps = list(sum_df['index'])

    # filter recent views based on nps with 0 views, and get the highest non-zero views
    cur_sum_df = cur_sum_df[cur_sum_df['index'].isin(new_nps)]
    cur_sum_df = cur_sum_df.sort_values(by=metric, ascending=False).head(count)
    cur_sum_df = cur_sum_df[cur_sum_df['views'] > 0]

    to_return = []
    for i, nps in enumerate(list(cur_sum_df['index'])):
        to_return.append(str(i + 1) + ". " + nps)
    return "<br/>".join(to_return)

def get_current_max_chart_data(nps_df, count):
    max_nps = get_current_max_nps(nps_df, count)
    labels = []
    values = []
    for nps in max_nps:
        labels.append(nps)
        values.append(get_fraction_nps(nps, nps_df))
    labels.append('Others')
    values.append(round(100-sum(values),1))
    return pd.DataFrame({'labels':labels, 'values':values})
    # return list(increasing_nps.keys())[0:5]

piecewise_df = get_nps_piecewise_df(nps_df)