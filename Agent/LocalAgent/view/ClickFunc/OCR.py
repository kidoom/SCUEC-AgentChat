# encoding:utf-8
from Agent.config.AgentConfig import Config,load_config,load_article_config
import requests
import base64
load_article_config()
token = Config.access_token

'''
通用文字识别（高精度含位置版）
'''

request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate"
# 二进制方式打开图片文件
f = open('D:\SCUEC-AgentChat\good.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image":img}
access_token = "24.d631505ce7c5dd47c18b16c75ec71a95.2592000.1723043155.282335-90270783"
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())