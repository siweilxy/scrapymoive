# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import re
import urllib2
import MySQLdb

def insertIndb(seed,title):
    logging.critical("************************************db start************************************")
    db = MySQLdb.connect(host="192.168.1.16",port=3306,user="root", passwd="root",
                         db="movies",charset="utf8")
    cursor = db.cursor()
    sql = "INSERT INTO movie(url,title) VALUES ('%s','%s')" % (seed, title)
    logging.critical(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception, ex:
        logging.critical(ex, exc_info=1)
        db.rollback()
    db.close()
    logging.critical("************************************db close************************************")

def processHaotorItem(item):
    if 'title' in item and 'seed' in item:
        title = item['title'][0]
        seed = item['seed'][0]
        if re.search(".torrent", title):
            logging.critical("************************************")
            logging.critical(title)
            logging.critical(seed)
            f = urllib2.urlopen(seed)
            ts = "/home/siwei/torrent/"
            tt = ts + title.strip()
            logging.critical(tt)
            with open(tt, "wb") as code:
                code.write(f.read())
            insertIndb(seed, title)
            logging.critical("************************************")

class GetmoviesPipeline(object):
    def process_item(self, item, spider):
        if spider.name == "haotor":
            processHaotorItem(item)
        return item

