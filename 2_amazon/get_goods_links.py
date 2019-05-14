# -*- coding: utf-8 -*-
"""
Created on Mon May 13 14:47:49 2019

@author: DataAnt
"""

from requests_html import HTMLSession, HTML
from urllib.parse import unquote
from selenium import webdriver
import time
import re
import pickle

session = HTMLSession()


def get_category_links() -> list:
    '''
    获取所有的商品分类链接
    '''
    url = 'https://www.amazon.de/Schn%C3%A4ppchen/bbp/bb/ref=bbp_bb_a77114_tr_w_9ea285'
    res = session.get(url)
    goods_category = res.html.find('a.bb-s-cat-link')
    root = 'https://www.amazon.de'
    # 所有商品分类的链接
    category_links = [unquote(root + e.attrs['href']) for e in goods_category]
    return category_links


def get_goods_links(category_link: str) -> list:
    '''
    根据商品分类链接进入对应网页，从网页中获取所有商品的链接，返回包含所有链接的列表
    :category_link: 商品分类链接的地址
    :return: 分类链接地址对应页面中的商品链接地址组成的list
    '''
    goods_links = []
    driver = webdriver.Chrome(r'D:\Tools\chromedriver.exe')
    driver.set_page_load_timeout(30)
    driver.get(category_link)
    js="var q=document.documentElement.scrollTop=%s0000"
    # 通过js实现页面滚动，每次滚动后解析页面得到链接地址，添加到列表中
    # 这里假定页面内容的长度滚动不超过20次，以后需要考虑优化代码
    for i in range(1, 21):
        driver.execute_script(js % i)
        time.sleep(1)
        page = driver.page_source
        html = HTML(html=page)
        elements = html.find('a.a-link-normal.bb-s-item-url')
        links = [e.attrs['href'] for e in elements]
        goods_links.extend(links)
    driver.close()
    return goods_links


def get_category_name(category_link: str) -> str:
    '''
    从商品分类的链接中提取商品分类名称
    :category_link: 商品分类链接的地址
    :return: 从链接地址中提取的分类名称
    '''
    pattern = r'(?<=\=\/)\S*$'
    name = re.findall(pattern, category_link)[0]
    if not name:
        return 'all'
    return name


if __name__ == '__main__':
    # 获取所有商品类别的链接
    category_links = get_category_links()
    # 将每个商品类别下所有商品的链接存入字典
    goods_dict = {}
    for link in category_links:
        name: str = get_category_name(link)
        goods_links: list = get_goods_links(link)
        goods_dict[name] = goods_links    
    # 字典持久化
    with open('goods_dict', 'wb') as f:
        pickle.dump(goods_dict, f, 0)



        
