#-*- coding:utf-8 -*-
"""
" ip2region python seacher client module
"
" Author: koma<komazhang@foxmail.com>
" Date : 2015-11-06
"""'''


这里面是ip搜索算法.






'''
import struct, io, socket, sys

class Ip2Region(object):
    __INDEX_BLOCK_LENGTH  = 12
    __TOTAL_HEADER_LENGTH = 8192

    __f          = None
    __headerSip  = []
    __headerPtr  = []
    __headerLen  = 0
    __indexSPtr  = 0
    __indexLPtr  = 0
    __indexCount = 0
    __dbBinStr   = ''

    '''
    核心就是这3个算法
    '''



    def __init__(self, dbfile):
        self.initDatabase(dbfile)







    def memorySearch(self, ip):
        """
        " memory search method
        " param: ip
        """
        if not ip.isdigit(): ip = self.ip2long(ip)


        if self.__dbBinStr == '':
            self.__dbBinStr   = self.__f.read() #read all the contents in file
            self.__indexSPtr  = self.getLong(self.__dbBinStr, 0)
            self.__indexLPtr  = self.getLong(self.__dbBinStr, 4)
            self.__indexCount = int((self.__indexLPtr - self.__indexSPtr)/self.__INDEX_BLOCK_LENGTH)+1


#下面根据ip获取data.
        l, h, dataPtr = (0, self.__indexCount, 0)
        while l <= h:
            m = int((l+h) >> 1) #就是2分发. 一个头一个尾 ,m中间.
            p = self.__indexSPtr + m*self.__INDEX_BLOCK_LENGTH
            sip = self.getLong(self.__dbBinStr, p)

            if ip < sip:
                h = m -1
            else:
                #读下一个地址.
                eip = self.getLong(self.__dbBinStr, p+4)
                if ip > eip:
                    l = m + 1;
                else:#这时ip=elp,数据放他后面了.所以读下一个.就得到了data.
                    dataPtr = self.getLong(self.__dbBinStr, p+8)
                    break

        if dataPtr == 0: raise Exception("Data pointer not found")

        return self.returnData(dataPtr)










    def binarySearch(self, ip):
        """
        " binary search method ,跟上面一样...
        " param: ip
        """
        if not ip.isdigit(): ip = self.ip2long(ip)

        if self.__indexCount == 0:
            self.__f.seek(0)
            superBlock = self.__f.read(8)
            self.__indexSPtr = self.getLong(superBlock, 0)
            self.__indexLPtr = self.getLong(superBlock, 4)
            self.__indexCount = int((self.__indexLPtr - self.__indexSPtr) / self.__INDEX_BLOCK_LENGTH) + 1

        l, h, dataPtr = (0, self.__indexCount, 0)
        while l <= h:
            m = int((l+h) >> 1)
            p = m*self.__INDEX_BLOCK_LENGTH

            self.__f.seek(self.__indexSPtr+p)
            buffer = self.__f.read(self.__INDEX_BLOCK_LENGTH)
            sip = self.getLong(buffer, 0)
            if ip < sip:
                h = m - 1
            else:
                eip = self.getLong(buffer, 4)
                if ip > eip:
                    l = m + 1
                else:
                    dataPtr = self.getLong(buffer, 8)
                    break

        if dataPtr == 0: raise Exception("Data pointer not found")

        return self.returnData(dataPtr)

    def btreeSearch(self, ip):
        '''
        就是做2词2分.

        :param ip:
        :return:
        '''
        """
        " b-tree search method
        " param: ip
        """
        if not ip.isdigit(): ip = self.ip2long(ip)

        if len(self.__headerSip) < 1:
            headerLen = 0
            #pass the super block
            self.__f.seek(8)
            #read the header block
            b = self.__f.read(self.__TOTAL_HEADER_LENGTH)
            #parse the header block
            for i in range(0, len(b), 8):
                sip = self.getLong(b, i)
                ptr = self.getLong(b, i+4)
                if ptr == 0:
                    break
                self.__headerSip.append(sip)
                self.__headerPtr.append(ptr)
                headerLen += 1
            self.__headerLen = headerLen

        l, h, sptr, eptr = (0, self.__headerLen, 0, 0)
        while l <= h:
            m = int((l+h) >> 1)

            if ip == self.__headerSip[m]:
                if m > 0:
                    sptr = self.__headerPtr[m-1]
                    eptr = self.__headerPtr[m]
                else:
                    sptr = self.__headerPtr[m]
                    eptr = self.__headerPtr[m+1]
                break

            if ip < self.__headerSip[m]:
                if m == 0:
                    sptr = self.__headerPtr[m]
                    eptr = self.__headerPtr[m+1]
                    break
                elif ip > self.__headerSip[m-1]:
                    sptr = self.__headerPtr[m-1]
                    eptr = self.__headerPtr[m]
                    break
                h = m - 1
            else:
                if m == self.__headerLen - 1:
                    sptr = self.__headerPtr[m-1]
                    eptr = self.__headerPtr[m]
                    break
                elif ip <= self.__headerSip[m+1]:
                    sptr = self.__headerPtr[m]
                    eptr = self.__headerPtr[m+1]
                    break
                l = m + 1

        if sptr == 0: raise Exception("Index pointer not found")

        indexLen = eptr - sptr
        self.__f.seek(sptr)
        index = self.__f.read(indexLen + self.__INDEX_BLOCK_LENGTH)
        
        l, h, dataPrt = (0, int(indexLen/self.__INDEX_BLOCK_LENGTH), 0)
        while l <= h:
            m = int((l+h) >> 1)
            offset = int(m * self.__INDEX_BLOCK_LENGTH)
            sip = self.getLong(index, offset)

            if ip < sip:
                h = m - 1
            else:
                eip = self.getLong(index, offset+4)
                if ip > eip:
                    l = m + 1;
                else:
                    dataPrt = self.getLong(index, offset+8)
                    break

        if dataPrt == 0: raise Exception("Data pointer not found")

        return self.returnData(dataPrt)












    def initDatabase(self, dbfile):
        """
        " initialize the database for search
        " param: dbFile
        """
        try:
            self.__f = io.open(dbfile, "rb")
        except IOError as e:

            sys.exit()

    def returnData(self, dataPtr):
        """
        " get ip data from db file by data start ptr
        " param: dsptr
        """
        dataLen = (dataPtr >> 24) & 0xFF  #内存中地址是一个32位的数字,所以这行代码是取前8位.为1的那些数.
        dataPtr = dataPtr & 0x00FFFFFF #再变成26位.

        self.__f.seek(dataPtr)
        data = self.__f.read(dataLen)

        return {
            "city_id": self.getLong(data, 0),
            "region" : data[4:]
        }

    def ip2long(self, ip):
        _ip = socket.inet_aton(ip)
        return struct.unpack("!L", _ip)[0]  #struct pack unpack模块可以在字符串和python对象之间互相转化.

    #这里面就是  把后面的_ip转化为一个

    #模式:https://blog.csdn.net/w83761456/article/details/21171085 这里面是说明

    def isip(self, ip):
        p = ip.split(".")

        if len(p) != 4           : return False
        for pp in p:
            if not pp.isdigit()  : return False
            if len(pp) > 3       : return False
            if int(pp) > 255     : return False

        return True

    def getLong(self, b, offset):#截取一个整数
        if len(b[offset:offset+4]) == 4:
            return struct.unpack('I', b[offset:offset+4])[0]
        return 0

    def close(self):
        if self.__f != None:
            self.__f.close()

        self.__dbBinStr  = None
        self.__headerPtr = None
        self.__headerSip = None
