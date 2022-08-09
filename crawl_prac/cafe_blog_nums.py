import requests
import re
import json
import pandas as pd
import numpy as np
import datetime
from urllib import parse
import random
import time
from datetime import datetime,timedelta
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def to_int(text):
    import re
    p = re.compile(r'[()ㄱ-힣,\\n%]+') 
    return int(re.sub(p,"",text))

def cafe_blog_nums():
    characters = ["뽀로로","티니핑","타요","로보카폴리","쥬쥬","콩순이","옥토넛","또봇","터닝메카드","포켓몬","신비아파트","슈퍼윙스","브레드이발소","핑크퐁",
    "베이비버스","미니특공대","토닥토닥꼬모","스푸키즈","페파피그","라바","파자마삼총사","헬로카봇","소피루비","공룡메카드","빠샤메카드","슈퍼조조","리틀엔젤",
    "코코몽","다이노코어","미미월드","두다다쿵","미니언즈","티티체리","엄마까투리","아머드사우루스","베이블레이드","매지컬파티","슈퍼텐","메카드볼","요괴메카드",
    "띠띠뽀"]

    collect_date = format(datetime.now() ,'%Y-%m-%d')
    blog_date = format(datetime.now() - timedelta(days=1),'%Y-%m-%d')
    cafe_date = format(datetime.now() - timedelta(days=1),'%Y.%m.%d')
    cafe_query_date = format(datetime.now() - timedelta(days=1),'%Y%m%d')

    ua = UserAgent()

    blog_posting = []
    blog_posting_oneday = []
    cafe_posting = []
    cafe_posting_oneday = []

    for i in characters:
        headers = {"accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "referer": "https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=ALL&orderBy=sim&keyword="+parse.quote(i),
        "user-agent": ua.random,
        "sec-fetch-site": "same-origin"}

        url = 'https://section.blog.naver.com/ajax/SearchList.naver?countPerPage=7&currentPage=1&endDate=&keyword='+i+'&orderBy=sim&startDate=&type=post'
        response = requests.get(url,headers=headers)
        s = random.randint(3,6)
        time.sleep(s)

        data = response.text
        bp = data.split('"totalCount":')[1].split(",")[0]
        blog_posting.append(to_int(bp))
    ################################################################################################
        headers = {"accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "referer": "https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=PERIOD&orderBy=sim&startDate="+blog_date+"&endDate="+blog_date+"&keyword="+parse.quote(i),
        "user-agent": ua.random,
        "sec-fetch-site": "same-origin"}

        url = "https://section.blog.naver.com/ajax/SearchList.naver?countPerPage=7&currentPage=1&endDate="+blog_date+"&keyword="+i+"&orderBy=sim&startDate="+blog_date+"&type=post"
        response = requests.get(url,headers=headers)
        s = random.randint(3,6)
        time.sleep(s)

        data = response.text
        bpo = data.split('"totalCount":')[1].split(",")[0]
        blog_posting_oneday.append(to_int(bpo))
    ###############################################################################################
        headers = {"accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": '"ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"',
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://section.cafe.naver.com",
        "referer": "https://section.cafe.naver.com/ca-fe/home/search/articles?q="+parse.quote(i),
        "user-agent": ua.random,
        "sec-fetch-site": "same-site"}

        url = "https://apis.naver.com/cafe-home-web/cafe-home/v1/search/articles"
        cafe_query = {"query": i, "page": 1, "sortBy": 0, "period": ["20031201", "20220804"]}
        response = requests.post(url,headers=headers, data=json.dumps(cafe_query))
        s = random.randint(3,6)
        time.sleep(s)

        data = response.json()
        cp = data['message']['result']['totalCount']
        cafe_posting.append(cp)
    ##########################################################################################
        headers = {"accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": '"ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"',
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://section.cafe.naver.com",
        "referer": "https://section.cafe.naver.com/ca-fe/home/search/articles?q="+parse.quote(i)+"&pr=7&ps="+cafe_date+"&pe="+cafe_date,
        "user-agent": ua.random,
        "sec-fetch-site": "same-site"}

        url = "https://apis.naver.com/cafe-home-web/cafe-home/v1/search/articles"
        cafe_query = {"query": i, "page": 1, "sortBy": 0, "period": [cafe_query_date, cafe_query_date]}
        response = requests.post(url,headers=headers, data=json.dumps(cafe_query))
        s = random.randint(3,6)
        time.sleep(s)

        data = response.json()
        cpo = data['message']['result']['totalCount']
        cafe_posting_oneday.append(cpo)

    df = pd.DataFrame()
    df['character'] = characters
    df['collect_date'] = collect_date
    df['cafe_posting'] = cafe_posting
    df['blog_posting'] = blog_posting
    df['cafe_posting_oneday'] = cafe_posting_oneday
    df['blog_posting_oneday'] = blog_posting_oneday

    return df.to_excel("cafe_blog_nums.xlsx",index=False)

if __name__ == "__main__":
    cafe_blog_nums()
