from os import mkdir
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os;

FETCH_URL = "https://www.quanben-xiaoshuo.com/n/hongloumeng/xiaoshuo.html"
NOVEL_DIR = "红楼梦"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def work():
    root_url = FETCH_URL
    print(f"开始抓取网页: {root_url}")
    resp = requests.get(root_url , headers={
        'User-Agent': UA
    })
    if resp.status_code != 200:
        print(f"catch error {resp.status_code}")
        return
    soup = BeautifulSoup(resp.text , "html.parser")
    chapters = soup.find_all("a",attrs={"itemprop":"url"})
    index = 1
    if not os.path.exists(NOVEL_DIR):
        mkdir(NOVEL_DIR)
    already_have_list = os.listdir(NOVEL_DIR)
    for ch in chapters :
        print(ch.text)
        href = urljoin(root_url, ch['href'])
        # print(href)
        if not (ch.text+".txt" in already_have_list):
            fetch_content(href , ch.text , str(index) + "/" + str(len(chapters)))
            already_have_list.extend(ch.text+".txt")
        index += 1

def fetch_content(url , title , progess ):
    print(f"抓取 {title} : ({progess})")
    resp = requests.get(url , headers={
        'User-Agent': UA
    })
    if resp.status_code != 200:
        print(f"catch error {url}")
        return

    soup = BeautifulSoup(resp.text , "html.parser")

    body = soup.find(id="articlebody")
    chs = body.find_all("p")
    content = ""
    for ch in chs :
        content += ("    "+ch.text+"\n")
    # print(content)
    f = open(f"{NOVEL_DIR}/{title}.txt" ,"w" ,encoding='utf-8')
    f.write(content)
    f.close()
    print(f"获取成功 写入文件 {f.name}")

work()

if __name__ == "main":
    work()

