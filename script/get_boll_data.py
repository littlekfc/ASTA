#!/usr/bin/python                                                               
# -*- coding: utf-8 -*-

import requests
import json
import logging
import datetime
import MySQLdb
import market_config


class GetBollData(object):

    BOLL_TECH_ANAL_DAY = "http://ifzq.gtimg.cn/appstock/indicators/BOLL/D1?market=%s&code=%s&args=20&start=&end=&limit=2&fq=qfq"
    BOLL_TECH_ANAL_WEEK = "http://ifzq.gtimg.cn/appstock/indicators/BOLL/W1?market=%s&code=%s&args=20&start=&end=&limit=2&fq=qfq"
    BOLL_TECH_ANAL_MONTH = "http://ifzq.gtimg.cn/appstock/indicators/BOLL/M1?market=%s&code=%s&args=20&start=&end=&limit=2&fq=qfq"

    TIMEOUT = 10

    def __init__(self):
        date = "%s" % datetime.datetime.today().date()
        logging.basicConfig(filename='../log/%s.log' % date, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        logging.getLogger('requests').setLevel(logging.ERROR)

        try:
            self.conn = MySQLdb.connect(host='localhost', user='root', passwd='root321', db='asta', port=3306)
            self.cur = self.conn.cursor()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def find_best(self, market):
        for i in market["range"]:
            stock_num = market['code'] % i
            full_code = market['full_code'] % i
            boll_url_day = self.BOLL_TECH_ANAL_DAY % (market['market'], stock_num)
            boll_url_week = self.BOLL_TECH_ANAL_WEEK % (market['market'], stock_num)
            boll_url_month = self.BOLL_TECH_ANAL_MONTH % (market['market'], stock_num)
            try:
                boll_info_day = requests.get(boll_url_day, timeout=self.TIMEOUT).json()
                boll_info_week = requests.get(boll_url_week, timeout=self.TIMEOUT).json()
                boll_info_month = requests.get(boll_url_month, timeout=self.TIMEOUT).json()
                boll_data_day = boll_info_day['data'][-2]
                boll_data_week = boll_info_week['data'][-2]
                boll_data_month = boll_info_month['data'][-2]
                logging.info('get -- %s : Day:%s Week:%s Month:%s' % (full_code, boll_data_day,boll_data_week,boll_data_month))
                self.cur.execute(
                    "REPLACE INTO boll (code,day_up_bound,day_middle,day_low_bound,week_up_bound,week_middle,week_low_bound,month_up_bound,month_middle,month_low_bound,date) VALUES ('%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s')" % (
                    stock_num, boll_data_day['UB'], boll_data_day['BOLL'], boll_data_day['LB'],
                    boll_data_week['UB'], boll_data_week['BOLL'], boll_data_week['LB'],
                    boll_data_month['UB'], boll_data_month['BOLL'], boll_data_month['LB'], boll_data_day['DATE']))
                self.conn.commit()

            except Exception as e:
                logging.info("error %s" % e)
                pass

    def start(self):
        self.find_best(market_config.SZ_A)
        self.find_best(market_config.SH_A1)
        self.find_best(market_config.SH_A2)
        self.find_best(market_config.SH_A3)
        self.cur.close()
        self.conn.close()

if __name__ == "__main__":
    get_boll_data = GetBollData()
    get_boll_data.start()



