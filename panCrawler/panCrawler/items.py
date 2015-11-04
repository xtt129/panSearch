# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BaiduUserStat(Item):
    userId = Field()
    shares = Field()
    follows = Field()
    fans = Field()


class UserIdResult(Item):
    userId = Field()

