#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from os import listdir
from os.path import isfile, join
import codecs
mypath = '/Volumes/video/明明爱/torrent/[波多野结衣]种子超大合集300多部'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
onlyTxt = [ torrent for torrent in onlyfiles if torrent.endswith('.txt')]
ed2ks = []
for torrent in onlyTxt:
	for line in codecs.open(mypath + "/" + torrent, "r", "gbk"):
		if line.find("ed2k:") != -1:
			ed2ks.append(line)
			break
shellFile = codecs.open("/Users/paradox/bdls.txt", "w", "utf-8")
for ed2k in ed2ks:
	shellFile.write(ed2k + '\n')
shellFile.close()