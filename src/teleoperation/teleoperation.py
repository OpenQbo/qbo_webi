import cherrypy
from mako.template import Template
from tabsClass import TabClass
import roslib; roslib.load_manifest('qbo_webi')
import rospy
from geometry_msgs.msg import Twist

class TeleoperationManager(TabClass):

    def __init__(self,language):
          self.language = language
          self.htmlTemplate = Template(filename='teleoperation/templates/teleoperationTemplate.html')
	  self.jsTemplate = Template(filename='teleoperation/templates/teleoperationTemplate.js')
          self.variablesTemplate = Template(filename='static/js/generalVariables.js')
          self.cmd_vel_pub=rospy.Publisher('/cmd_vel', Twist)

    @cherrypy.expose
    def index(self):
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



    def sendSpeed(self,line,angu):
        speed_command=Twist()
        speed_command.linear.x=line
        speed_command.linear.y=0
        speed_command.linear.z=0
        speed_command.angular.x=0
        speed_command.angular.y=0
        speed_command.angular.z=angu
        self.cmd_vel_pub.publish(speed_command)



