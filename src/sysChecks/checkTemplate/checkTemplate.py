import cherrypy
from mako.template import Template
from sysChecks.chekers.chekers import chekers
#incluir dependencias de ROS

class checkTemplate(chekers):

    def __init__(self,lang):
        #Este es obligatorio
        chekers.__init__(self,'checkTemplate',lang)

        #Codigo ROS

        #Este es obligatorio. Modificar si es necesario la direccion y nombre del template
        self.htmlTmpl = Template(filename='sysChecks/chekers/'+self.name+'/templates/checkTemplateTemplate.html')

        #Esto si no existe no se pone
        #self.jsTmpl = Template(filename='sysChecks/chekers/checkTemplate/templates/checkTemplateTemplate.js')
        #self.cssTmpl = Template(filename='sysChecks/chekers/checkTemplate/templates/checkTemplateTemplate.css')


