from os import mkdir
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os;

FETCH_URL = "https://www.tuiimg.com/meinv/3069/"
# DIR = "3057"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

DIR_NAME = FETCH_URL.split("/")[-2]

def fetch_pics(url):
    print(f"抓取 {url}")
    resp = requests.get(url , headers={
        'User-Agent': UA
    })
    if resp.status_code != 200:
        print(f"catch error {url}")
        return
    
    # DIR_NAME = url.split("/")[-2]
    print(f"DIR_NAME: {DIR_NAME}")

    soup = BeautifulSoup(resp.text , "html.parser")

    content = soup.find(id="content")
    first_img = content.find("img")
    print(first_img)

    all_scripts = soup.find_all("script")
    pd = []

    for sc in all_scripts:
        script_content = sc.text
        if "_pd =" in  script_content:
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

    for index in range(total_image_count) :
        img_url = fileurl + str(index + 1) + ".jpg" 
        print(img_url + " progress(%d/%d)"%(index,total_image_count))
        download_pic(img_url , "img_" + str(index + 1) + ".jpg" )

    
def download_pic(resUrl , filename):
    print(f"download {resUrl}")
    if not os.path.exists(DIR_NAME):
        os.makedirs(DIR_NAME)
    r = requests.get(resUrl, stream=True)
    if r.status_code == 200:
        with open(f"{DIR_NAME}/{filename}" , "wb") as f:
           f.write(r.content)
        print("dowload " + resUrl +" success! to " + f.name) 
    else:
        print("dowload " + resUrl +" failed!") 
    


if __name__ == "__main__":
    fetch_pics(FETCH_URL)
