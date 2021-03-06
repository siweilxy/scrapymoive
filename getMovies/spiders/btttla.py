from getMovies.items import GetmoviesItem
from scrapy.loader import ItemLoader
from scrapy.http import Request
from scrapy.loader.processors import MapCompose,Join
from scrapy.spiders import CrawlSpider,Rule
import re
import urlparse
import sys


class HaotorSpider(CrawlSpider):
    name="btttla"
    allowed_domains=["www.bttt.la"]
    start_urls=["https://www.bttt.la/"]

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        next_selector=response.xpath("//a/@href")
        for url in next_selector.extract():
            yield Request(urlparse.urljoin(response.url,url))
        selector=response.xpath("//a")
        for s in selector:
            yield self.parse_item(s,response)

    def parse_item(self,selector,response):
        l=ItemLoader(item=GetmoviesItem(),selector=selector)
        l.add_xpath('title','./text()')
        l.add_xpath('seed','./@href')

        return l.load_item()