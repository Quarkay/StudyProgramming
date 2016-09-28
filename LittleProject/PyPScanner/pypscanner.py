#coding:utf-8
#author:PyPScanner Group
#date:2015.12

__metaclass__ = type

import config
import PypInit

if PypInit.service in PypInit.pluginList:
	serviceMod = __import__('Plugins.service.'+PypInit.service,fromlist=[PypInit.service])
else:
	print 'No such plugin...maybe we will add this plugin in someday.'
	exit()

if config.Debug :
	print 'Loading the plugin...details：'
	print serviceMod,'\n'

#初始化完毕，开始各种动作
service = serviceMod.serviceInit(PypInit.ip,PypInit.port[0],PypInit.port[1],PypInit.number,PypInit.time,PypInit.log)
#取得服务端口列表
portList = service.getActivePorts()

if portList:
	print 'Port list found:',portList
	if raw_input('Get the version of '+ PypInit.service +'(y/*)?') == 'y':
		print 'Trying to get the service\'s version:'
		versionList = service.getVersion()
		if versionList :

			print PypInit.service + "version: " 
			print "*******************************************************"
			print versionList
			print "*******************************************************"
			print "\n"

			if raw_input('Whether try to load exploits(y/*)?') == 'y' :
				print "Loading ..."
				expList = PypInit.getPluginList('./Plugins/exps')
				print expList
				leg = len(PypInit.service)
				print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
				for tmp in expList:
					if tmp.startswith(PypInit.service):
						print tmp[leg:] + ", ",
				print "\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
				while True:
					expName = raw_input('Which exp do you want to use?')
					try:
						expMod = __import__('Plugins.exps.'+PypInit.service+expName,fromlist=[PypInit.service+expName])
					except Exception:
						print "It seems that the name is wrong!..."
					else:
						break
				expService = expMod.expInit(PypInit.ip,versionList)
				print "Exp info :"
				print "---------------------------------------------------------"
				print expMod
				print expService.helpInfo();
				print "---------------------------------------------------------"
				raw_input('Ready to attack(enter any word)?')
				res = expService.tryToAttack()
				print res

		else:
			print "-------------------------------------------------------"
			print "Fail to get the version of "+PypInit.service
			print "-------------------------------------------------------"

	if raw_input('Whether to use weak-password attack(y/*)?') == 'y' :
		padPath = raw_input('The filename of the weak-pad text:')
		padThreadNum = raw_input('The amount of the threads to use:')
		service.weakPasswordAttack(padPath,padThreadNum)
	else:
		exit()
else:
	print 'Can\'t find ' + PypInit.service +' any server port!'