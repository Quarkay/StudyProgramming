#encoding=utf-8

__metaclass__ = type

class FileScanner:

	def __init__ (self,filename):
		#用于标示文件是第一次读取，改善文件为空时提示信息
		self.FirstStart = 1
		try:
			self.fp = open(filename,'rb')
			self.charBuffer = ''
			self.row = 1
		except Exception, e:
			self.errorFeed('打开源文件出错：'+filename)

	def getChar(self):
		'''
		读取下一个字符，同时自动加入缓冲区
		'''
		try:
			tmpChar = self.fp.read(1)
			if tmpChar :
				self.FirstStart = 0
				if tmpChar == '\n':
					self.row += 1
				self.charBuffer += tmpChar
				return tmpChar
			else:	
				if self.FirstStart == 1:
					self.errorFeed('文件为空...',0)
				return -1
		except Exception, e:
			return -1
			pass

	def backChar(self):
		'''
		回退一个字符，文件指针自动定位，同时缓冲区自动删除该字符
		'''
		try:
			nowIp = self.fp.tell()
			if nowIp == 0:
				self.fp.seek(0)
				self.row = 1
				return 0
			else:
				self.fp.seek(nowIp-1)
				tmpChar = self.getChar()
				if tmpChar == '\n':
					self.row -= 1 
				self.fp.seek(nowIp-1)
				self.charBuffer = self.charBuffer[0:-1]
			self.charBuffer = self.charBuffer[0:-1]
			return nowIp-1
		except Exception, e:
			self.errorFeed(e)

	def cleanBuffer(self):
		'''
		清空缓冲区
		'''
		self.charBuffer = ''

	def errorFeed(self,msg,lineInfo=1):
		'''
		错误信息反馈
		'''
		if lineInfo==1 :
			print str(msg)+'-------------------->>>on line'+str(self.row)
		else :
			print str(msg) 
		exit()

	def endScan(self):
		'''
		关闭扫描
		'''
		try:
			self.fp.close()
		except Exception, e:
			pass

if __name__ == '__main__':
	test = FileScanner('test.txt')
	print test.getChar()
	print test.getChar()
	print test.charBuffer
	test.backChar()
	print test.charBuffer
	print test.getChar()
	print test.charBuffer