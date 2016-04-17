#coding: utf-8
#Date: 2016.03
#Author: 一把杀猪刀 blog: www.mierhuo.com

pat =  'abaabcac'
'   ####01122312'

def get_nextArr(pat):
	'get the next array of pattern that will be used in kmp algorithm'
	pat = ' ' + pat
	patLen = len(pat)-1
	nextArr = [None]*(patLen+1)

	i = 1
	j = 0
	nextArr[0] = patLen
	nextArr[1] = 0

	while i < patLen :
		if j == 0 or pat[i] == pat[j] :
			i += 1
			j += 1
			nextArr[i] = j
		else :
			j = nextArr[j]
	return nextArr

print get_nextArr(pat)