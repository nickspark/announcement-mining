import jieba
import jieba.analyse
import pandas as pd

jieba.load_userdict("../words/newdict.txt")
stopkey = [line.strip("\n") for line in open('stopwords.txt', encoding='UTF-8').readlines()]

#类似把所有内容分词，把找到满足条件的公告做分词并统计词频
def jieba_pro(filename):
#传入参数为文件名是在SingleEventFun.py中生成的筛选后的标题的dataframe，
# 文件中有筛选出的title即可，通过把每个title分词并放在一起然后进行词频统计
    wfd = pd.Series()
    df = pd.read_csv("%s.csv" % filename,encoding='ANSI')
    df.columns = ["ind","date","code","title","type","forecast_return","status","date_code"]
    titles = df["title"][:]
    titles = titles.to_frame()
    titles["jieba"] = titles.title.map(lambda x: list(jieba.cut(x)))
    all_words = titles.jieba.sum()
    wf = pd.Series(pd.unique(all_words), index=pd.unique(all_words)).map(lambda x: all_words.count(x))
    #f = wf.sort_values(ascending=False)

    wfd = wfd.add(wf[~wf.index.isin(stopkey)], fill_value=0)

    res = wfd.sort_values(ascending=False)
    print(res)
    res.to_csv('res_per_5_freq.csv',encoding="utf_8_sig")


if __name__=="__main__":
    jieba_pro('result_5per')
    #print(freq_type('res_all_sep'))
