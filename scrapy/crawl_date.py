# coding:utf8
import urllib
import urllib.parse
import urllib.request
import json
import pandas as pd
#发送request请求，请求内加入时间戳，就可以获得三个披露时间的json数据，解析后可获得结果
def crawl_date(year,date):
    url = 'http://www.cninfo.com.cn/cninfo-new/information/prbookinfo-1'
    values = {
        "sectionTime": str(year)+'-'+date
    }
    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    try:
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
            page = the_page.decode('utf-8')
            json_datas = json.loads(page)
            print(len(json_datas))
            df = pd.DataFrame(json_datas)
            #print(df.columns)
            return df
        # for json_data in json_datas:
        #     print (json_data)
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    df = pd.DataFrame(columns=["secname","seccode","f002d_0102","f006d_0102","f003d_0102","f004d_0102","f005d_0102","f001d_0102","orgId"])
    for year in range(2007,2019):
        df1 = crawl_date(year, '03-31')
        df2 = crawl_date(year, '06-30')
        df3 = crawl_date(year, '09-30')
        df4 = crawl_date(year, '12-31')
        frames= [df,df1,df2,df3,df4]
        df = pd.concat(frames,sort=False)
    df.to_csv('date_res.csv')
