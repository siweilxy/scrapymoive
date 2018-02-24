import redis
import logging
class redisoperator():
    def __init__(self):
        self.r = redis.Redis(host='192.168.1.16', port=6379, db=0)
        logging.critical("!!!!!!!!!!!!!!!redis connected!!!!!!!!!!!!!!!!!!!!!")

    def set(self,url):
        try:
            logging.critical("set 1%s"%url)
            self.r.set(url,1)
            logging.critical("set 2")
        except Exception,e:
            logging.critical(e)
            logging.critical("set failed")


    def get(self,url):
        try:
            logging.critical("get 1")
            i = self.r.get(url)
            logging.critical("get 2")
            return 0
        except Exception,e:
            logging.critical(e)