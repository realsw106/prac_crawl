import requests
import re
import json
import pandas as pd
import numpy as np
import datetime
from fake_useragent import UserAgent
import time
from module import today_date,to_int

def wmp():
    collect_date = today_date()

    ua = UserAgent()
    headers = {'user-agent': ua.random}
    url = 'https://front.wemakeprice.com/best/16?categoryId=1100078'
    response = requests.get(url,headers=headers)
    time.sleep(3)
    data = response.text

    collect_date = datetime.datetime.now().strftime("%Y-%m-%d")

    cleandata = re.search("GV.set\('initialData', JSON.parse\(.*}}'\)\);",data).group().rstrip("'));").lstrip("GV.set(\'initialData\', JSON.parse(\'")
    jdata = json.loads(cleandata.replace('\\', '\\\\'), strict=False)

    data = {}
    for i,j in enumerate(jdata["deals"]):
        data[str(i)] = {
            "title":j["dispNm"],
            "img_url" : j["originImgUrl"],
            "price_1" : j["originPrice"],
            "price" : j["salePrice"],
            "discount_price" : j["discountPrice"],
            "discount_rate" : j["discountRate"],
            "delivery" : j["shipText"],
            "review" : j["reviewCount"]}

    df = pd.DataFrame(data)
    df = df.transpose()

    df['discount_price'][df['discount_price'] == 0] = np.nan
    df['discount_rate'][df['discount_rate'] == 0] = np.nan
    df['price_1'][df['price_1'] == 0] = np.nan
    df['review'][df['review'] == 0] = np.nan
    df["discount_price"][df['discount_rate'].notnull() & df['discount_price'].isnull() & df['price'].notnull() & df['price_1'].notnull()] = df['price']
    df['price'][df['discount_price'] == df['price'] & df['discount_rate'].notnull() & df['price_1'].notnull()] = df['price_1']

    df['ranking'] = np.nan
    for i in range(100):
        df['ranking'][i] = i+1

    df = df.loc[:,['ranking','img_url','title','delivery','price','discount_rate','discount_price','review']]

    df['collect_date'] = collect_date
    
    

    return df.to_excel("wmp.xlsx",index=False)

if __name__ == "__main__":
    wmp()