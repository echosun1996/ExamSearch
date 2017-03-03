#!/usr/bin/env python
# -*- coding:utf-8 -*-

###########mysql################
import configparser
import os
import urllib.request
import pymysql
from bs4 import BeautifulSoup
##连接数据库
def conn_db():
    cd_con = pymysql.connect(host='10.30.19.164', port=3306, user='echo', passwd='echosun', db='ScoreManagement',
                          charset='utf8')
    return [cd_con, cd_con.cursor()]
##新建用户、分配权限、新建数据库、新建表，完成后登出
def db_init():
    user = input('请输入数据库管理员用户名')
    pwd = input('请输入数据库管理员密码')+
    stu_pre=input('请输入学号前缀')
    exam_pre=input('请输入考试名前缀')
    try:
        con_tem = pymysql.connect(host='10.30.19.164', port=3306, user=user, passwd=pwd, db='mysql', charset='utf8')
        print("Connect OK!")
        cur_tem = con_tem.cursor()
    except:
        print('User information is wrong!')
        system_init()
    try:
        cur_tem.execute('DELETE FROM Management.ec_score_score;')
        cur_tem.execute('DROP TABLE ScoreManagement.Exam_Search')
        cur_tem.execute('DROP TABLE ScoreManagement.Students')
        cur_tem.execute('DROP TABLE ScoreManagement.System')
        con_tem.commit()
    except:
        print('Table not exist')
    try:
        cur_tem.execute('DROP DATABASE ScoreManagement')
        con_tem.commit()
    except:
        print('Database not exist')
    try:
        cur_tem.execute("""DROP USER 'echo'@'%'""")
        con_tem.commit()
    except:
        print('User not exist')
    try:
        cur_tem.execute("CREATE USER 'echo'@'%' IDENTIFIED BY 'echosun'")
        cur_tem.execute("create database ScoreManagement CHARACTER SET 'utf8' COLLATE 'utf8_general_ci'")
        cur_tem.execute("grant all on ScoreManagement.* to 'echo'@'%'")
        cur_tem.execute("grant all on Management.* to 'echo'@'%'")
        con_tem.commit()
        print("Finish init.")
    except:
        con_tem.rollback()
        print("Error(-1)")
    cur_tem.close()
    con_tem.close()
    con_tem2,cur_tem2=conn_db()
    print("OK")
    try:
        cur_tem2.execute(
            "CREATE TABLE System(Sys_Name  VARCHAR(100) NOT NULL PRIMARY KEY,Sys_Value  VARCHAR(100)NOT NULL )ENGINE=InnoDB DEFAULT CHARSET=utf8")
        cur_tem2.execute(
            "CREATE TABLE Students(No VARCHAR(30) NOT NULL PRIMARY KEY,Stu_Name  VARCHAR(100)NOT NULL ,Email VARCHAR(100),QQ VARCHAR(20),Stu_Finish INT,RankSum INT)ENGINE=InnoDB DEFAULT CHARSET=utf8")
        cur_tem2.execute(
            "CREATE TABLE Exam_Search(CID  SMALLINT NOT NULL PRIMARY KEY,Exam_Name VARCHAR(100)NOT NULL ,Status SMALLINT )ENGINE=InnoDB DEFAULT CHARSET=utf8")
        con_tem2.commit()
    except:
        print("Error(CREATE TABLE)")
    # 新建存储过程
    try:
        cur_tem2.execute("CREATE PROCEDURE insert_system(name VARCHAR(100),value VARCHAR(100))MODIFIES SQL DATA BEGIN INSERT INTO System(Sys_Name,Sys_Value)VALUES(name,value);END")
        con_tem2.commit()
    except:
        print("Establish PROCEDURE Error!")
    try:
        cur_tem2.execute("CALL insert_system('exam_pre',%s)", exam_pre)
        cur_tem2.execute("CALL insert_system('student_pre',%s)", stu_pre)
        con_tem2.commit()
        print("Establish the table.")
    except:
        print("Error(0)")

    #删除存在的触发器
    #try:
    #    cur_tem2.execute("DROP TRIGGER IF EXISTS insert_on_management;")
    #except:
    #    print("Trigger Not Exist(1)")
    #try:
    #    cur_tem2.execute("DROP TRIGGER IF EXISTS update_on_management;")
    #except:
    #    print("Trigger Not Exist(2)")

    #新建触发器
    try:
        cur_tem2.execute("CREATE TRIGGER insert_on_management AFTER INSERT ON Students FOR EACH ROW BEGIN INSERT INTO Management.ec_score_score (NO,Stu_name,Email,QQ,Stu_Finish,RankSum)VALUES(new. NO,new.Stu_name,new.Email,new.QQ,new.Stu_Finish,	new.RankSum	) ;END;")
        con_tem2.commit()
    except:
        print("Establish Trigger Not Success！(1)")
    try:
        cur_tem2.execute("CREATE TRIGGER update_on_management AFTER UPDATE ON Students FOR EACH ROW BEGIN UPDATE Management.ec_score_score SET Stu_Finish=new.Stu_Finish WHERE Management.ec_score_score.No=new.No;UPDATE Management.ec_score_score SET RankSum=new.RankSum WHERE Management.ec_score_score.No=new.No;END;")
        con_tem2.commit()
    except:
        print("Establish Trigger Not Success！(2)")
    #新建视图
    try:
        cur_tem2.execute("CREATE VIEW display(学号,姓名,完成总数,排名和)AS SELECT NO,Stu_Name,Stu_Finish,RankSum FROM Students WHERE Stu_Finish!=0 AND RankSum!=0 ORDER BY Stu_Finish DESC;")
        con_tem2.commit()
    except:
        print("Establish View Error!")
    #新建多列索引
    try:
        cur_tem2.execute("ALTER TABLE Students ADD INDEX indexNo (NO(30),Stu_Name);")
        con_tem2.commit()
    except:
        print("Establish View Error!")
    #新建唯一索引
    try:
        cur_tem2.execute("ALTER TABLE Students ADD UNIQUE (NO);")
        cur_tem2.execute("ALTER TABLE Students ADD UNIQUE (Stu_Name);")
        con_tem2.commit()
    except:
        print("Establish View Error!")
    cur_tem2.close()
    con_tem2.close()

