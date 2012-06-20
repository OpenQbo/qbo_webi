import cherrypy
from mako.template import Template
from tabsClass import TabClass
import rospy
import roslib
import subprocess
from subprocess import Popen, PIPE, STDOUT
import signal
import shlex

class ConfWizardManager(TabClass):

    def __init__(self,language):
          self.language = language
          self.htmlTemplate = Template(filename='confWizard/templates/confWizardTemplate.html')


    def localclient(self):
        client=cherrypy.request.remote.ip
        if (client=="127.0.0.1" or client=="localhost" or cherrypy.request.headers['Host'].find(client)!=-1):
                islocal=True
        else:
                islocal=False
        return islocal;

    @cherrypy.expose
    def index(self):
        return self.htmlTemplate.render(language=self.language, localclient=self.localclient())

    @cherrypy.expose
    def camera_calib(self):
        try:
            self.camera_calibration = subprocess.Popen(shlex.split('gnome-terminal -x bash -c "roslaunch qbo_camera qbo_cameras_stereo_calibration.launch"'))
        except:
            return "false"            
        return "true"	

    @cherrypy.expose
    def hand_gesture_calib(self):
        try:    
            self.hand_gesture_calibration = subprocess.Popen(shlex.split('gnome-terminal -x bash -c "roslaunch qbo_music_player hand_gesture_calib.launch"'))
        except:
            return "false"
        return "true"

    @cherrypy.expose
    def save_password(self,userName,oldPassword,newPassword1,newPassword2):


        print "_------------------------------------__"
        if newPassword1 != newPassword2:
            print "**"
            return "-2"
        print "WW"
        
        path = roslib.packages.get_pkg_dir("qbo_http_api_login")

        #we create a temporally dicctionary from users_pwd file
        usersAndPasswords = {}
        f = open(path+'/config/users_pwd')
        for line in f.readlines():
            parts = line.split(" ")
            usersAndPasswords[ parts[0] ] = parts[1].replace("\n","")

        f.close()

        print str(usersAndPasswords)

        #change/add password to user
        if userName in usersAndPasswords:
            if oldPassword == usersAndPasswords[userName]:        
                usersAndPasswords[userName] = newPassword1    
            else:
                return "-1"
        else:
            usersAndPasswords[userName] = newPassword1


        f = open(path+'/config/users_pwd','w')
        #from dict to file
        for name in usersAndPasswords:
            f.write(name+" "+usersAndPasswords[name]+"\n")




