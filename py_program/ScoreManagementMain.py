#!/usr/bin/env  python
#-*- coding: utf-8 -*-
import ScoreManagementFuns as funs

if __name__ == '__main__':
    print('system is working!')
    com = input('Input the command')
    while True:
        #time with the fun
        if com == '0':
            #init->admin
            funs.system_init()
            com = '1'
        elif com == '1':
            funs.ExamSearch_config()#find exam
            com = '2'
        elif com == '2':
            funs.Student_config()#find student
            com ='3'
        elif com == '3':
            funs.ExamSelect()#funs.ExamRes_config(1669)
            com = input('Input the command')
        elif com == '4':
            #set->user add system alue
            funs.system_config()
        elif com == '-1':
            exit(0)
        else :
            print('Command is error!')
            funs.demo()
            ##0->1->2->3
            ##SELECT * FROM Students WHERE Stu_Finish != 0 ORDER BY Stu_Finish DESC