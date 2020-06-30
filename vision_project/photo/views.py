import pymysql as pymysql
from django.shortcuts import render
from collections import Counter
import sys
import argparse
import requests

# Create your views here.
def insert(request):
    data = request.GET.get('style')
    conn = pymysql.connect(host='localhost', port=3708, user='root', password='1234', db='test', charset='utf8')
    curs = conn.cursor()
    sql = "insert into test_user values('" + data + "')"
    curs.execute(sql)
    conn.commit()
    conn.close()
def select_phtot():
    conn = pymysql.connect(host='localhost', port=3708, user='root', password='1234', db='test', charset='utf8')
    curs = conn.cursor()
    sql = "select * from test_photo order by rand() limit 5"
    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()
    test_list=[]
    for x in rows:
        test_dic={}
        test_dic['img']=x[0]
        test_dic['style']=x[1]
        test_list.append(test_dic)
    return test_list

def select_style():
    conn = pymysql.connect(host='localhost', port=3708, user='root', password='1234', db='test', charset='utf8')
    curs = conn.cursor()
    sql = "select * from test_user"
    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()
    return rows
def best(style):
    conn = pymysql.connect(host='localhost', port=3708, user='root', password='1234', db='test', charset='utf8')
    curs = conn.cursor()
    sql = "select * from test_photo where style='"+style+"'order by rand() limit 1"
    curs.execute(sql)
    rows = curs.fetchone()
    conn.close()
    return rows
def best_all(style):
    conn = pymysql.connect(host='localhost', port=3708, user='root', password='1234', db='test', charset='utf8')
    curs = conn.cursor()
    sql = "select * from test_photo where style='"+style+"'order by rand() limit 10"
    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()
    return rows
def main(request):
    test_list=select_phtot()
    user_list=select_style()
    if len(user_list) ==0:
        ff_dic = {"user": user_list, "photo": test_list}
        return render(request, 'photo/main.html',{"list":ff_dic})
    else:
        test_b = []
        for x in select_style():
            test_b.append(x[0])
        best_user = Counter(test_b).most_common(1)[0][0]
        best_one = best(best_user)

        API_URL = 'https://kapi.kakao.com/v1/vision/multitag/generate'
        MYAPP_KEY = '3a61addcaafcb1ed123b812e733f963a'
        sites = []
        for u in best_all(best_user):
            sites.append(u[0])
        parser = argparse.ArgumentParser(description='')
        parser.add_argument('image_url', type=str, nargs='?', default=sites)
        args = parser.parse_args()
        head = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)}
        test_list1 = []
        for x2 in sites:
            data = {'image_url': x2}
            result = requests.post(API_URL, headers=head, data=data)
            json = result.json()
            result_json = json['result']
            data2 = result_json['label_kr']
            for z in data2:
                test_list1.append(z)
        best_style={"name":Counter(test_list1).most_common(1)[0][0],"count":Counter(test_list1).most_common(1)[0][1]}
        best_dic = {"img":best_one[0],"user":best_one[1]}
        ff_dic={"user":user_list,"photo":test_list,"best":best_dic,"best_style":best_style}

        return render(request,'photo/main.html',{"list":ff_dic})

