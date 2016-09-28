#coding:utf-8
#author:PyPScanner Group
#date:2015.12

__metaclass__ = type

import config
import os
import sys

args = sys.argv[1:]
if (not args) or ('-ip' not in ''.join(args)):
	print config.helpInfo
	exit()

'''
默认设置
'''
port = config.defaultP
service = config.defaultS
number = config.defaultN
time = config.defaultT
log = config.defaultL

'''
参数设置
'''
for arg in args:
	if arg.startswith('-ip'):
		ip = arg[3:]
	elif arg.startswith('-p'):
		port = arg[2:].split('-')
	elif arg.startswith('-s'):
		service = arg[2:]
	elif arg.startswith('-n'):
		number = arg[2:]
	elif arg.startswith('-t'):
		time = arg[2:]
	elif arg.startswith('-l'):
		log = arg[2:]


if config.Debug:
	print '\n参数数据:',args
	print 'host参数:',ip
	print 'port参数:from',port[0],'to',port[1]
	print 'service参数:',service
	print 'number参数:',number
	print 'time参数:',time
	print 'log参数:',log
	print '参数获取完毕...\n'


def getPluginList(path):
	pluginList = []
	if config.PluginStyle == 1:
		pluginList = [plugin[:-3] for plugin in os.walk(path).next()[2] if not (plugin.startswith('_') or plugin.endswith('pyc'))]
	elif config.PluginStyle == 2:
		for fileList in os.walk(path):
			for plugin in fileList[2]:
				if not (plugin.startswith('_') or plugin.endswith('pyc')):
					pluginList.append(plugin[:-3])
	return pluginList

'''
插件信息
'''
pluginList = getPluginList('./Plugins/service')

if config.Debug:
	print '准备加载插件文件...'
	print '可用插件列表',pluginList,'\n'

if not pluginList:
	print '\n无可用插件..gg...'
	exit()

'''
后面需要的各种参数、插件信息都预存在Pypinit域
参数说明：

扫描地址： ip     --> -ip
端口：	   port   --> -p
	开始端口：port[0]
	结束端口：port[1]
服务名：   service--> -s
线程数：   number --> -n
超时时间： time   --> -t
log目录：  log
'''