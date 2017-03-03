#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
if __name__=="__main__":
    con = pymysql.connect(host='10.30.19.164', port=3306, user='echo', passwd='echosun', db='ScoreManagement',
                           charset='utf8')
    cur = con.cursor()
    sql = 'select * from ExamRes_1669'
    cur.execute(sql)
    # 获取查询结果
    result = cur.fetchall()
    for i in result:
        print(i[1])
    cur.close()
    con.close()





