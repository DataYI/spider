import requests
import time

url = 'http://zjj.sz.gov.cn/bzflh/lhmcAction.do?method=queryYgbLhmcList'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'http://zjj.sz.gov.cn/bzflh//lhmcAction.do?method=queryYgbLhmcInfo&waittype=1',
    'Origin': 'http://zjj.sz.gov.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
}

payload = {
    'pageNumber': 1,
    'pageSize': 100,
    'waittype': 1,
    'num': 0,
    'shoulbahzh': '',
    'xingm': '',
    'idcard': '', 
    'start_paix': '',
    'end_paix': '',
    'undefined': ''
}


def get_json(page):
    '''
    修改POST方法发送的数据中的pageNumber，然后请求数据，返回响应结果中的json数据
    :param page: 要获取数据的页码
    :return: dict
    '''
    payload['pageNumber'] = page
    res = requests.post(url, headers=headers, data=payload)
    return res.json()


def get_values(json, is_key=False):
    '''
    解析从响应结果中得到的json数据，把每一条记录转成文本，最终返回所有记录文本的集合
    :param json: dict
    :param is_key: 值为True时返回的是记录的字段名，反之返回的是所有记录的值集合
    :return: is_key为True时返回str，反之返回list
    '''
    rows = json['rows']

    # 用于解析字典的键或值为文本
    def items_to_str(d):
        try:
            del d['ROWNUM_']
        except KeyError:
            pass
        items = d.values()
        if is_key:
            items = d.keys()
        string = str(tuple(items))
        string = string.replace('None', '').replace("'", '')[1:-1]
        return string + '\n'
    if is_key:
        return items_to_str(rows[0])
    values = [items_to_str(r) for r in rows]
    return values


def download(page_start, page_stop):
    '''
    指定要下载页面的起始页码和结束页码，下载的页面数据会直接写入工作目录下的data.csv文件
    :param page_start: 起始页码
    :param page_stop: 结束页码
    :return: None
    '''
    with open('data.csv', 'a', encoding='utf-8') as f:
        # 如果data.csv内容为空，就先写入字段名
        if f.tell() == 0:
            f.writelines(columns)
        for i in range(page_start, page_stop + 1):
            json = get_json(i)
            values = get_values(json)
            for value in values:
                f.writelines(value)
            print('第%s页数据下载完成...' % i)
            time.sleep(0.1)


if __name__ == '__main__':
    res = requests.post(url, headers=headers, data=payload)
    # 从响应结果中获取记录的总条数
    total = res.json()['total']
    # 每页100条记录，计算出最大页码数
    page_max = (total // 100) + 1
    # 每条记录中所有数据对应的字段名
    columns = get_values(res.json(), is_key=True)
    # -------------------------
    page_start = 1
#    page_stop = 5
    page_stop = page_max
    # -------------------------
    download(page_start, page_stop)