##增加数据
def update_db(ud_con, ud_cur, ud_sql, value):
    try:
        sta = ud_cur.execute(ud_sql, value)
        ud_con.commit()
        return sta
    except:
        ud_con.rollback()
        print("error")
##查找数据
def select_db(sd_con, ud_cur, ud_sql):
    try:
        ud_cur.execute(ud_sql)
        sd_res = ud_cur.fetchall()
        sd_con.commit()
        return sd_res
    except:
        sd_con.rollback()
        print("error")
##关闭数据库
def close_db(cd_con, cd_cur):
    cd_cur.close()
    cd_con.close()
def system_init():
    conf_ini = configparser.ConfigParser()
    if conf_ini.read('conf.ini') == [] or conf_ini.sections() == [] or conf_ini.get('status', 'fun') != '1':
        print("数据库初始化开始")
        db_init()
        # createdb
        si_con, si_cur = conn_db()
        close_db(si_con, si_cur)
        # set conf.ini
        conf_fp = open('conf.ini', 'w')
        conf_ini.add_section('status')
        conf_ini.set('status', 'fun', '1')
        conf_ini.write(conf_fp)
        conf_fp.close()
    else:
        com = input('System having establish,reestablish?(y/n)')
        if com == 'y':
            os.remove('conf.ini')
            system_init()
        else:
            exit()
########################stystem表更新程序###########################
def update_system(name, value):
    [us_con,us_cur] = conn_db()
    try:
        us_cur.execute("INSERT INTO System(Sys_Name,Sys_Value)VALUES(%s,%s)", (name, value))
        us_con.commit()
        us_con.close()
        us_cur.close()
    except:
        print('update_system error!')
###################system_config###################################
def system_config():
    name = input()
    value = input()
    update_system(str(name), str(value))
