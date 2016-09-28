#coding:utf-8
#Date:2016.4
#Author:一把杀猪刀

__metaclass__ = type

import pcap
import dpkt
import config
import pprint
import threading


def ipAddrFormat(ipOrigin):
    '转换16进制的一串IP地址为用户友好的'
    res = ''
    for tmpChar in ipOrigin:
        res = res+' '+str(ord(tmpChar))
    res = '.'.join(res.strip().split(' '))
    return res


def ipv6AddrFormat(ipOrigin):
    '转换16进制的一串IPV6地址为用户友好的'
    res = list(ipOrigin.encode('hex'))
    for i in xrange(0,7):
        index = (i+1)*4+i
        res[index:index] = ':'
    res = ''.join(res)
    return res


def macAddrFormat(macOrigin):
    '转换16进制的一串mac信息为用户友好的'
    res = ''
    for tmpChar in str(macOrigin):
        tmpChar = str(hex(ord(tmpChar)))[2:]
        if len(tmpChar)<2:
            res = res+' 0'+tmpChar
        else:
            res = res+' '+tmpChar
    return ':'.join(res.strip().split(' '))


class GetData(threading.Thread):

    def __init__(self,newDataList,devname=None):
        super(GetData, self).__init__()
        self.isStarted = 1
        self.newDataList = newDataList
        self.pc = pcap.pcap(name=devname if devname else self.getDev())
        #pc.setfilter()

    def run(self):
        self.startGet()

    def startGet(self):
        for timestamp,rawData in self.pc:
            if self.isStarted :
                self.newDataList.append(self.analyRawCont(timestamp,rawData))
                #pprint.pprint(self.analyRawCont(timestamp,rawData))
                #print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
                #print self.pc.stats()
                #print type(self.newDataList)
                #print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            else:
                continue

    def analyRawCont(self,timestamp,rawData):
        '''
        初步解析数据包，方便使用
        smac : 源mac地址
        dmac : 目的地mac地址
        IP 、 IP6 、 ARP : 对应协议的整个数据报
        @:return dict
        '''
        eth = dpkt.ethernet.Ethernet(rawData)
        res = dict([('IP',0),('IP6',0),('ARP',0),('timestamp',timestamp)])
        res['origin'] = eth
        res['smac'] = macAddrFormat(eth.src)
        res['dmac'] = macAddrFormat(eth.dst)
        tmpData = eth.data
        while True:
            try:
                if isinstance(tmpData,dpkt.ip.IP):
                    res['IP'] = tmpData
                    break
                if isinstance(tmpData,dpkt.ip6.IP6):
                    res['IP6'] = tmpData
                    #print [tmpData]
                    break
                if isinstance(tmpData,dpkt.arp.ARP):
                    res['ARP'] = tmpData
                    break
                tmpData = tmpData.data
            except Exception,e :
                break
        return res

    def getDev(self):
        return pcap.lookupdev()

if __name__ == '__main__':
    test = GetData([],'wlan0')
    test.startGet()