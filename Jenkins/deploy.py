#!/usr/bin/env python

import time
import os
import sys
import commands


Project_Home = os.getcwd()

Deploy_time = time.strftime('%Y_%m_%d_%H_%M')

artifact = sys.argv[1] + Deploy_time

def Update_package():
    """

    :return:
    """
    if os.path.isfile('build/release64/bin/feed_fisher') == True:
        retcode = commands.getstatusoutput('curl --upload-file build/release64/bin/feed_fisher -u admin:weiboinf'
                                           ' -v http://nexus.biz.weibo.com/repository/files/deploy/%s')%(artifact)
        if retcode[0] == 0:
            print "上传成功！！！"
    else:
        print "Error：编译未生成软件包"
12

def deploy_online():
    pass


