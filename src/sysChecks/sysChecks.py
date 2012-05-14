import cherrypy
from mako.template import Template
import json
import os
import glob

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

class sysChecksManager:
    def __init__(self,lang):
        self.lang=lang
        self.htmlTemplate = Template(filename='sysChecks/templates/sysChecksTemplate.html')

        #creo la lista de chekers
        self.availableChekers={}
        checkersDirs=next(os.walk('sysChecks/chekers'))[1]
        if 'templates' in checkersDirs:
            checkersDirs.remove('templates')
        for i in range(len(checkersDirs)):
            checkersDirs[i]='sysChecks/chekers/'+checkersDirs[i]
        filesToImport=[]
        for direc in checkersDirs:
            fileToImport=glob.glob(direc+'/[a-zA-Z]*.py')
            module = my_import(fileToImport[0][:-3].replace('/','.'))
            meth = fileToImport[0][:-3].split('/')[-1]
            code=getattr(module,meth)
            self.availableChekers[meth]=code(self.lang)

        #Actualizo los lenguajes
        self.language={}
        for checkerKey in self.availableChekers.keys():
          self.language.update(self.availableChekers[checkerKey].language)

    def index(self, *cheker):
        if not cheker:
            return self.htmlTemplate.render(language=self.language, availableChekers=self.availableChekers)
        cheker=cheker[0]
        if cheker in self.availableChekers.keys():
            returnDataDic={}
            returnDataDic['htmlElement']=self.availableChekers[cheker].get_html()
            js=self.availableChekers[cheker].get_js()
            css=self.availableChekers[cheker].get_css()
            if js:
                returnDataDic['jsElement']=js
            if css:
                returnDataDic['cssElement']=css
            return json.dumps(returnDataDic)
        else:
            json.dumps(False)

    index.exposed=True
