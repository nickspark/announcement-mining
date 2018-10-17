
# coding: utf-8

# In[2]:

import sys
sys.path.append("/home/cedar/PlayGround/PyHolyHawk")
from FactorLib.testimport import *
import seaborn as sns
sns.set(style="whitegrid", palette="muted")
import pandas as pd
import os
prc = load_indicator("qfq","m")
ret = (prc/prc.shift(1)-1).replace([np.inf,-np.inf],np.nan) 


# In[51]:

event_list = ['异常']
filenames = list(os.walk("./result/"))[0][2]
event_mat=ret>10
for u in event_mat.columns:
    if event_mat[u].dtype==bool:
        event_mat[u]=event_mat[u].astype('int')


# In[74]:

#把公告拼接起来，存入和price矩阵相同的矩阵，一只股票一天有多个公告时用‘--’分隔

all_list=[]
df_all = pd.DataFrame(columns=["date","code"])
for ticker in filenames[:]:
    df_temp = pd.read_csv("./result/%s"%ticker,usecols=[0,2])
    df_temp.columns = ["title","date"]
    df_temp.date= df_temp.date.map(lambda x:int(x[:10].replace('-','')))
    df_dup=df_temp.duplicated(["date"])
    df_temp_dup=df_temp.drop_duplicates(["date"])
    if ticker[0] == '6':
        ticker = str(ticker[:6])+'.SH'
    else:
        ticker = str(ticker[:6])+'.SZ'
    for index,row in df_temp_dup.iterrows():
        list_temp=''
        df_temp_1=df_temp[df_temp.date==row['date']]
        date=row['date']
        if date not in event_mat.index:
            date=event_mat.index[event_mat.index >= date][0]
        for index,row1 in df_temp_1.iterrows():
            list_temp=list_temp+'--'+(str(row1["title"]).strip())
        event_mat.loc[date,ticker]=list_temp
print(event_mat)


# In[1]:


