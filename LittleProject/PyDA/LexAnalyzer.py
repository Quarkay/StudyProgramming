#encoding=utf-8
from TokenJudger import TokenJudger

__metaclass__ = type

class LexAnalyzer(TokenJudger):
	'''
	词法分析，识别、获取token，基本的判断错误
	'''

	def __init__(self,filename):
		super(LexAnalyzer,self).__init__(filename)
		self.tokenBuffer = ''  #当前Token暂存

	def getToken(self):
		'''
		获取下一个记号，且自动暂存于tokenBuffer
		'''
		blackList = ['\r','\n',' ','\t']
		possibleSymbol = list(';,()+')
		while True:
			tmpChar = self.getChar()
			if tmpChar == -1:
				self.tokenBuffer = -1
				try:
					self.endScan() #发现扫描完毕则自动关闭扫描
				except Exception, e:
					pass
				return -1 #记号获取完毕
			if tmpChar in blackList: #过滤掉空格换行回车制表符这类空白字符
				self.cleanBuffer()
				continue
			if tmpChar.isalpha():
				#必然是ID类符号
				self.tokenBuffer = self.judgeId()
				return self.tokenBuffer
			elif tmpChar.isdigit():
				#必然是CONST_ID类符号（数）
				self.tokenBuffer = self.judgeFloat()
				return self.tokenBuffer
			elif tmpChar == '-' or tmpChar == '/':
				self.tokenBuffer = self.judgeComment()
				return self.tokenBuffer
			elif tmpChar == '*' or tmpChar == '^':
				self.tokenBuffer =  self.judgePower()
				return self.tokenBuffer
			elif tmpChar in possibleSymbol:
				self.tokenBuffer = self.judgeSymbol()
				return self.tokenBuffer
			else:
				self.errorFeed('非法字符')


	def getUsefulToken(self):
		'''
		获取有实际操作意义的token
		'''
		useLessList = ['COMMENT',]
		while True:
			self.getToken()
			if -1 == self.tokenBuffer :
				return -1
			else:
				if self.tokenBuffer[0]  not in useLessList:
					return self.tokenBuffer
				else:
					print 'useLess ---> ',self.tokenBuffer
					continue

	def backNowToken(self):
		'''
		回退缓冲区的token读取（token不会换行,直接操作即可）
		'''
		try:
			leng = len(self.tokenBuffer[1])
			self.fp.seek(self.fp.tell() - leng)
			self.tokenBuffer = ''
			self.cleanBuffer()
		except Exception,e:
			print 'token回退出错...'




	def stopLexAnalyzer(self):
		'''
		释放文件占用，一般会自动处理，无需手动调用
		'''
		self.endScan()






if __name__ == '__main__':

	test = LexAnalyzer('test.txt')
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print '--------------------'
	print test.tokenBuffer
	print '--------------------'
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print '--------------------'
	print test.getToken()
	test.backNowToken()
	test.getUsefulToken()
	print test.tokenBuffer
	test.getUsefulToken()
	print test.tokenBuffer
	print '--------------------'
	print test.tokenBuffer
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	print test.getToken()
	test.stopLexAnalyzer()
