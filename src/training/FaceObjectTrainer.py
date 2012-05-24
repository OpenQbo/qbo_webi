import cherrypy
from mako.template import Template
from tabsClass import TabClass
import rospy


import subprocess
from subprocess import Popen, PIPE, STDOUT
import signal

from std_msgs.msg import String
from sensor_msgs.msg  import Image
from qbo_talk.srv import Text2Speach
from qbo_object_recognition.srv import RecognizeObject
from qbo_object_recognition.srv import Teach
from qbo_object_recognition.srv import LearnNewObject
from qbo_face_msgs.srv  import GetName
import unicodedata





class FaceObjectTrainer(TabClass):


    def __init__(self,language):
          self.language = language
          self.htmlTemplate = Template(filename='training/templates/trainingTemplate.html')
          self.jsTemplate = Template(filename='training/templates/trainingTemplate.js')
          self.variablesTemplate = Template(filename='static/js/generalVariables.js')
	
	  self.exposed = True
    	  self.faceON = False
          self.objectON = True


    @cherrypy.expose
    def index(self):
        return self.htmlTemplate.render(language=self.language)

    @cherrypy.expose
    def trainingJs(self, parameters=None):
        return self.jsTemplate.render(language=self.language)

    @cherrypy.expose
    def trainingVariables(self, parameters=None):
        return self.variablesTemplate.render(language=self.language)

    @cherrypy.expose
    def selectFaceRecognition(self):
	self.faceON = True
	self.objectON = False

    @cherrypy.expose
    def selectObjectRecognition(self):
        self.faceON = False
        self.objectON = True


    @cherrypy.expose
    def launchNodes(self):
        if self.faceON:
                #call face traningi bellow
		rospy.loginfo("Launching Face Recognition Node")
        else:
		self.launchObjectNode()


    @cherrypy.expose
    def stopNode(self):
        if self.faceON:
                #call face traningi bellow
		pass
        else:
                self.stopObjectNode()


    @cherrypy.expose
    def startLearning(self,objectName):
        if self.faceON:
                return True
        else:
		rospy.loginfo("VAMOS A APRENDER UN OBJETO")
		rospy.loginfo("en concreto un "+objectName)
		return self.learnObject(objectName)


    @cherrypy.expose
    def startTraining(self):
	if self.faceON:
		#call face traningi bellow
		rospy.loginfo("Starting Face Learning")
		return True
	else:
		return self.trainingObjects()


    @cherrypy.expose
    def startRecognition(self):
        if self.faceON:
                #call face recog bellow
		rospy.loginfo("Starting Face Recognition")
		return True

        else:
		return self.startRecognizeObject()








############ Face Area ###################################################################################

############ Object Area #################################################################################

    def launchObjectNode(self):
    	rospy.loginfo(" Launching Object Recognizer")
        cmd = "roslaunch qbo_brainchat_pro object_recognition_web.launch"
        self.processObjectNode = subprocess.Popen(cmd.split())


    def stopObjectNode(self):
        try:
        	self.processObjectNode.send_signal(signal.SIGINT)
        except Exception as e:
                rospy.loginfo("ERROR when trying to kill Object Recognizer Process"+e)


    def startRecognizeObject(self):
        rospy.loginfo("____________vamos a reconocer objeto")
        rospy.wait_for_service("qbo_object_recognition/recognize_with_stabilizer")
        rospy.loginfo("____________es lservicio esta listo")
        recog = rospy.ServiceProxy('/qbo_object_recognition/recognize_with_stabilizer',RecognizeObject)
        respuesta = recog()

        if (respuesta.recognized):
                rospy.loginfo(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>"+respuesta.object_name)
                return respuesta.object_name
        else:
                rospy.loginfo("no reconocio NADA!")
                return ""


    def learnObject(self,objectName):
        rospy.loginfo("____________vamos a aprender objeto")
        rospy.wait_for_service("qbo_object_recognition/learn")
        rospy.loginfo("____________el servicio para aprender esta listo")
        learn = rospy.ServiceProxy('/qbo_object_recognition/learn',LearnNewObject)
        rospy.loginfo(objectName+"________________________")
        asciiObjectName = unicodedata.normalize('NFKD', objectName).encode('ascii','ignore')
        resultLearn = learn(asciiObjectName)
        rospy.loginfo("RESULTADO DE LEARN "+str(resultLearn))
        return str(resultLearn)

    def trainingObjects(self):
        #entrenamos las imagenes capturadas
        rospy.loginfo("_____________entrenamos lo visto")
        rospy.wait_for_service("qbo_object_recognition/teach")
        rospy.loginfo("_____________el servicio para entrenarse esta listo")
        training = rospy.ServiceProxy('/qbo_object_recognition/teach',Teach)
        resultTraining = training()
        rospy.loginfo("Biennnnnnnnnnn")
        rospy.loginfo("RESULTADO DE TEACH "+str(resultTraining))

        return "True"



