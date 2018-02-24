from getMovies.items import GetmoviesItem
from getMovies.redis import redisoperator
from scrapy.loader import ItemLoader
from scrapy.http import Request
from scrapy.loader.processors import MapCompose,Join
from scrapy.spiders import CrawlSpider,Rule
import re
import urlparse
import sys
import logging
import redis

class HaotorSpider(CrawlSpider):
    name="haotor"
    allowed_domains=["www.haotor.com"]
    start_urls=["http://www.haotor.com"]

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        baseUrl= "http://www.haotor.com"
        r = redis.Redis(host='192.168.1.16', port=6379, db=0)
        next_selector=response.xpath("//a/@href")
        for url in next_selector.extract():
            if r.get(url) is None and url != baseUrl:
                if url == baseUrl:
                    logging.critical("this is baseurl")
                r.set(url,1)
                yield Request(urlparse.urljoin(response.url,url))
        #yield Request(urlparse.urljoin(response.url, "http://www.haotor.com"))
        selector = response.xpath("//a")
        for s in selector:
            yield self.parse_item(s,response)

    def parse_item(self,selector,response):
        l=ItemLoader(item=GetmoviesItem(),selector=selector)
        l.add_xpath('title','./text()')
        l.add_xpath('seed','./@href')
        return l.load_item()