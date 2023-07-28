# -*- coding: utf-8 -*-
"""
@Author  : 江洁
@time   : 2023/7/27 17:31
"""

import requests
import time
import yaml
def get_timestamp():
    return str(int(time.time() * 1000))
timestamp = get_timestamp()
#定义
class Baselogin:
    def get_token(self,url,data,headers,method='GET'):
        if method.upper()=='GET':
            return requests.get(url,data,headers=headers)
        elif method.upper()=='PUT':
            return requests.put(url,json=data,headers=headers)
        else:
            print("请求方式错误")
if __name__ == '__main__':
    url = "http://dev-bms.k7.cn/login"
    data = {
        "admin_name": "jiang",
        "password": "c33367701511b4f6020ec61ded352059"
    }
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "x-k7-timestamp": timestamp
    }
    method='PUT'
    res=Baselogin().get_token(url,data,headers,method)
    print(res.json())
    token=res.json()['data']
    data = {"x-k7-token": token}
    if 'data' in res.json():
        token = res.json()['data']
    else:
        # 处理未找到 'data' 键的情况
        # 可以打印错误消息或采取其他操作
        print("未找到 'data' 键")

with open("token.yaml", "w") as f:
    yaml.dump(data, f, default_flow_style=False)
    # 实时刷新
while True:
        # 每隔10分钟更新一次token
    time.sleep(10 * 60)
    new_token = token
    if new_token:
        token = new_token
        data = {"x-k7-token": new_token
                    }
        print("Token已更新:", token)
        with open("token.yaml", "w") as f:
                yaml.dump(data, f, default_flow_style=False)
    else:
        print("token更新失败.")

