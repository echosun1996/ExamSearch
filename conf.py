#!/usr/bin/env python
# -*- coding:utf-8 -*-
import configparser
if __name__=="__main__":
    fun=0
    conf = configparser.ConfigParser()

    #0/不存在 新建用户、分配权限、新建数据库、新建表，完成后登出
    while(conf.read('conf.ini')==[] or conf.sections()==[]):

        fp=open('conf.ini','w')
        conf.add_section('status')
        conf.set('status', 'fun', '0')
        conf.write(fp)
        fp.close()

    fp = open('conf.ini', 'w')
    conf.set('status', 'fun', '0')
    conf.write(fp)

    print(conf.get('status','fun' ))

    for sn in conf.sections():
        print(sn,'-->')
        for attr in conf.options(sn):
            print(attr,'=',conf.get(sn,attr))


    fp.close()