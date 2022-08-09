from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl
import time
import random
import numpy as np
import os
import datetime
from fake_useragent import UserAgent

def to_int(text):
    import re
    p = re.compile(r'[()ㄱ-힣,\\n%]+')  #\\n%추가
    return int(re.sub(p,"",text))

def gmarket():
    collect_date = datetime.datetime.now().strftime("%Y-%m-%d")

    ua = UserAgent()
    url = 'http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G04&subGroupCode=S076'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    best100 = soup.select('div.thumb')
    best100_info = soup.select('div.item_price')

    url_list = []
    title = []
    img_url = []
    discount_price = []
    price = []
    discount_rate = []
    free_delivery = []
    for i in range(100):
        co = best100[i].select_one('a img.lazy')['data-original'].split('/')[3]
        url = 'http://browse.gmarket.co.kr/search?keyword=' + co
        url_list.append(url)
        img = best100[i].select_one('a img.lazy')['data-original']
        img_url.append(img)
        ti = best100[i].select_one('a img.lazy')['alt']
        title.append(ti)
        dp = to_int(best100_info[i].select_one('div.s-price strong span').text)
        discount_price.append(dp)
        try:
            pr = to_int(best100_info[i].select_one('div.o-price span').text)
            price.append(pr)
        except:
            price.append(np.nan)
        try:
            dr = to_int(best100_info[i].select_one('div.s-price span em').text)
            discount_rate.append(dr)
        except:
            discount_rate.append(np.nan)
        try:
            fd = best100_info[i].select_one('div.icon img')['alt']
            free_delivery.append(fd)
        except:
            free_delivery.append(np.nan)

    brand = []
    store = []
    delivery = []
    purchase = []
    review = []
    empty = []
    for i in url_list:
        headers = {'user-agent': ua.random}
        response = requests.get(i,headers=headers)
        time.sleep(random.randint(2,5))
        html = response.text
        time.sleep(random.randint(2,5))
        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            st = soup.select_one('span.text__seller').text
            store.append(st)
        except:
            store.append(np.nan)

        try:
            br = soup.select_one('span.text__brand').text
            brand.append(br)
        except:
            brand.append(np.nan)

        try:
            de = soup.select_one('li.list-item__tag').text
            delivery.append(de)
        except:
            delivery.append(np.nan)
        try:
            pur = to_int(soup.select_one('li.list-item.list-item__pay-count > span.text').text)
            purchase.append(pur)
        except:
            purchase.append(np.nan)

        try:
            rv = to_int(soup.select_one('li.list-item.list-item__feedback-count > span.text').text)
            review.append(rv)
        except:
            review.append(np.nan)
            
        try:
            ty = soup.select_one('em.text__keyword').text
            empty.append(ty)
        except:
            empty.append(np.nan)   

    df = pd.DataFrame()

    df['img_url'] = img_url
    df['title'] = title
    df['brand'] = brand
    df['store'] = store
    df['free_delivery'] = free_delivery
    df['delivery'] = delivery
    df['price'] = price
    df['discount_rate'] = discount_rate
    df['discount_price'] = discount_price
    df['purchase'] = purchase
    df['review'] = review
    df['empty'] = empty

    df['ranking'] = np.nan
    for i in range(100):
        df['ranking'][i] = i+1

    df['price'][df['price'].isnull()] = df['discount_price']
    df['discount_price'][df['discount_rate'].isnull()] = np.nan
    df['delivery'][df['free_delivery'].notnull()] = df['free_delivery']
    df['delivery'][df['empty'].notnull()] = '일시품절'

    df.drop(['free_delivery','empty'],axis=1,inplace=True)
    df['collect_date'] = collect_date

    return df

if __name__ == "__main__":
    gmarket()
