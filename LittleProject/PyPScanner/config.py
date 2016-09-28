#encoding=utf-8
#author:PyPScanner Group
#date:2015.12


#帮助信息
helpInfo = \
'''
-h  show help information
-v  version of the tool
-ip the ip host(must need)
-p  the port of host
		eg: -p5555-65535
		default port value:
			500-65535
-s 	service name
		eg: memcached、mysql
		default s value:
			mysql-server
-n  the number of thread that will be actived to scan the host
		default n value:
			666
-t  the time (how many seconds) that will be used to judge
		default t value:
			3
-l the file name that will be used to put in the result of scanning.
		default log file:
			./PyPScanner.log
'''


#默认设置
defaultP = (500,65535)
defaultS = 'mysql'
defaultN = 666
defaultT = 3
defaultL = './PyPScanner.log'

#插件设置
PluginStyle = 1 # 1一级目录遍历插件  
				# 2递归式遍历插件

#调试设置
Debug = 1 #调试信息输出控制