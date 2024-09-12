# 读取股票的日k线数据
# 计算其60日均线，30日均线，20日均线，7日均线
# 根据均线的关系判断其未来5日的涨跌概率
# 如果未来5日的日均涨幅大于0.05，则买入，并于5日后卖出

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
import datetime

# 读取股票的日k线数据
def get_k_data(code, start, end):
    data = ts.get_k_data(code, start, end)
    data = data.set_index('date')
    return data

# 计算均线
def get_ma(data, days):
    ma = pd.Series(np.nan, index=data.index)
    for i in range(days-1, len(data)):
        ma[i] = data[i-days+1:i+1]['close'].mean()

    return ma

# 计算未来5日的涨跌幅
def get_future(data, days):
    future = pd.Series(np.nan, index=data.index)
    for i in range(len(data)-days):
        future[i] = (data[i+days]['close'] - data[i]['close']) / data[i]['close']

    return future

# 计算未来5日的涨跌概率
def get_prob(data, days):
    future = get_future(data, days)
    prob = pd.Series(np.nan, index=data.index)
    for i in range(len(data)-days):
        prob[i] = future[i] > 0.05

    return prob 

# 买入卖出策略
def trade(data, prob, days):
    buy = pd.Series(np.nan, index=data.index)
    sell = pd.Series(np.nan, index=data.index)
    for i in range(len(data)-days):
        if prob[i]:
            buy[i] = data[i]['close']
            sell[i+days] = data[i+days]['close']

    return buy, sell

# 画图
def plot(data, ma1, ma2, ma3, ma4, buy, sell):
    plt.figure()
    plt.plot(data['close'], label='close')
    plt.plot(ma1, label='ma60')
    plt.plot(ma2, label='ma30')
    plt.plot(ma3, label='ma20')
    plt.plot(ma4, label='ma7')
    plt.scatter(buy.index, buy, color='r', label='buy')
    plt.scatter(sell.index, sell, color='g', label='sell')
    plt.legend()
    plt.show()

# 主函数
def main():
    code = '600519'
    start = '2018-01-01
    end = '2018-12-31'
    data = get_k_data(code, start, end)
    ma60 = get_ma(data, 60)
    ma30 = get_ma(data, 30)

    prob = get_prob(data, 5)
    buy, sell = trade(data, prob, 5)
    plot(data, ma60, ma30, buy, sell)
    