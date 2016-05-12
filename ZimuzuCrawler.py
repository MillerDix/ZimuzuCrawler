# !usr/bin/env python3
# -- coding:utf-8 --

import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import re
import os

# 配置登录页面
login_url = 'http://www.zimuzu.tv/User/Login/ajaxLogin'
# 登录参数
account = input("请输入账户名:\n")
password = input("请输入登录密码:\n")
params = {'account': account, 'password': password, 'remember': '1', 'url_back': 'http://www.zimuzu.tv'}
post_data = urllib.parse.urlencode(params).encode()
# 请求头
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}

# cookie配置
print("配置cookie...\n")
cookie_filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

# 获取cookie
print("尝试登录...\n")
request = urllib.request.Request(login_url, post_data, headers)
try:
    response = opener.open(request)
    page = response.read().decode()
except urllib.error.URLError as error:
    print(error.code, ':', error.reason)

# 打印cookie
print("cookie信息如下:\n")
print(cookie)
for item in cookie:
    print('Name = ' + item.name)
    print('Value = ' + item.value)

# 保存cookie到cookie.txt中
print("存储cookie...\n")
cookie.save(ignore_discard=True, ignore_expires=True)


# 登录后查看页面
# get_url = 'http://www.zimuzu.tv/resource/list/26154'
get_url = input("请输入下载页面地址(http://www.xxx.com/xxx):\n")

print("获取内容中,请稍后...\n")
get_request = urllib.request.Request(get_url, headers=headers)
get_response = opener.open(get_request)

# 结果存储文件
file = open("results.txt", "w")
# 正则提取地址
allfinds = re.findall(r'<li class="clearfix" format="1080P.+?\s+.+?\s+.+?\s+.+?\s+<a href="(.+?)" type="ed2k">电驴</a>', get_response.read().decode())
# 写入文件
print("正在写入文件....\n")
for i in allfinds:
    print(i)
    file.writelines("{}\n".format(i))
file.close()

# 完成提示
print("\n已完成, 文件已保存至{}/results.txt".format(os.getcwd()))

