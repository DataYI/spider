from requests_html import HTMLSession
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os 

session = HTMLSession()
url_root = 'http://www.chinamoney.com.cn'
url = url_root + '/fe/jsp/CN/chinamoney/market/searchBondDetailInfo.jsp?bondDefinedCode=3405698857'
#path = r'E:\PythonData\spider'
path = os.getcwd()


def get_iframe(url):
    """
    获取iframe标签的链接，并通过PhantomJS请求动态加载后的数据，最后返回iframe中的html代码
    """
    r = session.get(url)
    iframe = r.html.find('iframe#detailsBond')[0]
    url_src = url_root + iframe.attrs['src']
    browser = webdriver.PhantomJS()
    browser.get(url_src)
    time.sleep(10)
    html = browser.page_source
    return html


def get_urls(html):
    """
    解析html，拿到下载链接
    """
    soup = BeautifulSoup(html, 'lxml')
    a_list = soup.find_all(name='a',attrs={"class":"text-default cell-plus-arrow"}) 
    def fun(tag):
        """
        从a标签中获取文件名的下载链接
        """
        key = tag.attrs['title']
        suffix = tag.attrs['href']
        value = url_root + suffix.replace('mode=open', 'mode=save')
        return key, value
    urls = dict([fun(a) for a in a_list])
    return urls


def download(title, url):
    res = session.get(url, stream=True)
    with open(os.path.join(path, '%s.pdf' % title), 'wb') as f:
        for content in res.iter_content():
            f.write(content)


iframe_html = get_iframe(url)
download_urls = get_urls(iframe_html)
for k, v in download_urls.items():
    download(k, v)
    time.sleep(3)
