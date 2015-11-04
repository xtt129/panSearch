__author__ = 'tixie'

import redis
from panCrawler.util import rBloomFilter
from panCrawler.parser.baiduParser import baiduParser
from scrapy.http import Response

#region bloomFilter
    # filter = rBloomFilter(10000, 0.1, 'test')
    # filter.setBloomFilterBits('aaaa', 1)
    # print(filter.checkBloomFilterBits('aaa'))
    # print(filter.checkBloomFilterBits('aaaa'))
    # r= redis.StrictRedis(host='localhost', port= 6379, db =0)
    # r.set('foo','hello')
    # print(r.get('foo'))
    # r.setbit('testbits',0x1, 1)
    # print(r.getbit('testbits', 0x1))
    # print(r.getbit('testbits', 0x2))
#endregion


#region baiduParser
    parser = baiduParser()
    pass
#endregion

