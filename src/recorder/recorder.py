# coding: utf-8
import cherrypy
import os
import glob
from mako.template import Template
from tabsClass import TabClass
import rospy

class RecorderManager(TabClass):
    
    def __init__(self,language):
        self.language = language
        self.htmlTemplate = Template(filename='recorder/templates/recorderTemplate.html')


    @cherrypy.expose
    def index(self):
        return self.htmlTemplate.render(language=self.language)
