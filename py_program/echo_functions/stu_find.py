#!/usr/bin/env  python
#-*- coding: utf-8 -*-
import urllib.request

from bs4 import BeautifulSoup

stu_pre='wl15'
stu_url='http://acm.sdibt.edu.cn/JudgeOnline/ranklist.php?search='
if __name__ == "__main__":
    stu_url += stu_pre
    response = urllib.request.urlopen(stu_url)
    soup = BeautifulSoup(response, "lxml", from_encoding="utf-8")
    print("网页标题:"+soup.title.string)#获取标题
    '''获取各种量'''
    for stu_tem in soup.findAll('tr'):
        if 'evenrow' in str(stu_tem) or 'oddrow' in str(stu_tem):
            print(stu_tem.td.string)#序号
            stu_tem = stu_tem.find_next('a')
            print(stu_tem.string)#学号
            stu_tem = stu_tem.find_next('td')
            print(stu_tem.string)#姓名
            stu_tem = stu_tem.find_next('a')
            print(stu_tem.string)  # AC
            stu_tem = stu_tem.find_next('a')
            print(stu_tem.string)  # Submit
            stu_tem = stu_tem.find_next('td')
            print(stu_tem.string)  # Ratio