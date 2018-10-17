
# coding: utf-8

# In[23]:

import sys
sys.path.append("/home/cedar/PlayGround/PyHolyHawk")
from FactorLib.testimport import *

status = load_indicator("status","m")
trading = pd.DataFrame(1,index=status.index,columns=status.columns)[status==0]

prc = load_indicator("qfq","m")
ret = (prc/prc.shift(1)-1).replace([np.inf,-np.inf],np.nan) 
cumret_False = ret.cumsum()
cumret_eq = (ret.T-ret.mean(axis=1)).T.cumsum()
size = load_indicator("total","m")*trading
sizewgt = (size.T/size.sum(axis=1)).T
cumret_size = (ret.T-(ret*sizewgt).sum(axis=1)).T.cumsum()
#更新status矩阵，更新涨跌停状态
status = load_indicator("status","m")
status[ret > 0.095] = 2
status[ret < -0.095] = 3

# def singleEventRet(date,code,benchmark='eq',window=[-20,20],ret=ret):
#     if benchmark is False:
#         cumret = cumret_False
#     elif benchmark == "eq":
#         cumret = cumret_eq
#     elif benchmark == "size":
#         cumret = cumret_size
#     else:
#         cumret = (ret.T-benchmark).T.cumsum()
#     date_list = ret.index[ret.index < date][window[0]:].append(ret.index[ret.index >= date][:window[1]+1])
#     cumret = cumret.loc[date_list,code]
#     return cumret

#直接做矩阵运算求day5和day0累计收益之差效率最高
x = cumret_eq.shift(-5)-cumret_eq 

mat_5 = x

#日期不在交易日后移到最近交易日
def forecast_return(code,date):
    if date not in ret.index:
        date=ret.index[ret.index >= date][0]
    return mat_5.loc[date,code],status.loc[date,code]



#%prun x.loc[20180620,"600000.SH"]


# In[24]:

#生成新的date	code	title	type	forecast_return	status	date_code的dataframe
df = df_all
x = df[:]
x["forecast_return"] = x.apply(lambda l: forecast_return(l.code,l.date)[0], axis=1);
x["status"] = x.apply(lambda l: forecast_return(l.code,l.date)[1], axis=1);

x["date_code"] = x.date.astype(str)+x.code

# In[25]:

#限制条件写在这里
res = x[(x.forecast_return > 0.005)&(x.status==0)]

res.to_csv('result_05per.csv')







