# coding: utf-8
import cherrypy
import os
import gen_grammar
from mako.template import Template
from tabsClass import TabClass

import roslib
roslib.load_manifest('qbo_webi');

import rospy


class VoiceRecognitionManager(TabClass):
    def __init__(self,language):
        self.language = language
        self.juliusPath=roslib.packages.get_pkg_dir("qbo_listen")
        self.htmlTemplate = Template(filename='voiceRecognition/templates/voiceRecognitionTemplate.html')
        self.jsTemplate = Template(filename='voiceRecognition/templates/voiceRecognitionTemplate.js')
        self.tmpdir="/tmp/"
        self.LMPaths="/config/LM/"
        self.AMPaths="/config/AM/"
        self.LMFileName="/sentences.conf"
        self.PhonemsFileName="/phonems"
        self.TiedlistFileName="/tiedlist"
        self.languages_names={'en':'English','es':'Español','pt':'Português','de':'Deutsch','fr':'Français','it':'Italiano'}


    @cherrypy.expose
    def voiceRecognitionJs(self, parameters=None):
        return self.jsTemplate.render(language=self.language)


    def getLanguages(self):
        try:
            dirList=os.listdir(self.juliusPath+self.LMPaths)
            dirList.sort()
        except:
            dirList=-1
        return dirList    


    def isQboListenInstalled(self):
        if self.getLanguages()==-1:
            return False
        else:
            return True

    def getLanguageModels(self,language):
        try:
            dirList=os.listdir(self.juliusPath+self.LMPaths+language)
            dirList.sort()
        except:
            dirList=-1
        return dirList

    def getLMSentences(self,language,model):
        try:
            #print self.juliusPath+self.LMPaths+language+"/"+model+self.LMFileName
            f = open(self.juliusPath+self.LMPaths+language+"/"+model+self.LMFileName,'r')
            return f.read()
        except:
            sentences=""
        return sentences

    @cherrypy.expose
    def getModels(self,lang):
        modelList=""
        try:
            dirList=os.listdir(self.juliusPath+self.LMPaths+lang)
            dirList.sort()
            for model in dirList:
                modelList=modelList+model+"::"
            modelList=modelList[:-2]
        except:
            modelList=-1
        return modelList

    @cherrypy.expose
    def test1(self,lang,text):
        f = open(self.tmpdir+'LModel', 'w')
        f.write(text)
        f.close()
        words=gen_grammar.verrors(self.tmpdir+'LModel',self.juliusPath+self.AMPaths+lang+"/"+self.PhonemsFileName)
        if words==0:
             return ""
        else:
            wordsList=""
            for word in words:
                wordsList=wordsList+word+"::"
            wordsList=wordsList[:-2]
            return wordsList

    @cherrypy.expose
    def test2(self,lang,text):
        errorlist=""
        print text
        wordlist=text.split()
        print wordlist
        for word in wordlist:
            if word[0]!="[" and word[0]!="<":
                print word
                f = open(self.tmpdir+'word', 'w')
                f.write("[sentence]\n")
                f.write(word)
                f.close()
                gen_grammar.createvoca(self.tmpdir+'word', self.juliusPath+self.AMPaths+lang+"/"+self.PhonemsFileName, self.tmpdir+'word')
                print self.tmpdir+'word'
                print self.juliusPath+self.AMPaths+lang+"/"+self.TiedlistFileName
                if gen_grammar.perrors(self.tmpdir+'word.voca',self.juliusPath+self.AMPaths+lang+"/"+self.TiedlistFileName)!=0:
                    errorlist=errorlist+word+"::"
        errorlist=errorlist[:-2]
        return errorlist
    
    @cherrypy.expose
    def saveToFile(self,lang,text,model):
        try:
            #print self.juliusPath+self.LMPaths+language+"/"+model+self.LMFileName
            f = open(self.juliusPath+self.LMPaths+lang+"/"+model+self.LMFileName,'w')
            f.write(text)
            f.close()
            gen_grammar.compilegrammar(model,lang)
        except:
            return "ERROR: Cant write the file"
        return ""

    @cherrypy.expose
    def getFile(self,lang="",model=""):
        if lang=="" or model=="":
            return "ERROR: lang:"+lang+"; model:"+model
        else:
            #print self.getLMSentences(lang,model)
            return self.getLMSentences(lang,model)


    @cherrypy.expose
    def index(self):
        tmp=""
        if self.isQboListenInstalled():
            for lang in self.getLanguages():
                for LM in self.getLanguageModels(lang):
                    text= self.getLMSentences(lang,LM)
                    break
                break

            return self.htmlTemplate.render(language=self.language,lannames=self.languages_names,alllanguage=self.getLanguages())
        else:
            return "Qbo listen not installed"
#        return self.htmlTemplate.render(language=self.language)
