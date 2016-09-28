#encoding=utf-8

from LexAnalyzer import LexAnalyzer

__metaclass__ = type

class SyntaxParser(LexAnalyzer):
	'''
	语法分析(递归下降分析)，构造语法树
	'''
	def __init__(self,filename):
		super(SyntaxParser,self).__init__(filename)
		syntaxTree = dict()

	def startProgram(self):
		'''
		分析启动函数
		'''
		while -1 !=  self.getUsefulToken():
			self.programStatement()
			self.matchSymbol(';')

	def programStatement(self):
		'''
		具体的各种statement分析
		'''
		tmp = self.tokenBuffer
		print 'which kind of statement---',tmp
		if tmp[0] == 'ORIGIN':
			print 'matched ORIGIN'
			self.originStatement()
		elif tmp[0] == 'ROT':
			print 'matched ROT'
			self.rotStatement()
		elif tmp[0] == 'SCALE':
			print 'matchedSCALE'
			self.scaleStatement()
		elif tmp[0] == 'FOR':
			print 'matchedFOR'
			self.forStatement()
		else:
			print 'erorr --->',self.tokenBuffer
			self.errorFeed('语法错误')

	def originStatement(self):
		self.matchStoredKey('IS')
		self.matchSymbol('(')
		self.matchExpression()
		self.matchSymbol(',')
		self.matchExpression()
		self.matchSymbol(')')

	def scaleStatement(self):
		self.matchStoredKey('IS')
		self.matchSymbol('(')
		self.matchExpression()
		self.matchSymbol(',')
		self.matchExpression()
		self.matchSymbol(')')
	
	def rotStatement(self):
		self.matchStoredKey('IS')
		self.matchSymbol('(')
		self.matchExpression()
		self.matchSymbol(',')
		self.matchExpression()
		self.matchSymbol(')')

	def forStatement(self):
		self.matchStoredKey('T')
		self.matchStoredKey('FROM')
		self.matchExpression()
		self.matchStoredKey('TO')
		self.matchExpression()
		self.matchStoredKey('STEP')
		self.matchExpression()
		self.matchStoredKey('DRAW')
		self.matchSymbol('(')
		self.matchExpression()
		self.matchSymbol(',')
		self.matchExpression()
		self.matchSymbol(')')

	def matchExpression(self):
		print 'try to match Expression---->',self.tokenBuffer
		self.matchTerm()
		while -1 != self.getUsefulToken():
			if self.tokenBuffer[1]=='+' or self.tokenBuffer[1]=='-':
				self.matchTerm()
			else :
				self.backNowToken()
				break

	def matchTerm(self):
		self.matchFactor()
		while -1 != self.getUsefulToken():
			if self.tokenBuffer[1]=='*' or self.tokenBuffer[1]=='/':
				self.matchFactor()
			else :
				self.backNowToken()
				break

	def matchFactor(self):
		self.getUsefulToken()
		print 'get in to matchFactor--->',self.tokenBuffer
		if self.tokenBuffer[1] == '+' or self.tokenBuffer[1]=='-':
			self.matchFactor()
		else:
			self.backNowToken()
			self.matchComponent()

	def matchComponent(self):
		self.getUsefulToken()
		print 'get in to matchComponent--->',self.tokenBuffer
		if self.tokenBuffer[0]=='POWER':
			self.matchComponent()
		else:
			self.backNowToken()
			self.matchAtom()
			self.getUsefulToken()
			if self.tokenBuffer[0] == 'POWER':
				self.matchComponent()
			else:
				self.backNowToken()
				return 1

	def matchAtom(self):
		self.getUsefulToken()
		print 'get in to matchAtom--->',self.tokenBuffer
		if self.tokenBuffer[0] =='CONST_ID':
			return 1
		elif self.tokenBuffer[1] == 'T':
			return 1
		elif self.tokenBuffer[1] == '(':
			self.matchExpression()
			self.matchSymbol(')')
		elif self.tokenBuffer[0] == 'FUNC':
			self.matchSymbol('(')
			self.matchExpression()
			self.matchSymbol(')')
		else:
			self.errorFeed('语法错误...')

	def matchSymbol(self,symbol):
		'''
		匹配终结符号
		'''
		self.getUsefulToken()
		print 'match symbol--->',self.tokenBuffer,'--->',symbol
		if self.tokenBuffer[1] == symbol :
			return 1
		else:
			self.errorFeed('语法错误')

	def matchStoredKey(self,key):
		'''
		匹配关键字
		'''
		self.getUsefulToken()
		print 'match key--->',self.tokenBuffer,'--->',key
		if self.tokenBuffer[1] == key:
			return 1
		else:
			self.errorFeed('语法错误')

	def checkContinue(self):
		'''
		尝试继续读入记号
		'''
		if -1 == self.getToken():
			return 0
		else:
			return 1

if __name__ == '__main__':

	test = SyntaxParser('test.txt')
	test.startProgram()



