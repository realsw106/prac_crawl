from gc import collect
from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl
import datetime
from selenium import webdriver
import chromedriver_autoinstaller
import time
import random
import numpy as np
import os
from fake_useragent import UserAgent

def to_int(text):
    import re
    p = re.compile(r'[()ㄱ-힣,\\n%]+')  #\\n%추가
    return int(re.sub(p,"",text))

def ssg():
    collect_date = datetime.datetime.now().strftime("%Y-%m-%d")

    ua = UserAgent()
    headers = {'user-agent': ua.random}
    
    url = 'https://www.ssg.com/service/bestMain.ssg?zoneId=5000016039&ctgId=6000161219'

    response = requests.get(url,headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    best100 = soup.select('li.cunit_t290')
    title = []
    delivery = []
    price = []
    discount_rate = []
    normal_price = []
    store = []
    brand=[]
    img_url = []
    review = []
    for i in range(len(best100)):
        img = best100[i].select_one('div.thmb a img')['src']
        img_url.append(img)
        ti = best100[i].select_one('div.title a em.tx_ko').text
        title.append(ti)
        pr = to_int(best100[i].select_one('div.opt_price em.ssg_price').text)
        price.append(pr)
        st = best100[i].select_one('span.cm_mall_ic.ty_rect_s.notranslate').text.strip()
        store.append(st)
        try : 
            deli = best100[i].select_one('div.tx_deiv').text.strip()
            delivery.append(deli)
        except:
            delivery.append(np.nan)
        try:
            rate = to_int(best100[i].select_one('span.sale').text)
            discount_rate.append(rate)
        except:
            discount_rate.append(np.nan)
        try:
            normal = to_int(best100[i].select_one('div.org_price em.ssg_price').text)
            normal_price.append(normal)
        except:
            normal_price.append(np.nan)
        try:
            rv = to_int(best100[i].select_one('span.rate_tx').text)
            review.append(rv)
        except:
            review.append(np.nan)
        try:
            br = best100[i].select_one('strong.brd em.tx_ko').text
            brand.append(br)
        except:
            brand.append(np.nan)

    df = pd.DataFrame()
    df['img_url'] = img_url
    df['title'] = title
    df['store'] = store
    df['delivery'] = delivery
    df['discount_price'] = price
    df['price'] = normal_price
    df['discount_rate'] = discount_rate
    df['review'] = review
    df['brand'] = brand

    df['price'][df['price'].isnull()] = df['discount_price'][df['price'].isnull() & df['discount_price'].notnull()]
    df['discount_price'][df['discount_price'] == df['price']] = np.nan
    df['discount_rate'][df['discount_rate'].isnull() & df['discount_price'].notnull()] = round((df['price'][df['price'].notnull()] - df['discount_price'][df['discount_price'].notnull()]) / df['price'][df['price'].notnull()] * 100)
    df['ranking'] = np.nan
    for i in range(len(df)):
        df['ranking'][i] = i+1

    df = df.loc[:,['ranking','img_url','title', 'store', 'brand','delivery','price','discount_rate','discount_price','review']]
    df['collect_date'] = collect_date
    
    return df.to_excel("ssg.xlsx",index=False)

if __name__ == "__main__":
    ssg()
