#!/usr/bin/python                                                               
# -*- coding: utf-8 -*-

import requests
import json
import logging
import datetime
import MySQLdb
import market_config


class GetBollData(object):

    BOLL_TECH_ANAL = "http://ifzq.gtimg.cn/appstock/indicators/BOLL/D1?market=%s&code=%s&args=20&start=&end=&limit=320&fq=qfq"

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
            boll_url = self.BOLL_TECH_ANAL % (market['market'], stock_num)
            try:
                boll_info = requests.get(boll_url, timeout=self.TIMEOUT).json()
                last_day_boll = boll_info['data'][-2]
                logging.info('get -- %s : %s' % (full_code, last_day_boll))
                self.cur.execute(
                    "REPLACE INTO boll (code,up_bound,middle,low_bound,date) VALUES ('%s',%s,%s,%s,'%s')" % (
                    stock_num, last_day_boll['UB'], last_day_boll['BOLL'], last_day_boll['LB'], last_day_boll['DATE']))
                self.conn.commit()

            except Exception as e:
                logging.info("error %s" % e)
                pass

        self.cur.close()
        self.conn.close()

    def start(self):
        self.find_best(market_config.SZ_A)
        self.find_best(market_config.SH_A1)
        self.find_best(market_config.SH_A2)
        self.find_best(market_config.SH_A3)

if __name__ == "__main__":
    get_boll_data = GetBollData()
    get_boll_data.start()



