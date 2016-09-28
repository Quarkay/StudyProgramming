#coding:utf-8
#Date:2016.4
#Author:一把杀猪刀

__metaclass__ = type

import threading
import GetData
import config
from time import *
from Tkinter import *



#搞一个最后调整窗口大小的线程


class Manager():

    def __init__(self,iface):
        self.iface = iface
        self.startStopLock = threading._allocate_lock()
        self.getter = None
        self.newDataList = []
        self.oldDataDict = dict()

    def startSniffer(self):
        '开启嗅探线程，获得的格式化数据存储于newDataList'
        self.newDataList[:] = []
        self.oldDataDict.clear()
        self.gui.clearResultList()
        if not self.getter :
            self.getter = GetData.GetData(self.newDataList,self.iface)
            self.getter.start()
            self.guiUpdater.start()
        self.setStartStopLock(1)
        self.gui.startBut.config(state=DISABLED)
        self.gui.stopBut.config(state=NORMAL)
        self.gui.quitBut.config(state=DISABLED)


    def stopSniffer(self):
        #print(self.newDataList)
        self.setStartStopLock(0)
        self.gui.startBut.config(state=NORMAL)
        self.gui.stopBut.config(state=DISABLED)
        self.gui.quitBut.config(state=NORMAL)


    def quitSniffer(self):
        self.setStartStopLock(0)
        try:
            self.guiUpdater._Thread__stop()
            self.getter.pc.close()
            self.getter._Thread__stop()
        except Exception,e:
            print e
        self.gui.quit()


    def filterActive(self,filterInfo):
        self.guiUpdater.filterInfo = filterInfo
        self.startSniffer()

    def setStartStopLock(self,flag):
        try:
            self.startStopLock.acquire()
            self.getter.isStarted = flag
            self.startStopLock.release()
        except Exception,e:
            print e


    def bindGui(self,gui):
        self.gui = gui

    def bindGuiUpdater(self,updater):
        self.guiUpdater = updater
        self.guiUpdater.newDataList = self.newDataList
        self.guiUpdater.oldDataDict = self.oldDataDict
        self.guiUpdater.gui = self.gui

    def queryFormatData(self,dataIndex):
        originData = str([self.oldDataDict[dataIndex]['origin']])
        return originData

if __name__ == '__main__' :
    class testClass:
        def __init__(self):
            self.resultList = []
    testObj = testClass()
    testMan = Manager(testObj)
    testMan.startSniffer()
    print '我在等。。。。'
    print testMan.getter.isDaemon()
    sleep(3)
    testMan.stopSniffer()
    print '--------------------------------'
    print testMan.newDataList