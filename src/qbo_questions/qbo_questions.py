import cherrypy
from mako.template import Template
from tabsClass import TabClass
import roslib; roslib.load_manifest('qbo_webi')
import rospy
import json
from qbo_talk.srv import Text2Speach

from mako.lookup import TemplateLookup


class Qbo_questionsManager(TabClass):
    def __init__(self,language):
        self.dialogue = {}
        self.dialogue_path = roslib.packages.get_pkg_dir("qbo_questions")
        self.language = language
        self.templatelookup = TemplateLookup(directories=['./'])
        self.htmlTemplate = Template(filename='qbo_questions/templates/qbo_questions.html',lookup=self.templatelookup)
        self.jsTemplate = Template(filename='qbo_questions/templates/qbo_questions.js')

    @cherrypy.expose
    def unload(self):
        return "ok"
        
    @cherrypy.expose
    def index(self):
        return self.htmlTemplate.render(language=self.language)	

    @cherrypy.expose
    def qbo_questionsJs(self,  **params):
        return self.jsTemplate.render(language=self.language)



    @cherrypy.expose
    def deleteSentence(self, sentence2delete):

        print "borrando ."+sentence2delete+"."


        aux = sentence2delete.split(":::")
        check1 = aux[0]
        check2 = aux[1]

        f = open(self.dialogue_path+'/config/dialogues')

        finalFileContent = ""
        alreayDeleted = False
        for line in f.readlines():


            aux_line = line.strip()            
            aux_line = aux_line.split(">>>")
            question =aux_line[0]
            answer =aux_line[1]

            print question.upper() +"=="+ check1.upper() +"and"+ answer +"=="+ check2.upper() +"and"+ str(not alreayDeleted)


            if question.upper() == check1.upper() and answer.upper() == check2.upper() and not alreayDeleted  :
                alreayDeleted = True
            else:
                finalFileContent = finalFileContent+line
        
        f.close()


        f = open(self.dialogue_path+'/config/dialogues','w')
        f.write(finalFileContent)
        f.close()
 
        return self.getActualDialogue()

    @cherrypy.expose
    def addSentence(self, question, answer):
        f = open(self.dialogue_path+'/config/dialogues',"a") 
        f.write(question +">>>"+answer+"\n")
        f.close()

        # we check wheter the input line alreayd exists, if so, we add to its own list
        if question in self.dialogue:
           self.dialogue[question].append(answer.upper())
           self.dialogue[question].sort()
        else:
            #self.dialogue_input does not exist
            self.dialogue[question.upper()] = [answer.upper()]

        return json.dumps(self.dialogue)

    @cherrypy.expose
    def getActualDialogue(self):
        self.dialogue = {}
        f = open(self.dialogue_path+'/config/dialogues')
        for line in f.readlines():
            try:
                line = line.replace("\n","")
                parts = line.split(">>>")

                dialogue_input = parts[0].upper()
                dialogue_output = parts[1].upper()


                # we check wheter the input line alreayd exists, if so, we add to its own list
                if dialogue_input in self.dialogue:
                    self.dialogue[dialogue_input].append(dialogue_output)
                    self.dialogue[dialogue_input].sort()
                else:
                    #self.dialogue_input does not exist
                    self.dialogue[dialogue_input] = [dialogue_output]
            except ValueError:
                print "Error when creating dialog at qbo_questions tab "
                pass

        print str(self.dialogue)
        return json.dumps(self.dialogue)

