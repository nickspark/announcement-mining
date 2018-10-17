
# coding: utf-8

# 先执行这里以及后面代码，初始化函数且读入
import sys

sys.path.append("/home/cedar/PlayGround/PyHolyHawk")
from FactorLib.testimport import *
import seaborn as sns

sns.set(style="whitegrid", palette="muted")
import pandas as pd
import os
import pickle as pk

# In[7]:

prc = load_indicator("qfq", "m")
ret = (prc / prc.shift(1) - 1).replace([np.inf, -np.inf], np.nan)
status = load_indicator("status", "m")
status[ret > 0.095] = 2
status[ret < -0.095] = 3


# 返回观察窗口的return list (return in percentage)
# benchmark = "eq","size",False,或者自定义的return series
def eventrets(ret, signalmask, benchmark=False, window=[-20, 20], startdate=20100101, enddate=ret.index[-1]):
    """
    ret可以是excess return或者raw return，close price return或者open price return (若使用excess return的话请先自定义合适的benchmark index)
    signalmask为一个由true和false组成的dataframe，注意：signalmask和ret的shape必须一致，否则会报错
    window为事件交易前后的观察窗口，window[0]必须小于0，window[1]必须大于0,两者绝对值不需要相等
    不同日期的事件和发生事件的所有股票都同等处理，无权重方面的考虑
    """
    # ensure that the ret dataframe does not contain any suspended stocks
    # status = load_indicator("status","m")
    # trading = pd.DataFrame(1,index=status.index,columns=status.columns)[status==0]
    # ret = (ret*trading).loc[startdate:enddate]

    # Define benchmark index
    if benchmark is False:  # default
        cumret = ret.cumsum()
    elif benchmark == "eq":
        cumret = (ret.T - ret.mean(axis=1)).T.cumsum()
    elif benchmark == "size":
        size = load_indicator("total", "m") * trading
        sizewgt = (size.T / size.sum(axis=1)).T
        cumret = (ret.T - (ret * sizewgt).sum(axis=1)).T.cumsum()
    else:
        cumret = (ret.T - benchmark).T.cumsum()

    # MAIN PART
    windowrets = []

    signaldf = pd.DataFrame(1, index=signalmask.index, columns=signalmask.columns)[signalmask].loc[startdate:enddate]
    for i in range(window[0], window[1] + 1):
        diff = (cumret.shift(-i) - cumret) * signaldf
        #         print(signaldf.count().sum())
        #         print (diff.count().sum())
        windowrets.append(diff.sum().sum() / diff.count().sum() * 100)
    noo = str((ret * signaldf).count().sum())
    print("Number of occurences: " + noo)

    return windowrets, noo


def plot_eventrets(name, bm, windowrets_list, window=[-20, 20], tickwidth=5, title="Event Impact", legend=[]):
    # window参数需要和eventImpact function中的window一致
    # 可以画几组windowrets，比如中证300中的事件vs.中证500中的事件
    # 图中，-1 to signal date：signal date当天的return
    for windowrets in windowrets_list:
        plt.plot(windowrets, ".-")
    plt.xticks(np.arange(0, len(windowrets_list[0]), tickwidth),
               list(range(window[0], 0, tickwidth)) + ["Signal Date"] + list(
                   range(tickwidth, window[1] + 1, tickwidth)))
    plt.title(title)
    plt.ylabel("Accumulated Return (%)")
    plt.legend(legend)
    #输出路径在此修改
    plt.savefig("./Event_figure/" + name + " bm=" + str(bm) + ".png")
    plt.show()


def readfile(filename):
#把txt里的list转成list
    list = []
    f = open(filename, 'r', encoding='gbk')
    for line in f.readlines():
        list.append(line.strip())
    return list

# In[1]:


#事件矩阵由来见EventLoad
event_mat = pk.load(open("event_mat.pkl",'rb'))


# In[9]:

#在list里放入要测试的事件列表
event_list = readfile('event_list.txt')


# In[10]:

#循环函数，分别测试list中的事件并把测试图存起来
for event in event_list:
    event_mask=(ret>10)
    #找对应事件转画图需要的bool矩阵
    test1 = event_mat.applymap(lambda x: event in str(x))
    event_mask=pd.DataFrame(True,index=test1.index,columns=test1.columns)[test1]
    event_mask[event_mask!=True]=False

    matrix = event_mask.astype('bool')
    
    bm='eq'
    windowrets_list=[]
    windowrets,noo=eventrets(ret, matrix, benchmark=bm, window=[-20,20], startdate=20100101, enddate=ret.index[-1])
    windowrets_list.append(windowrets)
    plot_eventrets(event,bm,windowrets_list, window=[-20,20], tickwidth=5, title=("Event Impact benchmark="+str(bm)+" number="+str(noo)), legend=[])
    
    bm=False
    windowrets_list=[]
    windowrets,noo=eventrets(ret, matrix, benchmark=bm, window=[-20,20], startdate=20100101, enddate=ret.index[-1])
    windowrets_list.append(windowrets)
    plot_eventrets(event,bm,windowrets_list, window=[-20,20], tickwidth=5, title=("Event Impact benchmark="+str(bm)+" number="+str(noo)), legend=[])
    #这里的两个函数在欣源姐画的上面做了一些修改，目的是把出现次数，benchmark呈现在图片里，也为了把图片输出到文件夹

# In[6]:



