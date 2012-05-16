import cherrypy
from mako.template import Template
import json
from sysChecks.sysChecks import sysChecksManager
import os
#incluir dependencias de ROS

pathh = '/'.join(os.path.abspath( __file__ ).split('/')[:-1])
os.chdir(pathh)

print pathh





class Root:
    def __init__(self):
        self.indexHtmlTemplate = Template(filename='templates/indexTemplate.html')
        self.confWizardHtmlTemplate = Template(filename='templates/confWizzardTemplate.html')
        self.teleoperationHtmlTemplate = Template(filename='templates/teleoperationTemplate.html')
        self.settingsHtmlTemplate = Template(filename='templates/settingsTemplate.html')
        self.trainingHtmlTemplate = Template(filename='templates/trainingTemplate.html')



        self.lang='en'
        #Load default dict
        fp=open('lang/en.txt','r')
        self.language=json.load(fp)
        fp.close()

        #Load specific dict
        if self.lang!='en':
            fp=open('lang/'+self.lang+'.txt','r')
            self.language.update(json.load(fp))
            fp.close()

    def index(self):
        return self.indexHtmlTemplate.render(language=self.language)
    index.exposed = True

    def localclient(self):
        client=cherrypy.request.remote.ip
        if (client=="127.0.0.1" or client=="localhost" or cherrypy.request.headers['Host'].find(client)!=-1):
                islocal=True
        else:
                islocal=False
	return islocal;

    def confWizzard(self):
        return self.confWizardHtmlTemplate.render(language=self.language, var1="testing", localClient=self.localclient())
    confWizzard.exposed = True

    def teleoperation(self):
        return self.teleoperationHtmlTemplate.render(language=self.language)
    teleoperation.exposed = True

    def settings(self):
        return self.settingsHtmlTemplate.render(language=self.language)
    settings.exposed = True

    def training(self):
        return self.trainingHtmlTemplate.render(language=self.language)
    training.exposed = True




cherrypy.root = Root()
cherrypy.root.checkers = sysChecksManager(cherrypy.root.lang)

conf = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 7070,
    },

	'/img': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/static/img'},

        '/js': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/static/js'},

        '/css': {'tools.staticdir.on': True,
        'tools.staticdir.dir': pathh+'/static/css'},



}

cherrypy.quickstart(cherrypy.root, '/', conf)
