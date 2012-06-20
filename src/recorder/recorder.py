# coding: utf-8
import cherrypy
import os
import glob
from mako.template import Template
from tabsClass import TabClass
import rospy
import subprocess
import os
import signal

class RecorderManager(TabClass):
    
    def __init__(self,language):
        self.language = language
        self.htmlTemplate = Template(filename='recorder/templates/recorderTemplate.html')
        self.jsTemplate = Template(filename='recorder/templates/recorderTemplate.js')
        self.processname = 'qbo_video_record'
        self.command="rosrun qbo_video_record qbo_video_record"

    def runningProcess(self):
        pids=[]
        for line in os.popen("ps xa | grep qbo_video_record | grep -v grep"):
            fields=line.split()
            pids.append(fields[0])
        return pids

    def killall(self):
        for line in os.popen("ps xa | grep qbo_video_record | grep -v grep"):
            fields=line.split()
            os.kill(int(fields[0]), signal.SIGINT)
        return True

    @cherrypy.expose
    def status(self):
        if len(self.runningProcess())>0:
            return "1"
        else:
            return "0"

    @cherrypy.expose
    def record(self):
        if len(self.runningProcess())==0:
            subprocess.Popen(self.command.split())
            return "1"
        else:
            self.killall()
            return "0"

    @cherrypy.expose
    def recorderJs(self, **params):
        return self.jsTemplate.render(language=self.language)

    @cherrypy.expose
    def index(self):
        return self.htmlTemplate.render(language=self.language)
