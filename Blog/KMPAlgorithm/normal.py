#coding: utf-8
#Date: 2016.03
#Author: 一把杀猪刀 blog: www.mierhuo.com

testStr = 'this is the testStr'
pat = 'is'

tmp = i = j = 0
testMax = len(testStr) - 1
patMax = len(pat) - 1

while i<=(testMax-patMax) and j<=patMax :
	if testStr[i] == pat[j] :  #当前匹配的字符相等，于是都继续往后进行匹配
		i += 1
		j += 1
	else :
		tmp += 1  #发生了不匹配的情况，原始字符串往左挪一位继续尝试匹配
		i = tmp
		j = 0  #要搜索的字符串索引归零，重新开始往后进行匹配
print tmp