########################ExamSearch表新增程序###########################
def Insert_ExamSearch(cid, exam_name, status):
    [ue_con, ue_cur] = conn_db()
    try:
        ue_cur.execute("INSERT INTO Exam_Search(CID,Exam_Name,Status)VALUES(%s,%s,%s)", (cid, exam_name, status))
        ue_con.commit()
        ue_con.close()
        ue_cur.close()
    except:
        print(' ')

##################ExamSearch_config###################################
def ExamSearch_config():
    ##比赛爬虫
    exam_pre = get_pre(2)
    exam_url = 'http://acm.sdibt.edu.cn/JudgeOnline/contest.php?search='
    exam_url += exam_pre
    response = urllib.request.urlopen(exam_url)
    soup = BeautifulSoup(response, "lxml", from_encoding="utf-8")
    print("网页标题:" + soup.title.string)  # 获取标题
    '''获取各种量'''
    for exam_tem in soup.findAll(align='center'):
        if 'evenrow' in str(exam_tem) or 'oddrow' in str(exam_tem):
            cid = exam_tem.td.string
            print("id:" + exam_tem.td.string)
            exam_name = exam_tem.a.string
            print("title:" + exam_tem.a.string)
            exam_status = exam_tem.find_next('font').string
            if exam_status == ' Running ':
                exam_status = 'Running'
                Insert_ExamSearch(cid, exam_name, 0)
            else:
                Insert_ExamSearch(cid, exam_name, 1)
            print('status:' + exam_status)
########################student表更新程序###########################
def update_student(No, Stu_Name,Email,QQ):
    [us_con,us_cur] = conn_db()
    try:
        us_cur.execute("INSERT INTO Students(No,Stu_Name,Email,QQ,Stu_Finish,RankSum)VALUES(%s,%s,%s,%s,0,0)", (No, Stu_Name,Email,QQ))
        us_con.commit()
        us_con.close()
        us_cur.close()
    except:
        print('update_system error!')

###################student_config###################################
def Student_config():
    ##学生爬虫
    stu_pre = get_pre(1)
    stu_url = 'http://acm.sdibt.edu.cn/JudgeOnline/ranklist.php?search='
    stu_url += stu_pre
    response = urllib.request.urlopen(stu_url)
    soup = BeautifulSoup(response, "lxml", from_encoding="utf-8")
    print("网页标题:" + soup.title.string)  # 获取标题
    '''获取各种量'''
    for stu_tem in soup.findAll('tr'):
        if 'evenrow' in str(stu_tem) or 'oddrow' in str(stu_tem):
            #print(stu_tem.td.string)  # 序号
            stu_tem = stu_tem.find_next('a')
            #print(stu_tem.string)  # 学号
            No = stu_tem.string
            stu_tem = stu_tem.find_next('td')
            #print(stu_tem.string)  # 姓名
            Stu_Name = stu_tem.string
            stu_tem = stu_tem.find_next('a')
            #print(stu_tem.string)  # AC
            stu_tem = stu_tem.find_next('a')
            #print(stu_tem.string)  # Submit
            stu_tem = stu_tem.find_next('td')
            #print(stu_tem.string)  # Ratio
            if len(No) < 6 :
                continue

            Email = Student_info(No)
            QQ = ""
            if Email is "":
                QQ = ""
            else:
                re_email1 = re.compile(r'[0-9a-zA-Z.]+@qq.com')
                re_email2 = re.compile(r'[0-9a-zA-Z.]+qq.com')
                if re_email1.match(Email):
                    #print(str(Email).split('@')[0])
                    QQ = str(Email).split('@')[0]
                elif re_email2.match(Email):
                    QQ = Email[0:Email.find("qq.com")]
            print(Email+QQ)
            update_student(No, Stu_Name,Email,QQ)
