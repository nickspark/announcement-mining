反向找事件思路是设定一个条件，如信号日后第五日累计收益高出信号日累计收益1%
在筛出来的股票代码和日期里筛选所有公告，把这些公告分词，统计词频

SingleEventFun.py 用来生成筛选满足设定条件的公告

jieba_process.py 把找到满足条件的公告做分词并统计词频

找到关键词需要测试可以使用上一级的EventTestLoop.py

这里在排序的时候要注意次数排序以及次数比排序的含义

EventFigure里的图片是选择了排名靠前的词测试的结果，测试集是整个股票池，分别有等权去了benchmark和不去benchmark的结果

csv文件含义：
result_*per.csv :*代表day5累计收益高于day0的百分比（05为千五）
res_all_freq.csv：所有公告分词的词频