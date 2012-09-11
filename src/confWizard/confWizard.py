#!/usr/bin/env python
#
# Software License Agreement (GPLv2 License)
#
# Copyright (c) 2012 TheCorpora SL
#
# This program is free software; you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as 
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 
# MA 02110-1301, USA.
#
# Authors: Miguel Julian <miguel.julian@openqbo.com>; 


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
    def create_user(self,userName,newPassword1,newPassword2):
        if newPassword1 != newPassword2:
            return "-2"        

        path = roslib.packages.get_pkg_dir("qbo_http_api_login")

        #we create a temporally dicctionary from users_pwd file
        usersAndPasswords = {}
        f = open(path+'/config/users_pwd')
        for line in f.readlines():
            parts = line.split(" ")
            usersAndPasswords[ parts[0] ] = parts[1].replace("\n","")

        f.close()

        #add password to user
        if userName in usersAndPasswords:
                return "-1"
        else:
            usersAndPasswords[userName] = newPassword1


        f = open(path+'/config/users_pwd','w')
        #from dict to file
        for name in usersAndPasswords:
            f.write(name+" "+usersAndPasswords[name]+"\n")


    @cherrypy.expose
    def save_password(self,userName,oldPassword,newPassword1,newPassword2):
        if newPassword1 != newPassword2:
            return "-2"
        
        path = roslib.packages.get_pkg_dir("qbo_http_api_login")

        #we create a temporally dicctionary from users_pwd file
        usersAndPasswords = {}
        f = open(path+'/config/users_pwd')
        for line in f.readlines():
            parts = line.split(" ")
            usersAndPasswords[ parts[0] ] = parts[1].replace("\n","")

        f.close()

        #change/add password to user
        if userName in usersAndPasswords:
            print userName+" -------------- "+oldPassword+" --------"+  usersAndPasswords[userName]
            if oldPassword == usersAndPasswords[userName]:        
                usersAndPasswords[userName] = newPassword1    
            else:
                return "-1"
        else:
            return "-3"           


        f = open(path+'/config/users_pwd','w')
        #from dict to file
        for name in usersAndPasswords:
            f.write(name+" "+usersAndPasswords[name]+"\n")


    @cherrypy.expose
    def get_list_users(self):
        path = roslib.packages.get_pkg_dir("qbo_http_api_login")

        #we create a temporally dicctionary from users_pwd file
        users = ""
        f = open(path+'/config/users_pwd')
        for line in f.readlines():
            parts = line.split(" ")
            users = parts[0]+":::"+users

        f.close()

        return users




