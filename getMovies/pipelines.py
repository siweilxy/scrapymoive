# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import re
import urllib2
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
                with open(title,"wb") as code:
                    logging.critical(f.read())
                    #code.write(f.read())
                logging.critical("************************************")
        return item
