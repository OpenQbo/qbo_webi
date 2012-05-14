import cherrypy
from mako.template import Template
from sysChecks.chekers.chekers import chekers

class globalCheck(chekers):

    def __init__(self,lang):
        chekers.__init__(self,'globalCheck',lang)

        #Codigo ROS

        self.htmlTmpl = Template(filename='sysChecks/chekers/'+self.name+'/templates/globalCheckTemplate.html')


