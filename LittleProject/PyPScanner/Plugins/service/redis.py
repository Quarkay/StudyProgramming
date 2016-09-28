#!/usr/bin/env python
#coding:utf-8
import redis
import threading

class checkThread(threading.Thread):
	def __init__(self,checkQueue,activeQueue,host,db,lock):
		super(checkThread,self).__init__()
		self.checkQueue = checkQueue
		self.activeQueue = activeQueue
		self.host = host
		self.db = db
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
				conn = redis.Redis(host = str(self.host),port = int(port),db = int(self.db),password='123456')
				try:
					conn.get(1)
				except Exception,e:
					if ('invalid password' in e):
						print 'port found!  ---> ',port
						self.activeQueue.append(port)
				else:
					#直接就连上了（虽然概率很小...）
					self.activeQueue.append(port)
					print "*****************************\nhost,'---',port,'root---123456'\n*****************************\n"
					break
			else:
				#print 'con_over......'
				break

class weakThread(threading.Thread):
	def __init__(self,passQueue,okQueue,host,port,db,lock):
		super(weakThread,self).__init__()
		self.passQueue = passQueue
		self.okQueue = okQueue
		self.host = host
		self.port = port
		self.db = db
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

				tmpPass = passTmp[0]
				while (tmpPass[-1:] in ['\r','\n']):
					tmpPass = passTmp[0][:-1]
				print 'checking password--->',tmpPass
				conn = redis.Redis(host=str(self.host),port=int(self.port),db = self.db,password = tmpPass)
				try:
					conn.get(1)
				except Exception,e:
					pass
				else:
					self.okQueue.append([tmpPass])
			else:
				break
	
class myredis:
	def __init__(self,host,fromPort,toPort,threadNumber,db,logPath):
		self.host = str(host)
		self.fromPort = int(fromPort)
		self.toPort = int(toPort)
		self.threadNumber = int(threadNumber)
		self.db = int(db)
		self.logPath = str(logPath)
		self.checkQueue = []
		self.activeQueue = []
		for tmpPort in xrange(self.fromPort,self.toPort+1):
			self.checkQueue.append(tmpPort)

	def getActivePorts(self):
		lock = threading.Lock()
		threadList = []
		for n in xrange(1,self.threadNumber+1):
			#print 'creating thread--->',n
			threadList.append(checkThread(self.checkQueue,self.activeQueue,self.host,self.db,lock))
		for t in threadList:
			t.start()
		print 'waiting...'
		for t in threadList:
			t.join()

		return self.activeQueue

	def weakPasswordAttack(self,padPath,padThreadNum):
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
				threadList.append(weakThread(self.passQueue,self.weakPasswordDict[port],self.host,port,self.db,lock))
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

def serviceInit(host,fromPort,toPort,threadNumber,db,logPath):
	return myredis(host,fromPort,toPort,threadNumber,db,logPath)