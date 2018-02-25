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
from scrapy.http import Request

class GetmoviesPipeline(object):

    def checkIndb(self,title):
        cursor = self.db.cursor()
        sql="select title from movie where title = '%s'" % (title)
        try:
            cursor.execute(sql)
            return type(cursor.fetchall())
        except Exception,ex:
            logging.critical(ex,exc_info=1)
            return 0


    def insertIndb(self,seed, title):
        logging.critical("************************************insert db start************************************")
        cursor = self.db.cursor()
        sql = "INSERT INTO movie(url,title) VALUES ('%s','%s')" % (seed, title)
        #logging.critical(sql)
        try:
            cursor.execute(sql)
            self.db.commit()
        except Exception, ex:
            logging.critical(ex, exc_info=1)
            self.db.rollback()
        logging.critical("************************************insert db end************************************")

    def savetorrent(self,seed,title):
        if re.search(".torrent", title):
            #logging.critical("****************savetorrent start********************")
            logging.critical("title :%s,seed :%s"%(title,seed))
            #logging.critical(seed)
            f = urllib2.urlopen(seed)
            ts = "/home/siwei/torrent/"
            if platform.system() == "Darwin":
                ts = "/Users/siwei/torrent/"
            tt = ts + title.strip()
            #logging.critical(tt)
            logging.critical("*****************write file start*******************")
            with open(tt, "wb") as code:
                code.write(f.read())
            logging.critical("*****************write file end*******************")
            if self.checkIndb(title=title) is 0:
                self.insertIndb(seed, title)
            else:
                logging.critical("this is in DB!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #logging.critical("*****************savetorrent end*******************")


    def processHaotorItem(self,item):
        if 'title' in item and 'seed' in item:
            title = item['title'][0]
            seed = item['seed'][0]
            self.savetorrent(seed,title)
        elif 'seed' in item:
            seed=item['seed'][0]
            title="unknown"
            self.savetorrent(seed,title)
    """
    def processBttlaItem(self,item):
        if 'title' in item and 'seed' in item:
            title = item['title'][0]
            seed = "https://www.bttt.la" + item['seed'][0]
            if re.search(".html", seed):
                logging.critical("******************html start**********************")
                logging.critical("this is html")
                logging.critical(seed)
                logging.critical("******************html end************************")
            logging.critical(title)
            logging.critical(seed)
        elif 'seed' in item:
            title = "unknown"
            seed = "https://www.bttt.la" + item['seed'][0]
            if re.search(".html", seed):
                logging.critical("******************html start no title**********************")
                logging.critical("this is html")
                logging.critical(seed)
                logging.critical("******************html end no title************************")
            logging.critical(title)
            logging.critical(seed)
    """

    def __init__(self):
        logging.critical("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!db connected!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.db = MySQLdb.connect(host="192.168.1.16",port=3306,user="root", passwd="root",
                         db="movies",charset="utf8")

    def process_item(self, item, spider):
        if spider.name == "haotor":
            self.processHaotorItem(item)
        elif spider.name == "btttla":
            self.processBttlaItem(item)
        return item

    def close_spider(self):
        logging.critical("close db!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.db.close()
