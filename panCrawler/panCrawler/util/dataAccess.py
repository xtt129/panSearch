__author__ = 'tixie'

import  redis
import  logging
from rBloomFilter import rBloomFilter

class dataAccess:
    rClient = redis.StrictRedis(host='localhost', port= 6379, db =0)
    slotSize = 27
    bloomFilter = rBloomFilter(10000000, 0.1, 'baiduId')

    def __key__(self, name, intValue):
        old = intValue
        index = intValue >> self.slotSize
        intValue = intValue & ((1 << (self.slotSize+1)) -1)
        kv = { 'key': "{0}{1}".format(name, index), 'value': intValue}
        logging.warn(kv)
        logging.warn(old)
        return  kv

    def exists(self, name, intValue):
        return self.bloomFilter.IfKeyVisited(str(intValue))
        #kv = self.__key__(name, intValue)
        #return self.rClient.getbit(kv['key'], kv['value']) == 1

    def setbit(self, name, intValue):
        #kv = self.__key__(name, intValue)
        #self.rClient.setbit( kv['key'], kv['value'], True)
        self.bloomFilter.setBloomFilterBits(str(intValue),1)


dbAccessor = dataAccess()

