# coding:utf8
from bs4 import BeautifulSoup
import requests
import urllib
import json
import xlrd
import os
import csv
import time
import threading
import signal
import socket
def readfile(filename):

    list=[]
    f=open(filename,'r')
    for line in f.readlines():
        list.append(line.strip())
    return list

#给定公告链接，提取公告内容
def returnRESBS(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    headers = {"User-Agent": user_agent}
    while True:
        try:
            socket.setdefaulttimeout(60)
            req = urllib.request.Request(url, headers=headers)
            wp = urllib.request.urlopen(req)
            data = wp.read().decode("gbk",'ignore')
            if url == wp.geturl():
                #这里为了判断是否是不可解析的pdf，若果是网址会重定向
                #如果是则存pdf地址
                soup = BeautifulSoup(data,'html.parser')
                res = soup.find_all(class_='detail-body')
                if res:
                    temp=res[0].find_all('div')
                    if temp:
                        res1=temp[0].string
                    else:
                        res1='none'
                else:
                    res1 = 'none'
                return res1
            else:
                return wp.geturl()
        except Exception as e:
            with open('timeout.txt', 'w') as f:
                f.write(url +'-------'+str(e)+ '\n')
            f.close()
            print (str(e))
            time.sleep(120)


def returntxt(str1,title,stock_code):
    if str1==None:
        str1=' '
    # 把标题和内容存入txt，这里为了避免报错，把标题中不能存的字符都改成了‘-’
    title = title.replace(':', '-')
    title = title.replace('/', '-')
    title = title.replace('\\', '-') #  '\'转义
    title = title.replace('*', '-')
    title = title.replace('?', '-')
    title = title.replace('"', '-')
    title = title.replace('|', '-')
    title = title.replace('<', '-')
    title = title.replace('>', '-')
    code=str(stock_code)
    print (stock_code)
    # flag=title.index(':')
    # print (flag)
    if os.path.exists('D:/result/' +str(stock_code))== False:
        os.makedirs('D:/result/' +str(stock_code))
    with open('D:/result/' +code+'/'+ title[:30] + '.txt', 'w',encoding='utf-8') as f:
        f.write(str1)
        f.close()
        return title

def main_fun(code): #
    csv_reader = csv.reader(open(('./result1/' + str(code) + '.csv'), encoding='utf-8'))
    for j, row in enumerate(csv_reader):
        if j > 0:
            url = row[3]
            title = row[0]
            print(title)
            #传入url取内容，title做文件标题，code分类文件夹
            returntxt(returnRESBS(url), title, code)

if __name__ == "__main__":
    list=readfile('list.txt')
    count = 0
    for i in list:
        main_fun(i)