########################Student_info爬虫###########################
import re
def Student_info(info_id):
    ##学生信息爬虫
    info_url = 'http://acm.sdibt.edu.cn/JudgeOnline/userinfo.php?user='
    info_url += info_id
    response = urllib.request.urlopen(info_url)
    soup = BeautifulSoup(response, "lxml", from_encoding="utf-8")
    print("网页标题:" + soup.title.string)  # 获取标题
    '''获取各种量'''
    for stu_tem in soup.findAll('td'):
        if 'Email:' in str(stu_tem):
            stu_tem = stu_tem.find_next('td')
            if stu_tem.string is None:
                return ""
            else:
                print(stu_tem.string)  # 序号
                return stu_tem.string
########################ExamRes表更新程序###########################
def update_ExamRes(ue_name, ue_info, ue_res, ue_sum):
    ue_sql='INSERT INTO ExamRes_' + ue_name + ' VALUES('
    for i in range(5):
        #print(info[i])
        ue_sql+= "'"+ue_info[i]+"'" + ','
    for i in range(ue_sum):
        if ue_res[i] == 'N':
            ue_sql += "'" + "'" + ','
        else:
            ue_sql+="'"+ue_res[i]+"'" + ','
    ue_sql=ue_sql[:-1]
    ue_sql+=')'
    print(ue_sql)
    [us_con,us_cur] = conn_db()
    print(str(ue_info[4]))
    #try:
    ##更新比赛数据
    us_cur.execute(ue_sql)
    us_con.commit()
    ##更新用户数据
    us_cur.execute('UPDATE Students SET Stu_Finish = Stu_Finish + %s WHERE Students.No = %s',
                   (str(ue_info[3]),str(ue_info[1])))
    us_con.commit()
    us_cur.execute('UPDATE Students SET RankSum = RankSum + %s WHERE Students.No = %s',
                   (str(ue_info[0]),str(ue_info[1])))
    us_con.commit()
    #except:
         #print('update_system error!')
    us_con.close()
    us_cur.close()
######################ExamRes表建立程序###############################
def set_ExamRes(se_name ,se_sum):
    [us_con,us_cur] = conn_db()
    try:
        ExamRes_sql = 'DROP TABLE ' + 'ExamRes_' + se_name
        us_cur.execute(ExamRes_sql)
        us_con.commit()
    except:
        print("is null")
    try:
        ExamRes_sql = 'CREATE TABLE ' + 'ExamRes_' + se_name + '(Rank SMALLINT PRIMARY KEY,Stu_ID VARCHAR (100) NOT NULL,Stu_Name VARCHAR (100) NOT NULL,Solved SMALLINT,Penalty VARCHAR (100))ENGINE = INNODB DEFAULT CHARSET = utf8'
        us_cur.execute(ExamRes_sql)
        us_con.commit()
    except:
        print('update_system error!')
    for i in range(se_sum):
        try:
            ExamRes_sql2 = "ALTER TABLE " + 'ExamRes_' + se_name + " ADD COLUMN " + chr(i + ord('A')) + " TIME"
            print(ExamRes_sql2)
            us_cur.execute(ExamRes_sql2)
            us_con.commit()
        except:
            print('update_system error!')
    us_con.close()
    us_cur.close()
