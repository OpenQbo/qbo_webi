# coding: utf-8
import cherrypy
from mako.template import Template
from tabsClass import TabClass
import roslib; roslib.load_manifest('qbo_webi')
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
from qbo_talk.srv import Text2Speach
#from qbo_pymouth import mouth
from qbo_arduqbo.msg import Mouth as Mouth_msg
import math
from  otherFunctionalities.mjpegServerFuntions.MjpegServerFunctions  import MjpegServerFunctions
from  otherFunctionalities.runCmd.RunCmd  import RunCmd 

from mako.lookup import TemplateLookup

import subprocess
from subprocess import Popen, PIPE, STDOUT
from random import *
import string
import json
import time

class Mouth:

    def __init__(self,idN,name,b1,b2,b3):
        self.idN=int(idN)
        self.name=str(name)
        self.b1=int(b1)
        self.b2=int(b2)
        self.b3=int(b3)

class TeleoperationManager(TabClass):
    def __init__(self,language):
	self.path2webi = roslib.packages.get_pkg_dir("qbo_webi")
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
        #self.qbo_mouth_control=mouth()
        self.mouth_pub=rospy.Publisher('/cmd_mouth', Mouth_msg)
        self.vMouths=[]
        self.vMouths.append(Mouth(0,"Happy",0,136,14));
        self.vMouths.append(Mouth(1,"Sad",0,112,17));
        self.vMouths.append(Mouth(2,"Ooh",92,140,14));
        self.vMouths.append(Mouth(3,"Pucker the mouth to the right",192,15,0));
        self.vMouths.append(Mouth(4,"Pucker the mouth to the left",192,135,0));
        self.vMouths.append(Mouth(5,"Straight face",0,248,0));
        self.vMouths.append(Mouth(6,"Small mouth",136,82,4));
        self.vMouths.append(Mouth(7,"Speak 1",62,0,0));
        self.vMouths.append(Mouth(8,"Speak 2",190,3,0));
        self.vMouths.append(Mouth(9,"Speak 3",126,116,0));
        self.vMouths.append(Mouth(10,"Speak 4",254,119,0));
        self.vMouths.append(Mouth(11,"Speak 5",126,140,14));
        self.vMouths.append(Mouth(12,"Speak 6",254,255,14));
        self.vMouths.append(Mouth(13,"None",0,0,0));
        self.vMouths.append(Mouth(14,"surprise",92,140,14));
        self.vMouths.append(Mouth(15,"regular",130,32,8));
        self.vMouths.append(Mouth(16,"tongue",192,47,2));

        self.changeLang = rospy.ServiceProxy("/qbo_talk/festival_language", Text2Speach)

        self.voice_SP = "JuntaDeAndalucia_es_sf_diphone"
        self.voice_EN = "cmu_us_awb_arctic_clunits"

	self.command = RunCmd()

	self.chars = string.ascii_letters + string.digits

    def setMouth(self,mo):
        boca=Mouth_msg()
        boca.mouthImage=[]
        boca.mouthImage.append(mo.b1)
        boca.mouthImage.append(mo.b2)
        boca.mouthImage.append(mo.b3)
        boca.mouthColor = 0
        self.mouth_pub.publish(boca)

    @cherrypy.expose
    def unload(self):
        #self.mjpegServer.stop("8081")
        self.changeLang(self.voice_EN)


	print self.command.killProcess(self.processLinphone)
	print self.command.killProcess(self.processSipd)
        print self.command.killProcess(self.processSiprtmp)

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

	#Start SIP & RTMP services
	#out = command.runCmd("python "+self.path2webi+"/src/teleoperation/sip2rtmp/rtmplite/siprtmp.py")
	#print out[0]





	client=cherrypy.request.remote.ip
        if (client=="127.0.0.1" or client=="localhost" or cherrypy.request.headers['Host'].find(client)!=-1):
                islocal=True
        else:
                islocal=False

        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX = "+client

	print str(cherrypy.request.headers.get("Referer","/"))

	host = cherrypy.request.headers.get("Referer","/")

	host = host.replace("/","")

	parts = host.split(":")

	self.host = parts[1]

	print "HOSSSSSSSTTTTTTTTT "+host

	rospy.set_param("linphone_host",host)

	self.command.addToPythonPath("/opt/ros/electric/stacks/qbo_stack/qbo_webi/src/teleoperation/sip2rtmp/p2p-sip:/opt/ros/electric/stacks/qbo_stack/qbo_webi/src/teleoperation/sip2rtmp/p2p-sip/src:/opt/ros/electric/stacks/qbo_stack/qbo_webi/src/teleoperation/sip2rtmp/p2p-sip/src/app:/opt/ros/electric/stacks/qbo_stack/qbo_webi/src/teleoperation/sip2rtmp/p2p-sip/src/external:/opt/ros/electric/stacks/qbo_stack/qbo_webi/src/teleoperation/sip2rtmp/rtmplite:");


        #self.mjpegServer.start("8081")
        return self.htmlTemplate.render(language=self.language)	

    @cherrypy.expose
    def getAuth(self):
        return json.dumps({"host": self.host, "auth": self.auth})

    @cherrypy.expose
    def getAuthBot(self):
	#this is called right before making the call to the bot. We delay the answer, in order to make
        #sure everything is settle down.ç
	time.sleep(1)
	return json.dumps({"host": self.host, "auth": self.authBot})


    @cherrypy.expose
    def startSIPService(self):

	self.auth = "notDefined"
	self.authBot = "notDefined"
        
	auth = "".join(choice(self.chars) for x in range(randint(4, 4)))
        authBot = "".join(choice(self.chars) for x in range(randint(4, 4)))

	#launch sipd.py
        cmd = "python "+self.path2webi+"/src/teleoperation/sip2rtmp/p2p-sip/src/app/sipd.py -u "+auth+" -b "+authBot
        print "Usuario= "+ auth +"     BOT= "+authBot
        self.processSipd = self.command.runCmdWithPidBack(cmd)

	#launch siprtmp.py
        cmd = "python "+self.path2webi+"/src/teleoperation/sip2rtmp/rtmplite/siprtmp.py"
        self.processSiprtmp = self.command.runCmdWithPidBack(cmd)

	#we give them sometime to finish the job
	time.sleep(0.5)

	self.auth = auth
	self.authBot =authBot

	#launch bot client linphone
        rospy.set_param("linphone_botName",authBot)
	rospy.set_param("linphone_host","localhost")
        cmd = "roslaunch qbo_linphone launch_on_robot.launch"
        self.processLinphone = self.command.runCmdWithPidBack(cmd)




    @cherrypy.expose
    def stopSIPService(self):
	self.auth = "notDefined"
        self.authBot = "notDefined"

        print self.command.killProcess(self.processLinphone)
        print self.command.killProcess(self.processSipd)
        print self.command.killProcess(self.processSiprtmp)

    @cherrypy.expose
    def teleoperationJs(self, parameters=None):
        return self.jsTemplate.render(language=self.language)

    @cherrypy.expose
    def teleoperationVariables(self, parameters=None):
        return self.variablesTemplate.render(language=self.language)

    @cherrypy.expose
    def move(self,line,angu):
        print 'line: ',line,' angu: ',angu
        #line='0.0'
        #angu='0.0'
        self.sendSpeed(float(line),float(angu))

    @cherrypy.expose
    def head(self,yaw,pitch):
        print 'yaw: ',yaw,' pitch: ',pitch
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
    def changeMouth(self,mouth):
        #self.mouth.changeMouth(mouth)
        if int(mouth) > len(self.vMouths):
            return "KO"
        for mo in self.vMouths:
            if mo.idN == int(mouth):
                self.setMouth(mo)
                return "OK"
        return "KO"


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

