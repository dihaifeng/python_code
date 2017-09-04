#!/usr/bin/env python
# -*-coding:utf-8-*-
import urllib
import urllib2
import json
import sys
import platform
import time
  
  
def auth(uid, username, password, api_url):
    """
    zabbix认证
    :param uid:
    :param username:
    :param password:
    :return:
    """
    dict_data = {}
    dict_data['method'] = 'user.login'  # 方法
    dict_data['id'] = uid  # 用户id
    dict_data['jsonrpc'] = "2.0"  # api版本
    dict_data['params'] = {"user": username, "password": password}  # 用户账号密码
    jdata = json.dumps(dict_data)  # 格式化json数据
    content = post_data(jdata, api_url)  # post json到接口
    return content  # 返回信息
  
  
def post_data(jdata, url):
    """
    POST方法
    :param jdata:
    :param url:
    :return:
    """
    req = urllib2.Request(url, jdata, {'Content-Type': 'application/json'})
    response = urllib2.urlopen(req)
    # content = response.read()
    content = json.load(response)
    return content
  
  
def create_maintenance(name, groupid, active_since, active_till, period, auth_code, api_url):
    """
    create maintenance
    :return:
    """
    dict_data = {}
    dict_data['method'] = 'maintenance.create'  # 方法
    dict_data['id'] = uid  # 用户id
    dict_data['jsonrpc'] = "2.0"  # api版本
    dict_data['auth'] = auth_code  # api版本
    dict_data['description'] = "UPDATE" + groupid  # api版本
    # group
    groupids = [groupid]
    # timeperiods
    timeperiods = [{"timeperiod_type": 0, "start_time": 64800, "period": period}]
    dict_data['params'] = {"name": name, "active_since": active_since, "timeperiods": timeperiods,
                           "active_till": active_till, "groupids": groupids}  # 用户账号密码
    jdata = json.dumps(dict_data)  # 格式化json数据
    content = post_data(jdata, api_url)  # post json到接口
    print content
    return content  # 返回信息
  
  
def get_groupid(groupname, auth_code, uid, api_url):
    """
    use groupname get groupid
    :param groupname:
    :param auth:
    :param uid:
    :return:
    """
    dict_data = {}
    dict_data['method'] = 'hostgroup.get'  # 方法
    dict_data['id'] = uid  # 用户id
    dict_data['jsonrpc'] = "2.0"  # api版本
    name = {"name": groupname}
    dict_data['params'] = {"filter":name }  # 主机名
    dict_data['auth'] = auth_code  # auth串
    jdata = json.dumps(dict_data)  # 格式化json数据
    print jdata
    content = post_data(jdata, api_url)  # post json到接口
    return content  # 返回信息
  
  
def logout(uid, auth_code, api_url):
    """
    退出
    :param uid:
    :param auth_code:
    :return:
    """
    dict_data = {}
    dict_data['method'] = 'user.logout'  # 方法
    dict_data['id'] = uid  # 用户id
    dict_data['jsonrpc'] = "2.0"  # api版本
    dict_data['params'] = []
    dict_data['auth'] = auth_code  # auth串
    jdata = json.dumps(dict_data)  # 格式化json数据
    content = post_data(jdata, api_url)  # post json到接口
    return content  # 返回信息
  
  
if __name__ == '__main__':
    # user info
    uid = 29# 用户ID
    username = 'haifeng18'
    password = '123456'
    api_url = "http://10.73.29.79/zabbix/api_jsonrpc.php"
    res = auth(29, username, password, api_url)  # 认证
    if res['result']:
        auth_code = res['result']  # 认证串
        #groupname = platform.node()  # 主机名
        groupname = sys.argv[1]  # 主机名
        res = get_groupid(groupname, auth_code, uid, api_url)
        if res['result']:
            period = 600  # 维护时长
            active_since = int(time.time())  # 开始时间
            active_till = int(time.time()) + period  # 结束时间
            groupid = res['result'][0]['groupid']  # 主机
            #groupid = str(52)  # 主机
            res = create_maintenance('AutoMaintenance_' + groupname + '_' + str(active_since), groupid, active_since, active_till, period,auth_code, api_url)  # 创建维护
            logout(uid, auth_code, api_url)  # 退出登录
            print res
    else:
        pass
