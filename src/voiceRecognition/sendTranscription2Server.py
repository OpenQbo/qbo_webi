#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2

import sys


#transcriptionASCII=sys.argv[2].encode('ASCII')
#print transcriptionASCII
#transcription=sys.argv[2].decode("utf-8")
#print transcription
data="data=userName:"+sys.argv[1]+",transcription:"+urllib2.quote(sys.argv[2])+",lang:"+sys.argv[3]+",fromBot:true";
#data="data={\"userName\":\""+sys.argv[1]+"\", \"transcription\":\""+  urllib2.quote(sys.argv[2])   +"\", \"lang\":\""+  sys.argv[3]  +"\", \"fromBot\": true  }";
print "TRANSCRIPTION SENDER"
print data
#data=data.encode("ASCII")
#test=urllib2.quote(data)
#print test
print data
req = urllib2.Request("http://"+sys.argv[4]+":"+sys.argv[5]+"/save", data)
f = urllib2.urlopen(req)
response = f.read()

#print response
