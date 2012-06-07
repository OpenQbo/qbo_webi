import cherrypy
from mako.template import Template
import json

class chekers:

    def __init__(self,name,lang):
        self.name=name
        self.load_language(lang)

        self.result='waiting'

        self.htmlTmpl = None
        self.jsTmpl = None
        self.cssTmpl = None

    def load_language(self,lang):
        self.lang=lang
        fp=open('sysChecks/chekers/'+self.name+'/lang/en.txt','r')
        self.language=json.load(fp)
        fp.close()
        #Load specific dict
        if self.lang!='en':
            try:
                fp=open('sysChecks/chekers/'+self.name+'/lang/'+self.lang+'.txt','r')
                self.language.update(json.load(fp))
                fp.close()
            except IOError:
                print "ERROR:cant read:"+'sysChecks/chekers/'+self.name+'/lang/'+self.lang+'.txt'
            except ValueError:
                print "ERROR:Bad format of this file:"+'sysChecks/chekers/'+self.name+'/lang/'+self.lang+'.txt'
                

    def get_html_content(self):
        return self.htmlTmpl.render(language=self.language)

    def get_html(self,cheker):
        print 'checker data: ',cheker,' len: ',len(cheker)
        if not cheker or len(cheker)==0:
            return self.get_html_content()
        else:
            methodToCall = getattr(self, cheker[0])
            return methodToCall(cheker[1:])

    def get_js(self):
        if not self.jsTmpl:
            return None
        else:
            return self.jsTmpl.render(language=self.language)

    def get_css(self):
        if not self.cssTmpl:
            return None
        else:
            return self.cssTmpl.render(language=self.language)


