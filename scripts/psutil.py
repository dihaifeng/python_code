#!/usr/bin/env python
#-*- coding:utf-8 -*-

import psutil,time

def getProcessInfo(proc):
    cpu=int(proc.cpu_percent(interval=1))    #获取CPU使用率
    rss='%.2f'%proc.memory_percent()         #获取物理内存使用率,单位为GB
    name=proc.name()                         #获取进程名
    pid=proc.pid                             #获取进程PID
    cwd=proc.cwd()                           #获取进程部署路径
    return [pid,name,cpu,rss,cwd]

def getAllProcessInfo():
    instances = []
    all_processes = list(psutil.process_iter())       #获取当前机器全部的进程            
    for proc in all_processes:
        instances.append(getProcessInfo(proc))
    return instances

ret=getAllProcessInfo()
for i in ret:
    if i[4] == '/' or i[1] == 'sudo' or i[1] =='su':      #过滤掉系统进程
        pass
    else:
        print i
