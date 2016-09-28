#coding:utf-8
#Date:2016.4
#Author:一把杀猪刀

__metaclass__ = type

from ActiveGui import ActiveGui
import config
from Manager import Manager
from UpdateGui import UpdateGui
import os

if os.getuid() != 0:
    print '当前不是root权限！'
    exit()

while True:
    iface = raw_input("请输入network device名称：")
    if iface :
        break

manager = Manager(iface)
updater = UpdateGui()
gui = ActiveGui(manager)

manager.bindGui(gui)
manager.bindGuiUpdater(updater)

gui.mainloop()