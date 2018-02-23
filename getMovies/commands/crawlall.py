from scrapy.commands import ScrapyCommand
import logging


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        spider_list = self.crawler_process.spider_loader.list()
        logging.critical(spider_list)
        for name in spider_list:
            self.crawler_process.crawl(name,**opts.__dict__)
        self.crawler_process.start()

    #def __init__(self):
     #   configure_logging(install_root_handler=False)
      #  logging.basicConfig(
       #     format='%(filename)s[line:%(lineno)d]',
        #)
        #logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
         #                   datefmt='%a, %d %b %Y %H:%M:%S',
          #                  filemode='w')
        #logging.critical("set logging config")