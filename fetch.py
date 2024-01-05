import json
from turtle import title
import requests
from bs4 import BeautifulSoup
import os

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


class ChildPage:
    def __init__(self, url, title, thumb):
        self.url = url
        self.title = title
        self.thumb = thumb
        self.tags: list[str] = []
        self.images: list[str] = []
        self.DIR_NAME = None
    def fetch(self):
        print(f"fetch {self.url}")
        resp = requests.get(self.url, headers={
            'User-Agent': UA
        })
        if resp.status_code != 200:
            print(f"catch error {self.url}")
            return

        self.DIR_NAME = self.url.split("/")[-2]
        print(f"DIR_NAME: {self.DIR_NAME}")

        soup = BeautifulSoup(resp.text, "html.parser")
        self.parse_page(soup)

    def parse_page(self, soup):
        content = soup.find(id="content")
        first_img = content.find("img")
        print(first_img)

        all_scripts = soup.find_all("script")
        pd = []

        for sc in all_scripts:
            script_content = sc.text
            if "_pd =" in script_content:
                # print(script_content)
                left = script_content.find("[") + 1
                right = script_content.find("]")
                page_info = script_content[left:right]
                # print(page_info)
                for info in page_info.split(","):
                    pd.append(info.strip(" \""))
                print(pd)

        fileurl = 'https://i.tuiimg.net/' + pd[1];

        total_image_count = int(pd[3])
        print(f"total image count : {total_image_count}")

        for index in range(total_image_count):
            img_url = fileurl + str(index + 1) + ".jpg"
            self.images.append(img_url)
            print(img_url + " progress(%d/%d)" % (index, total_image_count))
            self.download_pic(img_url, "img_" + str(index + 1) + ".jpg")

        #find tags
        tag_info = soup.find("div", attrs={"class": "info"})
        tags = tag_info.find_all("a")
        for a_tag in tags:
            self.tags.append(a_tag.text)

        print(self)
    
    def __str__(self):
        return str(self.toMap())

    def toMap(self):
        jsonObjMap = {}
        jsonObjMap['title'] = self.title
        jsonObjMap['url'] = self.url
        jsonObjMap['images'] = self.images
        jsonObjMap['thumb'] = self.thumb
        jsonObjMap['tags'] = self.tags
        return jsonObjMap

    def download_pic(self, resUrl, filename):
        print(f"download {resUrl}")
        if not os.path.exists(self.DIR_NAME):
            os.makedirs(self.DIR_NAME)
        r = requests.get(resUrl, stream=True)
        if r.status_code == 200:
            with open(f"{self.DIR_NAME}/{filename}", "wb") as f:
                f.write(r.content)
            print("download " + resUrl + " success! to " + f.name)
        else:
            print("download " + resUrl + " failed!")


class Spider:
    def __init__(self, url):
        self.URL = url
        self.page_list = []
        self.info_list = []

    def fetch(self):
        self.page_list = self.fetch_root_page()
        print(f"this have {len(self.page_list)} pages")
        for page in self.page_list:
            page.fetch()
            self.info_list.append(page.toMap())

    def fetch_root_page(self):
        child_page_list = []
        print(f"fetch {self.URL}")
        resp = requests.get(self.URL, headers={
            'User-Agent': UA
        })

        if resp.status_code != 200:
            print(f"catch error {self.URL}")
            return child_page_list

        soup = BeautifulSoup(resp.text, "html.parser")
        self.parse_root_page(soup, child_page_list)
        return child_page_list

    def parse_root_page(self, soup, child_page_list):
        div = soup.find("div", attrs={"class": "beauty"})
        li_list = div.find_all("li")
        for el_li in li_list:
            # item = PageItem(el_li.text)
            a_tag = el_li.find("a")
            title = el_li.text
            url = a_tag['href']
            img_tag = a_tag.find("img")
            print(url + " " + title + " " + img_tag['src'])
            child_page = ChildPage(url, title, img_tag['src'])
            child_page_list.append(child_page)

# def fetch():
#     spider = Spider("https://www.tuiimg.com/meinv/list_155.html")
#     spider.fetch()

def find_page_count():
    url = "https://www.tuiimg.com/meinv/"
    resp = requests.get(url, headers={
        'User-Agent': UA
    })

    if resp.status_code != 200:
        print(f"catch error {url}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    page_info = soup.find("div" , attrs={"class": "page"})
    a_tags = page_info.find_all("a")
    print(a_tags[-1].text)

    return int(a_tags[-1].text)

def catch_all():
    pages = []

    total_page = find_page_count()
    print("total_page = " + str(total_page))
    
    # total_page = 10
    for index in range(1 , total_page + 1):
        pages.append(f"https://www.tuiimg.com/meinv/list_{index}.html")
    
    print(pages)
    
    info_list = []
    for page_url in pages:
        spider = Spider(page_url)
        spider.fetch()
        info_list.extend(spider.info_list)
    
    #print(info_list)

    with open("json.txt" , "w" , encoding="utf-8") as f:
        f.write(str(info_list))
    
    print("写入完成")

if __name__ == "__main__":
    page_url = "https://www.tuiimg.com/meinv/"
    spider = Spider(page_url)
    spider.fetch()
    
    # spider = Spider("https://www.tuiimg.com/meinv/list_155.html")
    # spider.fetch()
