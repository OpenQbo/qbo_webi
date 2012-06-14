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
from qbo_face_msgs.srv  import LearnFaces
from qbo_face_msgs.srv  import Train
import unicodedata
from  otherFunctionalities.mjpegServerFuntions.MjpegServerFunctions  import MjpegServerFunctions


class FaceObjectTrainer(TabClass):


    def __init__(self,language):
        self.language = language
        #self.mjpegServer = MjpegServerFunctions()
        self.htmlTemplate = Template(filename='training/templates/trainingTemplate.html')
        self.jsTemplate = Template(filename='training/templates/trainingTemplate.js')
        self.variablesTemplate = Template(filename='static/js/generalVariables.js')
        self.exposed = True
    	self.faceON = False

    @cherrypy.expose
    def unload(self):
        #self.mjpegServer.stop("8081")
        return "ok"

    @cherrypy.expose
    def index(self):
        #self.mjpegServer.start("8081")
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


    @cherrypy.expose
    def selectObjectRecognition(self):
        self.faceON = False


    @cherrypy.expose
    def launchNodes(self):
        if self.faceON:
            #call face traningi bellow
            rospy.loginfo("Launching Face Recognition Node")
            self.launchFaceNode()
        else:
	        self.launchObjectNode()


    @cherrypy.expose
    def stopNode(self):
        if self.faceON:
            #call face training bellow
            self.stopFaceNode()
        else:
            self.stopObjectNode()


    @cherrypy.expose
    def startLearning(self,objectName):
        if self.faceON:
            rospy.loginfo("Called face learning service with name:"+objectName)
            return self.learnFace(objectName)
        else:
            rospy.loginfo("VAMOS A APRENDER UN OBJETO")
            rospy.loginfo("en concreto un "+objectName)
            return self.learnObject(objectName)

    @cherrypy.expose
    def startTraining(self):
	    if self.faceON:
		    #call face traningi bellow
		    rospy.loginfo("Starting Face Training")
		    return self.trainingFaces()
	    else:
		    return self.trainingObjects()


    @cherrypy.expose
    def startRecognition(self):
        if self.faceON:
            #call face recog bellow
	        rospy.loginfo("Starting Face Recognition")
	        return self.startRecognizeFace()
        else:
		    return self.startRecognizeObject()

############ Face Training and Recognition ######################################

    def launchFaceNode(self):
    	rospy.loginfo("Qbo Webi: Launching Face Recognizer nodes")
        cmd = "roslaunch qbo_webi qbo_face_recognition_training.launch"
        self.processFaceNode = subprocess.Popen(cmd.split())
        rospy.loginfo(" END Launching Face Recognizer nodes")


    def stopFaceNode(self):
        try:
            rospy.loginfo("Qbo Webi: Killing Face Recognizer nodes")
            self.processFaceNode.send_signal(signal.SIGINT)
        except Exception as e:
            rospy.loginfo("ERROR when trying to kill Face Recognizer Process"+e)

    def startRecognizeFace(self):
        rospy.loginfo("Qbo Webi: Started face recognizer mode. Waiting for service...")
        rospy.wait_for_service("/qbo_face_recognition/get_name")
        rospy.loginfo("Qbo Webi: Recognize Face service is ready!")
        recog = rospy.ServiceProxy('/qbo_face_recognition/get_name',GetName)
        response = recog()

        if (response.recognized):
            rospy.loginfo("Qbo Webi: Person recognized ->"+response.name)
            return response.name
        else:
            rospy.loginfo("Qbo Webi: Person seen is unkown!")
            return ""

    def learnFace(self,faceName):
        rospy.loginfo("Qbo Webi: Started face learning mode (Capturing person's images). Waiting for service...")
        rospy.wait_for_service("/qbo_face_recognition/learn_faces")
        rospy.loginfo("Qbo Webi: Service for face learning is ready")
        learn = rospy.ServiceProxy('/qbo_face_recognition/learn_faces',LearnFaces)
        rospy.loginfo("Qbo Webi: Person to learn ->"+faceName)
        asciiFaceName = unicodedata.normalize('NFKD', faceName).encode('ascii','ignore')
        resultLearn = learn(asciiFaceName)
        rospy.loginfo("Qbo Webi: Learning result->"+str(resultLearn.learned))
        return str(resultLearn)

    def trainingFaces(self):
        #entrenamos las imagenes capturadas
        rospy.loginfo("Qbo Webi: Starting face training")
        rospy.wait_for_service("/qbo_face_recognition/train")
        rospy.loginfo("Qbo Webi: Face Train service is available")
        training = rospy.ServiceProxy('/qbo_face_recognition/train',Train)
        resultTraining = training()
        rospy.loginfo("Qbo Webi: Response from Face Train Service -> "+str(resultTraining.taught))
        return str(resultTraining.taught)


############ Object Training and Recognition ########################

    def launchObjectNode(self):
    	rospy.loginfo("Qbo Webi: Launching Object Recognizer")
        cmd = "roslaunch qbo_webi qbo_object_recognition_training.launch"
        self.processObjectNode = subprocess.Popen(cmd.split())


    def stopObjectNode(self):
        try:
            rospy.loginfo("Qbo Webi: Killing Object Recognizer nodes")
            self.processObjectNode.send_signal(signal.SIGINT)
        except Exception as e:
                rospy.loginfo("ERROR when trying to kill Object Recognizer Process"+e)


    def startRecognizeObject(self):
        rospy.loginfo("Qbo Webi: Started object recognizer mode. Waiting for service...")
        rospy.wait_for_service("/qbo_object_recognition/recognize_with_stabilizer")
        rospy.loginfo("Qbo Webi: Recognize service is ready!")
        recog = rospy.ServiceProxy('/qbo_object_recognition/recognize_with_stabilizer',RecognizeObject)
        respuesta = recog()

        if (respuesta.recognized):
            rospy.loginfo("Qbo Webi: Object recognized ->"+respuesta.object_name)
            return respuesta.object_name
        else:
            rospy.loginfo("Qbo Webi: Object seen is unkown!")
            return ""


    def learnObject(self,objectName):
        rospy.loginfo("Qbo Webi: Started object learning mode (Capturing object's images). Waiting for service...")
        rospy.wait_for_service("/qbo_object_recognition/learn")
        rospy.loginfo("Qbo Webi: Service for object learning is ready")
        learn = rospy.ServiceProxy('/qbo_object_recognition/learn',LearnNewObject)
        rospy.loginfo("Qbo Webi: Object to learn ->"+objectName)


        if type(objectName) is unicode:
            asciiObjectName = unicodedata.normalize('NFKD', objectName).encode('ascii','ignore')
            resultLearn = learn(asciiObjectName)
        else:
            resultLearn = learn(objectName)


        rospy.loginfo("Qbo Webi: Learning result->"+str(resultLearn.learned))
        return str(resultLearn)

    def trainingObjects(self):
        #entrenamos las imagenes capturadas
        rospy.loginfo("Qbo Webi: Starting object teaching")
        rospy.wait_for_service("/qbo_object_recognition/teach")
        rospy.loginfo("Qbo Webi: Object teach service is available")
        training = rospy.ServiceProxy('/qbo_object_recognition/teach',Teach)
        resultTraining = training()
        rospy.loginfo("Qbo Webi: Response from Object Teach Service -> "+str(resultTraining.taught))
        return "True"

