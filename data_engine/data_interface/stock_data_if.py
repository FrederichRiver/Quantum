import datetime
import re
from matplotlib import cbook
import requests
import json

sse_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "ba17301551dcbaf9_gdp_session_id=4447eaf6-1df9-4dc5-b979-313afafb4c57; gdp_user_id=gioenc-de4612ad%%2Cadd6%%2C50dg%%2Cc63b%%2C274a6070a55b; ba17301551dcbaf9_gdp_session_id_sent=4447eaf6-1df9-4dc5-b979-313afafb4c57; ba17301551dcbaf9_gdp_sequence_ids={%%22globalKey%%22:5%%2C%%22VISIT%%22:2%%2C%%22PAGE%%22:3%%2C%%22VIEW_CLICK%%22:2}",
    "Host": "query.sse.com.cn",
    "Referer": "https://www.sse.com.cn/",
    "Sec-Fetch-Dest": "script",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

def srv_get_stock_list_from_sse() -> list[dict]:
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

def srv_init_table_stock_list_to_mysql(stock_list):
    import sys
    if "/home/fred/dev/Quantum/" not in sys.path:
        sys.path.append("/home/fred/dev/Quantum/")
    from data_engine.mysql_util.mysql_api import mysqlEngine
    
    engine = mysqlEngine('localhost','stock', 'Stock@2024', 'stock')
    # 使用insert方法将数据写入到stock_list表中
    # insert方法的参数为表名和数据列表
    engine.dict_insert('stock_list', ['stock_code', 'stock_name'], stock_list)
    engine.close()

em_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "push2his.eastmoney.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome//128.0.0.0 Safari/537.36",
    "Cookie": r"qgqp_b_id=ebf3648421340d8173fcf266254de845; st_si=50556165073761; st_asi=delete; HAList=ty-0-002224-%u4E09%20%u529B%20%u58EB%2Cty-0-300059-%u4E1C%u65B9%u8D22%u5BCC; st_pvi=21238051950321; st_sp=2024-09-08%2023%3A38%3A14; st_inirUrl=https%3A%2F%2Fquote.eastmoney.com%2Fsz002224.html; st_sn=229; st_psi=20240910235838780-113200301201-9124668404"
}

em_header2 = {
    "Accept": r"*/*",
    "Accept-Encoding": "gzip",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": r"qgqp_b_id=ebf3648421340d8173fcf266254de845; st_si=50556165073761; st_asi=delete; HAList=ty-0-002224-%u4E09%20%u529B%20%u58EB%2Cty-0-300059-%u4E1C%u65B9%u8D22%u5BCC; st_pvi=21238051950321; st_sp=2024-09-08%2023%3A38%3A14; st_inirUrl=https%3A%2F%2Fquote.eastmoney.com%2Fsz002224.html; st_sn=229; st_psi=20240910235838780-113200301201-9124668404",
    "Host": "push2his.eastmoney.com",
    "Referer": "http://quote.eastmoney.com/sz002224.html",
    "Sec-Fetch-Dest": "script",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "sec-ch-ua": "Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
}

def get_stock_list_from_database():
    import sys
    if "/home/fred/dev/Quantum/" not in sys.path:
        sys.path.append("/home/fred/dev/Quantum/")
    from data_engine.mysql_util.mysql_api import mysqlEngine
    
    engine = mysqlEngine('localhost','stock', 'Stock@2024', 'stock')
    # 使用insert方法将数据写入到stock_list表中
    # insert方法的参数为表名和数据列表
    stock_list = engine.select(['stock_code', 'stock_name'], 'stock_list', "1")
    engine.close()
    return stock_list

def create_stock_table_from_list():
    import sys
    if "/home/fred/dev/Quantum/" not in sys.path:
        sys.path.append("/home/fred/dev/Quantum/")
    from data_engine.mysql_util.mysql_api import mysqlEngine
    
    engine = mysqlEngine('localhost','stock', 'Stock@2024', 'stock')
    # 使用insert方法将数据写入到stock_list表中
    # insert方法的参数为表名和数据列表
    stock_list = engine.select(['stock_code', 'stock_name'], 'stock_list', "1")
    for item in stock_list:
        engine.duplicate_table(f"{item[0]}", 'template_stock')
    engine.close()

def get_daily_data_from_eastmoney(stock_code: str, stock_name: str):  
    import random
    em_url = f"http://push2his.eastmoney.com/api/qt/stock/kline/get"
    ts = int(datetime.datetime.now().timestamp() * 1000)
    secid = stock_code.replace('SH', '1.').replace('SZ', '0.')
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
        "_": f"{ts + 137}"
    }
    result = requests.Session().get(
        url=em_url,
        params=payload,
        headers=em_header2,
        # verify=False
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
    import sys
    if "/home/fred/dev/Quantum/" not in sys.path:
        sys.path.append("/home/fred/dev/Quantum/")
    from data_engine.mysql_util.mysql_api import mysqlEngine
    
    engine = mysqlEngine('localhost','stock', 'Stock@2024', 'stock')
    # 使用insert方法将数据写入到stock_list表中
    # insert方法的参数为表名和数据列表
    engine.dict_insert(stock_code,
                       ['trade_date', 'stock_code','stock_name', 'open_price', 'close_price', 'high_price', 'low_price', 'volume', 'turnover', 'amplitude', 'change_rate'],
                       daily_data)
    engine.close()

    return daily_data

def srv_load_stock_data_from_em():
    stock_list = get_stock_list_from_database()
    for stock_code, stock_name in stock_list:
        get_daily_data_from_eastmoney(stock_code, stock_name)

if __name__ == '__main__':
    stock_list = get_stock_list_from_database()
    for stock_code, stock_name in stock_list:
        get_daily_data_from_eastmoney(stock_code, stock_name)
    # get_daily_data_from_eastmoney('SZ002224')
    # create_stock_table_from_list()