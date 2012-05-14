import cherrypy
from mako.template import Template
from sysChecks.chekers.chekers import chekers

class cameraCheck(chekers):

    def __init__(self,lang):
        chekers.__init__(self,'cameraCheck',lang)
        self.htmlTmpl = Template(filename='sysChecks/chekers/'+self.name+'/templates/cameraCheckTemplate.html')


