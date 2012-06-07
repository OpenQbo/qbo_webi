import cherrypy
import rospy
import roslib
import os
from mako.template import Template
from sysChecks.chekers.chekers import chekers
#incluir dependencias de ROS

class soundCheck(chekers):

    def __init__(self,lang):
        #Este es obligatorio
        chekers.__init__(self,'soundCheck',lang)

        #Codigo ROS

        #Este es obligatorio. Modificar si es necesario la direccion y nombre del template
        self.htmlTmpl = Template(filename='sysChecks/chekers/'+self.name+'/templates/SoundCheckTemplate.html')
        self.jsTemplate = Template(filename='sysChecks/chekers/'+self.name+'/templates/SoundCheckTemplate.js')

        #Esto si no existe no se pone
        #self.jsTmpl = Template(filename='sysChecks/chekers/checkTemplate/templates/checkTemplateTemplate.js')
        #self.cssTmpl = Template(filename='sysChecks/chekers/checkTemplate/templates/checkTemplateTemplate.css')

    #redefine in is necesary
    #def get_html_content(self):
        #return self.htmlTmpl.render(language=self.language)



    def soundCheckJs(self, parameters=None):
        return self.jsTemplate.render(language=self.language)




    def play(self,src):


        src=src[0]


        path = roslib.packages.get_pkg_dir("qbo_webi");

        print "Playing sound "+path

        if (src=="left"):
            filename="check_sound_left.mp3"
        elif (src=="right"):
            filename="check_sound_right.mp3"
        elif (src=="center"):
            filename="check_sound_center.mp3"


        os.system('mpg123 '+path+"/src/sysChecks/static/mp3/"+filename)
        
        return "ok"


    @cherrypy.expose
    def stop(self):
        global p
        global filename #nombre:mac_lan.wav


        if(p==None):
            print "P ES NULL!!??"
        else:
            p.send_signal(signal.SIGINT)
        
