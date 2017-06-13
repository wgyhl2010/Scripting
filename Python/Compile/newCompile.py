#!/usr/bin/env python
# -*- coding: UTF-8 -*-  
import os
import os.path
import sys
import ConfigParser
import commands

#获取src下的所有文件(相对路径),src为根路径,如/root/src,最后没有/
def getFiles(src):
	result = []
	for root, dirs, files in os.walk(src):
		for file in files:
			tmp = os.path.join(root, file)
			target = tmp[len(src)+1:]
			result.append(target)
	return result

#去除路径最后的斜杠
def removeSlash(path):
	if path.endswith('/'):
		return path[0:len(path)-1]
	else:
		return path

#拼接,args的长度为一条命令中参数的个数
def splice(template, *args):
	result = template 
	if len(args) <= 0:
		return result;
	count = len(args[0])
	if count <= 0:
		return result;
	result = ""
	for i in range(count):
		params = []
		for arg in args:
			params.append(arg[i])
		result += template.format(*params)
	return result
#拼接cp指令
def spliceCpy(template, src, out, files):
	source = []
	target = []
	for file in files:
		source.append(src + "/" + file)
		target.append(out + "/" + file)
	return splice(template, source, target)
	
#从输入的数组中排除制定的文件或者文件夹,ignore[0]要忽略的文件,ignore[1]要忽略的文件夹
#忽略列表可以什么都不传,可以值传忽略文件,但是不可以只传忽略文件夹
def excludeFileAndFolder(fileList, *ignore):
	result = fileList
	if len(ignore) > 2:
		print "warn:ignore不能超过两个忽略列表"
		return result
	result = []
	for file in fileList:
		canAdded = True
		if len(ignore) >= 1:
			for ignoreFile in ignore[0]:
				if file.endswith(ignoreFile):
					#print file + " is ingnored"
					canAdded = False
					break
		if len(ignore) >= 2:
			for ignoreFolder in ignore[1]:
				if file.find(ignoreFolder + "/") >= 0:
					#print file + " is ingnored"
					canAdded = False
					break
		if canAdded:
			result.append(file)
	return result

#提取制定的文件
def extractFile(fileList, *include):
	result = []
	for file in fileList:
		for includeFile in include:
			if file.endswith(includeFile):
				result.append(file)
				break
	return result

#创建Java输出目录的标准结构
def conStandardOutput(output):
	if os.path.isdir(output):  
		os.system("rm -rf " + output)
		print "output direction exists, deleted"
	if not os.path.exists(output + "/lib"):
		try:
			os.makedirs(output + "/lib")
		except Exception,msg:
			print "Can not create output lib path:" + output + "/lib"
			sys.exit()
	if not os.path.exists(output + "/META-INF"):
		try:
			os.makedirs(output + "/META-INF")
		except Exception,msg:
			print "Can not create META-INF path:" + output + "/META-INF"
			sys.exit()
cfg = sys.argv[1]
cf = ConfigParser.ConfigParser()    
cf.read(cfg)
javaHome = removeSlash(cf.get("java", "javaHome"))
src = removeSlash(sys.argv[2])
libPath = src[0:src.rfind("/")] + "/lib"
output = removeSlash(sys.argv[3])
classPath=".:" + javaHome + "/lib/dt.jar:" + javaHome + "/lib/tools.jar"

dependencies = extractFile(getFiles(libPath), ".jar")
classPath += ":" + libPath + "/" +  (":" + libPath + "/").join(dependencies)
files = getFiles(src)
sourceFiles = src + "/" +  (" " + src + "/").join(extractFile(files, ".java"))
otherFiles  = excludeFileAndFolder(files, [".java"])
print otherFiles
#生成src目录下其他文件的拷贝命令
if len(otherFiles) == 0:
	cpOtherFiles = ""
else:
	cpOtherFiles = spliceCpy("cp {0} {1};", src, output, otherFiles)
#生成jar包的拷贝命令
if len(dependencies) == 0:
	cpJarFiles = ""
else:
	cpJarFiles = spliceCpy("cp {0} {1}; ", libPath, output + "/lib", dependencies)
print "----------------------Parameters----------------------"
print "javaHome:" + javaHome 
print "classPath:" + classPath
print "libPath:" + libPath 
print "sourceFiles:" + sourceFiles
print "cpOtherFiles:" + cpOtherFiles
print "cpJarFiles:" + cpJarFiles
print "------------------------------------------------------"

#创建标准的输出目录
conStandardOutput(output)

#拷贝MF文件
metaPath = src[0:src.rfind("/")]
srcMeta = metaPath + "/" + "*.MF"
status, cmdResult = commands.getstatusoutput("ls " + srcMeta)

#将src的上级目录作为生成jar文件的名称
jarName =  metaPath[metaPath.rfind("/") + 1:] + ".jar"

#如果MF文件存在就拷贝到output/META-INF下,并生成打包的命令
if status == 0:
	jarCmd = "cd " + output + "; jar cfm " + output + "/" + jarName + " META-INF/*.MF ."
	os.system("cp " + srcMeta + " " + output + "/META-INF")
else:
	jarCmd = "cd " + output + "; jar cf " + output + "/" + jarName + " ."


#生成class文件
cmd = "javac -cp \"" + classPath + "\" -nowarn -encoding utf-8 -d " + "\"" + output + "\" -sourcepath \"" + src + "\" " +  sourceFiles 
os.system(cmd)
#拷贝src目录下的其他文件到输出目录
os.system(cpOtherFiles)
#拷贝jar包依赖到output的lib目录下
os.system(cpJarFiles)
#打包生成的class文件到jar包中
os.system(jarCmd)
print "compile finished"



	
