#!/usr/bin/env python
# coding: utf-8

#ROS stuff
import roslib
roslib.load_manifest('qbo_webi');

import rospy

#Other imports
import cherrypy
from mako.template import Template
import json
from sysChecks.sysChecks import sysChecksManager
from training.FaceObjectTrainer import FaceObjectTrainer
from settings.settings import SettingsManager
#CHANGED
from teleoperation.teleoperation import TeleoperationManager
from confWizard.confWizard import ConfWizardManager
from otherFunctionalities.mjpegServerFuntions.MjpegServerFunctions  import MjpegServerFunctions
from voiceRecognition.voiceRecognition import VoiceRecognitionManager
from xmms2.xmms2 import XMMS2Manager
from mjpeg.mjpeg import MjpegGrabber
import os
import sys


pathh = '/'.join(os.path.abspath( __file__ ).split('/')[:-1])
os.chdir(pathh)

rospy.loginfo("Webi: "+pathh)

class Root(object):

    def __init__(self):
        self.indexHtmlTemplate = Template(filename='templates/indexTemplate.html')


        self.lang='en'
        #Load default dict
        fp=open('lang/en.txt','r')
        self.language=json.load(fp,'utf-8')
        fp.close()
        #Load specific dict
        if self.lang!='en':
            fp=open('lang/'+self.lang+'.txt','r')
            self.language.update(json.load(fp,'utf-8'))
            fp.close()


    def readLanFile(self):
        config=ConfigParser.ConfigParser()
        config.readfp(open("lang/en.txt"))
        allsections=config.sections()
        for i in allsections:
            if req.command==config.get(i,"input"):
                execparams=config.get(i, "command")
                result=commands.getoutput(execparams)
                return result
        return "Error, input not exist"


    def setCookieLang(self,lan):
        cookie = cherrypy.response.cookie
        cookie['language'] = lan
        cookie['language']['path'] = '/'
        cookie['language']['max-age'] = 360000
        cookie['language']['version'] = 1

    def readCookieLang(self):
        cookie = cherrypy.request.cookie
	try: 
            res=cookie['language'].value
        except KeyError:
            print "KEY ERROR"
            res=""
        return res

    def index(self,new_lang="",activeTab=0):
        if new_lang!="":
            self.change_language(new_lang)
        else:
            cookielang=self.readCookieLang()
            if cookielang!="":
                self.change_language(cookielang)

        return self.indexHtmlTemplate.render(language=self.language,tab=activeTab)


    index.exposed = True


    def change_language(self, new_lang):
        #Load specific dict
        #Load default dict
        if self.lang!=new_lang:
            self.setCookieLang(new_lang)
            fp=open('lang/en.txt','r')
            self.language=json.load(fp,'utf-8')
            fp.close()
            try:
                fp=open('lang/'+new_lang+'.txt','r')
#            self.language.update(json.load(fp))
                self.language.update(json.load(fp))
                fp.close()
                self.lang = new_lang
            except IOError:
                print "Language error"
        cherrypy.root.checkers.set_language(self.language)
        cherrypy.root.training.set_language(self.language)
        cherrypy.root.settings.set_language(self.language)
        cherrypy.root.teleoperation.set_language(self.language)
        cherrypy.root.confWizard.set_language(self.language)
        cherrypy.root.voiceRecognition.set_language(self.language)
        cherrypy.root.xmms2.set_language(self.language)
        #Reload the checkers dictionary
#        return "HOLA"+new_lang


cherrypy.root = Root()
cherrypy.root.checkers = sysChecksManager(cherrypy.root.language)
cherrypy.root.training = FaceObjectTrainer(cherrypy.root.language)
cherrypy.root.settings = SettingsManager(cherrypy.root.language)
cherrypy.root.teleoperation = TeleoperationManager(cherrypy.root.language)
cherrypy.root.confWizard = ConfWizardManager(cherrypy.root.language)
cherrypy.root.voiceRecognition = VoiceRecognitionManager(cherrypy.root.language)
cherrypy.root.xmms2 = XMMS2Manager(cherrypy.root.language)
cherrypy.root.mjpegServer = MjpegServerFunctions() 
cherrypy.root.image = MjpegGrabber()

#Initialize ROS node associated with Q.bo Webi
rospy.init_node(name="qbo_webi", argv=sys.argv)



#Get ROS parameter of the server Port
server_port = rospy.get_param("server_port", 7070)

conf = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': server_port,
    },

    '/img': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/static/img'},

        '/js': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/static/js'},

        '/css': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/static/css'},

        '/training/static/img': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/training/static/img'},

        '/training/static/js': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/training/static/js'},

        '/training/static/css': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/training/static/css'},

        '/settings/static/img': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/settings/static/img'},

        '/settings/static/js': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/settings/static/js'},

        '/settings/static/css': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/settings/static/css'},

        '/confWizard/static/img': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/confWizard/static/img'},

        '/confWizard/static/js': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/confWizard/static/js'},

        '/confWizard/static/css': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/confWizard/static/css'},

        '/teleoperation/static/img': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/teleoperation/static/img'},

        '/teleoperation/static/js': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/teleoperation/static/js'},

        '/teleoperation/static/css': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/teleoperation/static/css'},



        '/sysChecks/static/img': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/sysChecks/static/img'},

        '/sysChecks/static/js': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/sysChecks/static/js'},

        '/sysChecks/static/css': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/sysChecks/static/css'},

        '/sysChecks/static/wav': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/sysChecks/static/wav'},

        '/xmms2/static/img': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/xmms2/static/img'},
        
        '/xmms2/static/css': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/xmms2/static/css'},
        '/xmms2/songs': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/xmms2/songs'},





}

def roskill_handler():
    print "qbo_webi ROS node is shuting down"
    rospy.signal_shutdown("ROS Node kill was sent by exterior process")
    cherrypy.engine.exit()
    #sys.exit(0)


rospy.on_shutdown(roskill_handler)
cherrypy.quickstart(cherrypy.root, '/', conf)

