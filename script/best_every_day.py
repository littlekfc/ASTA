#!/usr/bin/python                                                               
# -*- coding: utf-8 -*-

import requests
import json
import logging

class BestEveryDay(object):

    STOCK_PRICE_URL = "http://ifzq.gtimg.cn/appstock/app/fqkline/get?p=1&param=sz%s,day,,,320,qfq"
    BOLL_TECH_ANAL = "http://ifzq.gtimg.cn/appstock/indicators/BOLL/D1?market=SZ&code=%s&args=20&start=&end=&limit=320&fq=qfq"
    #http://baike.baidu.com/view/965844.htm
    SZ_A = "000%03d"


    def __init__(self):
        logging.basicConfig(filename='best.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        logging.getLogger('requests').setLevel(logging.ERROR)

    def start(self):
        for i in xrange(1, 1000):
            stock_num = self.SZ_A % i
            stock_price_url = self.STOCK_PRICE_URL % stock_num
            boll_url = self.BOLL_TECH_ANAL % stock_num
            try:
                stock_info = requests.get(stock_price_url).json()
                boll_info = requests.get(boll_url).json()
                last_day_boll = boll_info['data'][-2]
                last_day_price = stock_info['data']['sz%s' % stock_num]['qfqday'][-2]
                name = stock_info['data']['sz%s' % stock_num]['qt']['sz%s' % stock_num][1]
                logging.info('start -- %s' % name)
                if (last_day_price[2] - last_day_boll['LB']) / last_day_price[2] <= 0.05:
                    logging.info('get -- (%s, %s)' % (name, stock_num))
            except Exception as e:
                pass


if __name__ == "__main__":
    best_every_day = BestEveryDay()
    best_every_day.start()



