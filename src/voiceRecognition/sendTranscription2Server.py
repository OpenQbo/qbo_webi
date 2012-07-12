
#Envio de file -> http://atlee.ca/software/poster/
import urllib2

import sys



data="data={\"userName\":\""+sys.argv[1]+"\", \"transcription\":\""+  sys.argv[2]   +"\", \"lang\":\""+  sys.argv[3]  +"\", \"fromBot\": true  }";

req = urllib2.Request("http://"+sys.argv[4]+":"+sys.argv[5]+"/save", data)
f = urllib2.urlopen(req)
response = f.read()

print response

