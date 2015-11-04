# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from items import *
import  logging
from config import *


class BaiduUserStatPipeline(object):
    def __init__(self):
        self.file = open(config.DATA_DIR+ '\\userIds.txt', 'wb')
        self.statfile = open(config.DATA_DIR+'\\stats.txt','wb')
    def process_item(self, item, spider):
        logging.warning('processing item:' +  str(item['userId']))
        if type(item) is BaiduUserStat:
            self.statfile.write("{0},{1},{2},{3}\n".format(item['userId'],item['shares'], item['follows'], item['fans']))
        else:
            self.file.write("{0}\n".format(item['userId']))