###################ExamRes_config###################################
def ExamRes_config(res_pre):
    res_url = 'http://acm.sdibt.edu.cn/JudgeOnline/contestrank.php?cid='
    res_url += res_pre
    response = urllib.request.urlopen(res_url)
    soup = BeautifulSoup(response,"lxml",from_encoding="utf-8")
    print("网页标题:"+soup.title.string)#获取标题
    '''
    获取题目数量
    '''
    sum = 0
    for s in soup.findAll('a'):
       if s.string is not None:
            if len(s.string)==1 and "A" <= s.string[0] <= "Z":
                #print("--"+s.string+"--")
                sum+=1
    print("题目数:", end="")
    print(sum)
    '''获取各种量'''
    set_ExamRes(res_pre, sum)
    for res_tem in soup.findAll(align='center'):
        if 'evenrow' in str(res_tem) or 'oddrow' in str(res_tem):
            stu_info=''
            res_tem1=res_tem.td
            res_tem1 = res_tem1.find_next('td')
            #print(res_tem1.string)#序号
            stu_info=stu_info+res_tem1.string+'*'
            res_tem1 = res_tem1.find_next('a')
            print(res_tem1.string)#学号
            stu_info = stu_info + res_tem1.string + '*'
            res_tem1 = res_tem1.find_next('a')
            #print(res_tem1.string)#姓名
            stu_info = stu_info + res_tem1.string + '*'
            res_tem1 = res_tem1.find_next('td')
            #print(res_tem1.string)#做出题目数Solved
            stu_info = stu_info + res_tem1.string + '*'
            res_tem1 = res_tem1.find_next('td')
            #print(res_tem1.string)#做题总时长Penalty
            stu_info = stu_info + res_tem1.string + '*'
            stu_res = ''
            for i in range(sum):
                res_tem1 = res_tem1.find_next('td')
                res_tem2 = res_tem1.getText('*').split("*")
                if res_tem2[0] != '':
                    if res_tem2[0][0] !='(':
                        #print(chr(i + ord('A')) + ':'+res_tem2[0])
                        stu_res=stu_res+res_tem2[0]+'*'
                    else:
                        #print(chr(i + ord('A')) + ':' + 'NULL')
                        stu_res = stu_res +'N' + '*'
                else:
                    #print(chr(i+ ord('A'))+':'+'NULL')
                    stu_res = stu_res + 'N' + '*'
            print(stu_info.split('*'))
            print(stu_res.split('*'))

            update_ExamRes(res_pre,stu_info.split('*'), stu_res.split('*'),sum)
            print(stu_info.split('*')[3])

def ExamSelect():
    [exam_con, exam_cur] = conn_db()
    try:
        ExamSelect_sql = "SELECT CID FROM Exam_Search WHERE Status = 1"
        exam_cur.execute(ExamSelect_sql)
        data = exam_cur.fetchall()
        for exam in data:
            print(exam[0])
            ExamRes_config(str(exam[0]))#新建并处理exam表
            try:
                exam_cur.execute("UPDATE Exam_Search SET Status = 2 WHERE CID = %s",(str(exam[0])))
                exam_con.commit()
            except:
                print("Not Found!!")
    except:
        print("Error!")
    exam_con.close()
    exam_cur.close()
#获取所需要的前缀1返回学生名，2返回考试的前缀
def get_pre(i):
    [exam_con, exam_cur] = conn_db()
    if i==1:
        try:
            exam_cur.execute("SELECT Sys_Value from ScoreManagement.System WHERE Sys_Name='student_pre';")
            student_pre=exam_cur.fetchall()
            return student_pre[0][0]
        except:
            print("Error(get_1)")
    elif i==2:
        try:
            exam_cur.execute("SELECT Sys_Value from ScoreManagement.System WHERE Sys_Name='exam_pre';")
            exam_pre=exam_cur.fetchall()
            return exam_pre[0][0]
        except:
            print("Error(get_2)")
    else:
        print("Error(get_?)")
    exam_pre.close()
    exam_con.close()

########################ExamSearch表更新程序###########################
def Update_ExamSearch(cid, exam_name, status):
    [ue_con, ue_cur] = conn_db()
    try:
        ue_cur.execute("INSERT INTO Exam_Search(CID,Exam_Name,Status)VALUES(%s,%s,%s)", (cid, exam_name, status))
        ue_con.commit()
        ue_con.close()
        ue_cur.close()
    except:
        print(' ')

def demo():
    [exam_con, exam_cur] = conn_db()
    try:
        #exam_cur.execute({"SELECT Sys_Value from ScoreManagement.System WHERE Sys_Name='test_pre';")
        print(123)
    except:
        print("Error in search sysname!")
    exam_con.commit()
    exam_con.close()
    exam_cur.close()
    # ## try:
    # print(int("123")+55)
    # exam_cur.execute('UPDATE Students SET Stu_Finish = Stu_Finish + %s WHERE No = %s',
    #                (str("123"), str("wl15174217")))
    # exam_con.commit()
    # #except:
    # print("Error!")
    # exam_con.close()
    # exam_cur.close()
    # print(123)