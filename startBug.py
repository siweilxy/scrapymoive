import time
import os
import logging
i=0

def initLog():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filemode='w')
    #logging.basicConfig(level=logging.INFO, format='%(levelno)s-%(levelname)s-%(filename)s-%\
    #(funcName)s-%(lineno)d-%(asctime)s-%(thread)d-%(threadName)s-%(process)d-%(message)s')

while(1):
    #initLog()
    logging.critical("*********************************************************")
    os.system("scrapy crawl haotor")
    #os.system("scrapy crawlall")
    logging.critical("*********************************************************")
    time.sleep(1)
    i=i+1
    print "i is "+str(i)
