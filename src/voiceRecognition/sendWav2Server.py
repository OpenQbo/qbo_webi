
#Envio de file -> http://atlee.ca/software/poster/
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

import sys

register_openers()

file1= open(sys.argv[1], "rb")
datagen, headers = multipart_encode({"file1": file1  })

url = "http://"+sys.argv[2]+":"+sys.argv[3]+"/upload"
request = urllib2.Request(url, datagen, headers)
print urllib2.urlopen(request).read()

file1.close()

