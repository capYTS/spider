# -*- coding: UTF-8 -*-

import sys
import time
import urllib
import urllib3
import requests
import numpy as np
from bs4 import BeautifulSoup
from openpyxl import Workbook
from lxml import etree
# reload(sys)
# sys.setdefaultencoding('utf8')

# Some User Agents

import requests
from lxml import etree
import csv
import time


def get_parse(result):
    items = etree.HTML(result,etree.HTMLParser())
    # print(items)
    # 共6页，分为⽂学，流⾏，⽂化，⽣活，经管，科技
    for i in range(1, 7):
        item = items.xpath('//*[@id="content"]/div/div[1]/div[2]/div[{}]'.format(i))
        for it in item:
            # 归属⼤类
            category = it.xpath('./a/@name')[0]
            print(category)
            # 辅助列
            fuzhu = it.xpath('./table/tbody/tr')
            for its in fuzhu:
                try:
                    for j in range(1, 50):
                        # ⼩类型
                        leixing = its.xpath('./td[{}]/a/text()'.format(j))[0]
                        # ⼩类型链接
                        lianjie = its.xpath('./td[{}]/a/@href'.format(j))[0]
                        # 书籍数⽬
                        shumu = its.xpath('./td[{}]/b/text()'.format(j))[0].strip('(').strip(')')
                        print(leixing)
                        print(lianjie)
                        print(shumu)
                        # 书籍解析
                        get_content(category,leixing,lianjie,shumu)
                except:
                    pass
def get_content(category,leixing,lianjie,shumu):
    D=[]
    # 最多展⽰50页
    for i in range(0, 50):
        time.sleep(1)
        print('+++++++++++++++++++++',i)
        # 链接
        # https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=40&type=T

        lianjie1 = 'https://book.douban.com/tag/' + leixing + '?start={}&type=T'.format(i * 20)
        print(lianjie1)
        response = requests.get(url=lianjie1, headers=headers)
        # print(response)
        items = etree.HTML(response.text)
        item = items.xpath('//*[@id="subject_list"]/ul/li')
        # print(item)
        for its in item:
            # 封⾯
            fengmian = its.xpath('./div[1]/a/img/@src')[0]
            # print(fengmian)
            # 书名
            shuming = its.xpath('./div[2]/h2/a/text()')[0]
            # 删除不需要的单元格
            shuming1 = shuming.replace('\n', '').replace('\t', '').strip()
            # 保存图⽚
            # save1(shuming1,fengmian)
            # print(shuming)
            # 辅助列
            fuzhu = its.xpath('./div[2]/div[1]/text()')[0]
            fuzhu = fuzhu.replace('\n', '').replace('\t', '').strip().split('/')
            # print(fuzhu)
            # print(len(fuzhu))
            if len(fuzhu) == 5:
                guojia=fuzhu[0].split(']')[0].strip('[')
                # print(guojia)
                # 作者
                zuozhe = fuzhu[0]
                # 翻译⼈
                fanyi = fuzhu[1].strip()
                # 出版社
                chuban = fuzhu[2].strip()
                # 出版⽇期
                riqi = fuzhu[3].strip()
                # 价格
                jiage = fuzhu[4].strip()
                # print(zuozhe)
                # print(fanyi)
                # print(chuban)
                # print(riqi)
                # print(jiage)
            elif len(fuzhu) == 4:
                # 国家
                guojia='中'
                # 作者
                zuozhe = fuzhu[0]
                fanyi = ''
                # 出版社
                chuban = fuzhu[1].strip()
                # 出版社⽇期
                riqi = fuzhu[2].strip()
                # 价格
                jiage = fuzhu[3].strip()
            guojia=guojia
            zuozhe=zuozhe
            fanyi=fanyi
            chuban=chuban
            riqi=riqi
            jiage=jiage
            # print(zuozhe)
            # print(fanyi)
            # print(chuban)
            # print(riqi)
            # print(jiage)
            # 评分
            pingfen = its.xpath('./div[2]/div[2]/span[2]/text()')[0]
            # print(pingfen)
            # 评价⼈数
            pingjiarenshu = its.xpath('./div[2]/div[2]/span[3]/text()')[0]
            pingjiarenshu=pingjiarenshu.replace('\n', '').replace('\t','').strip().strip('(').strip(')')
            # print(pingjiarenshu)
            # 书籍简介
            jianjie = its.xpath('./div[2]/p/text()')[0].replace('\n', '').replace('\t','')
            # print(jianjie)
            data=[category,leixing,shumu,fengmian,shuming1,guojia,zuozhe,fanyi,chuban,riqi,jiage,pingfen,pingjiarenshu,jianjie]
            print(data)
            D.append(data)


hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}, \
       {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}, \
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

# url='http://www.douban.com/tag/%E5%B0%8F%E8%AF%B4/book?start=0' # For Test
url = 'https://book.douban.com/tag/小说?start=20&type=T'

http = urllib3.PoolManager()
response = http.request("GET", url,headers=hds[1])
a = response.data.decode("utf-8")
# print(a)
# get_parse(a)
from bs4 import BeautifulSoup
bs = BeautifulSoup(a,'html.parser')
c = bs.body.contents[1]
a = bs.find_all("li", class_="subject-item")
import re
titleE = r'title="(.+)"'
titlePattern = re.compile(titleE)
infoE=r"(.+ / .+ / .+ / .+)"
infoPattern=re.compile(infoE)
for x in a:
    d=x.find_all("div",class_="info")
    # print(d)
    for y in d:
        aa = y.find_all("a",class_="")
        book_name = re.findall(titlePattern, str(aa[0]))[0]
        author = (re.findall(infoPattern,str(y.find_all("div", class_="pub")[0]))[0]).split(" / ")[0]
        publisher = (re.findall(infoPattern,str(y.find_all("div", class_="pub")[0]))[0]).split(" / ")[1]
        publishDate = (re.findall(infoPattern,str(y.find_all("div", class_="pub")[0]))[0]).split(" / ")[2]
        price = (re.findall(infoPattern,str(y.find_all("div", class_="pub")[0]))[0]).split(" / ")[3]
        print(book_name , author, publisher,publishDate,price)
# print(bs.div.attrs)




