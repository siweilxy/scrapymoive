# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import re
import urllib2
import MySQLdb
import platform


class GetmoviesPipeline(object):

    def insertIndb(self,seed, title):
        logging.critical("************************************insert start************************************")

        cursor = self.db.cursor()
        sql = "INSERT INTO movie(url,title) VALUES ('%s','%s')" % (seed, title)
        logging.critical(sql)
        try:
            cursor.execute(sql)
            self.db.commit()
        except Exception, ex:
            logging.critical(ex, exc_info=1)
            self.db.rollback()

            logging.critical(
                "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!db connected!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            self.db = MySQLdb.connect(host="192.168.1.16", port=3306, user="root", passwd="root",
                                      db="movies", charset="utf8")

        logging.critical("************************************insert end************************************")

    def processHaotorItem(self,item):
        if 'title' in item and 'seed' in item:
            title = item['title'][0]
            seed = item['seed'][0]
            if re.search(".torrent", title):
                logging.critical("************************************")
                logging.critical(title)
                logging.critical(seed)
                f = urllib2.urlopen(seed)
                ts = "/home/siwei/torrent/"
                if platform.system() == "Darwin":
                    ts = "/Users/siwei/torrent/"
                tt = ts + title.strip()
                logging.critical(tt)
                with open(tt, "wb") as code:
                    code.write(f.read())
                self.insertIndb(seed, title)
                logging.critical("************************************")

    def __init__(self):
        logging.critical("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!db connected!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.db = MySQLdb.connect(host="192.168.1.16",port=3306,user="root", passwd="root",
                         db="movies",charset="utf8")

    def process_item(self, item, spider):
        if spider.name == "haotor":
            self.processHaotorItem(item)
        return item

    def close_spider(self):
        logging.critical("close db!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.db.close()
