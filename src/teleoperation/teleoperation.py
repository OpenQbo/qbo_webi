import cherrypy
from mako.template import Template
from tabsClass import TabClass
import roslib; roslib.load_manifest('qbo_webi')
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
import math
from  otherFunctionalities.mjpegServerFuntions.MjpegServerFunctions  import MjpegServerFunctions

class TeleoperationManager(TabClass):
    def __init__(self,language):
        self.camera="left"
        self.language = language
        self.htmlTemplate = Template(filename='teleoperation/templates/teleoperationTemplate.html')
        self.jsTemplate = Template(filename='teleoperation/templates/teleoperationTemplate.js')
        self.variablesTemplate = Template(filename='static/js/generalVariables.js')
        self.cmd_vel_pub=rospy.Publisher('/cmd_vel', Twist)
        self.cmd_joints_pub=rospy.Publisher('/cmd_joints', JointState)
        self.mjpegServer = MjpegServerFunctions()

    @cherrypy.expose
    def unload(self):
        self.mjpegServer.stop("8081")
        return "ok"
        
    @cherrypy.expose
    def index(self):
        self.mjpegServer.start("8081")
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

        yaw=float(yaw)
        pitch=float(pitch)

        print "-----------------__"+str(yaw)

        maxLimit = 500

        if yaw>maxLimit:
		    yaw=maxLimit
        if pitch>maxLimit: 
		    pitch=maxLimit
        if yaw<maxLimit*-1: 
		    yaw=-maxLimit
        if pitch<maxLimit*-1: 
	    	pitch=-maxLimit
    
        radYaw = (yaw*(math.pi/2))/maxLimit
        radPitch = (pitch*(math.pi/2))/maxLimit 


        self.sendHeadPose(float(radYaw),float(radPitch))



    def sendSpeed(self,line,angu):
        speed_command=Twist()
        speed_command.linear.x=line
        speed_command.linear.y=0
        speed_command.linear.z=0
        speed_command.angular.x=0
        speed_command.angular.y=0
        speed_command.angular.z=angu
        self.cmd_vel_pub.publish(speed_command)

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


