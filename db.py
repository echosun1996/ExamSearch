#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
import random
import string
import getpass
#sql1="""select * from student"""
def db_init():
    user=raw_input('请输入数据库管理员用户名')
    pwd= getpass.getpass('请输入数据库管理员密码')
    con_tem = pymysql.connect(host='10.30.19.140', port=3306, user=user, passwd=pwd)
    print("Connect OK!")
    cur_tem = con_tem.cursor()
    try:
        cur_tem.execute("""CREATE USER 'echo' @ '%' IDENTIFIED BY 'echosun'""")
        cur_tem.execute("""create database ScoreManagement""")
        cur_tem.execute("""grant all on ScoreManagement.* to 'echo'@'%'""")
        con_tem.commit()
        print("Establish the table.")
        cur_tem.close()
        con_tem.close()
    except:
        con_tem.rollback()
        print("Error(-1)")

def init_db(con,conn,cursor):
    sql = """CREATE TABLE Students(
             No  VARCHAR(30) NOT NULL PRIMARY KEY,
             Name  VARCHAR(100)NOT NULL ,
             Email VARCHAR(100))"""
    try:
        sta = cursor.execute(sql)
        conn.commit()
        print("Establish the table.")
        return sta
    except:
        con.rollback()
        print("Error(0)")
def  conn_db():
    conn=pymysql.connect(host='10.30.19.140', port=3306, user='echo', passwd='echosun', db='ScoreManagement')
    cur=conn.cursor()
    print(123)
    return (conn,cur)
def update_db(con,cur,sql,value):
    try:
        sta = cur.execute(sql,value)# 执行成功后sta值为1。
        con.commit()
        return (sta)
    except:
        con.rollback()
        print("error")
def close_db(con,cur):
    cur.close()
    con.close()

if __name__=="__main__":
    fun=-1
    if(fun!=-1):
        con, cur = conn_db()
    if(fun==-1):
        print("数据库初始化开始")
        db_init();
    elif(fun==0):
        init_db(con,cur)
    elif(fun==1):
        sql = 'INSERT INTO ScoreManagement.Students(No, Name) VALUES (%s,%s)'
        update_db(con, cur, sql,('no','name'))

    #随机写入测试
    testtp=0
    class st:
        def init(self, a, b):
            self.no = a
            self.name = b
        def dis(self):
            return self.no, self.name
    test = st()
    while(testtp):
        salt1 = ''.join(random.sample(string.ascii_letters + string.digits, 3))
        salt2 = ''.join(random.sample(string.ascii_letters + string.digits, 3))
        test.init(str(salt1),str(salt2))
        sql = 'INSERT INTO ScoreManagement.Students(No, Name) VALUES (%s,%s)'
        if(update_db(con, cur, sql, test.dis())!=1):
            exit()
    close_db(con,cur)





