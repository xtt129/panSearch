__author__ = 'tixie'
import redis
import math

class rBloomFilter:
    rClient = redis.StrictRedis(host='localhost', port= 6379, db =0)
    name = None
    factors = (7, 11, 13, 17, 19, 23, 29)
    def __init__(self, itemCount,fp, filterName='bloomfilter' ):
        self.calculateKfactor(itemCount, fp)
        self.name = filterName

    def calculateKfactor(self, itemCount, fp):
        maxBitsSize = 1 << 27
        if itemCount <= 0 or fp <0 or fp >=1:
            raise  Exception('Argument Error')
        #kfactor = math.log(2)*( maxBitsSize /itemCount)
        expectM = (long)(1.0/fp)
        expectM = math.log(expectM) * itemCount / (math.log(2) * math.log(2))
        if expectM > maxBitsSize:
            raise Exception('expected bit size exceeded 2^27.')

    def IfKeyVisited(self, key):
        for factor in self.factors:
            hashValue = self.hash(key, factor)
            bitValue = self.rClient.getbit(self.name, hashValue)
            if bitValue == 0:
                return  False
        return True

    def setBloomFilterBits(self, key, bitValue):
        for factor in self.factors:
            hashValue = self.hash(key, factor)
            self.rClient.setbit(self.name, hashValue, bitValue)

    def hash(self, key, factor):
        hashValue  = 0
        mask = (1 << 27) -1
        for ch in key:
            hashValue = (hashValue * factor + ord(ch)) & mask
        return hashValue


import uuid
if __name__=="__main__":
    filter = rBloomFilter(10000, 0.1, 'test')
    filter.setBloomFilterBits('aaaa', 1)
    print(filter.checkBloomFilterBits('aaa'))
    print(filter.checkBloomFilterBits('aaaa'))
    for i in range(0,100):
        key = str(uuid.uuid4())
        print(key+':' + str(filter.checkBloomFilterBits(key)))
        filter.setBloomFilterBits(key, 1)
        print(filter.checkBloomFilterBits(key))

