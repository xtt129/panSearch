# -*- coding: utf-8 -*-
import logging
from scrapy.spiders import Spider
from scrapy.http.request import  Request
from panCrawler.items import *
from panCrawler.util.dataAccess import  *
from panCrawler.config import config
from panCrawler.parser.baiduParser import baiduParser


class BaiduSpider(Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = []
    parser = baiduParser()
    userIdKey = 'bids'
    meta = {
              'dont_redirect': True,
              'handle_httpstatus_list': [301,302]
            }

    def __init__(self, *args, **kwargs):
        super(BaiduSpider, self).__init__(*args, **kwargs)
        input = open("{0}\\ids.txt".format(config.DATA_DIR))
        for uId in input.readlines():
            if len(uId.strip()) >0:
                #self.start_urls.append(self.parser.fansUrl(id.strip()))
                #self.start_urls.append(self.parser.followersUrl(id.strip()))
                userId = int(uId)
                if not dbAccessor.exists(self.userIdKey, userId):
                    dbAccessor.setbit(self.userIdKey, userId)
                    self.start_urls.append(self.parser.homeUrl(uId))

    def make_requests_from_url(self, url):
        return Request(url, dont_filter=True, meta = self.meta)


    def parse_users(self, response):
        logging.warning('response url:'+response.url)
        userId = self.parser.parseIdFromUrl(response.url)
        ids = self.parser.parseUserIds(response)
        logging.warn(ids)
        for userId in ids:
            if not dbAccessor.exists(self.userIdKey, userId):
             dbAccessor.setbit(self.userIdKey, userId)
             yield Request(self.parser.homeUrl(userId), meta= self.meta, callback= self.parse)
             item = UserIdResult()
             item['userId'] = userId
             yield  item

    def parse(self, response):
        logging.warning('response url:'+response.url)
        userId = self.parser.parseIdFromUrl(response.url)
        if userId == None:
            return

        if self.parser.isHomeUrl(response.url):
            counts = self.parser.parseCounts(response)
            logging.warn("{0}  stat: {1}, {2}, {3}".format(response.url, counts['shares'], counts['follows'], counts['fans']))
            #if not dbAccessor.exists(self.userIdKey, userId) or self.start_urls.count(response.url) >0:
            item = BaiduUserStat(counts)
            item['userId'] = userId
            yield  item
            ##generate other page links
            followsPages = (item['follows'] -1) / config.Baidu_PageSize +1
            fansPages = (item['fans'] -1) / config.Baidu_PageSize +1
            if item['follows'] >0:
                for page in range(0, followsPages+1):
                    yield Request(self.parser.followersUrl(userId, page), meta=self.meta, callback= self.parse_users)
            if item['fans'] >0:
                for page in range(0, fansPages+1):
                    yield Request(self.parser.fansUrl(userId, page), meta=self.meta, callback=self.parse_users)
            #else:
             #   logging.error("this should not happen")
        #else:
            ##parse userId of this page, then create new request.
            # ids = self.parser.parseUserIds(response)
            # logging.warn(ids)
            # for userId in ids:
            #     if not dbAccessor.exists(self.userIdKey, userId):
            #      dbAccessor.setbit(self.userIdKey, userId)
            #      yield Request(self.parser.homeUrl(userId))
            #      item = UserIdResult()
            #      item['userId'] = userId
            #      yield  item



