# coding:utf8

from bs4 import BeautifulSoup
import requests
import urllib
import json
import re
import pandas
import os
import time
from pandas import DataFrame

def readfile(filename):

    list=[]
    f=open(filename,'r')
    for line in f.readlines():
        list.append(line.strip())
    return list

#传入股票代码，可以把该股票所有公告从json中解析出来，然后保存到相应csv
def crawl(stock_code):
    if os.path.exists('./res/' +str(stock_code))== False:
        os.makedirs('./res/' +str(stock_code))
    #参数传1500可以在一页显示所有公告，因为没有公司公告书超过1500
    url = 'http://data.eastmoney.com/notices/getdata.ashx?StockCode =' + str(stock_code) + '&CodeType=1&PageIndex=1&PageSize=1500&rt=50239182'
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    headers = {"User-Agent": user_agent}
    req = urllib.request.Request(url, headers=headers)
    try:
        wp = urllib.request.urlopen(req)
        data = wp.read().decode("gbk",'ignore')
        start_pos = data.index('=')
        #print(data[start_pos + 1:-1])
        json_data = data[start_pos + 1:-1]
        dict = json.loads(json_data)
        notices = dict['data']
        list1=[]
        #分析网页可以发现返回内容是两个json嵌套，内层json在data里，可以拿出来循环然后解析
        for notice in notices:
            title = notice.get('NOTICETITLE')
            date = notice.get('NOTICEDATE')
            url = notice.get('Url')
            ANN_RELCOLUMNS = notice.get('ANN_RELCOLUMNS')
            date = notice.get('NOTICEDATE')
            if(int(date[0:4])<2007):
                break
            type_notice=ANN_RELCOLUMNS[0].get('COLUMNNAME')
            #print (url)
            list1.append([title, type_notice,date, url,notice])
        df = DataFrame(list1)
        if not df.empty:
            df.columns=['title','type','date','url','content']
        df.to_csv("./result/" + str(stock_code) + '.csv', encoding="utf_8_sig", index=False)
        print(str(stock_code) + 'over')
        #print (list)
    except  urllib.error.HTTPError as e:
        print (e)

    #time.sleep(2)


if __name__ == "__main__":
    #这里的list是股票代码list
    list=readfile('list4.txt')
    for i in list:
        crawl(i)
        #time.sleep(3)


