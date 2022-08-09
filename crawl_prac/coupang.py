import requests
import pandas as pd
import numpy as np
from urllib import parse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from module import today_date,to_int

def coupang():
    collect_date = today_date()

    ua = UserAgent()

    headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "referer": "https://www.coupang.com/np/categories/349657",
    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": ua.random}

    url = 'https://www.coupang.com/np/categories/349657?listSize=120&brand=&offerCondition=&filterType=&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&component=349557&rating=0'
    response = requests.get(url,headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    best120 = soup.select('dl.baby-product-wrap')

    title = []
    delivery = []
    delivery_rocket = []
    discount_price = []
    discount_rate = []
    price = []
    img_url = []
    review = []
    for i in range(120):
        ti = best120[i].select_one('div.name').text.strip()
        title.append(ti)
        img = best120[i].select_one('dt.image img')['src']
        img_url.append(img)
        dp = to_int(best120[i].select_one('strong.price-value').text)
        discount_price.append(dp)
        try:
            pr = to_int(best120[i].select_one('del.base-price').text)
            price.append(pr)
        except:
            price.append(np.nan)
        try:
            dr = to_int(best120[i].select_one('span.discount-percentage').text)
            discount_rate.append(dr)
        except:
            discount_rate.append(np.nan)
        try:
            deli = best120[i].select_one('span.badge.delivery-info').text
            delivery.append(deli)
        except:
            delivery.append(np.nan)
        try:
            rocket = best120[i].select_one('span.badge.rocket img')['alt']
            delivery_rocket.append(rocket)
        except:
            delivery_rocket.append(np.nan)
        try:
            rv = to_int(best120[i].select_one('span.rating-total-count').text)
            review.append(rv)
        except:
            review.append(np.nan)

    df = pd.DataFrame()
    df['title'] = title
    df['delivery'] = delivery
    df['delivery_rocket'] = delivery_rocket
    df['price'] = price
    df['discount_price'] = discount_price
    df['discount_rate'] = discount_rate
    df['img_url'] = img_url
    df['review'] = review
    df['collect_date'] = collect_date
    df['ranking'] = np.nan

    for i in range(len(df)):
        df['ranking'][i] = i+1

    df['delivery'][df['delivery'].isnull() & df['delivery_rocket'].notnull()] = df['delivery_rocket'][df['delivery'].isnull() & df['delivery_rocket'].notnull()]
    df.drop(['delivery_rocekt'],axis=1,inplace=True)

    df['price'][df['price'].isnull() & df['discount_price'].notnull()] = df['discount_price'][df['price'].isnull() & df['discount_price'].notnull()]
    df['discount_price'][df['discount_price'] == df['price']] = np.nan

    df = df.loc[:,['ranking','img_url','title','delivery','price','discount_rate','discount_price','review','collect_date']]

    return df.to_excel("coupang.xlsx")

if __name__ == "__main__":
    coupang()
