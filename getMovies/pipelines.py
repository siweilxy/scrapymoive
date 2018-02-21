# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import re
import urllib2
import MySQLdb
import chardet
import sys
class GetmoviesPipeline(object):
    def process_item(self, item, spider):
        #logging.critical(item)
        if 'title' in item and 'seed' in item:
            title=item['title'][0]
            seed=item['seed'][0]
            if re.search(".torrent",title):
                logging.critical("************************************")
                logging.critical(title)
                logging.critical(seed)
                f=urllib2.urlopen(seed)
                ts="/Users/siwei/torrent/"
                tt=ts+title.strip()
                logging.critical(tt)
                with open(tt,"wb") as code:
                    code.write(f.read())
                    db=MySQLdb.connect("192.168.1.16","root","root","movies")
                    cursor=db.cursor()
                    sql="INSERT INTO movie(url,title) VALUES ('%s','%s')" % (seed,title)
                    logging.critical(sql)
                    try:
                        cursor.execute(sql)
                        db.commit()
                    except Exception,ex:
                        logging.critical(ex,exc_info=1)
                        db.rollback()
                logging.critical("************************************")
                db.close()
        return item

