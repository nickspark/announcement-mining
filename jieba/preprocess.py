import jieba
import jieba.analyse
import pandas as pd
import os
#用户词典中的词不会被删除
jieba.load_userdict("E:/newdict.txt")
#停顿词将会被去除
stopkey = [line.strip("\n") for line in open('E:/stopwords.txt', encoding='UTF-8').readlines()]



filenames = list(os.walk("E:/result/"))[0][2]

wfd = pd.Series()
#遍历所有文件且分词统计词频
for ticker in filenames[:]:
    ticker = ticker[:-4]
    print(ticker)
    df = pd.read_csv("E:/result/%s.csv" % ticker)
    df.columns = ["title", "type", "date", "url", "content"]

    titles = df["title"]

    titles = titles.to_frame()

    titles["jieba"] = titles.title.map(lambda x: list(jieba.cut(x)))

    all_words = titles.jieba.sum()

    wf = pd.Series(pd.unique(all_words), index=pd.unique(all_words)).map(lambda x: all_words.count(x))
    wf = wf.sort_values(ascending=False)

    wfd = wfd.add(wf[~wf.index.isin(stopkey)], fill_value=0)

res = wfd.sort_values(ascending=False)
print(res)
res.to_csv('res.csv',encoding="utf_8_sig")
#wfd.sort_values(ascending=False) / len(titles)