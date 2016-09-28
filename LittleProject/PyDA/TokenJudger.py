#encoding=utf-8
from FileScanner import FileScanner

__metaclass__ = type

class TokenJudger(FileScanner):
	'''
	判定符号类别
	'''

	def __init__(self,filename):
		'''
		初始化预定义“表”
		'''
		super(TokenJudger,self).__init__(filename)
		#保留字
		self.storedKey = ['ORIGIN','SCALE','ROT','IS','TO','STEP','DRAW','FOR','FROM']
		#参数字
		self.paraKey = ['T']
		#函数字
		self.funcKey = ['SIN','COS','TAN','LN','EXP','SQRT']


	def judgeId(self):
		'''
		判断ID类型，同时可判断出是否是函数
		'''
		while True:
			tmpChar = self.getChar()
			if tmpChar == -1:
				break
			if not (tmpChar.isalpha() or tmpChar.isdigit()):
				self.backChar()
				break
		tmpBuffer = self.charBuffer
		if tmpBuffer in self.storedKey:
			return self.__resultFeed(tmpBuffer)
		elif tmpBuffer in self.paraKey:
			return self.__resultFeed(tmpBuffer)
		elif tmpBuffer in self.funcKey:
			return self.__resultFeed('FUNC',0.0,tmpBuffer.lower())
		else:
			return self.__resultFeed('ID')


	def judgeFloat(self):
		'''
		判断是否是整数或者浮点数
		'''
		while True:
			tmpChar = self.getChar()
			if tmpChar == -1:
				break
			if tmpChar.isdigit():
				continue
			elif tmpChar=='.':
				tmpChar = self.needChar()
				if not tmpChar.isdigit():
					self.errorFeed('语法错误')
				while True:
					tmpChar = self.getChar()
					if tmpChar == -1:
						break
					if not tmpChar.isdigit():
						self.backChar()
						break
				break
			else:
				self.backChar()
				break
		return self.__resultFeed('CONST_ID',float(self.charBuffer))

	def judgeComment(self):
		'''
		判断是否是注释
		'''
		self.getChar()
		if self.charBuffer == '--' or self.charBuffer == '//':
			comment = ''
			while True:
				tmp = self.getChar()
				if tmp == '\n':
					break
				if tmp == '\r':
					continue
				comment += tmp
			self.charBuffer = self.charBuffer[0:2]
			return self.__resultFeed('COMMENT',comment)
		else:
			self.backChar()
			if self.charBuffer == '-':
				return self.__resultFeed('MINUS')
			else:
				return self.__resultFeed('DIV')

	def judgePower(self):
		'''
		判断是否是指数操作符
		'''
		if self.charBuffer == '^':
			return self.__resultFeed('POWER')
		self.getChar()
		if self.charBuffer == '**':
			return self.__resultFeed('POWER')
		else:
			self.backChar()
			return self.__resultFeed('MUL')

	def judgeSymbol(self):
		'''
		判断特殊符号类型
		'''
		if self.charBuffer == '(':
			return self.__resultFeed('L_BRACKET')
		elif self.charBuffer == ')':
			return self.__resultFeed('R_BRACKET')
		elif self.charBuffer == ';':
			return self.__resultFeed('SEMICO')
		elif self.charBuffer == '+':
			return self.__resultFeed('PLUS')
		elif self.charBuffer == ',':
			return self.__resultFeed('COMMA')

	def needChar(self):
		'''
		安全地获取下一字符，不能获取则报错
		'''
		tmpChar = self.getChar()
		if tmpChar == -1:
			self.errorFeed('语法错误')
		else:
			return tmpChar

	def __resultFeed(self,tokenType,tokenValue=0.0,tokenAddr=None):
		'''
		结果反馈
		'''
		tokenIn = self.charBuffer
		self.cleanBuffer()
		return [tokenType,tokenIn,tokenValue,tokenAddr]


if __name__ == '__main__':

	test = TokenJudger()
