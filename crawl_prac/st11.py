from gc import collect
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import chromedriver_autoinstaller
import time
import numpy as np
from fake_useragent import UserAgent
from module import today_date,to_int

def st11():
    ua = UserAgent()
    
    collect_date = today_date()

    options = webdriver.ChromeOptions() # 크롬 옵션 객체 생성
    # options.add_argument('headless') # headless 모드 설정
    options.add_argument(f'user-agent={ua}')
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    driver = webdriver.Chrome(driver_path,options=options)

    url = 'https://www.11st.co.kr/browsing/BestSeller.tmall?method=getBestSellerMain&cornerNo=6&dispCtgrNo=1001362'
    driver.get(url=url)
    time.sleep(3)
    scroll_location = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        if scroll_location == scroll_height:
            break
        else:
            scroll_location = driver.execute_script("return document.body.scrollHeight")

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    best500 = soup.select('div.box_pd.ranking_pd')
    title = []
    delivery = []
    price = []
    discount_rate = []
    normal_price = []
    store = []
    img_url = []
    for i in range(len(best500)):
        img = best500[i].select_one('div.img_plot img')['src']
        img_url.append(img)
        ti = best500[i].select_one('div.pname p').text
        title.append(ti)
        pr = to_int(best500[i].select_one('strong.sale_price').text)
        price.append(pr)
        st = best500[i].select_one('div.store a').text
        store.append(st)
        try : 
            deli = best500[i].select_one('div.s_flag em').text
            delivery.append(deli)
        except:
            delivery.append(np.nan)
        try:
            rate = to_int(best500[i].select_one('span.sale').text)
            discount_rate.append(rate)
        except:
            discount_rate.append(np.nan)
        try:
            normal = to_int(best500[i].select_one('s.normal_price').text)
            normal_price.append(normal)
        except:
            normal_price.append(np.nan)

    df = pd.DataFrame()
    df['img_url'] = img_url
    df['title'] = title
    df['store'] = store
    df['delivery'] = delivery
    df['discount_price'] = price
    df['price'] = normal_price
    df['discount_rate'] = discount_rate

    df['price'][df['price'].isnull()] = df['discount_price'][df['price'].isnull() & df['discount_price'].notnull()]
    df['discount_price'][df['discount_price'] == df['price']] = np.nan
    df['discount_rate'][df['discount_rate'].isnull() & df['discount_price'].notnull()] = round((df['price'][df['price'].notnull()] - df['discount_price'][df['discount_price'].notnull()]) / df['price'][df['price'].notnull()] * 100)
    df['ranking'] = np.nan
    for i in range(len(df)):
        df['ranking'][i] = i+1

    df = df.loc[:,['ranking','img_url','title','delivery','price','discount_rate','discount_price']]
    df['collect_date'] = collect_date
    
    return df.to_excel("st11.xlsx",index=False)

if __name__ == "__main__":
    st11()
