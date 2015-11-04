__author__ = 'tixie'

import re
import logging
from scrapy.selector import Selector
from scrapy.http.response import Response
from panCrawler.config import config

class baiduParser:
    def parseUserIdsFromUrls(self, inputfile, savefile):
        input = open(inputfile,'r')
        output = open(savefile, "wb")
        p = re.compile(r'http://\S+\?\S*uk=(?P<id>\d+)')
        ids = {}
        for line in input.readlines():
            m = p.search(line)
            if m != None and not ids.has_key(m.group('id')):
                ids[m.group('id')] = ''
                output.write(m.group('id') + '\n')
        output.close()

    def isHomeUrl(self, url):
        p = re.compile(r'http://pan\.baidu\.com/wap/share/home\?uk=\d+$')
        return p.match(url) != None

    def homeUrl(self, userId):
        return "http://pan.baidu.com/wap/share/home?uk={0}".format(userId)

    def followersUrl(self, userId, pageIndex = 0):
        return "http://pan.baidu.com/wap/share/home/followers?uk={0}&start={1}".format(userId, pageIndex * config.Baidu_PageSize)

    def fansUrl(self, userId, pageIndex = 0):
        return "http://pan.baidu.com/wap/share/home/fans?uk={0}&start={1}".format(userId,pageIndex * config.Baidu_PageSize)

    def parseIdFromUrl(self, url):
        p = re.compile(r'\S+uk=(?P<id>\d+)')
        m = p.search(url)
        if m == None:
            return None
        return int(m.group('id'))

    def parseUserIds(self, response):
        urls = Selector(response = response).xpath('//a[@class="list-item"]/@href').extract()
        p = re.compile(r'\S+uk=(?P<id>\d+)')
        ids =[]
        for url in urls:
            m = p.search(url)
            if m == None:
                continue
            userId = int(m.group('id'))
            ids.append(userId)
        return ids

    def parseCounts(self, response):
        counts = Selector(response = response).xpath('//div[@class="sharebox-nums"]/a/em/text()').extract()
        if len(counts) != 3:
            return {'shares': 0, 'follows':0, 'fans':0}
        return {'shares': int(counts[0]), 'follows': int(counts[1]), 'fans': int(counts[2]) }

#
#
# import uuid
# import sys
# import os
#
# if __name__ == "__main__":
#     parser = baiduParser()
#     #lib_path = os.path.abspath(os.path.join('..','..\\panCrawler'))
#     #sys.path.append(lib_path)
#     #import panCrawler.settings
#     #dataDir = panCrawler.settings.DATA_DIR
#
#     #parser.parseUserIdsFromUrls("{0}\\urls.txt".format(dataDir),"{0}\\ids.txt".format(dataDir))
