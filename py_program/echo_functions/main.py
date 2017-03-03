#!/usr/bin/env python
# -*- coding:utf-8 -*-

import configparser
import pymysql
##新建用户、分配权限、新建数据库、新建表，完成后登出
def db_init():
    user = input('请输入数据库管理员用户名')
    pwd = input('请输入数据库管理员密码')
    con_tem = pymysql.connect(host='10.30.19.140', port=3306, user=user, passwd=pwd, db='mysql')
    print("Connect OK!")
    cur_tem = con_tem.cursor()
    try:
        cur_tem.execute("""CREATE USER 'echo'@'%' IDENTIFIED BY 'echosun'""")
        con_tem.commit()
        cur_tem.execute("""create database ScoreManagement""")
        con_tem.commit()
        cur_tem.execute("""grant all on ScoreManagement.* to 'echo'@'%'""")
        con_tem.commit()
        print("Finish init.")
        cur_tem.close()
        con_tem.close()
    except:
        con_tem.rollback()
        print("Error(-1)")
##连接数据库
def conn_db():
    conn = pymysql.connect(host='10.30.19.140', port=3306, user='echo', passwd='echosun', db='ScoreManagement')
    return [conn, conn.cursor()]
##新建学生表
def init_db(cur, con):
    try:
        sta = cur.execute('CREATE TABLE Students(No  VARCHAR(30) NOT NULL PRIMARY KEY,Name  VARCHAR(100)NOT NULL ,Email VARCHAR(100))')
        con.commit()
        print("Establish the table.")
        return sta
    except:
        con.rollback()
        print("Error(0)")
##增加数据
def update_db(con,cur,sql,value):
    try:
        sta = cur.execute(sql,value)
        con.commit()
        return sta
    except:
        con.rollback()
        print("error")
##查找数据
def select_db(con,cur,sql):
    try:
        cur.execute(sql)
        res = cur.fetchall()
        con.commit()
        return res
    except:
        con.rollback()
        print("error")
##关闭数据库
def close_db(con,cur):
    cur.close()
    con.close()
if __name__=="__main__":
    conf = configparser.ConfigParser()
    while True:
        #0或不存在
        while conf.read('conf.ini') == [] or conf.sections() == [] or conf.get('status', 'fun') == '0':
            print("数据库初始化开始")
            db_init()
            fp=open('conf.ini','r+')
            conf.add_section('status')
            conf.set('status', 'fun','1')
            conf.write(fp)
            fp.close()
        conf.read('conf.ini')
        fp = open('conf.ini', 'r+')
        con, cur = conn_db()
        if conf.get('status', 'fun') == '1':
            init_db(con, cur)
            conf.set('status', 'fun', '2')
            conf.write(fp)
        elif conf.get('status', 'fun') == '2':
            sql = 'INSERT INTO ScoreManagement.Students(No, Name) VALUES (%s,%s)'
            update_db(con, cur, sql, ('no', 'name'))
            conf.set('status', 'fun', '3')
            conf.write(fp)
        elif conf.get('status', 'fun')== '3':
            sql = 'SELECT * from Students'
            res = select_db(con, cur, sql)
            print(res)
            conf.set('status', 'fun', '4')
            conf.write(fp)
        elif conf.get('status', 'fun')== '4':
            conf.set('status', 'fun', '3')
            conf.write(fp)
            exit()
        else:
            conf.set('status', 'fun', '0')
            conf.write(fp)
        print('fun' + '=' + conf.get('status','fun'))
        fp.close()
        close_db(con, cur)