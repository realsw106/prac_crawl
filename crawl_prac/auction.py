from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random
import numpy as np
import datetime
from fake_useragent import UserAgent
from module import today_date,to_int

def auction():
    from module import today_date,to_int
    ua = UserAgent()

    url = 'http://corners.auction.co.kr/corner/categorybest.aspx?catetab=5&category=20000000'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    url_list = []
    img_url = []
    title = []
    price = []
    discount_price = []
    discount_rate = []
    delivery = []

    best100 = soup.select('div.info')

    for i in range(len(best100)):
        co = best100[i].select_one('div.img > a')['onclick'].split(".")[3].split(",")[1][2:12]
        url = 'http://browse.auction.co.kr/search/item?itemno='+co
        url_list.append(url)
        img = best100[i].select_one('div.img a img')['src']
        img_url.append(img)
        ti = best100[i].select_one('div.img a img')['alt']
        title.append(ti)
        dp = to_int(best100[i].select_one('span.sale span').text)
        discount_price.append(dp)

        try:
            pr = to_int(best100[i].select_one('strike span').text)
            price.append(pr)
        except:
            price.append(np.nan)
        try:
            dr = to_int(best100[i].select_one('span.down').text)
            discount_rate.append(dr)
        except:
            discount_rate.append(np.nan)
        try:
            deli = best100[i].select_one('div.icons.ic_free span').text
            delivery.append(deli)
        except:
            delivery.append(np.nan)

    review = []
    purchase = []
    store = []
    for i in url_list:
        url = i
        headers = {'user-agent': ua.random}
        response = requests.get(url, headers=headers)
        time.sleep(random.randint(2,5))
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        time.sleep(random.randint(2,5))
        try:
            rv = to_int(soup.select_one('span.text--reviewcnt').text)
            review.append(rv)
        except:
            review.append(np.nan)
        try:
            pur = to_int(soup.select_one('span.text--buycnt').text)
            purchase.append(pur)
        except:
            purchase.append(np.nan)
        try:
            st = soup.select_one('div.section--itemcard_info_shop a span.text').text
            store.append(st)
        except:
            store.append(np.nan)

    df = pd.DataFrame()
    df['title'] = title
    df['img_url'] = img_url
    df['price'] = price
    df['discount_price'] = discount_price
    df['discount_rate'] = discount_rate
    df['delivery'] = delivery
    df['review'] = review
    df['purchase'] = purchase
    df['store'] = store
    df['collect_date'] = collect_date

    df['price'][df['discount_price'].notnull() & df['price'].isnull()] = df['discount_price'][df['discount_price'].notnull() & df['price'].isnull()]
    df['discount_price'][df['discount_price']==df['price']] = np.nan

    df['price'][df['discount_price'].notnull() & df['price'].isnull()] = df['discount_price'][df['discount_price'].notnull() & df['price'].isnull()]
    df['discount_price'][df['discount_price']==df['price']] = np.nan
    df['ranking'] = np.nan
    for i in range(len(df)):
        df['ranking'][i] = i+1

    df = df.loc[:,['ranking','img_url','title','delivery','price','discount_rate','discount_price','store','review','purchase','collect_date']]

    return df.to_excel("auction.xlsx",index=False)

if __name__ == "__main__":
    auction()
