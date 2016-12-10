import requests
from bs4 import BeautifulSoup
import os

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
all_url = 'http://www.mzitu.com/all'
start_html = requests.get(all_url, headers = headers)
# print(start_html.text)
# ##打印出start_html (请注意，concent是二进制的数据，一般用于下载图片、视频、音频、等多媒体内容是才使用concent, 
# ##对于打印网页内容请使用text)


Soup = BeautifulSoup(start_html.text, 'lxml') 
#使用BeautifulSoup来解析我们获取到的网页（‘lxml’是指定的解析器 具体请参考官方文档哦）
#li_list = Soup.find_all('li') ##使用BeautifulSoup解析网页过后就可以用找标签呐！
#（find_all是查找指定网页内的所有标签的意思，find_all返回的是一个列表。）

all_a = Soup.find('div', class_='all').find_all('a')
##意思是先查找 class为 all 的div标签，然后查找所有的<a>标签。
for a in all_a:##a: <a href="###" target="_blank">###</a>
    title = a.get_text()
    path = str(title).strip() ##去掉空格
    os.makedirs(os.path.join("/home/vincent/git/Python/crawler", path)) ##创建一个存放套图的文件夹
    os.chdir("/home/vincent/git/Python/crawler//" + path)
    href = a['href']
    html = requests.get(href, headers = headers)
    html_Soup = BeautifulSoup(html.text, 'lxml')
    max_span = html_Soup.find('div', class_='pagenavi')
    if(max_span):
        span_cnt = max_span.find_all('span')[-2].get_text()
        for page in range(1, int(span_cnt)+1): 
            page_url = href + '/' + str(page)
            img_html = requests.get(page_url, headers=headers)
            img_Soup = BeautifulSoup(img_html.text, 'lxml')
            img_url = img_Soup.find('div', class_='main-image').find('img')['src']
            name = img_url[-9:-4]
            img = requests.get(img_url, headers = headers)
            f = open(name+'.jpg', 'ab')
            f.write(img.content)
            f.close() 
            print(img_url + "was saved")
