#coding:utf-8
#Date:2016.4
#Author:一把杀猪刀

__metaclass__ = type

from Tkinter import *
import config
from MainGui import MainGui


class ActiveGui(MainGui):

    def __init__(self,manager):
        MainGui.__init__(self)
        self.bindManager(manager)
        self.commandInit()
        self.stateInit()


    def commandInit(self):
        self.startBut.config(command=self.manager.startSniffer)
        self.stopBut.config(command=self.manager.stopSniffer)
        self.quitBut.config(command=self.manager.quitSniffer)
        self.resultList.bind('<Double-Button-1>',self.showResultDetail)
        self.filterButton.config(command=self.setFilter)


    def setFilter(self):
        filterInfo = {}
        filterInfo['detal'] = dict([('srcIP',self.sAddEntry.get()),('dstIP',self.dAddEntry.get()),('srcPort',self.spEntry.get()),('dstPort',self.dpEntry.get())])
        filterInfo['protocols'] = []
        for name,info in self.filterVarDict.iteritems():
            if info.get() == 1:
                filterInfo['protocols'].append(name)
        #print filterInfo
        self.manager.filterActive(filterInfo)



    def stateInit(self):
        self.stopBut.config(state=DISABLED)


    def addResultList(self,formatResData):
        self.resultList.insert(END,'sb')
        self.resultList.config(selectbackground='green',font='monospace 13')
        self.resultList.see(END)

    def clearResultList(self):
        self.resultList.delete(0,END)

    def showResultDetail(self,event):
        self.resultDetal.config(state=NORMAL)
        self.resultDetal.delete('0.0',END)
        dataIndex = int(self.resultList.get(self.resultList.curselection())[0:9])
        self.resultDetal.insert(INSERT,self.manager.queryFormatData(dataIndex))
        self.resultDetal.config(state=DISABLED)


    def guiTest(self):
        self.addResultList('sb')

    def bindManager(self,manager):
        self.manager = manager