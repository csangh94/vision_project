import pymysql
from bs4 import *
import urllib.request
for x in range(0,8):
    url = "https://ohou.se/contents/card_collections?style="+str(x)
    req = urllib.request.urlopen(url)
    res = req.read().decode('utf-8')
    soup = BeautifulSoup(res, 'html.parser')
    a=soup.find_all('a',{'class':'card-item__content__link'})
    # print(a[0]['href'])
    for y in a:
        url2 = "https://ohou.se"+y['href']
        req2 = urllib.request.urlopen(url2)
        res2 = req2.read().decode('utf-8')
        soup2 = BeautifulSoup(res2, 'html.parser')
        b=soup2.find('img', {'class': 'card-detail-card-image__image'})
        b2= soup2.find_all('span',{'class':'card-detail-header__prop'})
        if len(b2) <3:
            conn = pymysql.connect(host='localhost', port=3708, user='root', password='1234', db='test', charset='utf8')
            curs = conn.cursor()
            sql = "insert into test_photo values('"+b['src']+"','"+b2[0].text+"')"
            curs.execute(sql)
            conn.commit()
            conn.close()
        else:
            conn = pymysql.connect(host='localhost', port=3708, user='root', password='1234', db='test', charset='utf8')
            curs = conn.cursor()
            sql = "insert into test_photo values('"+b['src']+"','"+b2[1].text+"')"
            curs.execute(sql)
            conn.commit()
            conn.close()



