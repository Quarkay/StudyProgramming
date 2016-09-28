#coding:utf-8
#Date:2016.4
#Author:一把杀猪刀

__metaclass__ = type

import threading
from time import *
from Tkinter import *
import GetData
import dpkt

class UpdateGui(threading.Thread):

    def __init__(self):
        super(UpdateGui, self).__init__()
        self.filterInfo = None

    def run(self):
        self.resultListUpdate()

    def resultListUpdate(self):
        i = 0
        while True:
            if self.newDataList:
                i = i + 1
                tmp = self.newDataList[0]
                del self.newDataList[0]
                self.oldDataDict[i] = tmp
                info = self.getFormatData(tmp)
                if info:
                    self.gui.resultList.insert(END,('% 8d'%i)+' '+info)
                else:
                    del self.oldDataDict[i]
                    i = i-1
                self.gui.resultList.see(END)
            else:
                sleep(0.005)


    def getFormatData(self,tmp):
        res = dict()
        res['timestamp'] = tmp['timestamp']
        res['srcMac'] = tmp['smac']
        res['dstMac'] = tmp['dmac']
        res['origin'] = tmp['origin']
        if tmp['IP'] or tmp['IP6']:
            if(tmp['IP6']):
                ipData = tmp['IP6']
                res['srcIP'] = GetData.ipv6AddrFormat(ipData.src)
                res['dstIP'] = GetData.ipv6AddrFormat(ipData.dst)
            else:
                ipData = tmp['IP']
                res['srcIP'] = GetData.ipAddrFormat(ipData.src)
                res['dstIP'] = GetData.ipAddrFormat(ipData.dst)
            if isinstance(ipData.data,dpkt.tcp.TCP):
                res['type'] = 'TCP'
                tcpData = ipData.data
                res['srcPort'] = str(tcpData.sport)
                res['dstPort'] = str(tcpData.dport)
                if(str(tcpData.sport) == '80' or str(tcpData.dport) == '80'):
                    res['type'] = 'HTTP'
                if(str(tcpData.sport) == '443' or str(tcpData.dport) == '443'):
                    res['type'] = 'HTTPS'
                if(str(tcpData.sport) == '53' or str(tcpData.dport) == '53'):
                    res['type'] = 'DNS'
            elif isinstance(ipData.data,dpkt.udp.UDP):
                res['type'] = 'UDP'
                udpData = ipData.data
                res['srcPort'] = str(udpData.sport)
                res['dstPort'] = str(udpData.dport)
                if(str(udpData.sport) == '53' or str(udpData.dport) == '53'):
                    res['type'] = 'DNS'
            elif isinstance(ipData.data,dpkt.icmp.ICMP):
                res['type'] = 'ICMP'
            elif isinstance(ipData.data,dpkt.igmp.IGMP):
                res['type'] = 'IGMP'
            else:
                if tmp['IP6']:
                    res['type'] = 'IPV6'
                else:
                    res['type'] = 'IPV4'
            if res['type'] in ['TCP','UDP','DNS','HTTP','HTTPS']:
                resStr = '   '+res['type']+'        '+res['srcMac']+'    |->|    '+res['dstMac']+'          '+res['srcIP']+'  (:'+res['srcPort']+')   ===>>>   '+res['dstIP']+'  (:'+res['dstPort']+')'
            else:
                resStr = '   '+res['type']+'        '+res['srcMac']+'    |->|    '+res['dstMac']+'          '+res['srcIP']+'   ===>>>   '+res['dstIP'] + '       '
        elif tmp['ARP'] :
            res['type'] = 'ARP'
            resStr = '   '+res['type']+'        '+res['srcMac']+'    |->|    '+res['dstMac']
        else:
            res['type'] = '暂未支持分析的网络层数据包种类'
            resStr = '   '+res['type']+'        '+res['srcMac']+'    |->|    '+res['dstMac']

        if self.filterInfo :
            if res['type'] not in self.filterInfo['protocols']:
                #print self.filterInfo['protocols']
                #print res['type']
                print '不符合的数据包～～～！'
                return None
            #print self.filterInfo
            for name,weath in (self.filterInfo['detal']).items():
                if weath :
                    #print name
                    #print weath
                    try:
                        if not (res[name] == weath):
                            #print '不符合的数据包～～～！'
                            return None
                    except Exception,e:
                        #print '不符合的数据包～～～！'
                        return None
        return resStr