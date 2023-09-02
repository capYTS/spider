import random
import time

import urllib3
import re
from bs4 import BeautifulSoup
import traceback
import csv_excel
import sys

def getTagList(url, header):
    http = urllib3.PoolManager()
    response = http.request("GET", url,headers=header)
    repsonString = response.data.decode("utf-8")
    list = parseTagList(repsonString)
    return list



def parseTagList(repsonString):
    bs = BeautifulSoup(repsonString,'html.parser')
    a = bs.find_all("a")
    titleE = r'href="/tag/.+>(.+)</a>'
    titlePattern = re.compile(titleE)
    list = []  ## 空列表
    for x in a:
        # try:
        temp = re.findall(titlePattern,str(x))
        for i in temp:
                list.append(i)
        # except Exception:
        #     print(Exception)
    return list


def getBookList(url, header, category):
    notEnd = True
    page=0
    categoryList=[]
    while notEnd:
        http = urllib3.PoolManager()
        url_new = url.replace('${category}', category).replace('${num}', str(page * 20))
        response = http.request("GET", url_new,headers=header)
        repsonString = response.data.decode("utf-8")
        list = toBean(repsonString, category)
        csv_excel.writeRowsInfoToCsv(list, bookAttr, 'books_new.csv')
        time.sleep(10)
        categoryList = categoryList+list
        page=page+1
        if len(list) < 20:
            notEnd=False
    return categoryList



def toBean(repsonString,catory):
    bs = BeautifulSoup(repsonString,'html.parser')
    a = bs.find_all("li", class_="subject-item")
    titleE = r'title="(.+)"'
    titlePattern = re.compile(titleE)
    infoE=r"(.+ / .+)"
    infoPattern=re.compile(infoE)
    jianjieE=r"<p>(.+)</p>"
    jianjiePattern=re.compile(jianjieE)
    list = []  ## 空列表
    try:
        for x in a:
            d=x.find_all("div",class_="info")
            for y in d:
                aa = y.find_all("a",class_="")
                jianjie=''
                try:
                    jianjie1 = y.find_all("p", class_="")
                    jianjie = re.findall(jianjiePattern,str(jianjie1).replace("\n",' '))[0].strip()
                except Exception as e:
                    print(e)
                book_name = re.findall(titlePattern, str(aa[0]))[0].strip()
                book_info=''
                try:
                    book_info = re.findall(infoPattern,str(y.find_all("div", class_="pub")[0]))[0]
                    a = book_info[::-1].split(" / ")
                    price = a[0].strip()[::-1]
                    author=''
                    translator=''
                    publisher=''
                    publishDate=''
                    if len(a) ==3 :
                        publisher = a[1].strip()[::-1]
                        author = a[2].strip()[::-1]
                    elif len(a)==4:
                        publishDate = a[1].strip()[::-1]
                        publisher = a[2].strip()[::-1]
                        author = a[3].strip()[::-1]
                    elif len(a)==5:
                        publishDate = a[1].strip()[::-1]
                        publisher = a[2].strip()[::-1]
                        translator = a[3].strip()[::-1]
                        author = a[4].strip()[::-1]
                    info = {'category': catory, 'book_name': book_name, 'author': author, 'translator': translator, 'publisher': publisher, 'publishDate': publishDate, 'price': price,'jianjie':jianjie}
                except Exception as e:
                    traceback.print_exc()
                    print(e)
                    print(book_name)
                    info = {'category': catory, 'book_name': book_name, 'book_info':book_info,'jianjie':jianjie}
                list.append(info)
    except IndexError:
        print("not found")
    return list

url = 'https://book.douban.com/tag/${category}?start=${num}&type=T'

hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
       {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
header=hds[random.randint(0,2)]
tagUrl='https://book.douban.com/tag/'
tagList = getTagList(tagUrl,header)
bookAttr=['category','book_name','author','translator','publisher','publishDate','price','book_info','jianjie']
# csv_excel.writeHeaderInfoToCsv(bookAttr,'books_new.csv')
mark=0
for tag in tagList:

    try:
        if tag=='武侠':
            mark = 1
        if mark!=1:
            continue
        temp=getBookList(url, header, tag)
        print(tag)
        print(len(temp))
        if(len(temp)==0):
            print("aa")

        # csv_excel.writeRowsInfoToCsv(temp,bookAttr,'books.csv')

    except Exception :
        print(Exception)
