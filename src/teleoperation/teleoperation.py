# coding: utf-8
import cherrypy
from mako.template import Template
from tabsClass import TabClass
import roslib; roslib.load_manifest('qbo_webi')
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
from qbo_talk.srv import Text2Speach
import math
from  otherFunctionalities.mjpegServerFuntions.MjpegServerFunctions  import MjpegServerFunctions

from mako.lookup import TemplateLookup


class TeleoperationManager(TabClass):
    def __init__(self,language):
        self.camera="left"
        self.language = language
        self.templatelookup = TemplateLookup(directories=['./'])
        self.htmlTemplate = Template(filename='teleoperation/templates/teleoperationTemplate.html',lookup=self.templatelookup)
        self.jsTemplate = Template(filename='teleoperation/templates/teleoperationTemplate.js')
        self.variablesTemplate = Template(filename='static/js/generalVariables.js')
        self.cmd_vel_pub=rospy.Publisher('/cmd_vel', Twist)
        self.cmd_joints_pub=rospy.Publisher('/cmd_joints', JointState)
        self.client_speak = rospy.ServiceProxy("/qbo_talk/festival_say", Text2Speach)
        self.mjpegServer = MjpegServerFunctions()
        self.image_size=[640,480]
        self.head_velocity_factor = 2.0
        self.head_move_type = 1

        self.changeLang = rospy.ServiceProxy("/qbo_talk/festival_language", Text2Speach)

        self.voice_SP = "JuntaDeAndalucia_es_sf_diphone"
        self.voice_EN = "cmu_us_awb_arctic_clunits"


    @cherrypy.expose
    def unload(self):
        #self.mjpegServer.stop("8081")
        self.changeLang(voice_EN)
        return "ok"
        
    @cherrypy.expose
    def index(self):


        #Set Festival language
        self.lang = self.language["current_language"]
        if self.lang=="es":
            #Festival
            self.changeLang(self.voice_SP)
        else:
            #Festival
            self.changeLang(self.voice_EN)



        #self.mjpegServer.start("8081")
        return self.htmlTemplate.render(language=self.language)	

    @cherrypy.expose
    def teleoperationJs(self, parameters=None):
        return self.jsTemplate.render(language=self.language)

    @cherrypy.expose
    def teleoperationVariables(self, parameters=None):
        return self.variablesTemplate.render(language=self.language)

    @cherrypy.expose
    def move(self,line,angu):
        self.sendSpeed(float(line),float(angu))

    @cherrypy.expose
    def head(self,yaw,pitch):
        if self.head_move_type==1:
            self.headMoveType1(yaw, pitch)
        else:  
            self.headMoveType2(yaw, pitch)
  
    @cherrypy.expose
    def changeHeadMoveType(self,head_move_type):
        
        print "--------->Change head movement: ",head_move_type
        
        head_move_type = int(head_move_type)
    
        if head_move_type!=1 and head_move_type!=2:
            return

        print "----------> Change head movement accepted"
        self.head_move_type = head_move_type


    @cherrypy.expose
    def changeVideoSize(self,width, height):
        self.image_size=[float(width),float(height)]
        print "New Image size:"
        print self.image_size


    @cherrypy.expose
    def head_to_zero_position(self):
        print "Sending head to zero position"
        msg = JointState()
        msg.name = list()
        msg.position = list()
        msg.velocity = list()
        msg.effort = list()
        msg.name.append('head_pan_joint')  
        msg.position.append(0)   
        msg.velocity.append(1.0)
        msg.name.append('head_tilt_joint')
        msg.position.append(0)    
        msg.velocity.append(1.0)
        msg.header.stamp = rospy.Time.now()
        self.cmd_joints_pub.publish(msg)
       
    @cherrypy.expose
    def speak(self, message):
        message_encoded=message.encode('utf8')
        print "Message to speak: "+str(message_encoded)
        self.client_speak(message_encoded)
        return "true"


    def sendSpeed(self,line,angu):
        speed_command=Twist()
        speed_command.linear.x=line
        speed_command.linear.y=0
        speed_command.linear.z=0
        speed_command.angular.x=0
        speed_command.angular.y=0
        speed_command.angular.z=angu
        self.cmd_vel_pub.publish(speed_command)

    '''
        1st approach of head movement
    '''
    def headMoveType1(self,yaw,pitch):

        yaw=float(yaw)
        pitch=float(pitch)

        maxLimitYaw = self.image_size[0]
        maxLimitPitch = self.image_size[1]

        if yaw>maxLimitYaw:
		    yaw=maxLimitYaw
        if pitch>maxLimitPitch: 
		    pitch=maxLimitPitch
        if yaw<maxLimitYaw*-1: 
		    yaw=-maxLimitYaw
        if pitch<maxLimitPitch*-1: 
	    	pitch=-maxLimitPitch
    
        radYaw = (yaw*(math.pi/2))/maxLimitYaw
        radPitch = (pitch*(math.pi/2))/maxLimitPitch
        self.sendHeadPose(float(radYaw),float(radPitch))

    '''
        2st approach of head movement
    '''
    def headMoveType2(self,yaw,pitch):
        pan_pos=float(yaw)
        tilt_pos=float(pitch)

        pan_ratio = pan_pos/(self.image_size[0]/2.0)
        tilt_ratio = tilt_pos/(self.image_size[1]/2.0)

        pan_ratio = min(1,pan_ratio)
        pan_ratio = max(-1,pan_ratio)
        tilt_ratio = min(1,tilt_ratio)
        tilt_ratio = max(-1,tilt_ratio)

        print "Pan_pos:",pan_ratio,"| Tilt_ratio:",tilt_ratio
                  
        msg = JointState()
        msg.name = list()
        msg.position = list()
        msg.velocity = list()
        msg.effort = list()

        msg.name.append('head_pan_joint')        
        if pan_ratio>0:      
            msg.position.append(2)
        else:
            msg.position.append(-2)
        
        if abs(pan_ratio)<0.2:
            pan_ratio = 0.0
        elif pan_ratio>0.2:
            pan_ratio-=0.2
        elif pan_ratio < -0.2:
            pan_ratio+=0.2        

        msg.velocity.append(abs(pan_ratio)*self.head_velocity_factor)

        msg.name.append('head_tilt_joint')
        
        if tilt_ratio>0:      
            msg.position.append(2)
        else:
            msg.position.append(-2)    

        if abs(tilt_ratio)<0.2:
            tilt_ratio = 0.0
        elif tilt_ratio>0.2:
            tilt_ratio-=0.2
        elif tilt_ratio < -0.2:
            tilt_ratio+=0.2

        msg.velocity.append(abs(tilt_ratio)*self.head_velocity_factor)
        msg.header.stamp = rospy.Time.now()
        self.cmd_joints_pub.publish(msg)





    def sendHeadPose(self,yaw,pitch):
        msg = JointState()
        msg.name = list()
        msg.position = list()
        msg.velocity = list()
        msg.effort = list()

        msg.name.append('head_pan_joint')
        msg.position.append(float(yaw))
        msg.velocity.append(1.0)
        msg.name.append('head_tilt_joint')
        msg.position.append(float(pitch))
        msg.velocity.append(1.0)

        msg.header.stamp = rospy.Time.now()


        #print "mensaje en lib_qbo_pyarduqbo:    vamos a mover la cazbeza ",msg
        self.cmd_joints_pub.publish(msg)

