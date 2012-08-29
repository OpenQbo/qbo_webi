import cherrypy

class TabClass:

    #_cp_config = {
        #'auth.require': []
    #}

    @cherrypy.expose
    def unload(self):
        return "OK"
    def set_language(self,lang):
        self.language=lang
