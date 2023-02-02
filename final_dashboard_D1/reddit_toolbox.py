import pandas as pd
import re
import numpy as np
import pwlf

def function_find_pattern(string_to_search, dict_of_kwrds):
    r = re.compile('\\b'+string_to_search.strip()+'\\b', flags=re.I)
    newlist = list(filter(lambda elem: r.search(elem[1]), dict_of_kwrds.items()))
    if len(newlist) == 0:
        return string_to_search
    else:
        return dict_of_kwrds[newlist[0][0]]

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
    pattern = pattern.replace("+","\+")
    pattern = '\\b'+pattern+'\\b'
    pattern = re.compile(pattern, flags=re.IGNORECASE)  

    return pattern

#if condition returns False, AssertionError is raised:
# UNIT TEST 
test=pd.DataFrame(data={'text':['3-mmc 3  mmc 3mm 3MMC https://3mmc.sfsdf.sfdsf.sdfsf 3 mmc']})
test['text']=test['text'].str.replace(r'http\S+', '', regex=True, flags=re.IGNORECASE)
pattern = search_drug_pattern('3 -mmc')
x = test['text'].str.count(pattern)
assert x[0] == 4, "x should be 4" 

def search_mentions(df, drug_name ):
    text_to_analyse = df['title'].fillna('') + df['selftext'].fillna('') + df['body'].fillna('') #combines text from title, post body and comments
    text_to_analyse = text_to_analyse.str.replace(r'http\S+', '', regex=True, flags=re.IGNORECASE) #removs links
    
    pattern = search_drug_pattern(drug_name)

    df['contains'] =  text_to_analyse.str.contains(pat=pattern)
    return df


# #UNIT TEST
# import numpy as np
# data_test={'title':['https://3mmc.sfsdf.sfdsf.sdfsf','3mmc','3   mmc', '3MmC','','','']}
#
# data_test['selftext'] = np.nan
# data_test['body'] = np.nan
# test=pd.DataFrame(data=data_test)
# test.loc[4, 'selftext'] = '3mmc'
# test.loc[5, 'body'] = '3mmc'
# test.loc[6, 'body'] = '4 abc'
# display(search_mentions(test, drug_name='3mmc|4abc' ))
#
# assert np.prod(test['contains']==[False, True, True, True, True, True, True]), 'not all mentions were found'


def moving_average(data, field, window=4):
    Y = data[field].rolling(window).mean()
    Y = Y.fillna(0)
    return Y

def piecewise_lin_fit(data, field, number_of_breaks=12):
    ''' evaluate piece wise linear regression '''
    output = pd.DataFrame()
    X = np.arange(0,len(data))
    Y = moving_average(data, field, window=4)
    output['average'] = Y
    output.reset_index(inplace=True)
    output['year_month'] = data.index

    model = pwlf.PiecewiseLinFit(X, Y)
    model.fit(number_of_breaks)
    y_pred = model.predict(X)

    output['pwlf'] = y_pred

    return output


