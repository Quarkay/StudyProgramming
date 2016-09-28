#coding:utf-8
#author:PyPScanner Group
#date:2015.12

__metaclass__ = type

import sys
import MySQLdb
import threading
import socket
import re
#from Queue import Queue


class checkThread(threading.Thread):
	'''
	检测服务是否存在的线程
	'''
	def __init__(self,checkQueue,activeQueue,host,timeOut,lock):
		super(checkThread,self).__init__()
		self.checkQueue = checkQueue
		self.activeQueue = activeQueue
		self.host = str(host)
		self.timeOut = int(timeOut)
		self.lock = lock

   	def run(self):
		while True:
			if self.checkQueue:
				self.lock.acquire()
				if not self.checkQueue:
					self.lock.release()
					break
				port = self.checkQueue[0]
				del self.checkQueue[0]
				self.lock.release()
				#print 'checking port --->',port
				try:
					conn = MySQLdb.connect(host=str(self.host),user='root',passwd='123456',connect_timeout=int(self.timeOut),port=int(port))
				except Exception,e:
					if ('Access denied' in e[1]) or ('is not allowed' in e[1]) :
						print 'port found!  ---> ',port
						self.activeQueue.append(port)
				else:
					#直接就连上了（虽然概率很小...）
					self.activeQueue.append(port)
					print '*****************************\n'
					print host,'---',port,'root---123456'
					print 'Your MySQL database is under very dangerous situation! You should change your password! '
					print '*****************************\n'
					break
			else:
				#print 'con_over......'
				break


class weakThread(threading.Thread):
	'''
	测试弱密码的线程
	'''
	def __init__(self,passQueue,okQueue,host,port,timeOut,lock):
		super(weakThread,self).__init__()
		self.passQueue = passQueue
		self.okQueue = okQueue
		self.host = host
		self.port = port
		self.timeOut = timeOut
		self.lock = lock

   	def run(self):
		while True:
			if self.passQueue:
				self.lock.acquire()
				if not self.passQueue:
					self.lock.release()
					break
				passTmp = self.passQueue[0]
				passTmp = passTmp.split("	") # \t
				del self.passQueue[0]
				self.lock.release()

				tmpUser = passTmp[0]
				tmpPass = passTmp[1]
				while (tmpPass[-1:] in ['\r','\n']):
					tmpPass = passTmp[1][:-1]
				#print 'checking --->',tmpUser,'  ',tmpPass

				try:
					conn = MySQLdb.connect(host=str(self.host),user=tmpUser,passwd=tmpPass,connect_timeout=int(self.timeOut),port=int(self.port))
				except Exception,e:
					pass
				else:
					self.okQueue.append([tmpUser,tmpPass])
			else:
				break


class mysql:
	'''
	mysql服务插件主体
	'''

	def __init__(self,host,fromPort,toPort,threadNumber,timeOut,logPath):
		self.host = str(host)
		self.fromPort = int(fromPort)
		self.toPort = int(toPort)
		self.threadNumber = int(threadNumber)
		self.timeOut = int(timeOut)
		self.logPath = str(logPath)
		self.checkQueue = []
		self.activeQueue = []
		for tmpPort in xrange(self.fromPort,self.toPort+1):
			self.checkQueue.append(tmpPort)

	def getActivePorts(self):
		'''
		返回开放mysql服务的端口列表
		'''
		lock = threading.Lock()
		threadList = []
		for n in xrange(1,self.threadNumber+1):
			#print 'creating thread--->',n
			threadList.append(checkThread(self.checkQueue,self.activeQueue,self.host,self.timeOut,lock))
		for t in threadList:
			t.start()
		print 'waiting...'
		for t in threadList:
			t.join()

		return self.activeQueue

	def weakPasswordAttack(self,padPath,padThreadNum):
		'''
		弱密码攻击，提供弱密码文件路径和设置线程数
		'''
		try:
			fp = open(padPath)
		except Exception,e:
			print 'failed to open the weakPassword pad text file...'
			exit()

		self.passQueue = fp.readlines()[:]
		fp.close()

		self.weakPasswordDict = {}
		lock = threading.Lock()

		for port in self.activeQueue :
			self.weakPasswordDict[port] = []
			threadList = []
			for n in xrange(1,int(padThreadNum)+1):
				#print 'creating weakPasswordAttack thread--->',n
				threadList.append(weakThread(self.passQueue,self.weakPasswordDict[port],self.host,port,self.timeOut,lock))
			for t in threadList:
				t.start()
			print 'waiting...'
			for t in threadList:
				t.join()

		print "weak password result:"
		print "********************************************************************"
		print self.weakPasswordDict
		print "********************************************************************"
		return self.weakPasswordDict

	#def brutForceAttack(self,level=2):
	#	'''
	#	暴力攻击...
	#	level表示等级...
	#	这个肯定又会是各个插件都会用到的...看看能不能放common下？
	#	'''
	#	pass

	def getVersion(self):
		'''
		版本识别
		'''
		self.versionList = []
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		for port in self.activeQueue :
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((self.host, port))
			sock.send("I just want to get the version of you! :)")
			res = sock.recv(1024)
			if 'is not allowed' in res:
				continue
			res = re.findall('\d{1}\.\d{1}.\d+',res)
			if res:
				self.versionList.append([port,res[0]])
		return self.versionList


	#<del>
	#
	#<info>构造方式不合理<info>
	#
	#def versionExp(self):
	#	'''
	#	某些版本已知漏洞利用~
	#	'''
	#	pass
	#
	#<del>


def serviceInit(host,fromPort,toPort,threadNumber,timeOut,logPath):
	return mysql(host,fromPort,toPort,threadNumber,timeOut,logPath)