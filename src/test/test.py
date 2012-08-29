import cherrypy
from mako.template import Template
from tabsClass import TabClass
import rospy

from std_msgs.msg import String
from sensor_msgs.msg  import Image

import roslib.packages

import unicodedata

import time
import urllib
import urllib2_file
import urllib2
import sys, json
import os
import shutil

class TestManager(TabClass):


    def __init__(self,language):
        self.language = language
        self.htmlTemplate = Template(filename='test/templates/testTemplate.html')
        self.jsTemplate = Template(filename='test/templates/testTemplate.js')


    @cherrypy.expose
    def unload(self):
        #self.mjpegServer.stop("8081")
        return "ok"

    @cherrypy.expose
    def index(self):
        #self.mjpegServer.start("8081")
        return self.htmlTemplate.render(language=self.language)

    @cherrypy.expose
    def testJs(self, parameters=None):
        return self.jsTemplate.render(language=self.language)

