import cherrypy
from mako.template import Template
import json

class chekers:

    def __init__(self,name,lang):
        self.name=name
        self.lang=lang

        #Load default dict
        fp=open('sysChecks/chekers/'+self.name+'/lang/en.txt','r')
        self.language=json.load(fp)
        fp.close()

        #Load specific dict
        if self.lang!='en':
            fp=open('sysChecks/chekers/'+self.name+'/lang/'+self.lang+'.txt','r')
            self.language.update(json.load(fp))
            fp.close()

        self.htmlTmpl = None
        self.jsTmpl = None
        self.cssTmpl = None

    def get_html(self):
        return self.htmlTmpl.render(language=self.language)

    def get_js(self):
        if not self.jsTmpl:
            return None
        else:
            return self.jsTmpl.render(language=self.language)

    def get_css(self):
        if not self.jsTmpl:
            return None
        else:
            return self.cssTmpl.render(language=self.language)


