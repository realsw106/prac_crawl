def today_date():
    import datetime
    collect_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return collect_date

def to_int(text):
    import re
    p = re.compile(r'[ㄱ-힣,\\n%]+')  #\\n%추가
    return int(re.sub(p,"",text))