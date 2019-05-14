# -*- coding: utf-8 -*-
"""
Created on Tue May 14 16:31:31 2019

@author: DataAnt
"""
from requests_html import HTMLSession
import pickle
import re

session = HTMLSession()


def get_seller_link(goods_link: str) -> str:
    '''
    从商品信息页面获取商家信息页面的链接
    :goods_link: 商品页面的链接地址
    :return: 商家信息页面的链接地址
    '''
    res = session.get(goods_link)
    res.html.render(wait=5)
    element = res.html.find('div.a-section.a-spacing-mini > a#sellerProfileTriggerId')[0]
    link = 'https://www.amazon.de' + element.attrs['href']
    return link


def get_seller_link_re(goods_link: str) -> str:
    '''
    分析seller_link的拼写规律，通过goods_link直接生成seller_link，
    理论上与get_seller_link函数返回的结果一致
    :goods_link: 商品页面的链接地址
    :return: 商家信息页面的链接地址
    '''
    seller_id = re.findall(r'(?<=smid\=)\S*$', goods_link)[0]
    seller_link = 'https://www.amazon.de/gp/help/seller/at-a-glance.html/ref=dp_merchant_link?ie=UTF8&seller=%s'
    return seller_link % seller_id


def get_infos(seller_link: str) -> list:
    '''
    从商家信息页面获取需要的信息
    :seller_link: 商家信息页面的链接地址
    :return: 3条商家信息组成的list
    '''
    res = session.get(seller_link)
    elements = res.html.find('ul.a-unordered-list.a-nostyle.a-vertical > li > span.a-list-item > span.a-text-bold')
    infos = [elements[i].text for i in (0, 2, 3)]
    return infos


def get_sellers_dict(goods_dict: str) -> dict:
    '''
    :goods_dict: goods_dict的pickel文件路径
    :return: 包含商家信息页面地址的字典，key为商品分类，value为元素是str的list
    '''
    with open(goods_dict, 'rb') as f:
        goods_dict = pickle.load(f)
    # 根据每个商品的链接进入页面，获取对应的商家信息页面链接
    sellers_dict = {}
    for name, links in goods_dict.items():
        temp = []
        for link in links:
            seller_link = get_seller_link_re(link)
            temp.append(seller_link)
        sellers_dict[name] = temp
    return sellers_dict
    

if __name__ == '__main__':
    sellers_dict = get_sellers_dict('goods_dict')
    # 根据商家信息页面链接获取需要的信息
    print(get_infos(sellers_dict['mens'][9]))
    print(get_infos(sellers_dict['jewelry'][13]))
