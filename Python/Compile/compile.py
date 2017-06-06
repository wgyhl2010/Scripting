# -*- coding: UTF-8 -*-  
import os
import os.path
import sys
import ConfigParser

#去除路径最后的斜杠
def removeSlash(path):
	if path.endswith('/'):
		return path[0:len(path)-1]
	else:
		return path
#判断当前文件是否在忽略列表中
def ignore(filename, ignoreList):
	for ignoreFile in ignoreList:
		if filename.find(ignoreFile) >= 0:
			return True
	return False

functionName =  sys.argv[0]
configFile = sys.argv[1]
srcPath = removeSlash(sys.argv[2])
outputPath = removeSlash(sys.argv[3])
cf = ConfigParser.ConfigParser()    
cf.read(configFile)
ignoreList=[]
ignoreList.append(".svn")

#删除已经存在的输出文件
if os.path.isdir(outputPath):  
	os.system("rm -rf " + outputPath)
	print "output direction exists, deleted"

javahome = cf.get("java", "jdkhome")
jarname = cf.get("java", "jarname")
javahome = removeSlash(javahome)
classpath=".:"+javahome+"/lib/dt.jar:"+javahome+"/lib/tools.jar"

#获取src下的所有Java文件,并构造java文件对应的class文件的路径,生成其它诸如配置文件等的路径
javaFiles={}
src=srcPath
suffix=".java"
otherFiles=[]
classFiles=[]
for root, dirs, files in os.walk(src):
	for file in files:
		if file.endswith(suffix):
			javaFiles[root] = os.path.join(root, "*"+suffix)
			index = file.rfind(suffix)-1
			if index == 0:
				classFiles.append(root[len(src):] + "/" + file[0] + ".class")
			else:
				classFiles.append(root[len(src):] + "/" + file[0:index] + ".class")
		elif not ignore(os.path.join(root, file),ignoreList):
			otherFiles.append(os.path.join(root, file)[len(srcPath):])
			
#Java classpath下的及其子目录下的所有资源文件都需要拷贝
cpOtherFiles=""
#拼接所要打包所有项目
tarFiles=""
for other in otherFiles:
	cpOtherFiles += "cp " + srcPath + other + " " + outputPath + other + ";"
	tarFiles += " " + other[1:]
sourceFile=""
for file in javaFiles.itervalues():
	#print file
	sourceFile += " " + file
for classFile in classFiles:
	tarFiles += " " + classFile[1:]

#获取源码依赖的jar包的文件名,拼接拷贝jar文件到output的命令
jarFiles=[]
lib=src[0:src.rfind("/")] + "/lib" 
suffix=".jar"
cpJarFiles = ""
if os.path.exists(lib):
	for root, dirs, files in os.walk(lib):
		for file in files:
			if file.endswith(suffix):
				sourceJar = os.path.join(root, file)
				targetJar = os.path.join(outputPath + root[len(src):] + "/lib", file)
				tarFiles += " " + os.path.join(root[len(src):] + "/lib", file)[1:]
				cpJarFiles += "cp " + sourceJar + " " + targetJar + ";"
				jarFiles.append(sourceJar)
#构建classpath
for file in jarFiles:
	classpath += ":" + file

#拼接拷贝MANIFEST.MF的语句
cpOtherFiles += " cp " + src[0:src.rfind("/")] + "/*.MF" + " " + outputPath + "/META-INF;"
#拼接打包文件命令
tarFiles += " META-INF/*.MF"
print "--------------compile parameters--------------"
print "javahome:" + javahome
print ""
print "cpOtherFiles:" + cpOtherFiles
print ""
print "cpJarFiles:" + cpJarFiles 
print ""
print "sourceFile:" + sourceFile
print ""
print "classpath:" + classpath
print ""
print "tarFiles:" + tarFiles
print "-----------------------------------------------"

output=outputPath
#create output path
if not os.path.exists(output):
	try:
		os.makedirs(output)
	except Exception,msg:
		print "Can not create output path:" + output
		sys.exit()
	try:
		os.makedirs(output+"/META-INF")
	except Exception,msg:
		print "Can not create META-INF path:" + output + "/META-INF"
		sys.exit()

#create output lib path
if os.path.exists(lib):
	try:
		os.makedirs(output+"/lib")
	except Exception,msg:
		print "Can not create lib path:" + output + "/lib"
		sys.exit()
classoutput=output
#编译源码命令
cmd="javac -cp \"" + classpath + "\" -nowarn -encoding utf-8 -d " + "\"" + classoutput + "\" -sourcepath \"" + src + "\"" +  sourceFile 
#生成shell脚本文件
#shellName="compile_java.sh"
#shellFile = open(shellName, "wb")
#shellFile.write(cmd)
#shellFile.close()
#os.system("chmod +x " + shellName)
#os.system("./" + shellName)
#os.remove(shellName)
os.system(cmd)
#靠配源码目录的资源文件
os.system(cpOtherFiles)
#拷贝源码目录的依赖jar到output目录
os.system(cpJarFiles)
#生成jar包
os.system("cd " +  outputPath + "; jar cfm " + outputPath + "/" + jarname + " META-INF/MANIFEST.MF .")# + tarFiles
print "compile finished"



