import datetime
import json
import random
import re
import requests
import sys
if "/home/fred/dev/Quantum/" not in sys.path:
    sys.path.append("/home/fred/dev/Quantum/")
from data_engine.mysql_util.mysql_api import mysqlEngine
from headers import sse_headers, em_header
from random import randint

def api_get_stock_list_from_sse() -> list[dict]:
    """
    从上交所获取股票列表
    Returns:
    list[dict]: 返回股票列表，每个元素是一个字典，包含股票代码和股票名称
    """
    # 从上交所获取股票列表
    result = requests.get(
        url='http://query.sse.com.cn/commonQuery.do?jsonCallBack=jsonpCallback10000&isPagination=true&sqlId=COMMON_SSE_ZQPZ_GPLB_MCJS_SSAG_L&pageHelp.pageSize=1000&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.endPage=5&_=1592380730000',
        headers=sse_headers
        )
    data = result.text
    pattern = re.compile(r'jsonpCallback\d+\((.*)\)')
    result = pattern.findall(data)
    result = json.loads(result[0])
    stock_list = []
    for item in result['result']:
        stock_list.append({'stock_code': f"SH{item['PRODUCTID']}", 'stock_name': item['PRODUCTNAME']})
    return stock_list

def srv_init_table_stock_list_to_mysql(stock_list: list[dict]):
    """
    将股票列表写入到数据库中
    Args:
    stock_list (list[dict]): 股票列表，每个元素是一个字典，包含股票代码和股票名称
    """   
    engine = mysqlEngine('localhost','stock', 'Stock@2024', 'stock')
    # 使用insert方法将数据写入到stock_list表中
    # insert方法的参数为表名和数据列表
    engine.dict_insert('stock_list', ['stock_code', 'stock_name'], stock_list)
    engine.close()

def srv_load_stock_data_from_em():
    stock_list = api_get_stock_list_from_database()
    for stock_code, stock_name in stock_list:
        get_daily_data_from_eastmoney(stock_code, stock_name)

def api_get_stock_list_from_database():
    engine = mysqlEngine('localhost','stock', 'Stock@2024', 'stock')
    stock_list = engine.select(['stock_code', 'stock_name'], 'stock_list', "1")
    engine.close()
    return stock_list

def srv_create_stock_table_from_list():    
    engine = mysqlEngine('localhost','stock', 'Stock@2024', 'stock')
    stock_list = engine.select(['stock_code', 'stock_name'], 'stock_list', "1")
    for item in stock_list:
        engine.duplicate_table(f"{item[0]}", 'template_stock')
    engine.close()

def get_daily_data_from_eastmoney(stock_code: str, stock_name: str):  
    em_url = f"http://push2his.eastmoney.com/api/qt/stock/kline/get"
    ts = int(datetime.datetime.now().timestamp() * 1000)
    secid = stock_code.replace('SH', '1.').replace('SZ', '0.')
    rt = randint(100, 150)
    # the details for cb parameters is according to the code of jQuery 3.5.1
    payload = {
        "cb": f"jQuery351{str(random.random()).replace('.','')}_{ts}",
        "secid" : secid,
        "ut" : "fa5fd1943c7b386f172d6893dbfba10b",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt": 101,
        "fqt": 0,
        #"beg": "19900101",
        "end": "20500101",
        "lmt": "100000",
        "_": f"{ts + rt}"
    }
    result = requests.Session().get(
        url=em_url,
        params=payload,
        headers=em_header,
        verify=False
        )
    # 对返回的数据进行处理jQuery351021807036169344496_1726060643460({dict}）
    pattern = re.compile(r'jQuery\d+_\d+\((.*)\)')
    result = pattern.findall(result.text)
    jdata = json.loads(result[0])
    daily_data = []
    for item in jdata['data']['klines']:
        data_series = item.split(',')
        daily_data.append({
            'trade_date': data_series[0],
            'stock_code': stock_code,
            'stock_name': stock_name,
            'open_price': data_series[1],
            'close_price': data_series[2],
            'high_price': data_series[3],
            'low_price': data_series[4],
            'volume': data_series[5],
            'turnover': data_series[6],
            'amplitude': data_series[8],
            'change_rate': data_series[10]
        })
    engine = mysqlEngine('localhost','stock', 'Stock@2024', 'stock')
    engine.dict_insert(stock_code,
                       ['trade_date', 'stock_code','stock_name', 'open_price', 'close_price', 'high_price', 'low_price', 'volume', 'turnover', 'amplitude', 'change_rate'],
                       daily_data)
    engine.close()
    return daily_data

if __name__ == '__main__':
    stock_list = api_get_stock_list_from_database()
    for stock_code, stock_name in stock_list:
        get_daily_data_from_eastmoney(stock_code, stock_name)
    # get_daily_data_from_eastmoney('SZ002224')
    # create_stock_table_from_list()