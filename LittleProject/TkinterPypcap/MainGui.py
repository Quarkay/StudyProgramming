#!/usr/bin/env python
#coding:utf-8
#Date:2016.4
#Author:一把杀猪刀

__metaclass__ = type

from Tkinter import *
import config

class MainGui(Tk):

    def __init__(self):
        Tk.__init__(self,className=config.title)
        self.config(width=1111,height=600,bg='gray')
        self.frameInit()
        self.menuInit()
        self.filterInit()
        self.resultInit()


    def frameInit(self):
        self.menuFrame = Frame(self,height=20,bg='#F06292')
        self.menuFrame.pack(fill=X)
        self.filterFrame = Frame(self,bg='#F8BBD0')
        self.filterFrame.pack(fill=Y,side='left')
        self.resultWindow = PanedWindow(orient=VERTICAL,showhandle=True,sashrelief=RAISED,bg='#311B92')
        self.resultWindow.pack(fill=BOTH)



    def resultInit(self):
        '嗅探结果区域'
        '上部嗅探结果列表'
        self.resultListWindow = PanedWindow(orient=HORIZONTAL)
        tmpFrame = Frame()
        self.resultList = Listbox(tmpFrame,bg='#E1BEE7',selectmod=BROWSE)
        self.resultList.place(relwidth=0.985,relheight=1.0)
        listScrollBar = Scrollbar(tmpFrame,bg='#009688',troughcolor='#00695C')
        listScrollBar.place(relwidth=0.015,relx=0.985,relheight=1.0)
        self.resultList.config(yscrollcommand=listScrollBar.set)
        listScrollBar.config(command=self.resultList.yview)
        self.resultListWindow.add(tmpFrame)
        self.resultWindow.add(self.resultListWindow,height=480)
        '底部详细信息'
        self.resultDetal = Text(bg='black',fg='green',font='monospace 15')
        self.resultDetal.insert(INSERT,'双击上方列表即可显示详情,拖动可调节此窗口大小')
        self.resultDetal.config(state=DISABLED)
        self.resultWindow.add(self.resultDetal)


    def menuInit(self):
        '菜单栏初始化'
        self.startBut = Button(self.menuFrame,text='开始',fg='black',bg='Purple',bd=0)
        self.startBut.pack(fill=Y,side='left',padx=2)
        self.stopBut = Button(self.menuFrame,text='停止',fg='black',bg='Purple',bd=0)
        self.stopBut.pack(fill=Y,side='left',padx=2)
        self.quitBut = Button(self.menuFrame,text='退出',fg='black',bg='Purple',bd=0)
        self.quitBut.pack(fill=Y,side='left',padx=2)


    def filterInit(self):
        '左边栏(Filter)初始化'
        self.filterTable = Label(self.filterFrame,text='筛选条件',width=20,font='sans 16')
        self.filterTable.grid(row=0,column=0,columnspan=2)
        self.spLable = Label(self.filterFrame,text='源端口号')
        self.spLable.grid(row=1,column=0,pady=6)
        self.spEntry = Entry(self.filterFrame)
        self.spEntry.grid(row=1,column=1)
        self.dpLable = Label(self.filterFrame,text='终端口号')
        self.dpLable.grid(row=2,column=0,pady=6)
        self.dpEntry = Entry(self.filterFrame)
        self.dpEntry.grid(row=2,column=1)
        self.sAddLable = Label(self.filterFrame,text='源IP地址')
        self.sAddLable.grid(row=3,column=0,pady=6)
        self.sAddEntry = Entry(self.filterFrame)
        self.sAddEntry.grid(row=3,column=1)
        self.dAddLable = Label(self.filterFrame,text='终IP地址')
        self.dAddLable.grid(row=4,column=0)
        self.dAddEntry = Entry(self.filterFrame)
        self.dAddEntry.grid(row=4,column=1)
        checkList = ['TCP','UDP','ARP','IPV4','IPV6','ICMP','IGMP','DNS','HTTP','HTTPS']
        self.filterVarDict = dict()
        for i,protocal in enumerate(checkList) :
            self.filterVarDict[protocal] = IntVar(value=1)
            Checkbutton(self.filterFrame,text=protocal,variable=self.filterVarDict[protocal]).grid(row=int((i/2+5)),column=i%2,pady=8)
        self.filterButton = Button(self.filterFrame,text='确定',width=15)
        self.filterButton.grid(pady=15,columnspan=2)

    def start(self):
        self.mainloop()