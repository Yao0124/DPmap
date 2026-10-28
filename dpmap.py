# Copyright (c) 2026 Yao0124
# SPDX-License-Identifier: MIT
import requests
from fake_useragent import UserAgent
import argparse
import pyfiglet
import concurrent.futures
import os

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'
logo = pyfiglet.figlet_format("DPmap", font="slant")
print(f"{YELLOW}{logo}{RESET}")
print('by Yao0124')

ua = UserAgent()
HEADER = ua.random

parser = argparse.ArgumentParser(
    description='DPmap 目录扫描工具'
)
parser.add_argument('-u','--url',dest='url',help='目标URL')
parser.add_argument('-f','--file',dest='file',help='打开字典文件')
parser.add_argument('-t','--threads',dest='threads',type=int,help='线程数')
parser.add_argument('-g','--get',dest='get',action='store_true',help='get模式')
parser.add_argument('-p','--post',dest='post',action='store_true',help='post模式')
parser.add_argument('-he','--head',dest='head',action='store_true',help='head模式')

def main():
    args = parser.parse_args()
    url = args.url
    fileopen = args.file
    thre = args.threads
    get = args.get
    post = args.post
    head = args.head

    if args.url is None:
        parser.print_help()
        exit(0)

    if url is not  None and not url.startswith("http"):
            url = 'http://' + url
            headers = {'User-Agent': HEADER}

    threadstart(url,headers,fileopen,thre,get,post,head)

def code_print(target_url,code):
     if code == 200:
        print(f"{GREEN}[{code} OK] {target_url}{RESET}")
     elif code in [301, 302]:
        print(f"{YELLOW}[{code} 跳转] {target_url}{RESET}")
     elif code == 403:
        print(f"{RED}[{code} 禁止访问] {target_url}{RESET}")
     elif code == 500:
        print(f"{PURPLE}[{code} 服务器报错] {target_url}{RESET}")
     else:
        pass 
    
def send_request_get(url,headers,path):
    clean_url = url.rstrip('/')
    clean_path = path.lstrip('/')
    target_url = f'{clean_url}/{clean_path}'
    try:
        response = requests.get(target_url,headers=headers,timeout=10,allow_redirects=False)
        code = response.status_code
        code_print(target_url,code)
    except Exception as e:
        pass

def send_request_post(url,headers,path):
    clean_url = url.rstrip('/')
    clean_path = path.lstrip('/')
    target_url = f'{clean_url}/{clean_path}'
    try:
        response = requests.post(target_url,headers=headers,timeout=10,allow_redirects=False)
        code = response.status_code
        code_print(target_url,code)
    except Exception as e:
        pass

def send_request_head(url,headers,path):
    clean_url = url.rstrip('/')
    clean_path = path.lstrip('/')
    target_url = f'{clean_url}/{clean_path}'
    try:
        response = requests.head(target_url,headers=headers,timeout=10,allow_redirects=False)
        code = response.status_code
        code_print(target_url,code)
    except Exception as e:
        pass

def threadstart(url,headers,fileopen,thre,get,post,head):
    with concurrent.futures.ThreadPoolExecutor(max_workers=thre) as executor: 
        try:
            with open(fileopen,'r',encoding='utf-8',errors='ignore') as file:
                for line in file:
                    path = line.strip()
                    if path:
                        if get:
                            executor.submit(send_request_get,url,headers,path)
                        elif post:
                            executor.submit(send_request_post,url,headers,path)
                        elif head:
                            executor.submit(send_request_head,url,headers,path)
        except FileExistsError:
            print(f'字典不存在 检查一下路径吧：{fileopen}')
        except  Exception as e:
            print(f'异常错误：{e}')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('再见')
        os._exit(0)